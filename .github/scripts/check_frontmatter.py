#!/usr/bin/env python3
"""Check the YAML frontmatter of SKILL.md in one or more skill folders.

A host reads the name and the description of a skill from this block. If the block is not valid YAML, a strict
host cannot read them, and it cannot select the skill from its description.

Checks:
  1. SKILL.md starts with a frontmatter block between two '---' lines.
  2. The block is valid YAML under a strict parse: one mapping, no key twice.
  3. name: lowercase letters, digits and single hyphens only, at most 64 characters.
  4. description: no angle brackets (< or >), at most 1024 characters.

Checks 3 and 4 are the rules of the skill-creator validator (quick_validate.py) for these two fields.

Usage:
  python3 .github/scripts/check_frontmatter.py researchpho [MORE_SKILL_FOLDERS ...]

Exit code 1 if any ERROR is found. Needs PyYAML.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

NAME_MAX = 64
DESCRIPTION_MAX = 1024
NAME = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
# the same block that the skill-creator validator reads: from the first line '---' to the next '---'
FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.S)


class StrictLoader(yaml.SafeLoader):
    """PyYAML's safe loader, which also rejects a key that occurs twice in one mapping.

    PyYAML keeps the last value of such a key without a message. Some other YAML parsers stop with an error.
    """

    def construct_mapping(self, node: yaml.Node, deep: bool = False) -> dict:
        if isinstance(node, yaml.MappingNode):
            seen: set[str] = set()
            for key_node, _ in node.value:
                if isinstance(key_node, yaml.ScalarNode):
                    if key_node.value in seen:
                        raise yaml.constructor.ConstructorError(
                            None, None, f"the key '{key_node.value}' occurs twice", key_node.start_mark)
                    seen.add(key_node.value)
        return super().construct_mapping(node, deep=deep)


def yaml_problem(error: yaml.YAMLError) -> str:
    """The parser's message, with the line number counted in SKILL.md and the text at that position."""
    mark = getattr(error, "problem_mark", None)
    problem = getattr(error, "problem", None)
    if mark is None or problem is None:
        return str(error)
    text = f"{problem} (line {mark.line + 2}, column {mark.column + 1})"  # the block starts on line 2 of the file
    snippet = mark.get_snippet()
    return f"{text}\n{snippet}" if snippet else text


def text_field(data: dict, key: str, errors: list[str]) -> str | None:
    """The stripped text of a required field, or None after an error is recorded."""
    if key not in data:
        errors.append(f"The frontmatter has no '{key}'.")
        return None
    value = data[key]
    if value is None or (isinstance(value, str) and not value.strip()):
        errors.append(f"'{key}' is empty.")
        return None
    if not isinstance(value, str):
        errors.append(f"'{key}' must be text. YAML reads this value as {type(value).__name__}.")
        return None
    return value.strip()


def check_skill(path: Path) -> tuple[list[str], str]:
    """Return the errors of one SKILL.md and a one-line summary of its name and description."""
    if not path.is_file():
        return ["The file does not exist."], ""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return [f"The file is not valid UTF-8: {error}."], ""
    block = FRONTMATTER.match(text)
    if block is None:
        return ["The file does not start with a frontmatter block between two '---' lines."], ""
    try:
        data = yaml.load(block.group(1), Loader=StrictLoader)
    except yaml.YAMLError as error:
        return [f"The frontmatter is not valid YAML: {yaml_problem(error)}"], ""
    if not isinstance(data, dict):
        return ["The frontmatter is not a YAML mapping (lines of the form 'key: value')."], ""

    errors: list[str] = []
    name = text_field(data, "name", errors)
    if name is not None:
        if not NAME.fullmatch(name):
            errors.append(f"'name' must have only lowercase letters, digits and single hyphens. It is '{name}'.")
        if len(name) > NAME_MAX:
            errors.append(f"'name' has {len(name)} characters. The limit is {NAME_MAX}.")
    description = text_field(data, "description", errors)
    if description is not None:
        if "<" in description or ">" in description:
            errors.append("'description' contains an angle bracket (< or >). Remove it.")
        if len(description) > DESCRIPTION_MAX:
            errors.append(f"'description' has {len(description)} characters. The limit is {DESCRIPTION_MAX}.")
    summary = "" if errors else f"name '{name}', description {len(description or '')} of {DESCRIPTION_MAX} characters"
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folders", nargs="+", type=Path, metavar="SKILL_FOLDER",
                        help="a folder that contains SKILL.md")
    args = parser.parse_args()

    count = 0
    for folder in args.folders:
        path = folder / "SKILL.md"
        errors, summary = check_skill(path)
        count += len(errors)
        for error in errors:
            print(f"ERROR {path}: {error}")
        if not errors:
            print(f"OK    {path}: {summary}")
    print(f"{count} error(s)")
    return 1 if count else 0


if __name__ == "__main__":
    sys.exit(main())
