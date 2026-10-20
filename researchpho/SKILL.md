---
name: researchpho
description: ResearchPhO - learn research papers from outside your field by turning them into a physics-olympiad theory exam written to IPhO/APhO/PanPhO standards, for an undergraduate who knows the four core physics courses. The exam makes the reader model and solve each paper's key steps without being blocked by unfamiliar mathematics or by underspecified text; it translates the field's language into standard physics and shows what question each paper answers. Output, in one folder named <PaperName>_RPhO: the question paper (three independent 10-point problems with boxed subquestions), the solutions (marking scheme tagged computation/modelling, research appendices, a toolbox appendix) and one checklist page (HTML) that maps every question to the computation tools and modelling ideas it needs, with linked references, and ends with the open research problems. Use when someone wants to understand papers outside their field, enter a new field quickly, write olympiad-style (IPhO, APhO, PanPhO) problems from papers, turn a proposal into an exam with an available/missing register, or audit such an exam. Triggers include ResearchPhO, RPhO, learn this paper by solving problems, papers outside my field, olympiad-style problems from papers, 用论文出题, 奥赛风格, 快速入门新领域.
---

# ResearchPhO: learn papers from outside your field by solving them

Version 1.2.1.

Papers from another field are hard to read mostly because of their language, not their physics. A term such as
"flavor", "horizontal generator" or "prethermal" often names something the reader already knows under another name.
Physics-olympiad problems are written for exactly this situation. An IPhO/APhO/PanPhO problem expects the student
to model and solve a new situation independently, but it must not let mathematics or an underspecified sentence block
the student. ResearchPhO converts the papers themselves into such an exam. Solving it shows what question each paper
answers, how the answer is obtained, and what is still open.

The reader is an undergraduate who knows the four core physics courses (classical mechanics, electromagnetism,
quantum mechanics, thermal and statistical physics) and their mathematics, unless the user names another reader.

## Deliverables: three files in one folder

Create a folder named after the main paper, `<PaperName>_RPhO/` (the short title in CamelCase, for example
`MultiBandFractionalThoulessPumps_RPhO/`). It holds exactly three files:

| File | Content |
| --- | --- |
| `questions.pdf` | Exactly an IPhO/APhO theory paper: general instructions; three independent problems of 10 points (30 points, 5 hours); each problem has an introduction that ends with the question the paper answers, figures, given data, "Useful information", and parts A, B, ... with boxed subquestions and their points. Nothing else. |
| `solutions.pdf` | Answers and marking scheme per problem, each marking number tagged (C) computation or (M) modelling, answer figures; then Appendices: A paper map (question each paper answers, language map, chain of objects, open-link table), B source/scope/open notes per question, C register of available and missing results, D teacher notes, E toolbox (the smallest worked example of every tool the question paper states). |
| `checklist.html` | One self-contained page. The main line runs through the exam question by question; beside each question, the computation tools (blue, left) and modelling ideas (orange, right) it needs beyond the reader's level, each with a title, one short note and a linked reference. The line ends with the research segment: the chain of objects of Appendix A, with its open links, O-calc (amber, left) and O-theory (red, right). Every item has a checkbox; progress per category and per problem. |

Keep LaTeX sources, scripts, JSON and every intermediate file in a separate working folder, never in
`<PaperName>_RPhO/`. A quick version has one problem of 10 points and the same three files.

## Olympiad standards built into ResearchPhO

Each standard comes from the IPhO/APhO statutes and syllabus, the official exam booklets and marking schemes, or the
PanPhO comprehensive test. Each one is a rule here, with the step that enforces it.

