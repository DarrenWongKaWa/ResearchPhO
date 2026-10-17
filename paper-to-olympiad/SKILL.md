---
name: paper-to-olympiad
description: Turn research papers, the literature of a new field, or a research proposal into a self-contained IPhO/APhO/PanPhO-style guided problem set - a question booklet a reader can solve without the papers, plus a solution booklet with marking scheme - so that people learn the field by solving it. Use when someone wants to learn a new field or paper quickly, write olympiad-style or APhO/IPhO-style problems from papers, turn a proposal into guided questions with an available/missing register, or check such a booklet for answer leaks, notation clashes, missing definitions, point totals and layout. Triggers include 用论文出题, 出一套 APhO/IPhO 风格的题, 奥赛风格, 快速入门新领域, 读文献出题, proposal 拆成题目, guided problem set, paper to problems.
---

# Paper to olympiad: learn a field by writing its exam

A physics-olympiad theory problem (IPhO, APhO, PanPhO) is a very efficient learning format: one long problem
introduces an unfamiliar topic in plain words, then breaks it into 15-25 small steps, each with points, given data
and a checkable answer. IPhO rules even require that any concept outside the syllabus be "explained in terms of
topics in the Syllabus". This skill applies that format to research papers and proposals.

The output is two booklets: **Questions** (self-contained; no answers anywhere, including captions and box titles)
and **Solutions** (worked answers, marking breakdowns, teacher notes on provenance). The worked example in
`examples/mb1-fractional-pump/` was built from two arXiv papers on fractional Thouless pumps and projector geometry.

## When to use

- A person must enter a new field from a few papers, or teach a group the core of a paper.
- A research proposal must be checked: which steps are derivable now, which inputs are missing.
- An existing problem set must be audited: answer leaks, undefined jargon, symbol clashes, points, layout.

Not for: summarizing a paper in prose, or writing real olympiad exams for official use.

## Decide first (ask only what you cannot infer)

| Choice | Default |
| --- | --- |
| Goal | learn the field; for a proposal, add the synthesis question and the available/missing register |
| Reader level | advanced undergraduate in olympiad format; for a true olympiad, high-school mathematics only |
| Output | Full: LaTeX booklets + PDF (`assets/`). Lite: one Markdown sheet with 8-12 questions and answers |
| Size | one IPhO-sized problem = 10 points, 3-5 parts, 15-25 questions, about 5 h; larger sets: 20-30 points |
| Language | the user's language; keep symbols and labels identical across languages |
| Sources | list them; anything unpublished stays out of public outputs |

## Workflow (each stage has an exit check)

**1. Map the field as a chain of objects.** Write the research target in one sentence. List the objects from the
physical model to the measured quantity, one arrow per step (example: Hamiltonian -> Bloch matrix -> band projector ->
flavor and moving frame -> dressed frame and kept dynamics -> local state and current -> charge with error bar).
Label every arrow: **S** stated in a source, **P** project result, **D** derivable exactly here, **O** open.
Exit: every arrow is labelled; open arrows are written down. This becomes the reading-map picture and the
green/red frame coding. See [question design](references/question_design.md).

**2. Turn each arrow into 1-3 questions.** Use the archetypes in [question design](references/question_design.md):
bookkeeping, exact identity, solvable toy model, counterexample, bound chain, data interpretation, decision rule,
synthesis. Every question has one verb (Find, Prove, Show, Evaluate, Explain), a checkable answer, and 0.2-1.5
points. Where a reader may over-generalize, add a sub-part "what does this not establish?".
Exit: a table question -> arrow -> archetype -> answer type -> points.

**3. Make it self-contained before polishing.** Write, in this order: Background (2-3 pages, mechanism in plain
words, 2-3 pictures), Toolkit (numbered facts usable without proof), Glossary (every technical word and every label
of a non-public source), Notation table (one symbol, one meaning). Each question box states all data, definitions
and conventions it uses. Exit: a **cold read** - give only the question booklet to a fresh agent (or person) and ask
it to list every term, symbol or number it cannot interpret. Fix until the list is empty.

