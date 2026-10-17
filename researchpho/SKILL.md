---
name: researchpho
description: ResearchPhO - turn research papers, the literature of a new field, or a research proposal into a research-based physics-olympiad theory exam written strictly in the IPhO/APhO format (three independent problems of 10 points, boxed subquestions, answer sheets) plus solutions with marking scheme and research appendices, so that people learn a field by solving it. Use when someone wants to learn a new field or paper quickly, write olympiad-style (IPhO, APhO, PanPhO comprehensive-test style) problems from papers, turn a proposal into an exam with an available/missing register, or audit such an exam for answer leaks, research notes in the question paper, undefined terms, notation clashes, point totals and layout. Triggers include ResearchPhO, 用论文出题, 出一套 APhO/IPhO 风格的题, 奥赛风格, 快速入门新领域, 读文献出题, proposal 拆成题目, paper to problems.
---

# ResearchPhO: learn a field by writing its olympiad exam

A physics-olympiad theory problem introduces an unfamiliar topic in a few paragraphs, then breaks it into small
steps, each with points, given data and a checkable answer. IPhO rules require that any concept outside the syllabus
be "explained in terms of topics in the Syllabus". ResearchPhO applies this format, strictly, to research papers and
proposals.

Three booklets are produced:

- **Questions**: exactly an IPhO/APhO theory paper. General instructions; three independent problems of 10 points
  (30 points, 5 hours); each problem has an introduction, figures, given data, "Useful information", and parts
  A, B, ... with boxed subquestions A.1, A.2, ... and their points. Nothing else.
- **Answer Sheets**: one box per subquestion and sub-part (`scripts/make_answer_sheets.py`).
- **Solutions**: answers and marking scheme per problem, answer figures, then Appendices with all research
  context: research map, source/scope/open notes per question, register of available and missing results, teacher
  notes.

Worked example: `examples/mb1-fractional-pump/` (two arXiv papers on fractional Thouless pumps and projector geometry).

## The two rules that matter most

1. **The question paper contains only what a solver uses.** No coloured status frames, no "source" boxes, no
   "this does not establish ..." notes, no research map, no glossary page, no hand-offs between questions.
   Olympiad papers have none of these, and they distract the solver. Put all of it in the solution appendices.
2. **Every problem is self-contained.** Its introduction states the model, explains every non-syllabus concept in
   plain physics, and defines each term where it is first used; "Useful information" lists the facts the problem
   needs. Problems do not depend on each other; restate the model in each.

## When to use

- Someone must enter a new field from a few papers, or a group must learn the core of a paper.
- A proposal must be checked: which steps can be derived now, which inputs are missing (proposal mode).
- An existing exam must be audited for leaks, research notes in the question paper, jargon, symbols, points, layout.

Not for: summarizing a paper in prose, or writing official olympiad papers.

## Decide first (ask only what you cannot infer)

| Choice | Default |
| --- | --- |
| Size | full exam: 3 problems x 10 points, 3-5 parts each, 5 hours; quick version: 1 problem, 10 points |
| Reader | advanced undergraduate in olympiad format; for a true olympiad, high-school mathematics only |
| Language | the user's language; keep symbols and labels identical across translations |
| Sources | list them; anything unpublished stays out of public outputs |

## Workflow (each stage has an exit check)

1. **Map the field as a chain of objects** from the model to the measured quantity. Label each arrow: stated in a
   source, project result, derivable here, or open. Exit: every arrow labelled. This chain is Appendix A.
   See [question design](references/question_design.md).
2. **Split the chain into three independent problems** (e.g. model and geometry; mechanism and dynamics;
   observable and time). Give each 10 points and 3-5 parts. Exit: a table problem -> part -> question -> arrow ->
   archetype -> points.
3. **Write each question** with one verb (Find, Prove, Show, Evaluate, Explain), a checkable answer, and 0.2-2.5
   points. Archetypes: bookkeeping, exact identity, solvable toy model, counterexample, bound chain, data
   interpretation, decision rule, synthesis.
4. **Write the introductions and "Useful information"** so that each problem stands alone. Exit: a **cold read**:
   give one problem to a fresh agent and ask it to list every term, symbol, number or assumption it cannot
   interpret. Repeat until the list is empty.
5. **Draw figures that show the set-up, never the answer**: numbered "Figure 1.3" with a plain caption. Compute
   physical figures from the model and state their scope. Answer curves go to the solutions.
6. **Write solutions and marking.** Box final answers; each marking line sums exactly to the points; answer
   figures. Move every scope note, open condition, source remark and research-plan item into Appendices A-D.
7. **Make the answer sheets** with `scripts/make_answer_sheets.py questions.tex answersheets.tex`.
8. **Verify.** `scripts/check_booklets.py questions.tex solutions.tex --answers answersheets.tex --total 30
   --problem-total 10` (labels, points per problem, marking sums, answer leaks, research material in the
   question paper, internal paths). Check every derivable answer with a script; re-derive sign conventions
   independently; compile twice with zero overfull boxes; render every page with `scripts/render_sheets.py`.
   See [verification](references/verification.md).
9. **Publish cleanly.** No unpublished data, internal paths or "supplied in this conversation" in public versions.
   Keep earlier revisions; log label maps between revisions.

## Top pitfalls (details in [case study](references/case_study_mb1.md))

1. Research-status frames in the question paper (green "available", red "not established", blue picture frames,
   "source/scope" lines). They are not olympiad style and distract the solver. Move them to solution appendices.
2. A note next to a question that states its answer ("does not establish X" when the question asks whether it
   does). The appendix is the only place for such notes.
3. A title or caption with a numerical answer ("ILLUSTRATIVE 200T").
4. One symbol, several meanings (K = amplitude and generator; F = three objects; J = four objects).
5. Report jargon without definition ("external weight", "defect", "rotation"); define it in the problem text and
   flag your definition for the author.
6. Problems that depend on each other; restate the model and the needed result instead.
7. A figure that plots the answer the question asks for.
8. After regrouping questions, marks and cross-references drift: relabel with a map, rescale marking lines, and
   check prompts against the previous revision with a script.
9. `pdflatex ... > name.out` overwrites hyperref's bookmark file; redirect to another name.
10. A source paper's printed formula can disagree in sign with its own figure; check every sign independently.

## Proposal mode

The last part of problem 3 becomes the synthesis question ("list the inputs that must still be derived; why do
window-by-window certificates not locate the first failure?"). The available/missing register goes to Appendix C.
See [proposal mode](references/proposal_mode.md).

## Files

```
SKILL.md                         this file
references/olympiad_formats.md   IPhO, APhO, PanPhO comprehensive test: rules and what ResearchPhO copies
references/question_design.md    chain of objects, splitting into problems, archetypes, points, cold read
references/booklet_layout.md     question paper, answer sheets, solutions and appendices; macros; page codes
references/verification.md       checker, answer scripts, sign checks, rendering, leak review
references/proposal_mode.md      proposal -> chain -> register -> synthesis question
references/case_study_mb1.md     how the worked example was built, revision by revision
assets/questions_template.tex    strict IPhO/APhO question paper (3 problems x 10 points)
assets/solutions_template.tex    solutions, marking scheme, Appendices A-D
scripts/check_booklets.py        labels, points per problem, marking sums, leaks, research material in questions
scripts/make_answer_sheets.py    answer-sheet booklet from the question paper
scripts/render_sheets.py         PDF pages -> contact sheets for visual inspection
```
