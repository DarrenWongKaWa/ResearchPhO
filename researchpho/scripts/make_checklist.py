#!/usr/bin/env python3
"""Build a self-contained ResearchPhO checklist flowchart (HTML) from a JSON file.

Usage:
  python3 make_checklist.py data.json page.html [--profile study-guide|research|author] [--template FILE]

One component, several uses. A main line of nodes runs down the middle (questions in exam order, the chain of
objects of a paper, the steps of the workflow); two categories of items hang on its left and right sides, each in
its own colour; every item has a checkbox. Progress is shown per category and per group of nodes.

  {"schema": "researchpho-checklist/1", "lang": "en", "eyebrow": "...", "title": "...", "intro": "...",
   "storageKey": "...", "emptyNote": "...",
   "categories": [{"id": "tool", "name": "Computation tool", "plural": "Computation tools", "colour": "blue",
                   "noteLabel": "...", "refLabel": "Resource"}, {... the right-hand category ...}],
   "items": {"id": {"category": "tool", "name": "...", "meta": "...", "note": "...", "ref": "...", "url": "https://..."}},
   "start": {"title": "...", "text": "..."}, "end": {"title": "...", "text": "..."},
   "groups": [{"title": "...", "short": "...", "note": "...", "nodes": [
       {"label": "1.A.1", "title": "...", "points": 1.5, "meta": "...", "note": "...", "needs": ["id", ...]}]}],
   "footer": ["paragraph", ...]}

Colours: blue, orange, amber, red, green, purple. Profiles add the rules of one use:
  study-guide  categories tool (blue) and idea (orange); every item has a note and a resource (ref);
               every node has a title, points and a note (what the question asks, never its answer)
  research     categories O-calc (amber) and O-theory (red); every item has a note and a closest theory (ref)
  author       categories standard and check
Exit code 1 on any error. check_booklets.py --guide cross-checks a study guide against the question paper.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

SCHEMA = "researchpho-checklist/1"
COLOURS = ("blue", "orange", "amber", "red", "green", "purple")
ITEM_ID = re.compile(r"^[A-Za-z0-9_-]+$")
DATA_BLOCK = re.compile(r'(<script type="application/json" id="checklist-data">)(.*?)(</script>)', re.S)
DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "checklist_template.html"
PROFILES = {
    "generic": {"categories": None, "item": (), "node": ()},
    "study-guide": {"categories": ("tool", "idea"), "item": ("note", "ref"), "node": ("title", "points", "note")},
    "research": {"categories": ("O-calc", "O-theory"), "item": ("note", "ref"), "node": ("title",)},
    "author": {"categories": ("standard", "check"), "item": (), "node": ("title",)},
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


def check_categories(data: dict, profile: dict, errors: list[str]) -> set[str]:
    cats = data.get("categories")
    if not isinstance(cats, list) or len(cats) != 2:
        errors.append("'categories' must list exactly two categories: the left one, then the right one")
        return set()
    ids = []
    for index, cat in enumerate(cats, 1):
        where = f"category {index}"
        if not isinstance(cat, dict):
            errors.append(f"{where}: must be an object")
            continue
        for key in ("id", "name"):
            check_text(cat, key, where, errors, required=True)
        for key in ("plural", "noteLabel", "refLabel"):
            check_text(cat, key, where, errors, required=False)
        if cat.get("colour") not in COLOURS:
            errors.append(f"{where}: 'colour' must be one of {', '.join(COLOURS)}")
        ids.append(cat.get("id") if is_text(cat.get("id")) else None)
    if None not in ids and len(set(ids)) != len(ids):
        errors.append("the two categories need different ids")
    expected = profile["categories"]
    if expected and tuple(ids) != expected:
        errors.append(f"this profile needs the categories {expected[0]!r} (left) and {expected[1]!r} (right)")
    return {i for i in ids if isinstance(i, str)}


def check_items(data: dict, cat_ids: set[str], profile: dict, errors: list[str]) -> dict:
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
        if item.get("category") not in cat_ids:
            errors.append(f"{where}: 'category' must be one of {sorted(cat_ids)}")
        check_text(item, "name", where, errors, required=True)
        for key in ("meta", "note", "ref"):
            check_text(item, key, where, errors, required=key in profile["item"])
        url = item.get("url")
        if url is not None and not (isinstance(url, str) and re.match(r"^https?://", url)):
            errors.append(f"{where}: 'url' must start with http:// or https://")
    return items


def check_node(node: object, items: dict, labels: set[str], profile: dict, errors: list[str]) -> list[str]:
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
    for key in ("title", "meta", "note"):
        check_text(node, key, where, errors, required=key in profile["node"])
    points = node.get("points")
    if points is None:
        if "points" in profile["node"]:
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
    cat_ids = check_categories(data, profile, errors)
    items = check_items(data, cat_ids, profile, errors)
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
        check_text(group, "title", f"group {index}", errors, required=True)
        for key in ("short", "note"):
            check_text(group, key, f"group {index}", errors, required=False)
        for node in group["nodes"]:
            used.update(check_node(node, items, labels, profile, errors))
    for item_id in sorted(set(items) - used):
        errors.append(f"item '{item_id}' is not attached to any node; remove it or list it under 'needs'")
    return errors


def build(data: dict, template: str) -> str:
    if not DATA_BLOCK.search(template):
        raise ValueError('template has no <script type="application/json" id="checklist-data"> block')
    # no '<' inside the script element: '</script>' or '<!--' in a string would end or stall the data block
    payload = json.dumps(data, ensure_ascii=False, indent=1, allow_nan=False).replace("<", "\\u003c")
    html = DATA_BLOCK.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3), template, count=1)
    title = (data["eyebrow"] + ": " if data.get("eyebrow") else "") + data["title"]
    escaped = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"<title>.*?</title>", lambda m: f"<title>{escaped}</title>", html, count=1, flags=re.S)


def summary(data: dict) -> str:
    seen: dict[str, None] = {}
    nodes = 0
    for group in data["groups"]:
        for node in group["nodes"]:
            nodes += 1
            for item_id in node.get("needs", []):
                seen.setdefault(item_id)
    counts = [sum(1 for i in seen if data["items"][i]["category"] == cat["id"]) for cat in data["categories"]]
    names = [cat.get("plural", cat["name"]) for cat in data["categories"]]
    return f"checklist: {nodes} nodes, {counts[0]} {names[0]} (left), {counts[1]} {names[1]} (right)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", type=Path, help="checklist JSON file")
    parser.add_argument("output", type=Path, help="HTML file to write")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="generic")
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
