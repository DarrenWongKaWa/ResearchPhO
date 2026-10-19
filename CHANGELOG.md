# Changelog

## 1.2.1 (2026-10-20)

A second worked example; the skill itself is unchanged.

- **Worked example 2.** *How does disorder enter a model, a Hall current and a pump?* Deliverables in
  `examples/DisorderInducedNonlinearHallEffect_RPhO/` (questions 18 pages, solutions 24 pages, checklist with 33
  questions, 15 tools, 31 ideas, 4 O-calc and 5 O-theory links); sources in `examples/disorder-hall-pump/`. Built
  from several papers at once (anomalous-Hall review, disorder-induced nonlinear Hall effect and its quantum
  revision, average-symmetry topology, fractional pump with the Niu-Thouless invariant) around one research
  question: how a microscopic disorder model is built and then used for responses and for pumping in large systems.
  Modelling share 57%, 64%, 64%.
- The example's README records what the cold read and the trial solve changed: an inconsistency between a
  neglected overlap and the quantity asked for, symbol clashes, missing tools in one problem's "Useful information",
  and four answer or wording corrections.

## 1.2.0 (2026-10-19)

Three deliverables, one checklist, no answer sheets.

- **Deliverable folder.** The agent delivers exactly three files in `<PaperName>_RPhO/`: `questions.pdf`,
  `solutions.pdf` and `checklist.html`. LaTeX sources, scripts, data and build files stay in a separate working folder.
- **One checklist.** The study guide and the research checklist are merged into one page (schema
  `researchpho-checklist/2`). The exam runs down the middle question by question, with points; computation tools
  (blue) and modelling ideas (orange) sit beside each question, each with a title, a short note and a linked reference;
  the line ends with a research segment of open links, O-calc (amber) and O-theory (red). New layout: serif display
  type, sans body, mono labels, grid background; progress per category, per group and in total; filters; two-click
  reset; light and dark; one column at phone width. `make_checklist.py` validates the four categories and their
  sides, and allows only tools and ideas on exam nodes and only O-calc and O-theory links on research nodes
  (profile `rpho`, the default; `author` and `generic` remain).
- **No answer sheets.** The reader writes on plain sheets and labels each answer with its question.
  `scripts/make_answer_sheets.py` is removed; the question template says so in its instructions.
- **Reader.** The default reader is an undergraduate who knows the four core physics courses.
- **Tutor mode** is kept as a short reference for a reader who asks for hints; the checklist covers what each question
  needs.
- `check_booklets.py`: `--checklist checklist.json` (alias `--guide`) checks the exam segment against the booklets;
  research nodes are not counted as questions.
- **Worked example.** Deliverables in `examples/MultiBandFractionalThoulessPumps_RPhO/` (questions 14 pages, solutions
  28 pages, checklist with 18 questions, 11 tools, 18 ideas, 2 O-calc and 4 O-theory links); sources in
  `examples/mb1-fractional-pump/` with one `checklist.json`. The answer sheets, study guide and research checklist
  files are removed.

## 1.1.0 (2026-10-19)

Support for the reader who solves the exam: tutor mode, a study guide, a toolbox appendix, a trial solve, and marking
tags that measure the modelling share.

- **Tutor mode** (`references/tutor_mode.md`, a section in `SKILL.md`). For each question the agent prepares a card:
  the purpose of the part, a figure-reading table, the language-map entries used, the steps with one hint each,
  sanity checks (a limit, units, a small case), likely misreadings with corrections, and the research step. Rules:
  lead with questions, let the reader compute each step first, show no boxed answer before the reader asks; name
  every symbol before use and give each object one letter; introduce a picture (such as the Bloch vector) before
  using it; write every change of frame or representation as a table "quantity, description 1, description 2,
  relation"; give a tiny worked example before a new mathematical tool. Includes a seed list of misreadings and a
  worked card for 1.C.1 of the example.
