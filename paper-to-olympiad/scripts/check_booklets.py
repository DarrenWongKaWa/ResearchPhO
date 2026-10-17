#!/usr/bin/env python3
"""Consistency and leak checks for a question booklet and its solution booklet.

Reads the macros of the paper-to-olympiad templates:
  questions: \\question{label}{points}{text}, \\bridge{...}{...}{...}, \\extension{...}{...}{...}
  solutions: \\soltitle{label}{points}{title}, \\bridgesol{...}, \\extsol{...}, \\marking{...}

Usage:
  python3 check_booklets.py questions.tex solutions.tex [--total 10.0] [--forbid PHRASE ...]

Exit code 1 if any ERROR is found. WARN lines need a human look.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

QUESTION_MACROS = ("question", "bridge", "extension")
SOLUTION_MACROS = ("soltitle", "bridgesol", "extsol")
DEFAULT_FORBIDDEN = (
    "this conversation",
    "/Users/",
    "C:\\",
    "TODO",
    "FIXME",
)
NUMBER = re.compile(r"(?<![\w.])(\d+\.\d+)(?![\w])")


@dataclass(frozen=True)
class Item:
    label: str
    points: float
    text: str
    end: int


def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


def brace_groups(tex: str, start: int, count: int) -> tuple[list[str], int]:
    """Return `count` balanced {...} groups starting at index `start`."""
    groups, pos = [], start
    for _ in range(count):
        while pos < len(tex) and tex[pos].isspace():
            pos += 1
        if pos >= len(tex) or tex[pos] != "{":
            raise ValueError(f"expected '{{' at offset {pos}")
        depth, begin = 1, pos + 1
        pos += 1
        while depth:
            if pos >= len(tex):
                raise ValueError("unbalanced braces")
            char = tex[pos]
            if char == "\\":
                pos += 2
                continue
            depth += {"{": 1, "}": -1}.get(char, 0)
            pos += 1
        groups.append(tex[begin:pos - 1])
    return groups, pos


def items(tex: str, macros: tuple[str, ...]) -> list[Item]:
    found = []
    pattern = re.compile(r"\\(" + "|".join(macros) + r")(?=\s*\{)")
    for match in pattern.finditer(tex):
        # skip macro definitions such as \newcommand{\question}[3]{...}
        if tex[max(0, match.start() - 12):match.start()].endswith("newcommand{"):
            continue
        try:
            (label, points, text), end = brace_groups(tex, match.end(), 3)
            found.append(Item(label.strip(), float(points), text, end))
        except ValueError:
            continue
    return found


def strip_math(text: str) -> str:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    return re.sub(r"\$[^$]*\$", " ", text)


def marking_sums(sol: str, sol_items: list[Item]) -> list[str]:
    """Sum the decimals (outside math) of the marking text after each answer."""
    notes = []
    ordered = sorted(sol_items, key=lambda it: it.end)
    for index, item in enumerate(ordered):
        stop = ordered[index + 1].end if index + 1 < len(ordered) else len(sol)
        segment = sol[item.end:stop]
        marks = []
        for match in re.finditer(r"\\marking\{", segment):
            (body,), _ = brace_groups(segment, match.end() - 1, 1)
            marks.append(body)
        if not marks:
            notes.append(f"WARN  {item.label}: no \\marking line")
            continue
        total = sum(float(x) for body in marks for x in NUMBER.findall(strip_math(body)))
        if abs(total - item.points) > 1e-6:
            notes.append(f"WARN  {item.label}: marking numbers sum to {total:g}, points are {item.points:g}")
    return notes


def boxed_answers(sol: str) -> list[str]:
    answers = []
    for match in re.finditer(r"\\boxed\{", sol):
        try:
            (body,), _ = brace_groups(sol, match.end() - 1, 1)
            answers.append(body)
        except ValueError:
            continue
    return answers


def squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def leak_checks(questions: str, sol: str) -> list[str]:
    notes = []
    q_squashed = squash(questions)
    for answer in boxed_answers(sol):
        compact = squash(answer).rstrip(".,")
        if len(compact) >= 8 and compact in q_squashed:
            notes.append(f"WARN  boxed answer appears in question booklet: {answer.strip()[:70]}")
        for number in NUMBER.findall(answer):
            digits = number.replace(".", "").lstrip("0")
            if len(digits) >= 3 and re.search(r"(?<![\d.])" + re.escape(number) + r"(?![\d])", questions):
                notes.append(f"WARN  number {number} from a boxed answer appears in question booklet")
    return sorted(set(notes))


def forbidden(questions: str, phrases: list[str]) -> list[str]:
    notes = [f"ERROR forbidden text in question booklet: {p!r}" for p in phrases if p in questions]
    for name in sorted(set(re.findall(r"[\w./-]+\.(?:md|ipynb|docx)\b", questions))):
        notes.append(f"ERROR file name in question booklet: {name}")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("questions", type=Path)
    parser.add_argument("solutions", type=Path)
    parser.add_argument("--total", type=float, default=None, help="expected total points")
    parser.add_argument("--forbid", action="append", default=[], help="extra phrase that must not appear in questions")
    args = parser.parse_args()

    questions = strip_comments(args.questions.read_text(encoding="utf-8"))
    sol = strip_comments(args.solutions.read_text(encoding="utf-8"))
    q_items = items(questions, QUESTION_MACROS)
    s_items = items(sol, SOLUTION_MACROS)
    notes: list[str] = []

    q_points = {it.label: it.points for it in q_items}
    s_points = {it.label: it.points for it in s_items}
    for label in sorted(set(q_points) | set(s_points)):
        if label not in s_points:
            notes.append(f"ERROR {label}: no answer in solution booklet")
        elif label not in q_points:
            notes.append(f"ERROR {label}: answer without question")
        elif abs(q_points[label] - s_points[label]) > 1e-9:
            notes.append(f"ERROR {label}: {q_points[label]:g} pt in questions, {s_points[label]:g} pt in solutions")
    for label in {it.label for it in q_items if [x.label for x in q_items].count(it.label) > 1}:
        notes.append(f"ERROR {label}: label used twice in questions")
    total = sum(q_points.values())
    if args.total is not None and abs(total - args.total) > 1e-6:
        notes.append(f"ERROR total points {total:g}, expected {args.total:g}")

    notes += marking_sums(sol, s_items)
    notes += leak_checks(questions, sol)
    notes += forbidden(questions, list(DEFAULT_FORBIDDEN) + args.forbid)

    print(f"questions: {len(q_items)} scored items, {total:g} points; solutions: {len(s_items)} answers")
    for line in notes:
        print(line)
    errors = sum(line.startswith("ERROR") for line in notes)
    print(f"{errors} error(s), {len(notes) - errors} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
