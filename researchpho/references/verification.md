# Verification

A booklet is finished only when four kinds of check pass. Record their output next to the booklets.

## 1. Document checker

```bash
python3 scripts/check_booklets.py questions.tex solutions.tex --answers answersheets.tex \
    --total 30 --problem-total 10 --guide study_guide.json --forbid "200T"
```

It reports:

- **labels and points**: every scored label (problem.part.number) appears once in each booklet and on the answer
  sheets with the same points; every problem adds up to its title and to `--problem-total`; the sum equals
  `--total` (errors);
- **marking sums**: decimals outside math in each `\marking{}` add up to the question's points (warnings; a line
  such as "each link: 0.1" needs a manual look);
- **modelling share** (standards S2, S3): when marking numbers carry tags, "0.45 (M)" or "0.3 (C)", the marks per
  problem by tag and the modelling share of the tagged marks; a warning when it is below one half, and a warning for
  a tag that does not directly follow a number. Untagged lines are valid and are reported as untagged;
- **study guide** (`--guide study_guide.json`, or its HTML page): every scored question appears once in the guide
  with the same points, and every item a question needs is defined (errors);
- **answer leaks**: boxed answers from the solutions (`\boxed{...}`) that appear verbatim in the question
  booklet, and numbers with three or more significant digits from boxed answers (warnings: given data can look
  like an answer, and a statement the reader is asked to prove appears in both booklets by design);
- **research material in the question paper**: green/red frames, `\origin`, `\handoff`, "NOT ESTABLISHED",
  "AVAILABLE ---", "OPEN ---", "ADDED MODEL", "GIVEN BOUND", "PICTURE", "O-calc", "O-theory" (errors; move them
  to the appendices);
- **forbidden text**: internal paths (`/Users/`, `C:\`), "this conversation", `.md` file names, TODO, and your
  `--forbid` phrases (errors).

## 1b. Cold read (standards S3, S4)

Give one problem at a time to a fresh agent that has not seen the papers: "Do not solve the problem. List (a)
every term, symbol, number or assumption you cannot interpret from this text alone; (b) every step that needs
mathematics not provided in the text; (c) in your own words, the question this problem says the paper answers."
Fix (a) with the language map and definitions at first use, (b) with "Useful information", target results or
hints, and (c) by rewriting the end of the introduction. Record the final cold-read output with the booklets.

## 1c. Trial solve (after the cold read)

The cold read finds what the reader cannot interpret; the trial solve finds where a reader at the target level
gets stuck while solving, and what it misreads. Give the question paper (no solutions, no papers, no appendices) to
a fresh agent, one problem at a time: "You are [the reader level of the study guide]. Solve each question as in the
exam. For every question record: (1) your answer; (2) every place where you got stuck, with the step and what was
missing; (3) every sentence, symbol or figure you first understood differently from what you later concluded, and
why; (4) the tools or ideas you needed that you did not have."

Compare the records with the solutions and use them:

| Record | Use |
| --- | --- |
| stuck because a tool is missing | a line in "Useful information" and a toolbox entry; an item in the study guide |
| stuck because a step is too large | split the question, or give the intermediate result as a target |
| a misreading of the text or a figure | fix the text (define the symbol in the text, rename a letter used twice); add it to the misreading list of the tutor card |
| a misreading of the physics | the misreading list of the tutor card, with the counterexample that refutes it |
| a wrong answer by a reasonable route | a candidate partial-credit marking line, tagged (C) or (M) |
| (4) differs from the study guide | add or remove study-guide items |

Repeat the trial solve after large changes. Keep the records with the booklets; do not publish them with the exam.

## 2. Answer scripts

Write one script that recomputes every derivable answer and saves JSON:

- identities: random Hermitian/unitary matrices, compare both sides (tolerance 1e-10);
- exact numbers: rational arithmetic or high precision (e.g. constants from a contour estimate);
- toy-model dynamics: matrix exponentials at small time for short-time coefficients;
- arithmetic answers (certificate times, classifications);
- every result in the toolbox appendix.

When a revision regroups or renames questions, compare the new prompts with the previous revision after applying
the label map and the listed edits, so that a "relabel-only" change is proved to be relabel-only.

## 3. Independent physics checks

- **Signs and conventions**: recompute one transported quantity by a different method. In the worked example, the
  Wannier-centre motion and an explicit time evolution of a filled band both gave +2 per period, which agreed with
  the paper's figure but not with the sign of the current formula printed in the paper.
- **Scope of computed pictures**: if a picture shows single-particle geometry, say so; do not let it stand in for
  the interacting dynamics the problem is about.
- **Numbers taken from reports**: copy them exactly, give units, and define each quantity; mark your own
  definitions for the author to confirm.

## 4. Visual check

```bash
python3 scripts/render_sheets.py questions.pdf sheets/ --dpi 45 --cols 8 --rows 2
```

Look at every sheet: half-empty pages, split boxes, headings at the bottom of a page, overlapping labels in
pictures, text running into margins. Then open single pages at 80-100 dpi for pictures.

## 5. Leak review by hand

The checker cannot read meaning. Before release, read every frame that follows a question and every caption and
title with one question in mind: "does this sentence answer something the reader is asked?" Typical leaks:

- any scope or status remark in the question paper (it belongs to Appendix B);
- a sentence in an introduction that summarizes the conclusion of a question;
- a box title or caption with the final number;
- a research-status table that lists exactly the missing inputs a synthesis question asks for.
