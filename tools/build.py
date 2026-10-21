"""Convert my_prompts/*.md system prompts into Claude skills (skills/<name>/SKILL.md).

Usage: python build.py <my_prompts_dir> <output_repo_dir>
"""
import re
import sys
from pathlib import Path

from skills_config import SKILLS, HANDWRITTEN, HANDWRITTEN_REFS

REVIEWED = "2026-10"

TECH_RULES = """## How to Work (applies to every response)

1. **Clarify only what changes the answer.** If a missing detail would change the design, or a wrong guess could cause an outage, data loss, lockout, or surprise cost, ask up to 3 targeted questions in one round. Otherwise state your assumptions in one line and proceed.{clarify}
2. **Match depth to the request.** A quick question gets a short, direct answer. A design, build, or review request gets the full delivery format in this skill.
3. **Check silently.** Run this skill's pre-answer checklist internally. Never print checklists, `<verification>` tags, or status flags.
4. **Verify anything version-sensitive.** Product names, versions, limits, SKUs, and prices change. Confirm them with available tools (official docs, web search, Microsoft Learn MCP) or mark the item **[verify]**. Never invent commands, parameters, API fields, model numbers, or features — even ones that appear in this skill if your tools show otherwise.{safety}
{n}. **Scannable output.** Lead with the answer. Give the "why" in 1–2 sentences, then steps in small batches. Use `<PLACEHOLDER>` notation for environment values you don't know.
"""

SAFETY_RULE = """
5. **Safe by default.** Call out disruptive or destructive steps in **bold** with their impact, and include validation and rollback steps for every change."""

COACH_RULES = """## How to Work (applies to every response)

1. **Short and scannable.** Bold the key point, use small tables or bullets, and give at most 2–3 next steps at a time.
2. **Interview lightly.** Ask one question at a time by default, but if the user answers several at once, accept them and skip ahead. Never stall on optional details — state an assumption and keep going.{clarify}
3. **Check silently.** Run this skill's pre-answer checks internally. Never print checklists or `<verification>` tags.
4. **Flag facts that change.** Prices, hours, statistics, and program rules change. Label estimates clearly and say where to verify. Never invent facts, records, numbers, or sources.
5. **Zero shame.** Treat missed plans, gaps, and setbacks as neutral data, never as failures.
"""

PHASE2_NOTE = ("*Use this full structure for design, build, or review requests. "
               "For quick questions, answer directly and offer to expand.*")

SILENT_LINE = "Run this checklist internally before answering. Do not print it or any `<verification>` tags:"

# Rigid response-format phrasing -> scaled phrasing (content standards are left strict on purpose).
SOFTEN = [
    ("Output your final response structured exactly with these 6 sections:", "Use these 6 sections:"),
    ("Provide your response strictly using this 6-part format:", "Use this 6-part format:"),
    ("Your final response MUST follow this exact structure:", "Use this structure:"),
    ("Deliver your response strictly in this 6-part format:", "Use this 6-part format:"),
    ("Provide your response strictly adhering to this 6-part format:", "Use this 6-part format:"),
    ("you must strictly follow this two-phase protocol", "use this two-phase protocol"),
    ("strictly adhere to this two-phase execution protocol", "use this two-phase protocol"),
    ("you MUST adhere to the following two-phase protocol", "use the following two-phase protocol"),
    ("you MUST adhere to the following protocol", "use the following protocol"),
    ("All responses must adhere strictly to this two-phase structure.", "Use this two-phase structure for design, build, and review requests."),
    ("you must strictly enforce this **Two-Phase Response Protocol**", "use this **Two-Phase Response Protocol**"),
    ("you MUST execute the following two-phase protocol", "use the following two-phase protocol"),
]


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


# Anthropic skill authoring rules (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
RESERVED = ("anthropic", "claude")
XML_TAG = re.compile(r"</?[A-Za-z][\w-]*(\s[^>]*)?>")
MD_LINK = re.compile(r"\]\(([^)\s]+)\)")


def add_toc(content):
    """Give reference files over 100 lines a Contents list so partial reads still see their scope."""
    lines = content.split("\n")
    if len(lines) <= 100 or any(l.strip() == "## Contents" for l in lines):
        return content
    heads = [l[3:].strip() for l in lines if l.startswith("## ")]
    if len(heads) < 2:  # files organized under ### headings
        heads = [l[4:].strip() for l in lines if l.startswith("### ")]
    if len(heads) < 2:
        return content
    i = 1  # insert after the H1 and its header blockquote
    while i < len(lines) and (lines[i].strip() == "" or lines[i].startswith(">")):
        i += 1
    toc = ["## Contents", ""] + [f"- {h}" for h in heads] + [""]
    return "\n".join(lines[:i] + toc + lines[i:])


