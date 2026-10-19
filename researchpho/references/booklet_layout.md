# Booklet layout

## Deliverable folder

Deliver exactly three files in a folder named after the main paper, `<PaperName>_RPhO/` (the short title in
CamelCase, for example `MultiBandFractionalThoulessPumps_RPhO/`):

```
<PaperName>_RPhO/
  questions.pdf
  solutions.pdf
  checklist.html
```

Write and build everything in a separate working folder (LaTeX sources, scripts, `checklist.json`, logs); copy only
the three files into the deliverable folder. There is no answer-sheet booklet: the reader writes on plain sheets and
labels each answer with its question.

## Sources

Start from `assets/questions_template.tex` and `assets/solutions_template.tex`; build the checklist page with
`scripts/make_checklist.py`. All files are self-contained (no `\input`, no image files): figures are TikZ/pgfplots
code inside the `.tex`. TeX Live 2023 or newer (newtxmath, helvet, tcolorbox, amsmath, mathtools, microtype,
hyperref, dsfont, tikz, pgfplots, needspace, enumitem, booktabs, tabularx, fancyhdr).

## Question paper (strict IPhO/APhO theory format)

1. Cover, page code G-1: title, "Theoretical examination, 30 points", general instructions (5 hours; three problems of
   10 points; calculator; answers on plain sheets, labelled by question; front side only; problems independent; conventions such as hbar = 1), a
   table of the three problems.
2. Each problem starts on a new page, page codes T1-1, T1-2, ...: "Problem n: title (10 points)", an introduction
   (system, phenomenon, model, conventions; a footnote may cite the source papers), numbered figures, "Useful
   information" (only the facts this problem needs), then parts "Part A. title (x points)" with context, given data
   and boxed subquestions.
3. "End of the theoretical examination".

Nothing else: no status frames, source boxes, scope lines, hand-offs, reading maps, glossary or toolkit pages.

## Solutions

1. Cover (S0-1): how to mark, what (C) and (M) mean, mark allocation per problem.
2. Per problem (S1-, S2-, S3-): parts and answers in question order, each followed by `\marking{...}`; answer
   figures. Tag every number of a marking line: (M) for a modelling step (setting up the model, choosing the
   physics, interpreting a result, judging its scope), (C) for a computation step (algebra, solving, evaluating).
   A piece that mixes both is split into two numbers, or tagged by its larger part. More than half of each problem's
   marks go to (M) (S2, S3); `check_booklets.py` reports the share and warns below one half. When a problem holds a
   pure derivation (a proof reconstruction), give that question a last part that asks what the result establishes
   and what it does not, instead of inflating the (M) share elsewhere.
3. `\appendixstart` (SA-): Appendix A paper map (what each paper answers, the language map, the chain of objects
   with each arrow labelled D, O-calc or O-theory, and the open-link table: link, kind, closest existing theory,
   failing hypothesis or closing calculation, shared gap); Appendix B
   source, scope and open conditions per question (green/red frames are allowed here); Appendix C register of
   available and missing results, with the kind of each missing item; Appendix D teacher notes (provenance,
   interpretations to confirm, label maps between revisions, independent checks, sources); Appendix E toolbox
   (next section). A booklet without a register keeps the order and shifts the letters (the worked example has
   A paper map, B notes, C teacher notes, D toolbox).

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
| `\marking{...}` | solutions | decimals outside math add up to the points; each may be followed by (C) or (M) |
| `\appendixstart` | solutions | page code SA; research context starts |
| `greenbox`, `redbox` | solutions appendices only | source/scope and open conditions |

The checker reads exactly these macros; keep their argument order.

## Toolbox appendix (last appendix of the solutions)

For every tool stated under "Useful information", in a hint, or as a given identity, that is above the reader's
level, give the smallest worked example. One entry per tool:

- **Statement**: the line exactly as in the question paper, with the problem it belongs to.
- **Smallest example**: the smallest case in which the tool does something, computed in full and checked a second
  way. A 3-site ring determinant before the 5-site one; the N = 2 case of a product identity before general N; one
  qubit before a chain.
- **Used in**: the question labels.

