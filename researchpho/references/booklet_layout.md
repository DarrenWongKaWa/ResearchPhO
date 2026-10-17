# Booklet layout

Start from `assets/questions_template.tex` and `assets/solutions_template.tex`; generate the answer sheets with
`scripts/make_answer_sheets.py`. All files are self-contained (no `\input`, no image files): figures are TikZ/pgfplots
code inside the `.tex`. TeX Live 2023 or newer (newtxmath, helvet, tcolorbox, amsmath, mathtools, microtype,
hyperref, dsfont, tikz, pgfplots, needspace, enumitem, booktabs, tabularx, fancyhdr).

## Question paper (strict IPhO/APhO theory format)

1. Cover, page code G-1: title, "Theoretical examination, 30 points", general instructions (5 hours; three problems of
   10 points; calculator; answer sheets; front side only; problems independent; conventions such as hbar = 1), a
   table of the three problems.
2. Each problem starts on a new page, page codes T1-1, T1-2, ...: "Problem n: title (10 points)", an introduction
   (system, phenomenon, model, conventions; a footnote may cite the source papers), numbered figures, "Useful
   information" (only the facts this problem needs), then parts "Part A. title (x points)" with context, given data
   and boxed subquestions.
3. "End of the theoretical examination".

Nothing else: no status frames, source boxes, scope lines, hand-offs, reading maps, glossary or toolkit pages.

## Answer sheets

Page codes A1-1, ...; one framed box per subquestion, one per sub-part (a), (b), ...; box height grows with points.
Generate them after the question paper is final: `python3 make_answer_sheets.py questions.tex answersheets.tex`.

## Solutions

1. Cover (S0-1): how to mark, mark allocation per problem.
2. Per problem (S1-, S2-, S3-): parts and answers in question order, each followed by `\marking{...}`; answer
   figures.
3. `\appendixstart` (SA-): Appendix A paper map (what each paper answers, the language map, the chain of objects
   with open arrows); Appendix B
   source, scope and open conditions per question (green/red frames are allowed here); Appendix C register of
   available and missing results; Appendix D teacher notes (provenance, interpretations to confirm, label maps
   between revisions, independent checks, sources).

## Macros

| Macro | Booklet | Meaning |
| --- | --- | --- |
| `\problem{n}{title}{10.0}` | questions | new problem: page code Tn, figure numbers n.k |
| `\parttitle{A}{title}{points}` | both | part heading with its points |
| `\question{A.1}{0.8}{text}` | questions | boxed subquestion; use `\textbf{(a)}` for sub-parts |
| `\hint{...}` | questions | names a tool, never the step |
| `\begin{figpanel}{title} ... \figtext{caption} \end{figpanel}` | both | plain numbered figure |
| `\problemsol{n}{title}{10.0}` | solutions | solutions of problem n, page code Sn |
| `\soltitle{A.1}{0.8}{title}` | solutions | answer heading with points |
| `\marking{...}` | solutions | decimals outside math add up to the points |
| `\appendixstart` | solutions | page code SA; research context starts |
| `greenbox`, `redbox` | solutions appendices only | source/scope and open conditions |

The checker reads exactly these macros; keep their argument order.

## Figures

- Question paper: set-up only, plain caption ("Figure 1.3. Centres of localized orbitals. ..."). No "the question
  asks" text, no answer curves.
- Computed figures: generate data with a script that rewrites a marked block in the `.tex`
  (`% ==== BEGIN GENERATED FIGURE DATA ... END`), and state the scope in the caption.
- Put a figure next to the text that first uses it; keep figure and caption in one unbreakable minipage.

## Page-break control

- `\parttitle` and `\smallheading` include `\Needspace`; question boxes are unbreakable.
- Look at every page in contact sheets; fix pages less than one third full unless a problem ends there.

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error questions.tex > build.stdout   # twice
grep -a -c Overfull questions.log                                              # must be 0
```

Never redirect output to `questions.out`: hyperref writes its bookmarks to that file.
