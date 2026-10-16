"""Generate my_skills/README.md in the my_prompts README format."""
import re
import sys
from pathlib import Path

from skills_config import SKILLS

prompts_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
src_readme = (prompts_dir / "README.md").read_text(encoding="utf-8")

# file.md -> (persona, focus) from the my_prompts README tables
rows = {}
for m in re.finditer(r"^\| \*\*\[(.+?)\]\((.+?\.md)\)\*\* \| (.+?) \| (.+?) \|$", src_readme, re.M):
    rows[m.group(2)] = (m.group(1), m.group(3), m.group(4))

FOCUS_OVERRIDES = {
    "vmware-vsphere": "ESXi/vCenter/VCF, HA/DRS/FT, vMotion, vSAN OSA/ESA, Distributed Switches, NSX, VCF Operations, HCX, PowerCLI",
    "microsoft-ai-architect": "M365 Copilot agents, Copilot Studio, Microsoft Foundry, Agent Framework / Semantic Kernel, Azure AI Search RAG, MCP, Purview DSPM for AI",
    "monitoring-alerting": "USE/RED/Golden Signals, symptom-based alerting, SLO burn-rate alerts, Azure Monitor/AMBA, Prometheus/Grafana/Alertmanager, Zabbix, SCOM, VCF Operations",
    "pki-certificates": "AD CS hierarchy & templates (ESC risks), CRL/OCSP, ACME/SCEP, 200→47-day public cert lifetimes, Key Vault/Vault PKI, OpenSSL, TLS hardening",
    "kubernetes-platform": "Control plane HA, etcd/etcdutl, Cilium/Calico CNI, vSphere CSI, MetalLB, Gateway API, ArgoCD/Flux GitOps, Helm, Kyverno",
    "personal-finance": "Budget dashboard, debt avalanche/snowball with real payoff math, emergency fund, goal tracking (educational, not investment advice)",
    "meal-planner": "7-day budget meal plans, editable household profile, teen portion scaling, leftovers & prep plan, store-section grocery list",
    "prompt-engineering-architect": "Build/audit/refactor/combine prompts and skills, SKILL.md packaging, description triggers, audit rubric, test inputs",
    "terraform-iac": "HCL, multi-provider (Azure/AWS/VMware), state & locking, modules, terraform test, ephemeral secrets, Terragrunt, Sentinel/OPA",
    "cicd-gitops-pipelines": "Azure DevOps YAML, GitHub Actions OIDC, quality gates (tflint/Trivy/checkov/Pester), plan-artifact promotion, Atlantis, drift detection",
}

CATEGORIES = [
    ("infra", "🏗️ Infrastructure & Platform Engineering", "Core datacenter, virtualization, compute, networking, and operating system skills."),
    ("cloud", "☁️ Cloud, IaC & Automation", "Azure cloud services, infrastructure as code, configuration management, and scripting."),
    ("identity", "🔐 Identity, Security, Compliance & Cryptography", "Identity and endpoint management, security hardening, regulatory compliance, PKI, and certificate lifecycle management."),
    ("observability", "📊 Observability, Monitoring, SIEM & Log Engineering", "Metrics and alerting, log pipelines, SIEM platforms, and observability architecture."),
    ("bcdr", "🛡️ Backup, Disaster Recovery & Business Continuity", "Enterprise data protection, replication, cyber recovery, and DR orchestration."),
    ("ops", "📋 Operations, Communication & Documentation", "Incident management, project delivery, stakeholder communication, procedure documentation, and knowledge transfer."),
    ("daily", "⚡ Daily Productivity & Workflow", "Short, repeatable skills for every workday: start and end the day, clear the inbox, process meetings, make decisions, and digest reading."),
    ("personal", "🏠 Personal, Career & Lifestyle", "Non-technical skills for personal productivity, career growth, finance, and daily life."),
    ("meta", "🧰 Meta & Prompt Engineering", "Skills for building and maintaining this library."),
]

