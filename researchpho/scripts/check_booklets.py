#!/usr/bin/env python3
"""Consistency, format and leak checks for a ResearchPhO question paper and its solutions.

Reads the macros of the ResearchPhO templates:
  questions: \\problem{n}{title}{points}, \\question{label}{points}{text}
  solutions: \\problemsol{n}{title}{points}, \\soltitle{label}{points}{title}, \\marking{...}, \\appendixstart
Labels are keyed as "n.label" (e.g. 2.B.1); files without \\problem use the bare label.

Marking tags: a number in a \\marking line may be followed by (C) for a computation step or (M) for a modelling
step, e.g. "Energy change: 0.45 (M). Integer threshold: 0.3 (C)." Untagged lines stay valid. When any tag is
present, the modelling share of the tagged marks is reported per problem, with a warning below one half (S2, S3).

Usage:
  python3 check_booklets.py questions.tex solutions.tex [--total 30] [--problem-total 10]
                            [--answers answersheets.tex] [--guide study_guide.json] [--forbid PHRASE ...]
                            [--allow-frames]

Exit code 1 if any ERROR is found. WARN lines need a human look.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_FORBIDDEN = ("this conversation", "/Users/", "C:\\", "TODO", "FIXME")
# research-status material belongs in the solution appendices, not in the question paper
STATUS_MARKERS = ("\\begin{greenbox}", "\\begin{redbox}", "\\origin{", "\\handoff{", "NOT ESTABLISHED",
                  "AVAILABLE ---", "OPEN ---", "ADDED MODEL", "GIVEN BOUND", "PICTURE ", "O-calc", "O-theory")
NUMBER = re.compile(r"(?<![\w.])(\d+\.\d+)(?![\w])")
# a marking number with an optional kind tag, (C) computation or (M) modelling; the tag closes its piece, so it
# is followed by punctuation or the end of the line ("0.45 (M)." but not the sub-part label in "0.3 (C) Check")
TAGGED_NUMBER = re.compile(r"(?<![\w.])(\d+\.\d+)(?![\w])(?:\s*\(([CM])\)(?=\s*(?:[.,;:]|$)))?")
TAG = re.compile(r"\(([CM])\)")
LABEL_AFTER = re.compile(r"\s+[A-Za-z]")
MODELLING_SHARE_MIN = 0.5
GUIDE_BLOCK = re.compile(r'<script type="application/json" id="checklist-data">(.*?)</script>', re.S)


@dataclass(frozen=True)
class Item:
    key: str
    points: float
    text: str
    end: int


def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def body_of(tex: str) -> str:
    return tex.split("\\begin{document}", 1)[-1]


def group_end(tex: str, start: int) -> int:
    """Index just after the balanced {...} group that starts at tex[start] == '{'."""
    depth, pos = 0, start
    while pos < len(tex):
        char = tex[pos]
        if char == "\\":
            pos += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
        pos += 1
    raise ValueError("unbalanced braces")


def items(body: str, problem_cmd: str, item_cmd: str) -> tuple[list[Item], dict[str, float]]:
    found, problems, current = [], {}, ""
    pattern = re.compile(r"\\(" + problem_cmd + "|" + item_cmd + r")\{([^}]*)\}(?=\{)")
    for match in pattern.finditer(body):
        second_end = group_end(body, match.end())
        second = body[match.end() + 1:second_end - 1]
        if second_end >= len(body) or body[second_end] != "{":
            continue
        third_end = group_end(body, second_end)
        third = body[second_end + 1:third_end - 1]
        if match.group(1) == problem_cmd:
            current = match.group(2).strip() + "."
            problems[match.group(2).strip()] = float(third)
            continue
        found.append(Item(current + match.group(2).strip(), float(second), third, third_end))
    return found, problems


def strip_math(text: str) -> str:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    return re.sub(r"\$[^$]*\$", " ", text)


def marking_pieces(text: str) -> tuple[list[tuple[float, str]], int]:
    """Numbers outside math in one marking line, each with its tag 'C', 'M' or '' (untagged).

    Also returns the number of tags that do not directly follow a number."""
    plain = strip_math(text)
    matches = list(TAGGED_NUMBER.finditer(plain))
    pieces = [(float(m.group(1)), m.group(2) or "") for m in matches]
    used = {m.start(2) - 1 for m in matches if m.group(2)}
    # a (C)/(M) that opens a piece ("(C) Check: 0.4") is a sub-part label, not a misplaced tag
    stray = sum(1 for t in TAG.finditer(plain)
                if t.start() not in used and not LABEL_AFTER.match(plain, t.end()))
    return pieces, stray


def marking_sums(body: str, sol_items: list[Item]) -> tuple[list[str], dict[str, dict[str, float]]]:
    """Check that each question's marking numbers add up to its points; collect marks per tag."""
    notes, tagged = [], {}
    stop_all = body.find("\\appendixstart")
    stop_all = len(body) if stop_all < 0 else stop_all
    ordered = sorted(sol_items, key=lambda it: it.end)
    for index, item in enumerate(ordered):
        stop = ordered[index + 1].end if index + 1 < len(ordered) else stop_all
        segment = body[item.end:stop]
        total, found, by_tag = 0.0, False, {"C": 0.0, "M": 0.0, "": 0.0}
        for match in re.finditer(r"\\marking\{", segment):
            found = True
            text = segment[match.end():group_end(segment, match.end() - 1) - 1]
            pieces, stray = marking_pieces(text)
            for value, tag in pieces:
                total += value
                by_tag[tag] += value
            if stray:
                notes.append(f"WARN  {item.key}: {stray} (C)/(M) tag(s) not directly after a marking number")
        tagged[item.key] = by_tag
        if not found:
            notes.append(f"WARN  {item.key}: no \\marking line")
        elif abs(total - item.points) > 1e-6:
            notes.append(f"WARN  {item.key}: marking numbers sum to {total:g}, points are {item.points:g}")
    return notes, tagged


