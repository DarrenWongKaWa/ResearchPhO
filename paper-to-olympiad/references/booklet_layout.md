# Booklet layout

Start from `assets/questions_template.tex` and `assets/solutions_template.tex`. Both are self-contained (no
`\input`, no image files): pictures are TikZ/pgfplots code inside the `.tex`. They compile with TeX Live 2023 or
newer (packages: newtxmath, helvet, tcolorbox, amsmath, mathtools, microtype, hyperref, dsfont, tikz, pgfplots,
needspace, enumitem, booktabs, tabularx, fancyhdr, lastpage).

## Order of the question booklet

1. Cover: title, total points, "How to use this booklet", the colour legend, points table, conventions.
2. Notation table (one symbol, one meaning).
3. Background (2-3 pages) with 2-3 pictures.
4. Toolkit (T1, T2, ...) and Glossary.
5. Reading map: the chain-of-objects picture and a table "step - why the next object is needed - questions".
6. Parts: each starts on a new page with `\parttitle{A}{title}{points}`; sub-sections flow without page breaks.
7. Synthesis part (X) for proposals.
8. Sources (by content, not by private file name) and optional public reading.

The solution booklet mirrors the order, adds marking lines, answer pictures, a solution map, teacher notes and a
progress register (available vs missing).

## Macros in the templates

| Macro | Booklet | Meaning |
| --- | --- | --- |
| `\question{A.1}{0.6}{text}` | questions | scored question box (unbreakable) |
| `\bridge{M.1}{1.0}{text}` | questions | scored multi-part "modelling bridge" box |
| `\extension{B.G1}{1.0}{text}` | questions | scored supplement box |
| `\begin{greenbox}{SOURCE --- title}` | both | AVAILABLE: result with a named source |
| `\begin{redbox}{ADDED MODEL --- title}` | both | NOT ESTABLISHED: toy model, given bound, open item |
| `\begin{figpanel}{title} ... \figtext{caption} \end{figpanel}` | both | blue PICTURE frame |
| `\hint{...}`, `\handoff{...}`, `\origin{...}` | questions | hint, connection to next step, source/scope note |
| `\soltitle{A.1}{0.6}{title}`, `\bridgesol`, `\extsol` | solutions | answer heading with points |
| `\marking{...}` | solutions | marking breakdown; numbers must sum to the points |

The checker (`scripts/check_booklets.py`) reads exactly these macros; keep their argument order.

## Pictures

- Question booklet: set-up only. Good: the lattice with labelled bonds; the drive; the band structure; a domain;
  a contour in the complex plane; a sliding time window; a number line with a tolerance band. Bad: the curve the
  question asks for.
- Caption pattern: one sentence saying what is shown, then "**X.1 asks:** ..." in plain words.
- Computed pictures: generate data with a script that rewrites a marked block in the `.tex`
  (`% ==== BEGIN GENERATED FIGURE DATA ... END`), so the file stays self-contained and reproducible. State the scope:
  "single-particle geometry; no interacting dynamics".
- Place each picture at the start of its part, before the question boxes. A large unbreakable box placed after the
  questions leaves half-empty pages.

## Page-break control

- `\smallheading` includes `\Needspace{6\baselineskip}`; add `\par\Needspace{14\baselineskip}\bigskip` before a
  sub-section title instead of `\clearpage`.
- Question boxes are unbreakable; green/red frames may break.
- Check every page in contact sheets; fix pages that are less than one third full unless a part ends there.

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error questions.tex > build.stdout
pdflatex -interaction=nonstopmode -halt-on-error questions.tex > build.stdout
grep -c Overfull questions.log      # must be 0
```

Never redirect output to `questions.out`: hyperref writes its bookmarks to that file.
