"""Package each skill in skills/<name>/ into a deterministic upload-ready zip.

Usage:
    python tools/pack_zips.py                     # build root-layout zips in dist/ (Gemini & Copilot)
    python tools/pack_zips.py --format folder     # build folder-wrapped zips (claude.ai)
    python tools/pack_zips.py --clean             # remove stale zips for deleted/renamed skills
    python tools/pack_zips.py --check             # exit 1 if dist/ is out of date
    python tools/pack_zips.py vmware-vsphere ...  # build only named skills
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path

FIXED_DATE = (2026, 1, 1, 0, 0, 0)
EXCLUDED_DIRS = {"__pycache__", ".git", "__MACOSX"}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db"}
EXCLUDED_SUFFIXES = (".pyc", ".pyo")


def should_skip(rel_parts: tuple[str, ...]) -> bool:
    if any(p in EXCLUDED_DIRS for p in rel_parts[:-1]):
        return True
    name = rel_parts[-1]
    if name in EXCLUDED_FILES or name.endswith(EXCLUDED_SUFFIXES):
        return True
    return False


def build_zip_bytes(skill_dir: Path, fmt: str) -> bytes:
    """Return deterministic zip bytes for a single skill directory."""
    buf = io.BytesIO()
    prefix = f"{skill_dir.name}/" if fmt == "folder" else ""
    files = sorted(
        (p for p in skill_dir.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(skill_dir).as_posix(),
    )
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            rel = path.relative_to(skill_dir)
            if should_skip(rel.parts):
                continue
            arcname = prefix + rel.as_posix()
            info = zipfile.ZipInfo(filename=arcname, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix permissions for cross-platform compatibility
            info.external_attr = (0o100644) << 16
            data = path.read_bytes()
            zf.writestr(info, data)
    return buf.getvalue()


def discover_skills(skills_root: Path) -> list[Path]:
    return sorted(
        (d for d in skills_root.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()),
        key=lambda d: d.name,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Package skills into deterministic zip files.")
    parser.add_argument("skills", nargs="*", help="Optional skill names to package (default: all)")
    parser.add_argument(
        "--format",
        choices=("root", "folder"),
        default="root",
        help="Archive layout: 'root' puts SKILL.md at zip root (Gemini & Copilot); 'folder' wraps in <skill>/ (claude.ai).",
    )
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent, help="Repository root")
    parser.add_argument("--out", type=Path, default=None, help="Output directory (default: <repo>/dist)")
    parser.add_argument("--clean", action="store_true", help="Remove stale .zip files not matching any current skill")
    parser.add_argument("--check", action="store_true", help="Verify dist/ matches current skills without writing")
    args = parser.parse_args()

    skills_root = args.repo / "skills"
    out_dir = args.out if args.out is not None else (args.repo / "dist")
    available = discover_skills(skills_root)
    by_name = {d.name: d for d in available}

    if args.skills:
        unknown = [s for s in args.skills if s not in by_name]
        if unknown:
            print(f"ERROR: unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
            return 1
        selected = [by_name[s] for s in args.skills]
    else:
        selected = available

    expected_names = {f"{d.name}.zip" for d in available}

    if args.check:
        diffs: list[str] = []
        if not out_dir.is_dir():
            print(f"OUT OF DATE: {out_dir} does not exist", file=sys.stderr)
            return 1
        if not args.skills:
            existing = {p.name for p in out_dir.glob("*.zip")}
            for stale in sorted(existing - expected_names):
                diffs.append(f"stale zip: {stale}")
        for skill_dir in selected:
            zip_path = out_dir / f"{skill_dir.name}.zip"
            expected = build_zip_bytes(skill_dir, args.format)
            if not zip_path.is_file():
                diffs.append(f"missing: {zip_path.name}")
            elif zip_path.read_bytes() != expected:
                diffs.append(f"changed: {zip_path.name}")
        if diffs:
            for d in diffs:
                print(f"OUT OF DATE: {d}", file=sys.stderr)
            return 1
        print(f"OK: {len(selected)} skill zips in {out_dir} are up to date ({args.format} layout).")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    if args.clean and not args.skills:
        for existing_zip in sorted(out_dir.glob("*.zip")):
            if existing_zip.name not in expected_names:
                existing_zip.unlink()
                print(f"[DEL] {existing_zip.name}")
                removed += 1

    updated = 0
    for skill_dir in selected:
        zip_path = out_dir / f"{skill_dir.name}.zip"
        payload = build_zip_bytes(skill_dir, args.format)
        if zip_path.is_file() and zip_path.read_bytes() == payload:
            continue
        zip_path.write_bytes(payload)
        updated += 1

    print(
        f"Packaged {len(selected)} skills ({args.format} layout) in {out_dir} "
        f"— {updated} written, {len(selected) - updated} unchanged, {removed} removed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
