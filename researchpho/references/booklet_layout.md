# Booklet layout

Start from `assets/questions_template.tex` and `assets/solutions_template.tex`; generate the answer sheets with
`scripts/make_answer_sheets.py` and the checklist pages with `scripts/make_checklist.py`. All files are self-contained (no `\input`, no image files): figures are TikZ/pgfplots
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

1. Cover (S0-1): how to mark, what (C) and (M) mean, mark allocation per problem.
2. Per problem (S1-, S2-, S3-): parts and answers in question order, each followed by `\marking{...}`; answer
   figures. Tag every number of a marking line: (M) for a modelling step (setting up the model, choosing the
   physics, interpreting a result, judging its scope), (C) for a computation step (algebra, solving, evaluating).
   A piece that mixes both is split into two numbers, or tagged by its larger part. Most of each problem's marks go
   to (M) (S2, S3); `check_booklets.py` reports the share and warns below one half.
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
every toolbox result in the answer script. Tutor mode uses these entries as the third rung of help.

## Checklist flowcharts (study guide, research checklist, author checklist)

One self-contained HTML component draws a checklist as a flowchart: a **main line** of nodes down the middle,
grouped (for example by problem); **two categories** of items on its left and right sides, each in its own colour
and frame; a checkbox on every item; progress bars per category, for all items, and per group. Ticks are stored in
`localStorage` inside try/catch, so the page still works where storage is blocked. Light and dark themes follow the
system and can be switched; at phone width the chart becomes one column with the main line on the left. Filter
buttons show one category at a time; clearing all ticks takes two clicks. An item is drawn in full at the first
node that needs it and as a dashed reminder at later nodes; the reminders share its checkbox. A node turns green
when all its items are ticked.

Build a page from JSON: `python3 scripts/make_checklist.py data.json page.html --profile <use>` (template
`assets/checklist_template.html`; no external files). The script validates the data, refuses unknown items,
duplicate labels and unattached items, and writes the data into the page.

Data (`schema: researchpho-checklist/1`):

```json
{"eyebrow": "ResearchPhO study guide", "title": "...", "intro": "...", "storageKey": "researchpho-guide:<slug>",
 "emptyNote": "Nothing beyond the stated level.",
 "categories": [{"id": "tool", "name": "Computation tool", "plural": "Computation tools", "colour": "blue",
                 "noteLabel": "", "refLabel": "Resource"},
                {"id": "idea", "name": "Modelling idea", "plural": "Modelling ideas", "colour": "orange",
                 "refLabel": "Resource"}],
 "items": {"frame-change": {"category": "tool", "name": "...", "meta": "...", "note": "...", "ref": "...",
                            "url": "https://..."}},
 "start": {"title": "...", "text": "..."}, "end": {"title": "...", "text": "..."},
 "groups": [{"title": "Problem 1: ...", "short": "Problem 1", "note": "...", "nodes": [
   {"label": "1.C.1", "title": "...", "points": 2.3, "meta": "...", "note": "...", "needs": ["frame-change"]}]}],
 "footer": ["..."]}
```

| Field | Meaning |
| --- | --- |
| `categories` | exactly two: the first hangs on the left, the second on the right; `colour` is blue, orange, amber, red, green or purple; `noteLabel` and `refLabel` prefix an item's note and reference |
| `items` | `name` (required), `meta` (a small line, e.g. the question labels), `note` (one line), `ref` with an optional `url` (http or https only) |
| `groups[].nodes` | `label` (unique), `title`, `points` (shown as "x pt") or `meta`, `note`, `needs` (item ids, in display order) |
| `start`, `end` | optional terminal boxes at the two ends of the main line |
| `storageKey` | one key per page and exam, so that two pages never share ticks |

Three uses, each a profile of `make_checklist.py`:

| Use | Main line | Left (colour) | Right (colour) | Tick means |
| --- | --- | --- | --- | --- |
| study guide (`--profile study-guide`) | the questions in exam order, grouped by problem | computation tools (blue) | modelling ideas (orange) | the reader can use it without looking it up |
| research checklist (`--profile research`) | the chain of objects of Appendix A, from the model to the measured quantity | O-calc open links (amber) | O-theory open links (red) | a result closes the link |
| author checklist (`--profile author`; data in `assets/author_checklist.json`) | the eleven workflow steps | standards S1-S8 (purple) | verification checks (green) | the exam meets it, or the check ran and was read |

**Study guide.**

1. State the reader level. Default: an undergraduate who knows the four core physics courses (classical mechanics,
   electromagnetism, quantum mechanics, thermal and statistical physics) and their mathematics.
2. For each question, list what it needs beyond that level. Read the solution, not only the question. A question
   that needs nothing new gets an empty list.
3. Tag each item `tool` (a piece of mathematics the reader calculates with, such as a partial trace) or `idea` (a
   physical concept or model choice the reader reasons with, such as adiabatic following).
4. Give one resource per item, with the chapter or section when you are sure of it and a link when one exists.
   Check every link and every arXiv number.
5. Never answer a question in the guide. Item names and node notes name prerequisites and what is asked, never
   results ("short-time transition probabilities", not "a t^2 start is not a decay rate").

`check_booklets.py --guide study_guide.json` checks that every scored question appears once with the same points.

**Research checklist.** One node per object of the chain of objects, with its label (S, P, D, D/O-calc,
D/O-theory, O-theory) as `meta` and its questions as `note`; one item per row of the open-link table, attached to
the object it concerns, with the failing hypothesis or the closing calculation as `note`, the closest existing
theory as `ref`, and the questions as `meta`. Put the model in `start`, the research target in `end`, and the
shared gap in `footer`. It contains no more than Appendix A, so it is public exactly when the solutions are.

**Author checklist.** Copy `assets/author_checklist.json`, set `title` and `storageKey`, and build it; tick the
items while the exam is written and verified.

Render every page once at desktop and phone width, in both themes, and look at it.

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