- **Checklist flowcharts**, a new data-driven component (`assets/checklist_template.html`, schema
  `researchpho-checklist/1`). A main line of grouped nodes, two categories of items on its sides in their own colours
  and frames, a checkbox and a one-line note per item, progress per category, overall and per group; ticks in
  `localStorage` behind try/catch; filters per category; two-click reset; light and dark themes; one column at phone
  width. New script `scripts/make_checklist.py` validates the JSON (profiles `study-guide`, `research`, `author`)
  and writes the page. Three uses:
  - **Study guide**, a fourth output: for a stated reader level (default: an undergraduate who knows the four core
    physics courses), what each question needs beyond that level, as computation tools (blue) and modelling ideas
    (orange), one resource each.
  - **Research checklist**: the chain of objects of Appendix A as the main line, its open links as O-calc (amber) and
    O-theory (red), ticked off as results close them.
  - **Author checklist** (`assets/author_checklist.json`): the eleven workflow steps, standards S1-S8 and the
    verification checks.
- **Marking tags.** Each number of a `\marking` line may carry (C) computation or (M) modelling. `check_booklets.py`
  reports the modelling share of the tagged marks per problem and warns below one half (standards S2, S3); untagged
  lines stay valid, and a tag that does not follow a number is flagged. New option `--guide` checks that the study
  guide lists every scored question once with the same points.
- **Toolbox appendix** (Appendix E of the solutions template): the smallest worked example of every tool from
  "Useful information", a hint or a given identity that is above the reader's level. Layout rules in
  `references/booklet_layout.md`.
- **Trial solve** (`references/verification.md`, section 1c): after the cold read, a fresh agent at the target level
  solves each question and records where it gets stuck and what it misreads; the records feed the tutor-card
  misreading lists, the toolbox, the study guide and candidate partial-credit lines.
- **Worked example.** New study guide (`study_guide.json`, `study_guide.html`: 18 questions, 11 computation tools,
  18 modelling ideas) and research checklist (`research_checklist.json`, `research_checklist.html`: 7 objects,
  2 O-calc and 4 O-theory links, from the open-link table of Appendix A). All 18 marking lines are tagged; pieces that mixed both kinds were split, keeping every
  question's points. The first tagging gave modelling shares of 45%, 34% and 40%, below one half. The marking lines were rebalanced within each question, every total unchanged, to 56%, 53% and 52%. New
  Appendix D toolbox (solutions now 28 pages), recomputed in `check_answers.py`. In 1.C.1 the field direction
  n(t) is now defined in the text, not only in the caption of Figure 1.5, the Bloch vector is introduced before the
  figure, and "Useful information" uses d for a generic unit vector.
- **Two kinds of open link.** The open label O is split into **O-calc** (existing theory is enough; a calculation
  is missing) and **O-theory** (the closest existing theory needs a hypothesis that fails here). A new section 1a
  of the question-design reference gives the classification test, and asks for each O-theory link the limit in which
  the failing hypothesis would hold. When several O-theory links fail on the same point, that shared gap is stated in
  one sentence.
- Appendix A of the solutions template has an open-link table (link, kind, closest existing theory, hypothesis that
  fails or closing calculation, shared gap). Appendices B and C record the kind of each open item. The same applies to
  the proposal-review summary.
- Worked example: the chain figure marks each step as D, O-calc or O-theory, and Appendix A has the open-link table;
  the solutions grew by one page.
- `check_booklets.py` reports "O-calc" and "O-theory" in the question paper as research notes.
- Worked example, Appendix B fixes: four notes that sat under the following question now stand under their own
  question (1.B.1, 1.D.1, 2.C.2, 3.C.1); 2.B.1 has its own scope notes; the "three separate statements" list is
  restored; stale references (a removed background section, "Part B describes its motion") and mentions of a proof
  that the public excerpt does not contain are removed; an unused frame-legend macro is deleted.

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