def lint_skill(name, front, body, refs):
    """Fail the build on anything that breaks the skill authoring rules."""
    errs = []
    keys = set(re.findall(r"^([A-Za-z][\w-]*):", front, re.M))
    if not front.startswith("---\n"):
        errs.append("frontmatter must start on line 1")
    if keys - PORTABLE_KEYS:
        errs.append(f"non-portable frontmatter keys {sorted(keys - PORTABLE_KEYS)} (claude.ai uploads reject them)")
    if any(w in name for w in RESERVED):
        errs.append("name contains a reserved word (anthropic/claude)")
    desc = re.search(r"^description: (.*)$", front, re.M).group(1)
    if XML_TAG.search(desc):
        errs.append("description contains an XML tag")
    if re.match(r"(?i)(i|you|we|my)\b", desc):
        errs.append("description must be written in third person")
    if "use when" not in desc.lower():
        errs.append("description must say when to use the skill ('Use when ...')")
    n = body.count("\n")
    if n >= 500:
        errs.append(f"SKILL.md body is {n} lines (keep under 500; split into references/)")
    for target in MD_LINK.findall(body):
        if "\\" in target:
            errs.append(f"backslash path in link: {target}")
        if target.startswith("references/") and target[len("references/"):] not in refs:
            errs.append(f"broken reference link: {target}")
    for fname, content in refs.items():
        for target in MD_LINK.findall(content):
            if target.endswith(".md") and not target.startswith(("http", "#")):
                errs.append(f"references/{fname} links to {target} (keep references one level deep)")
    if errs:
        fail(f"[{name}] lint: " + "; ".join(errs))


def apply_fixes(text, fixes, name):
    for fix in fixes:
        old, new = fix[0], fix[1]
        replace_all = len(fix) > 2 and fix[2]
        count = text.count(old)
        if count == 0:
            fail(f"[{name}] fix target not found: {old[:90]!r}")
        if count > 1 and not replace_all:
            fail(f"[{name}] fix target found {count}x (set replace_all): {old[:90]!r}")
        text = text.replace(old, new)
    return text


def transform_protocol(text):
    """Make verification phases silent and soften rigid output formats."""
    lines = text.split("\n")
    out = []
    skip = set()
    for i, line in enumerate(lines):
        s = line.strip()
        if s in ("<verification>", "</verification>"):
            skip.add(i)
            # drop a code fence that only wraps the verification block
            if s == "<verification>" and i > 0 and lines[i - 1].strip().startswith("```"):
                skip.add(i - 1)
            if s == "</verification>" and i + 1 < len(lines) and lines[i + 1].strip() == "```":
                skip.add(i + 1)
    for i, line in enumerate(lines):
        if i in skip:
            continue
        heading = re.match(r"^(#{2,4}) ", line)
        if heading and re.search(r"(?i)phase 1", line) and re.search(r"(?i)verification|analysis|audit", line):
            line = f"{heading.group(1)} Phase 1: Silent Pre-Answer Check (internal — never printed)"
        elif "<verification>" in line or "</verification>" in line:
            if "after closing" in line.lower():
                line = "Then respond to the user:"
            elif re.match(r"^\s*In your", line):
                line = "Evaluate:"
            else:
                line = SILENT_LINE
        line = (line.replace("`[STATUS: CONTEXT_REQUIRED]`", "**Context missing**")
                    .replace("`[STATUS: SUFFICIENT]`", "**Context sufficient**"))
        out.append(line)
        already = any("Use this full structure" in l for l in lines[i + 1:i + 4])
        if (re.match(r"^#{2,4} .*(?i:phase 2)", line) or re.match(r"^\*\*Phase 2", line)) and not already:
            out.append("")
            out.append(PHASE2_NOTE)
    return "\n".join(out)


def strip_head(text):
    """Remove H1 + persona block (everything before the first '## ' heading)."""
    idx = text.find("\n## ")
    if idx == -1:
        fail("no level-2 heading found")
    body = text[idx + 1:]
    return body


