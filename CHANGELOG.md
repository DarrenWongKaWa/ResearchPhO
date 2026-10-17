# Changelog

## 1.0.0 (2026-10-17)

First stable release of ResearchPhO: learn papers from outside your field by solving them as a physics-olympiad
theory exam.

- **Strict IPhO/APhO theory format.** Question paper with general instructions and three independent problems of
  10 points (30 points, 5 hours); each problem has an introduction, figures, given data, "Useful information", and
  parts A, B, ... with boxed subquestions. No status frames, source boxes or research notes in the question paper.
- **Olympiad standards S1-S8** from the IPhO/APhO statutes and syllabus, the official booklets and marking schemes,
  and the PanPhO comprehensive test, each written as a rule with the step that enforces it.
- **What each paper answers.** Every introduction ends with the question its paper asks; the last part reaches the
  paper's answer. Appendix A states each paper's question and answer.
- **Language map** with four columns: paper term, physical process or picture, familiar equivalent, how it is
  computed or measured. Terms with no familiar equivalent are marked "new" with the questions that teach them.
- **Mathematics budget and modelling questions**: only mathematics the reader has, anything else stated in
  "Useful information"; at least one modelling question per problem.
- **Cold read** by a fresh agent: undefined terms, steps blocked by mathematics, and the paper's question in its
  own words.
- **Solutions** with itemized marking scheme and Appendices A-D (paper map, source/scope/open notes per question,
  available and missing results, teacher notes).
- **Templates** for questions and solutions; **scripts** `check_booklets.py` (labels, points per problem, marking
  sums, answer sheets, leaks, problem structure, research notes in the question paper), `make_answer_sheets.py`,
  `render_sheets.py`.
- **Worked example** `examples/mb1-fractional-pump`: three problems, 18 questions, 30 points, built from
  arXiv:2504.09338 and arXiv:2608.06777.

## Pre-release history

- 0.2.0 (2026-10-17): renamed ResearchPhO; strict olympiad format; answer sheets; research context moved to
  solution appendices; PanPhO reference limited to the comprehensive test.
- 0.1.0 (2026-10-17): first version as `paper-to-olympiad`, with Background, Toolkit and Glossary pages and
  colour-coded frames in the question booklet.
