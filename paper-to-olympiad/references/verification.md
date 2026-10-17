# Verification

A booklet is finished only when four kinds of check pass. Record their output next to the booklets.

## 1. Document checker

```bash
python3 scripts/check_booklets.py questions.tex solutions.tex --total 10.0 \
    --forbid "200T" --forbid "internal note"
```

It reports:

- **labels and points**: every scored label appears once in each booklet with the same points; the sum equals
  `--total` (errors);
- **marking sums**: decimals outside math in each `\marking{}` add up to the question's points (warnings; a line
  such as "each link: 0.1" needs a manual look);
- **answer leaks**: boxed answers from the solutions (`\boxed{...}`) that appear verbatim in the question
  booklet, and numbers with three or more significant digits from boxed answers (warnings: given data can look
  like an answer, and a statement the reader is asked to prove appears in both booklets by design);
- **forbidden text**: internal paths (`/Users/`, `C:\`), "this conversation", `.md` file names, TODO, and your
  `--forbid` phrases (errors).

## 2. Answer scripts

Write one script that recomputes every derivable answer and saves JSON:

- identities: random Hermitian/unitary matrices, compare both sides (tolerance 1e-10);
- exact numbers: rational arithmetic or high precision (e.g. constants from a contour estimate);
- toy-model dynamics: matrix exponentials at small time for short-time coefficients;
- arithmetic answers (certificate times, classifications).

The worked example's `verify` script also compares the new prompts with the previous revision after a notation map,
so that a "notation-only" change is proved to be notation-only.

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

- "OPEN: the result does not select a flavor" right after "Does it establish a selected flavor?";
- a hand-off paragraph that summarizes the conclusion of the previous question;
- a box title or caption with the final number;
- a research-status table that lists exactly the missing inputs a synthesis question asks for.