| # | Olympiad standard (source) | ResearchPhO rule | Enforced by |
| --- | --- | --- | --- |
| S1 | Theory exam: three problems, 30 marks in total, 5 hours (IPhO and APhO statutes) | three independent problems of 10 points, 3-5 parts each; a quick version has one 10-point problem | template; `check_booklets.py --problem-total 10` |
| S2 | Problems test creativity and understanding of physics, not mathematical virtuosity or speed (IPhO syllabus) | every problem contains modelling questions; more than half of each problem's marks are (M) | question plan (step 5); (M)/(C) tags; `check_booklets.py` modelling share |
| S3 | Solvable with standard mathematics, without extensive numerical calculation (statutes); small share of marks for mathematical manipulation; approximate solutions earn partial credit (IPhO syllabus) | only mathematics the reader has; any other tool stated in one line under "Useful information" and worked in Appendix E | cold read; trial solve; marking tags |
| S4 | Concepts outside the syllabus may appear only if the text explains them "in terms of topics in the Syllabus"; problem texts are concise (IPhO syllabus) | the paper's language is translated: standard physics words first, the paper's term in parentheses at first use; every term and symbol defined in the text where it first appears | language map; cold read |
| S5 | Context and given data before each question; boxed subquestions with points; itemized marking scheme (IPhO/APhO booklets) | `\problem`, `\parttitle`, `\question`; `\marking` lines that add up to the points; answers are written on plain sheets, labelled by question (no answer-sheet booklet) | templates; `check_booklets.py` |
| S6 | Research topics in olympiad problems (PanPhO comprehensive test syllabus: "科研最新进展"; IPhO 2016 problem on the LHC) | the papers are the problem source, at IPhO-like difficulty for the reader | steps 1-4 |
| S7 | Problems are independent; one English master text translated by team leaders (APhO statutes) | each problem restates its model; symbols and labels stay identical in translations | cold read per problem |
| S8 | Problems are moderated by an international board before the exam (IPhO/APhO) | no board exists here: scripts, a cold read and a trial solve by fresh agents, independent recomputation and sign checks, and a review by an expert of the field when the exam matters | steps 6 and 10 |

Details and sources: [olympiad formats](references/olympiad_formats.md).

## Two things every problem must make visible

