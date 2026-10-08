"""Validate standalone Tiled skill metadata and local links without external packages."""
import argparse
import ast
from pathlib import Path
import re
import sys


def scalar(text, key):
    match = re.search(r"^\s*" + re.escape(key) + r":\s*(.*?)\s*$", text, re.M)
    if not match or not match.group(1):
        raise ValueError(f"missing {key}")
    value = match.group(1)
    return ast.literal_eval(value) if value.startswith(('"', "'")) else value


def validate(skill, client="codex", require_openai_metadata=False):
    skill = Path(skill)
    errors = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return ["missing SKILL.md"]
    text = entry.read_text(encoding="utf-8")
    try:
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        if not match:
            raise ValueError("frontmatter delimiters missing")
        name = scalar(match.group(1), "name")
        if name != skill.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 63:
            errors.append("invalid or mismatched name")
        if not scalar(match.group(1), "description").strip():
            errors.append("missing description")
        ui_path = skill / "agents/openai.yaml"
        if client == "codex" and (require_openai_metadata or ui_path.is_file()):
            ui = ui_path.read_text(encoding="utf-8")
            if not re.search(r"^interface:\s*$", ui, re.M):
                raise ValueError("missing interface")
            if not scalar(ui, "display_name") or not 25 <= len(scalar(ui, "short_description")) <= 64:
                errors.append("invalid UI metadata")
            if "$" + skill.name not in scalar(ui, "default_prompt"):
                errors.append("default prompt must name skill")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, SyntaxError) as exc:
        errors.append("invalid metadata: " + str(exc))
    for doc in skill.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            dest = (doc.parent / target.split("#")[0]).resolve()
            if not dest.is_relative_to(skill.resolve()) or not dest.exists():
                errors.append(f"{doc.name}: missing or nonportable link {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(Path(__file__).resolve().parents[1] / "skills"))
    parser.add_argument("--client", choices=["codex", "claude"], default="codex")
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--require-openai-metadata", action="store_true")
    args = parser.parse_args()
    root = Path(args.path)
    if not root.is_dir():
        parser.error(f"skill path is not a directory: {root}")
    skills = [root] if (root / "SKILL.md").exists() else sorted(
        p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    problems = []
    if args.expected_count is not None and len(skills) != args.expected_count:
        problems.append(f"expected {args.expected_count} skills, found {len(skills)}")
    if not skills:
        problems.append("no skill directories found")
    for skill in skills:
        problems.extend(f"{skill.name}: {error}" for error in validate(
            skill, args.client, args.require_openai_metadata))
    print("\n".join(problems) if problems else f"Validated {len(skills)} skills.")
    return bool(problems)


if __name__ == "__main__":
    sys.exit(main())
