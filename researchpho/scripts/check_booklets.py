#!/usr/bin/env python3
"""Consistency, format and leak checks for a ResearchPhO question paper and its solutions.

Reads the macros of the ResearchPhO templates:
  questions: \\problem{n}{title}{points}, \\question{label}{points}{text}
  solutions: \\problemsol{n}{title}{points}, \\soltitle{label}{points}{title}, \\marking{...}, \\appendixstart
Labels are keyed as "n.label" (e.g. 2.B.1); files without \\problem use the bare label.

Usage:
  python3 check_booklets.py questions.tex solutions.tex [--total 30] [--problem-total 10]
                            [--answers answersheets.tex] [--forbid PHRASE ...] [--allow-frames]

Exit code 1 if any ERROR is found. WARN lines need a human look.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_FORBIDDEN = ("this conversation", "/Users/", "C:\\", "TODO", "FIXME")
# research-status material belongs in the solution appendices, not in the question paper
STATUS_MARKERS = ("\\begin{greenbox}", "\\begin{redbox}", "\\origin{", "\\handoff{", "NOT ESTABLISHED",
                  "AVAILABLE ---", "OPEN ---", "ADDED MODEL", "GIVEN BOUND", "PICTURE ")
NUMBER = re.compile(r"(?<![\w.])(\d+\.\d+)(?![\w])")


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


def marking_sums(body: str, sol_items: list[Item]) -> list[str]:
    notes = []
    stop_all = body.find("\\appendixstart")
    stop_all = len(body) if stop_all < 0 else stop_all
    ordered = sorted(sol_items, key=lambda it: it.end)
    for index, item in enumerate(ordered):
        stop = ordered[index + 1].end if index + 1 < len(ordered) else stop_all
        segment = body[item.end:stop]
        total, found = 0.0, False
        for match in re.finditer(r"\\marking\{", segment):
            found = True
            text = segment[match.end():group_end(segment, match.end() - 1) - 1]
            total += sum(float(x) for x in NUMBER.findall(strip_math(text)))
        if not found:
            notes.append(f"WARN  {item.key}: no \\marking line")
        elif abs(total - item.points) > 1e-6:
            notes.append(f"WARN  {item.key}: marking numbers sum to {total:g}, points are {item.points:g}")
    return notes


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
    parser.add_argument("--total", type=float, help="expected total points")
    parser.add_argument("--problem-total", type=float, help="expected points of every problem (IPhO/APhO: 10)")
    parser.add_argument("--forbid", action="append", default=[], help="extra phrase that must not appear in questions")
    parser.add_argument("--allow-frames", action="store_true", help="do not flag status frames in the question paper")
    args = parser.parse_args()

    q_body = body_of(strip_comments(args.questions.read_text(encoding="utf-8")))
    s_body = body_of(strip_comments(args.solutions.read_text(encoding="utf-8")))
    q_items, q_problems = items(q_body, "problem", "question")
    s_items, _ = items(s_body, "problemsol", "soltitle")
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
    notes += marking_sums(s_body, s_items)
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
    for line in notes:
        print(line)
    errors = sum(line.startswith("ERROR") for line in notes)
    print(f"{errors} error(s), {len(notes) - errors} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