1. **The question the paper answers.** The introduction ends with that question in plain words ("Can repulsion
   make this pump carry half a particle per period at integer filling, and why?"). The last part of the problem
   reaches the paper's answer, or the closest form that can be derived in an exam.
2. **The paper's language in standard physics.** Use the standard word and put the paper's term in parentheses at
   first use: "localized orbitals built from the Bloch states (Wannier orbitals)". The reader then recognizes the
   term when reading the paper. The full language map goes to Appendix A.

## Decide first (ask only what you cannot infer)

| Choice | Default |
| --- | --- |
| Reader | an undergraduate who knows the four core physics courses and their mathematics (linear algebra, calculus, Fourier series, complex numbers) |
| Size | full exam: 3 problems x 10 points, 5 hours; quick version: 1 problem, 10 points |
| Language | the user's language for the booklets; keep symbols and labels identical across translations |
| Sources | list them; anything unpublished stays out of public outputs |

## Workflow (each stage has an exit check)

1. **State what each paper answers.** One sentence for the question, one for the answer. Exit: both sentences per paper.
2. **Make the language map**: for each term of the paper, (i) the physical process or picture it names, (ii) the
   familiar equivalent the reader already knows, (iii) how it is computed or measured. A term with no familiar
   equivalent is a new concept: mark it and make sure a question teaches it. Exit: every term that a cold reader
   flags is in the map. See [question design](references/question_design.md).
3. **Map the field as a chain of objects** from the model to the measured quantity; label each arrow stated in a
   source, project result, derivable here, or open. Split the open arrows into **O-calc** (existing theory is
   enough; a calculation is missing) and **O-theory** (the closest existing theory needs a hypothesis that fails
   here, or no method exists); for O-theory, record that theory and the failing hypothesis. Exit: every open arrow
   has a kind, and the shared gap of the O-theory arrows is stated in one sentence.
4. **Split the chain into three independent problems** of 10 points and 3-5 parts each.
5. **Write the questions.** One verb each (Find, Prove, Show, Evaluate, Explain), a checkable answer, 0.2-2.5 points.
   Archetypes: modelling, bookkeeping, exact identity, solvable toy model, counterexample, bound chain, data
   interpretation, decision rule, synthesis. Every problem has modelling questions (S2); a pure derivation gets a last
   part that asks what the result establishes and what it does not. Check the mathematics budget (S3).
6. **Write each introduction and its "Useful information"**, ending with the question the paper answers. Exit: a
   **cold read**: a fresh agent reads one problem and lists (a) every term, symbol or number it cannot interpret,
   (b) every step blocked by mathematics that is not provided, (c) the question the paper answers, in its own words.
   Repeat until (a) and (b) are empty and (c) matches step 1.
7. **Draw figures that show the set-up, never the answer**, numbered "Figure 1.3" with a plain caption; compute
   physical figures from the model and state their scope. Define every symbol of a figure in the text as well.
8. **Write solutions and marking**; box final answers; marking lines add up to the points; tag each number (C) or
   (M), with more than half of each problem in (M). Move every scope note, open condition, source remark and
   research-plan item into Appendices A-D. Write Appendix E, the toolbox.
9. **Write the checklist** `checklist.json`: per question, the tools and modelling ideas beyond the reader's level
   (title, one short note, one reference with a link); then the research segment (the chain of objects and its open
   links). Build it with `scripts/make_checklist.py checklist.json checklist.html`. See
   [booklet layout](references/booklet_layout.md).
10. **Verify**: `scripts/check_booklets.py questions.tex solutions.tex --total 30 --problem-total 10 --checklist
    checklist.json`; a script for every derivable answer; independent sign checks; a **trial solve** by a fresh agent
    at the reader's level; two compiles with zero overfull boxes; `scripts/render_sheets.py` and a look at every page.
    See [verification](references/verification.md).
11. **Deliver**: copy `questions.pdf`, `solutions.pdf` and `checklist.html` into `<PaperName>_RPhO/`, nothing else.
    Public versions contain no unpublished data, internal paths or "supplied in this conversation".

## Top pitfalls (details in [case study](references/case_study_mb1.md))

1. Research-status frames or notes in the question paper ("available", "not established", "source/scope"). They are
   not olympiad style and distract the solver; they belong in the solution appendices.
2. The paper's jargon copied into the problem without translation; the reader is then blocked by language (S4).
3. A step that needs mathematics the reader does not have, without a one-line statement in "Useful information" (S3).
4. Problems that only check algebra and never ask the reader to model (S2).
5. An introduction that never says what question the paper answers.
6. A note, title or caption that states an answer ("ILLUSTRATIVE 200T").
7. One symbol, several meanings; a symbol defined only in a figure caption; problems that depend on each other.
8. After regrouping questions: drifting marks and cross-references; relabel with a map and check by script.
9. `pdflatex ... > name.out` overwrites hyperref's bookmark file.
10. A paper's printed formula can disagree in sign with its own figure; check every sign independently.

## Helping a reader who solves the exam

When a reader asks for help while solving, answer step by step: the purpose of the part, how to read its figure,
one hint before each step, and no boxed answer before the reader asks. The checklist is the reader's map. Rules and a
worked example: [tutor mode](references/tutor_mode.md).

## Proposal mode

The last part of problem 3 becomes the synthesis question ("list the inputs that must still be derived; why do
window-by-window certificates not locate the first failure?"); the available/missing register goes to Appendix C.
See [proposal mode](references/proposal_mode.md).

## Files

```
SKILL.md                         this file: deliverables, standards S1-S8, workflow, pitfalls
references/olympiad_formats.md   IPhO, APhO, PanPhO comprehensive test: rules, sources, what ResearchPhO copies
references/question_design.md    what the paper answers, language map, chain, problems, archetypes, maths budget
references/booklet_layout.md     deliverable folder, booklets, appendices, toolbox, macros, checklist schema
references/verification.md       checker, marking tags, cold read, trial solve, answer scripts, rendering, leaks
references/proposal_mode.md      proposal -> chain -> register -> synthesis question
references/tutor_mode.md         helping a reader while they solve: hints, notation rules, misreadings
references/case_study_mb1.md     how the worked example was built, revision by revision
assets/questions_template.tex    strict IPhO/APhO question paper (3 problems x 10 points)
assets/solutions_template.tex    solutions, (C)/(M)-tagged marking scheme, Appendices A-D, toolbox Appendix E
assets/checklist_template.html   the checklist page (data-driven, self-contained, light and dark, phone width)
assets/author_checklist.json     optional author checklist: workflow steps, standards S1-S8, checks
scripts/check_booklets.py        labels, points, marking sums, modelling share, leaks, structure, checklist labels
scripts/make_checklist.py        checklist JSON -> validated, self-contained HTML page
scripts/render_sheets.py         PDF pages -> contact sheets for visual inspection
```