COMBOS = [
    ("Cloud infrastructure deployment", "azure-solutions-architect", ["terraform-iac", "security-compliance-hardening"]),
    ("On-prem VM environment management", "vmware-vsphere", ["windows-server", "powershell-expert"]),
    ("Log pipeline engineering", "cribl-stream", ["elastic-stack"]),
    ("Dual-SIEM log routing & optimization", "cribl-elastic-sentinel-pipelines", ["elastic-stack", "microsoft-sentinel"]),
    ("Infrastructure automation", "ansible-automation", ["linux-sysadmin", "windows-server", "terraform-iac"]),
    ("Security audit & compliance hardening", "security-compliance-hardening", ["windows-server", "linux-sysadmin", "enterprise-networking"]),
    ("Enterprise PKI & certificate management", "pki-certificates", ["windows-server", "linux-sysadmin", "enterprise-networking"]),
    ("Production incident response", "incident-response", ["any technology skill", "executive-communication"]),
    ("Infrastructure project planning", "it-project-management", ["any technology skill"]),
    ("Hardware procurement & DC design", "datacenter-hardware", ["vmware-vsphere", "windows-server", "enterprise-networking"]),
    ("Disaster recovery & backup architecture", "bcdr-recovery-architect", ["vmware-vsphere", "windows-server", "azure-solutions-architect"]),
    ("Container platform & Kubernetes ops", "kubernetes-platform", ["linux-sysadmin", "ansible-automation", "enterprise-networking"]),
    ("Cloud cost reduction & FinOps governance", "cloud-finops", ["azure-solutions-architect", "terraform-iac"]),
    ("Infrastructure CI/CD & GitOps delivery", "cicd-gitops-pipelines", ["terraform-iac", "ansible-automation", "powershell-expert"]),
    ("Cloud SIEM, detection & SecOps engineering", "microsoft-sentinel", ["azure-solutions-architect", "cribl-stream", "security-compliance-hardening"]),
    ("Operational delegation & SOP generation", "sop-documentation", ["any technology skill for context"]),
    ("Entra ID / Conditional Access / Intune rollout", "entra-intune-identity", ["security-compliance-hardening", "powershell-expert", "windows-server"]),
    ("Monitoring & alert-noise cleanup", "monitoring-alerting", ["incident-response", "vmware-vsphere", "azure-solutions-architect"]),
    ("Outage comms, CAB submissions & exec updates", "executive-communication", ["incident-response", "it-project-management"]),
    ("Figuring out what career fits (teen or adult)", "career-interest-assessment", ["learning-coach", "career-interview-coach"]),
    ("Promotion, resume & interview prep", "career-interview-coach", ["executive-communication", "adhd-executive-function-coach"]),
    ("Starting and ending the workday", "daily-kickoff-shutdown", ["weekly-reset-planner", "adhd-executive-function-coach"]),
    ("Clearing a backed-up inbox or Teams", "inbox-triage", ["executive-communication"]),
    ("Turning meetings into tracked work", "meeting-notes", ["it-project-management", "daily-kickoff-shutdown"]),
    ("Stuck on a choice (work or home)", "decision-coach", ["personal-finance", "home-maintenance-ops", "formal-logic-analyzer"]),
    ("Release notes, advisories & long docs", "research-briefing", ["security-compliance-hardening", "the matching technical skill"]),
    ("Weekly planning that actually sticks", "weekly-reset-planner", ["adhd-executive-function-coach"]),
    ("Healthy routines for the whole family", "fitness-habit-coach", ["meal-planner", "weekly-reset-planner"]),
    ("Home repairs, projects & big-expense planning", "home-maintenance-ops", ["personal-finance"]),
    ("Family vacations & day trips", "family-trip-planner", ["personal-finance"]),
    ("Family tree & local history archive", "genealogy-research", ["sop-documentation (archive SOPs)"]),
    ("Learning a new technology or hobby", "learning-coach", ["the matching technical skill, e.g. kubernetes-platform"]),
    ("Adding or improving a skill in this repo", "prompt-engineering-architect", ["the skill being created or audited"]),
]


def code(s):
    return f"`/{s}`" if re.fullmatch(r"[a-z0-9-]+", s) else s


out = []
out.append(f"""# My Skills Repository

A curated library of **{len(SKILLS)}** Claude skills for enterprise systems engineering, identity, observability, security, communication, and personal productivity. Each skill is a converted and audited version of a prompt from [`my_prompts`](https://github.com/chadrothermel-dev/my_prompts) — see **[AUDIT.md](AUDIT.md)** for what was fixed and why.

---

## Quick Start

**Option A — Claude Code plugin (all skills, auto-updates):**

```bash
/plugin marketplace add chadrothermel-dev/my_skills
```

```bash
/plugin install my-skills@my-skills
```

Skills are then available as `/my-skills:<skill-name>` and load automatically when your request matches a skill's description.

**Option B — copy into your personal skills folder (Windows):**

```powershell
git clone https://github.com/chadrothermel-dev/my_skills.git; cd my_skills; ./install.ps1
```

Install a subset with `./install.ps1 -Skills vmware-vsphere,windows-server`. On macOS/Linux use `./install.sh` (optionally followed by skill names).

**Option C — claude.ai:** run `./install.ps1 -Zip` to build `dist/<skill>.zip` files, then upload one under **Settings → Capabilities → Skills**.

> [!TIP]
> **Combine skills for maximum impact.** Claude can load several skills in one conversation — see [Recommended Skill Combinations](#recommended-skill-combinations).

---
""")