def modelling_share(tagged: dict[str, dict[str, float]], numbered: bool) -> tuple[list[str], list[str]]:
    """Standards S2/S3: per problem, the share of tagged marks that go to modelling steps.

    Keys are "n.label" when the solutions use \\problemsol (numbered), else the bare label of one problem."""
    if not any(by_tag["C"] or by_tag["M"] for by_tag in tagged.values()):
        return [], []
    sums: dict[str, dict[str, float]] = {}
    for key, by_tag in tagged.items():
        number = key.split(".", 1)[0] if numbered else "1"
        acc = sums.setdefault(number, {"C": 0.0, "M": 0.0, "": 0.0})
        for tag, value in by_tag.items():
            acc[tag] += value
    report, notes = ["marking tags: (M) modelling, (C) computation"], []
    for number in sorted(sums, key=lambda n: (len(n), n)):
        acc = sums[number]
        tagged_total = acc["C"] + acc["M"]
        if not tagged_total:
            report.append(f"  problem {number}: no tags ({acc['']:g} pt untagged)")
            continue
        share = acc["M"] / tagged_total
        report.append(f"  problem {number}: M {acc['M']:.2f}, C {acc['C']:.2f}, untagged {acc['']:.2f} pt"
                      f" -> modelling {share:.0%} of tagged marks")
        if share < MODELLING_SHARE_MIN - 1e-9:
            notes.append(f"WARN  problem {number}: modelling share {share:.0%} of tagged marks is below one half"
                         " (standards S2, S3)")
    return report, notes