The example teaches the tool, never an exam step: do not reuse a question's model with other numbers. Recompute
every toolbox result in the answer script.

## The checklist page

One self-contained HTML page (`checklist.html`, built from `checklist.json` with `scripts/make_checklist.py`; template
`assets/checklist_template.html`). Its look: a light grid background, a serif display face for titles, a sans-serif
body, a monospace face for labels; a vertical **main line** with terminal boxes at both ends.

- **Exam segment.** One group per problem (its heading shows the points and the question the paper answers), one
  node per question (label, points, a short title). Beside each node: the **computation tools** it needs beyond the
  reader's level in blue frames on the left, the **modelling ideas** in orange frames on the right.
- **Research segment.** After the exam, one dashed group: the chain of objects of Appendix A, one node per object
  with its label (D, D/O-calc, D/O-theory, O-theory) as a coloured tag; its open links hang beside it, **O-calc** in
  amber on the left and **O-theory** in red on the right.
- **Items.** A checkbox, a title, one short note (one line) and one reference, linked to the source (DOI, arXiv or
  publisher page) whenever a stable link exists. An item appears in full at the first node that needs it and as a
  dashed reminder later; the reminders share its tick.
- **Progress.** Bars per category, for all items, and per group; a node turns green when all its items are ticked.
  Filter buttons show one category; clearing all ticks takes two clicks. Ticks are stored in `localStorage` inside
  try/catch. Light and dark themes; one column at phone width.

Data (`schema: researchpho-checklist/2`):

```json
{"lang": "en", "eyebrow": "ResearchPhO · arXiv:...", "title": "the exam title", "intro": "one or two sentences",
 "storageKey": "<slug>", "emptyNote": "—",
 "categories": [{"id": "tool", "name": "Computation tool", "plural": "Computation tools", "colour": "blue", "side": "left"},
                {"id": "idea", "name": "Modelling idea", "plural": "Modelling ideas", "colour": "orange", "side": "right"},
                {"id": "O-calc", "name": "Open link: calculation", "plural": "O-calc links", "colour": "amber", "side": "left"},
                {"id": "O-theory", "name": "Open link: new theory", "plural": "O-theory links", "colour": "red", "side": "right"}],
 "items": {"frame-change": {"category": "tool", "name": "...", "note": "...", "ref": "...", "url": "https://..."}},
 "start": {"title": "Start: the four core physics courses", "text": "..."},
 "end": {"title": "Research target", "text": "..."},
 "groups": [{"kind": "exam", "title": "...", "short": "Problem 1", "points": 10, "note": "the paper's question",
             "nodes": [{"label": "1.C.1", "title": "...", "points": 1.2, "needs": ["frame-change"]}]},
            {"kind": "research", "title": "From the exam to the open problem", "short": "Research", "note": "...",
             "nodes": [{"label": "p12(k, phi)", "meta": "D/O-theory", "title": "...", "needs": ["following-one-flavor"]}]}],
 "footer": ["..."]}
```

Rules (profile `rpho`, the default of `make_checklist.py`):

1. Reader level: an undergraduate who knows the four core physics courses and their mathematics, unless the user
   names another reader. For each question list only what it needs beyond that level; read the solution, not only
   the question. A question that needs nothing new gets an empty list.
2. Tag each item `tool` (mathematics the reader calculates with, such as a partial trace) or `idea` (a physical
   concept or model choice the reader reasons with, such as adiabatic following).
3. Keep the text short: a title, one line of note, one reference. Give the chapter or section when you are sure of
   it, and a link when a stable one exists; check every link and every arXiv number.
4. Never answer a question in the checklist. Names and notes name prerequisites, never results ("short-time
   transition probabilities", not "a t^2 start is not a decay rate").
5. The research segment holds no more than Appendix A (the chain, the open-link table, the shared gap in `footer`),
   so the checklist is public exactly when the solutions are.

`check_booklets.py --checklist checklist.json` checks that every scored question appears once with the same points.
The optional author checklist (`assets/author_checklist.json`, `--profile author`) tracks the workflow steps,
standards S1-S8 and checks with the same page. Render the page once at desktop and phone width, in both themes, and
look at it.

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