for key, heading, blurb in CATEGORIES:
    items = [c for c in SKILLS if c["category"] == key]
    if not items:
        continue
    out.append(f"## {heading}\n\n{blurb}\n")
    out.append("| Skill | Invoke | Persona | Key Focus Areas |\n| :--- | :--- | :--- | :--- |")
    for c in items:
        _, persona, focus = rows.get(c["src"], (c["title"], c["title"], ""))
        focus = FOCUS_OVERRIDES.get(c["name"], focus)
        persona = re.sub(r"(Distinguished |Board-Certified |30\+ Year |20\+ Year )", "", persona)
        out.append(f"| **[{c['title']}](skills/{c['name']}/SKILL.md)** | `/{c['name']}` | {persona} | {focus} |")
    out.append("\n---\n")

out.append("## Recommended Skill Combinations\n\nFor maximum effectiveness, combine related skills based on your current task:\n")
out.append("| Task | Primary Skill | Supporting Skill(s) |\n| :--- | :--- | :--- |")
names = {c["name"] for c in SKILLS}
for task, primary, support in COMBOS:
    assert primary in names, primary
    for s in support:
        assert (not re.fullmatch(r"[a-z0-9-]+", s)) or s in names, s
    out.append(f"| {task} | {code(primary)} | {', '.join(code(s) for s in support)} |")

out.append("""
---

## Using These Skills with Claude

| Platform | How |
| :--- | :--- |
| **Claude Code (plugin)** | `/plugin marketplace add chadrothermel-dev/my_skills` → `/plugin install my-skills@my-skills`. Invoke as `/my-skills:<name>` or just describe your task. |
| **Claude Code (personal)** | `./install.ps1` copies skills to `~/.claude/skills/<name>/`. Invoke as `/<name>`. |
| **claude.ai / Desktop** | `./install.ps1 -Zip`, then upload a zip under *Settings → Capabilities → Skills*. |
| **API / agents** | Upload via the Skills API, or use a `SKILL.md` body (minus frontmatter) as the system prompt. |

---

## Skill Anatomy (House Style)

Every skill follows the same skeleton so they're predictable and combinable:

1. **Frontmatter**: `name` (matches the folder) and a `description` that says *what* the skill does and *when* to use it — this is what Claude reads to decide whether to load it
2. **Role**: one line, what it does (no persona inflation)
3. **How to Work**: shared rules — clarify only what changes the answer, match depth to the request, check silently, verify version-sensitive facts, safe by default, scannable output
4. **Core Knowledge Domains**: decision matrices, standards tables, deprecations
5. **Silent Pre-Answer Check → Delivery Format**: the checklist runs internally; the full format is for design/build/review requests
6. **Ground Rules**: one-line *Never/Always* guardrails
7. **Accuracy & Currency Notes**: dated corrections that override older text above
8. **`references/`** *(optional)*: large catalogs that load only when needed

New skills: use [`/prompt-engineering-architect`](skills/prompt-engineering-architect/SKILL.md) in **Build** mode, put the skill in `skills/<kebab-case-name>/SKILL.md`, and add a row to the matching table above.

---

## Keeping Skills Current

Fast-moving facts are tagged **[verify]** and each skill carries a *reviewed* date. List everything that needs a periodic check:

```bash
grep -rn "\\[verify" skills/
```

**Rebuilding from `my_prompts`:** `tools/build.py` converts every prompt (shared rules, per-skill fixes in `tools/cfg_*.py`, reference splits) and fails loudly if a fix no longer matches its source:

```bash
python tools/build.py <path-to-my_prompts> . && python tools/gen_readme.py <path-to-my_prompts> .
```
""")

(out_dir / "README.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
print("README written:", len(SKILLS), "skills,", len(COMBOS), "combos")