**4. Draw pictures that show the set-up, never the answer.** One blue picture per part, placed at the start of
the part. Compute physical pictures from the model (bands, trajectories, spectra) and state their scope in the
caption ("single-particle geometry only"). Answer curves go to the solution booklet.
See [booklet layout](references/booklet_layout.md).

**5. Write solutions and marking.** Box every final answer. Each marking line sums exactly to the question's
points. Add Source/scope notes, and teacher notes for provenance, interpretations of unpublished records,
and everything removed from the question booklet.

**6. Verify.** Run `scripts/check_booklets.py questions.tex solutions.tex --total <points>` (labels, points, marking
sums, leaks, internal paths). Write a check script for every derivable answer (random matrices for identities,
exact arithmetic for numbers) and store its JSON output. Re-derive every sign convention independently. Compile
twice with zero overfull boxes; render all pages with `scripts/render_sheets.py` and look at every page.
See [verification](references/verification.md).

**7. Publish cleanly.** Public versions contain no unpublished data, no internal file paths, no "supplied in this
conversation". Keep earlier revisions; write a changelog; record what was moved and why.

## Colour code (use in both booklets)

- **Green - AVAILABLE**: a result with a named source (paper, proof, data table, exact identity). Use it as stated.
- **Red - NOT ESTABLISHED**: ADDED MODEL (teaching model with exact solution), GIVEN BOUND (an assumption for an
  exercise), OPEN (missing for the real system). Red does not mean wrong.
- **Blue - PICTURE**: explains a set-up (questions) or an answer (solutions). Adds no data.

## Top pitfalls (from the worked example; details in [case study](references/case_study_mb1.md))

1. A scope box after a question stated its answer ("does not establish X" when the question asks whether it
   establishes X). Check every box that follows a question.
2. A box title contained a numerical answer ("ILLUSTRATIVE 200T"). Scan titles and captions, not only body text.
3. One symbol, several meanings (K = modulation amplitude and generator; F = three objects; J = four objects).
4. Report jargon used without definition ("external weight", "defect", "rotation"). Define it in the question;
   flag the definition for the author to confirm.
5. The question booklet cited unpublished files and "this conversation". Students cannot use them; move them to
   teacher notes.
6. A picture plotted the answer (an excitation-probability curve for the question that asks for it).
7. Unbreakable figure boxes left half-empty pages: put pictures at part starts, let sub-sections flow, use
   `\Needspace` before headings, make question boxes unbreakable.
8. `pdflatex ... > name.out` overwrote hyperref's bookmark file `name.out`: fatal "Missing \begin{document}".
9. A string-surgery helper truncated a file. Use replacement helpers that assert the match count.
10. A source paper's printed current formula had the opposite sign to its own figure. An independent time
    evolution settled the convention. Never copy a sign without a check.

## Proposal mode

For a proposal, the booklet ends with a synthesis question (list the inputs that must still be derived; say why
window-by-window certificates do not locate the first failure) and the solutions add an available/missing register.
See [proposal mode](references/proposal_mode.md).

## Files

```
SKILL.md                         this file
references/olympiad_formats.md   IPhO, APhO, PanPhO rules and what to copy from each (with sources)
references/question_design.md    chain of objects, question archetypes, points, hints, cold read
references/booklet_layout.md     page layout, boxes, pictures, LaTeX template usage
references/verification.md       checker, answer scripts, sign checks, rendering, leak scan
references/proposal_mode.md      proposal -> chain -> register -> synthesis question
references/case_study_mb1.md     how the worked example was built, revision by revision
assets/questions_template.tex    self-contained LaTeX question booklet (boxes, pictures, points, notation)
assets/solutions_template.tex    matching solution booklet (soltitle, marking, teacher notes)
scripts/check_booklets.py        labels, points, marking sums, answer leaks, internal paths
scripts/render_sheets.py         render PDF pages to contact sheets for visual inspection
```