def extract_sections(text, headings, name):
    """Cut sections that start with any exact heading line; return (text, extracted)."""
    lines = text.split("\n")
    extracted = []
    first_pos = None
    for h in headings:
        try:
            start = lines.index(h)
        except ValueError:
            fail(f"[{name}] split heading not found: {h!r}")
        level = len(h) - len(h.lstrip("#"))
        end = start + 1
        while end < len(lines):
            m = re.match(r"^(#{1,6}) ", lines[end])
            if m and len(m.group(1)) <= level:
                break
            end += 1
        block = lines[start:end]
        # trim trailing separators
        while block and block[-1].strip() in ("", "---"):
            block.pop()
        extracted.append("\n".join(block))
        if first_pos is None or start < first_pos:
            first_pos = start
        lines = lines[:start] + ["@@CUT@@"] + lines[end:]
    text = "\n".join(lines)
    return text, extracted


def build_skill(cfg, prompts_dir, out_dir):
    name = cfg["name"]
    if name in HANDWRITTEN:
        body = HANDWRITTEN[name]
        refs = HANDWRITTEN_REFS.get(name, {})
    else:
        src = (prompts_dir / cfg["src"]).read_text(encoding="utf-8")
        text = apply_fixes(src, cfg.get("fixes", []), name)
        text = transform_protocol(text)
        for old, new in SOFTEN:
            text = text.replace(old, new)
        text = strip_head(text)
        if cfg.get("drop"):
            text, _ = extract_sections(text, cfg["drop"], name)
            text = text.replace("\n@@CUT@@", "").replace("@@CUT@@", "")
            text = re.sub(r"(\s*\n---)+\s*$", "\n", text)
        refs = {}
        for split in cfg.get("splits", []):
            text, parts = extract_sections(text, split["headings"], name)
            ref_path = f"references/{split['file']}"
            pointer = f"> 📎 **Reference:** {split['pointer']} → read [`{ref_path}`]({ref_path})."
            text = text.replace("@@CUT@@", pointer, 1).replace("\n@@CUT@@", "")
            header = f"# {split['title']}\n\n> Reference file for the `{name}` skill. Reviewed {REVIEWED}."
            if cfg.get("variant", "tech") == "tech":
                header += (" Version-sensitive details (models, SKUs, limits, prices, names) change — "
                           "verify before relying on them.")
            header += "\n"
            if split.get("warning"):
                header += f"\n> ⚠️ {split['warning']}\n"
            refs[split["file"]] = header + "\n" + "\n\n---\n\n".join(parts) + "\n"
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        text = re.sub(r"^(---\s*\n)+", "", text)

        clarify = ""
        if cfg.get("clarify"):
            clarify = "\n   *Questions that usually change the answer here:* " + "; ".join(cfg["clarify"]) + "."
        if cfg.get("variant", "tech") == "coach":
            rules = COACH_RULES.format(clarify=clarify)
        else:
            safety = cfg.get("safety", True)
            rules = TECH_RULES.format(clarify=clarify, safety=SAFETY_RULE if safety else "",
                                      n=6 if safety else 5)
        notes = ""
        if cfg.get("notes"):
            notes = (f"\n\n---\n\n## Accuracy & Currency Notes (reviewed {REVIEWED})\n\n"
                     "These corrections override anything above that conflicts with them.\n\n"
                     + "\n".join(f"- {n}" for n in cfg["notes"]))
        body = (f"# {cfg['title']}\n\n**Role:** {cfg['role']}\n\n{rules}\n---\n\n{text}{notes}\n")

    desc = cfg["description"].replace("\n", " ").strip()
    if len(desc) > 1024:
        fail(f"[{name}] description too long ({len(desc)})")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        fail(f"[{name}] invalid skill name")
    front = f"---\nname: {name}\ndescription: {desc}\n---\n\n"
    refs = {f: add_toc(c) for f, c in refs.items()}
    lint_skill(name, front, body, refs)
    skill_dir = out_dir / "skills" / name
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(front + body, encoding="utf-8", newline="\n")
    for fname, content in refs.items():
        (skill_dir / "references" / fname).write_text(content, encoding="utf-8", newline="\n")
    if not refs:
        (skill_dir / "references").rmdir()
    return (front + body).count("\n"), list(refs)


def main():
    prompts_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    srcs = {c["src"] for c in SKILLS}
    missing = [p.name for p in prompts_dir.glob("*_prompt.md") if p.name not in srcs]
    if missing:
        fail(f"prompts without a skill config: {missing}")
    for cfg in SKILLS:
        n, refs = build_skill(cfg, prompts_dir, out_dir)
        flag = "  <-- over 500 lines" if n > 500 else ""
        print(f"{cfg['name']:<36} {n:>4} lines  refs={refs}{flag}")
    print(f"\nBuilt {len(SKILLS)} skills.")


if __name__ == "__main__":
    main()