def guide_checks(path: Path, q_points: dict[str, float]) -> tuple[str, list[str]]:
    """The study guide (a checklist page or its JSON) lists every scored question once, with the same points."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return "", [f"ERROR study guide {path}: cannot read ({exc})"]
    if path.suffix.lower() in (".html", ".htm"):
        block = GUIDE_BLOCK.search(text)
        if not block:
            return "", [f"ERROR study guide {path.name}: no checklist-data block"]
        text = block.group(1).replace("<\\/", "</")
    try:
        data = json.loads(text)
    except ValueError as exc:
        return "", [f"ERROR study guide {path.name}: invalid JSON ({exc})"]
    if not isinstance(data, dict):
        return "", [f"ERROR study guide {path.name}: not a JSON object"]
    items = data.get("items") if isinstance(data.get("items"), dict) else {}
    groups = data.get("groups") if isinstance(data.get("groups"), list) else []
    nodes = [node for group in groups if isinstance(group, dict) and isinstance(group.get("nodes"), list)
             for node in group["nodes"]]
    notes, g_points, used = [], {}, set()
    for node in nodes:
        label = node.get("label") if isinstance(node, dict) else None
        if not isinstance(label, str):
            notes.append("ERROR study guide: a node without a text label")
            continue
        if label in g_points:
            notes.append(f"ERROR study guide: label {label} appears twice")
        points = node.get("points")
        valid = isinstance(points, (int, float)) and not isinstance(points, bool) and math.isfinite(points)
        g_points[label] = points if valid else None
        needs = node.get("needs", [])
        if not isinstance(needs, list):
            notes.append(f"ERROR study guide {label}: 'needs' is not a list")
            continue
        for item_id in needs:
            if not isinstance(item_id, str) or not isinstance(items.get(item_id), dict):
                notes.append(f"ERROR study guide {label}: unknown item {item_id!r}")
            else:
                used.add(item_id)
    for key in sorted(set(q_points) | set(g_points)):
        if key not in g_points:
            notes.append(f"ERROR study guide: no entry for question {key}")
        elif key not in q_points:
            notes.append(f"ERROR study guide: {key} is not a question of the paper")
        elif g_points[key] is None or abs(g_points[key] - q_points[key]) > 1e-9:
            notes.append(f"ERROR study guide {key}: points {node_points(g_points[key])}, question paper has "
                         f"{q_points[key]:g}")
    counts: dict[str, int] = {}
    for item_id in used:
        category = str(items[item_id].get("category"))
        counts[category] = counts.get(category, 0) + 1
    detail = ", ".join(f"{n} {c}" for c, n in sorted(counts.items()))
    return f"study guide: {len(g_points)} questions; items: {detail or 'none'}", notes


def node_points(value: object) -> str:
    return "missing or invalid" if value is None else f"{value:g}"


def boxed_answers(body: str) -> list[str]:
    answers = []
    for match in re.finditer(r"\\boxed\{", body):
        try:
            answers.append(body[match.end():group_end(body, match.end() - 1) - 1])
        except ValueError:
            continue
    return answers


def leak_checks(questions: str, sol: str) -> list[str]:
    notes, q_squashed = [], re.sub(r"\s+", "", questions)
    for answer in boxed_answers(sol):
        compact = re.sub(r"\s+", "", answer).rstrip(".,")
        if len(compact) >= 8 and compact in q_squashed:
            notes.append(f"WARN  boxed answer appears in question paper (fine if it is a 'prove that' target): {answer.strip()[:60]}")
        for number in NUMBER.findall(answer):
            digits = number.replace(".", "").lstrip("0")
            if len(digits) >= 3 and re.search(r"(?<![\d.])" + re.escape(number) + r"(?![\d])", questions):
                notes.append(f"WARN  number {number} from a boxed answer appears in question paper")
    return sorted(set(notes))


def problem_structure(body: str) -> list[str]:
    """Standards S3/S4: each problem has an introduction that asks the paper's question and a Useful information list."""
    notes = []
    starts = [(m.start(), m.group(1)) for m in re.finditer(r"\\problem\{([^}]*)\}", body)]
    for index, (start, number) in enumerate(starts):
        stop = starts[index + 1][0] if index + 1 < len(starts) else len(body)
        chunk = body[start:stop]
        first_part = chunk.find("\\parttitle")
        intro = chunk[:first_part if first_part > 0 else len(chunk)]
        prose = re.sub(r"\$[^$]*\$|\\\[.*?\\\]|\\[a-zA-Z]+|[{}]", " ", intro, flags=re.S)
        if len(prose.split()) < 60:
            notes.append(f"WARN  problem {number}: introduction shorter than 60 words before Part A")
        if "?" not in prose:
            notes.append(f"WARN  problem {number}: introduction states no question (end it with the question the paper answers)")
        if "Useful information" not in chunk:
            notes.append(f"WARN  problem {number}: no 'Useful information' list")
        if re.search(r"\\figtext\{[^}]*\basks\b", chunk):
            notes.append(f"WARN  problem {number}: a figure caption explains what is asked; keep captions descriptive")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("questions", type=Path)
    parser.add_argument("solutions", type=Path)
    parser.add_argument("--answers", type=Path, help="answer-sheet booklet to cross-check labels")
    parser.add_argument("--guide", type=Path, help="study guide JSON (or its HTML page) to cross-check labels and points")
    parser.add_argument("--total", type=float, help="expected total points")
    parser.add_argument("--problem-total", type=float, help="expected points of every problem (IPhO/APhO: 10)")
    parser.add_argument("--forbid", action="append", default=[], help="extra phrase that must not appear in questions")
    parser.add_argument("--allow-frames", action="store_true", help="do not flag status frames in the question paper")
    args = parser.parse_args()

    q_body = body_of(strip_comments(args.questions.read_text(encoding="utf-8")))
    s_body = body_of(strip_comments(args.solutions.read_text(encoding="utf-8")))
    q_items, q_problems = items(q_body, "problem", "question")
    s_items, s_problems = items(s_body, "problemsol", "soltitle")
    notes: list[str] = []

    q_points = {it.key: it.points for it in q_items}
    s_points = {it.key: it.points for it in s_items}
    for key in sorted(set(q_points) | set(s_points)):
        if key not in s_points:
            notes.append(f"ERROR {key}: no answer in solution booklet")
        elif key not in q_points:
            notes.append(f"ERROR {key}: answer without question")
        elif abs(q_points[key] - s_points[key]) > 1e-9:
            notes.append(f"ERROR {key}: {q_points[key]:g} pt in questions, {s_points[key]:g} pt in solutions")
    if len(q_points) != len(q_items):
        notes.append("ERROR duplicate question label inside one problem")
    total = sum(q_points.values())
    if args.total is not None and abs(total - args.total) > 1e-6:
        notes.append(f"ERROR total points {total:g}, expected {args.total:g}")
    for number, declared in q_problems.items():
        got = sum(v for k, v in q_points.items() if k.startswith(number + "."))
        if abs(got - declared) > 1e-6:
            notes.append(f"ERROR problem {number}: questions add to {got:g}, title says {declared:g}")
        if args.problem_total is not None and abs(declared - args.problem_total) > 1e-6:
            notes.append(f"ERROR problem {number}: {declared:g} points, expected {args.problem_total:g}")
    if args.answers:
        a_body = body_of(args.answers.read_text(encoding="utf-8"))
        labels, current = set(), ""
        for match in re.finditer(r"\\(sheetproblem|answerbox)\{([^}]*)\}", a_body):
            if match.group(1) == "sheetproblem":
                current = match.group(2).strip() + "."
            else:
                labels.add(current + match.group(2).split("(")[0].strip())
        for key in sorted(set(q_points) ^ labels):
            notes.append(f"ERROR {key}: question and answer sheet do not match")

    notes += problem_structure(q_body)
    sum_notes, tagged = marking_sums(s_body, s_items)
    notes += sum_notes
    share_report, share_notes = modelling_share(tagged, bool(s_problems))
    notes += share_notes
    guide_info = ""
    if args.guide:
        guide_info, guide_notes = guide_checks(args.guide, q_points)
        notes += guide_notes
    notes += leak_checks(q_body, s_body)
    for phrase in list(DEFAULT_FORBIDDEN) + args.forbid:
        if phrase in q_body:
            notes.append(f"ERROR forbidden text in question paper: {phrase!r}")
    for name in sorted(set(re.findall(r"[\w./-]+\.(?:md|ipynb|docx)\b", q_body))):
        notes.append(f"ERROR file name in question paper: {name}")
    if not args.allow_frames:
        for marker in STATUS_MARKERS:
            if marker in q_body:
                notes.append(f"ERROR research-status material in question paper ({marker.strip()}): move it to a solution appendix")

    print(f"questions: {len(q_items)} scored items in {len(q_problems) or 1} problem(s), {total:g} points; "
          f"solutions: {len(s_items)} answers")
    for line in share_report + ([guide_info] if guide_info else []):
        print(line)
    for line in notes:
        print(line)
    errors = sum(line.startswith("ERROR") for line in notes)
    print(f"{errors} error(s), {len(notes) - errors} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
