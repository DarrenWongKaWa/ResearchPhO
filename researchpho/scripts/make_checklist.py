#!/usr/bin/env python3
"""Build the self-contained ResearchPhO checklist page (HTML) from a JSON file.

Usage:
  python3 make_checklist.py checklist.json checklist.html [--profile rpho|author|generic] [--template FILE]

One page, one main line. The exam runs down the middle, problem by problem and question by question. Each question
node carries the items it needs: computation tools in blue frames on the left, modelling ideas in orange frames on
the right. A research segment continues the same line after the exam: the chain of objects of the papers, with the
open links that a calculation would close (O-calc, amber, left) and those that need new theory (O-theory, red,
right). Every item has a checkbox, a title, one short note and one reference, linked when a URL is given. Progress
is shown per category, per group and overall.

  {"schema": "researchpho-checklist/2", "lang": "en", "eyebrow": "...", "title": "...", "intro": "...",
   "storageKey": "...", "emptyNote": "...",
   "categories": [{"id": "tool", "name": "Computation tool", "plural": "Computation tools", "colour": "blue",
                   "side": "left"}, ...],
   "items": {"id": {"category": "tool", "name": "...", "note": "...", "ref": "...", "url": "https://...",
                    "meta": "..."}},
   "start": {"title": "...", "text": "..."}, "end": {"title": "...", "text": "..."},
   "groups": [{"kind": "exam", "title": "...", "short": "Problem 1", "points": 10, "note": "the question the
               paper answers", "nodes": [{"label": "1.A.1", "title": "...", "points": 0.8, "note": "...",
               "needs": ["id", ...]}]},
              {"kind": "research", "title": "...", "short": "Research", "note": "...", "nodes": [
               {"label": "p12(k, phi)", "meta": "D/O-theory", "title": "...", "note": "...", "needs": [...]}]}],
   "footer": ["paragraph", ...]}

Colours: blue, orange, amber, red, green, purple. Profiles:
  rpho     categories tool (blue, left) and idea (orange, right), optionally O-calc (amber, left) and O-theory
           (red, right) for a research segment; every item has a note and a reference; every exam node has a
           title and points; every research node has a title and a label tag (meta)
  author   categories standard and check (the author checklist of the skill)
  generic  only the schema
Exit code 1 on any error. check_booklets.py --checklist cross-checks the exam nodes against the question paper.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

SCHEMA = "researchpho-checklist/2"
COLOURS = ("blue", "orange", "amber", "red", "green", "purple")
SIDES = ("left", "right")
ITEM_ID = re.compile(r"^[A-Za-z0-9_-]+$")
DATA_BLOCK = re.compile(r'(<script type="application/json" id="checklist-data">)(.*?)(</script>)', re.S)
DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "checklist_template.html"
RPHO_CATEGORIES = {"tool": ("blue", "left"), "idea": ("orange", "right"),
                   "O-calc": ("amber", "left"), "O-theory": ("red", "right")}
PROFILES = {
    "generic": {"categories": None, "required": (), "item": (), "exam": (), "research": ()},
    "rpho": {"categories": RPHO_CATEGORIES, "required": ("tool", "idea"), "item": ("note", "ref"),
             "exam": ("title", "points"), "research": ("title", "meta")},
    "author": {"categories": {"standard": (None, "left"), "check": (None, "right")}, "required": ("standard", "check"),
               "item": (), "exam": ("title",), "research": ("title",)},
}


def is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_text(obj: dict, key: str, where: str, errors: list[str], required: bool) -> None:
    value = obj.get(key)
    if value is None:
        if required:
            errors.append(f"{where}: '{key}' is required")
    elif not is_text(value):
        errors.append(f"{where}: '{key}' must be a non-empty string")


def check_categories(data: dict, profile: dict, errors: list[str]) -> dict[str, dict]:
    cats = data.get("categories")
    if not isinstance(cats, list) or not 2 <= len(cats) <= 4:
        errors.append("'categories' must list two to four categories")
        return {}
    found: dict[str, dict] = {}
    for index, cat in enumerate(cats, 1):
        where = f"category {index}"
        if not isinstance(cat, dict):
            errors.append(f"{where}: must be an object")
            continue
        for key in ("id", "name"):
            check_text(cat, key, where, errors, required=True)
        check_text(cat, "plural", where, errors, required=False)
        if cat.get("colour") not in COLOURS:
            errors.append(f"{where}: 'colour' must be one of {', '.join(COLOURS)}")
        if cat.get("side") not in SIDES:
            errors.append(f"{where}: 'side' must be 'left' or 'right'")
        cid = cat.get("id")
        if is_text(cid):
            if cid in found:
                errors.append(f"{where}: duplicate id {cid!r}")
            found[cid] = cat
    rules = profile["categories"]
    if rules:
        for cid, cat in found.items():
            if cid not in rules:
                errors.append(f"category {cid!r} is not part of this profile ({', '.join(rules)})")
                continue
            colour, side = rules[cid]
            if colour and cat.get("colour") != colour:
                errors.append(f"category {cid!r} must be {colour}")
            if cat.get("side") != side:
                errors.append(f"category {cid!r} must hang on the {side}")
        for cid in profile["required"]:
            if cid not in found:
                errors.append(f"this profile needs the category {cid!r}")
    return found


def check_items(data: dict, cats: dict, profile: dict, errors: list[str]) -> dict:
    items = data.get("items")
    if not isinstance(items, dict) or not items:
        errors.append("'items' must be a non-empty object")
        return {}
    for item_id, item in items.items():
        where = f"item '{item_id}'"
        if not ITEM_ID.fullmatch(item_id):
            errors.append(f"{where}: ids may contain only letters, digits, '-' and '_'")
        if not isinstance(item, dict):
            errors.append(f"{where}: must be an object")
            continue
        if item.get("category") not in cats:
            errors.append(f"{where}: 'category' must be one of {sorted(cats)}")
        check_text(item, "name", where, errors, required=True)
        for key in ("meta", "note", "ref"):
            check_text(item, key, where, errors, required=key in profile["item"])
        url = item.get("url")
        if url is not None and not (isinstance(url, str) and re.match(r"^https?://", url)):
            errors.append(f"{where}: 'url' must start with http:// or https://")
    return items


def check_node(node: object, kind: str, items: dict, labels: set[str], profile: dict, errors: list[str]) -> list[str]:
    if not isinstance(node, dict):
        errors.append("every node must be an object")
        return []
    label = node.get("label")
    if not is_text(label):
        errors.append("every node needs a non-empty 'label'")
        return []
    where = f"node {label}"
    if label in labels:
        errors.append(f"{where}: duplicate label")
    labels.add(label)
    required = profile[kind]
    for key in ("title", "meta", "note"):
        check_text(node, key, where, errors, required=key in required)
    points = node.get("points")
    if points is None:
        if "points" in required:
            errors.append(f"{where}: 'points' is required")
    elif isinstance(points, bool) or not isinstance(points, (int, float)) or not math.isfinite(points) or points <= 0:
        errors.append(f"{where}: 'points' must be a positive number")
    needs = node.get("needs", [])
    if not isinstance(needs, list):
        errors.append(f"{where}: 'needs' must be a list (empty when nothing is attached)")
        return []
    if len(set(map(str, needs))) != len(needs):
        errors.append(f"{where}: an item is listed twice")
    for item_id in needs:
        if not isinstance(item_id, str) or item_id not in items:
            errors.append(f"{where}: unknown item {item_id!r}")
    return [i for i in needs if isinstance(i, str)]


def validate(data: object, profile_name: str = "generic") -> list[str]:
    if not isinstance(data, dict):
        return ["the file must contain one JSON object"]
    profile = PROFILES[profile_name]
    errors: list[str] = []
    if data.get("schema", SCHEMA) != SCHEMA:
        errors.append(f"'schema' must be '{SCHEMA}'")
    check_text(data, "title", "checklist", errors, required=True)
    for key in ("eyebrow", "intro", "storageKey", "emptyNote", "lang"):
        check_text(data, key, "checklist", errors, required=False)
    for key in ("start", "end"):
        if key in data and not (isinstance(data[key], dict) and is_text(data[key].get("title"))):
            errors.append(f"'{key}' must be an object with a 'title'")
    footer = data.get("footer", [])
    if not (isinstance(footer, list) and all(is_text(p) for p in footer)):
        errors.append("'footer' must be a list of paragraphs")
    cats = check_categories(data, profile, errors)
    items = check_items(data, cats, profile, errors)
    groups = data.get("groups")
    if not isinstance(groups, list) or not groups:
        errors.append("'groups' must be a non-empty list")
        groups = []
    labels: set[str] = set()
    used: set[str] = set()
    for index, group in enumerate(groups, 1):
        if not isinstance(group, dict) or not isinstance(group.get("nodes"), list) or not group["nodes"]:
            errors.append(f"group {index}: needs a non-empty list 'nodes'")
            continue
        kind = group.get("kind", "exam")
        if kind not in ("exam", "research"):
            errors.append(f"group {index}: 'kind' must be 'exam' or 'research'")
            kind = "exam"
        check_text(group, "title", f"group {index}", errors, required=True)
        for key in ("short", "note"):
            check_text(group, key, f"group {index}", errors, required=False)
        for node in group["nodes"]:
            needs = check_node(node, kind, items, labels, profile, errors)
            used.update(needs)
            if profile_name == "rpho":
                allowed = ("tool", "idea") if kind == "exam" else ("O-calc", "O-theory")
                for item_id in needs:
                    if item_id in items and items[item_id].get("category") not in allowed:
                        errors.append(f"node {node.get('label')}: a {kind} node takes only {' and '.join(allowed)} items")
    for item_id in sorted(set(items) - used):
        errors.append(f"item '{item_id}' is not attached to any node; remove it or list it under 'needs'")
    return errors


def build(data: dict, template: str) -> str:
    if not DATA_BLOCK.search(template):
        raise ValueError('template has no <script type="application/json" id="checklist-data"> block')
    # no '<' inside the script element: '</script>' or '<!--' in a string would end or stall the data block
    payload = json.dumps(data, ensure_ascii=False, indent=1, allow_nan=False).replace("<", "\\u003c")
    html = DATA_BLOCK.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3), template, count=1)
    escaped = data["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = re.sub(r"<title>.*?</title>", lambda m: f"<title>{escaped}</title>", html, count=1, flags=re.S)
    lang = data.get("lang", "en")
    return re.sub(r'<html lang="[^"]*">', f'<html lang="{lang}">', html, count=1)


def summary(data: dict) -> str:
    seen: dict[str, None] = {}
    nodes = {"exam": 0, "research": 0}
    for group in data["groups"]:
        nodes[group.get("kind", "exam")] += len(group["nodes"])
        for node in group["nodes"]:
            for item_id in node.get("needs", []):
                seen.setdefault(item_id)
    parts = []
    for cat in data["categories"]:
        n = sum(1 for i in seen if data["items"][i]["category"] == cat["id"])
        parts.append(f"{n} {cat.get('plural', cat['name'])}")
    return f"checklist: {nodes['exam']} exam nodes, {nodes['research']} research nodes; " + ", ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", type=Path, help="checklist JSON file")
    parser.add_argument("output", type=Path, help="HTML file to write")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="rpho")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    try:
        data = json.loads(args.data.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"ERROR cannot read {args.data}: {exc}")
        return 1
    errors = validate(data, args.profile)
    if errors:
        for line in errors:
            print(f"ERROR {line}")
        return 1
    try:
        html = build(data, args.template.read_text(encoding="utf-8"))
        args.output.write_text(html, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR {exc}")
        return 1
    print(summary(data))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
