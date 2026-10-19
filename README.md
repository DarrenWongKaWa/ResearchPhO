# ResearchPhO: learn papers from outside your field by solving them

**Version 1.1.0** (19 October 2026). See the [changelog](CHANGELOG.md).

A [Claude Code](https://claude.com/claude-code) skill. Give it a few papers from a field that is not yours. It turns
the papers themselves into a physics-olympiad theory exam written to the standards of the International Physics
Olympiad (IPhO), the Asian Physics Olympiad (APhO) and the Pan Pearl River Delta Physics Olympiad (PanPhO): a question
paper, answer sheets, solutions with a marking scheme and research appendices, and two checklist pages: a study guide
that lists what each question needs beyond your level, and a research checklist of the open problems. In tutor mode
the agent then works through the exam with you, one step at a time.

## Why an olympiad exam

**Olympiad standards fit the task.** An IPhO/APhO/PanPhO problem expects the student to model and solve an unfamiliar
situation independently. The same standards forbid two kinds of obstacle: mathematics beyond what the student has,
and text that does not say enough. A concept outside the syllabus may appear only if the problem explains it "in
terms of topics in the Syllabus" (IPhO syllabus).

**Papers from another field are hard mostly because of language.** "Flavor", "horizontal generator", "Wilson loop",
"prethermal": such words often name physics the reader already knows under another name. Not understanding the
words does not mean not knowing the physics. The exam translates the language into standard physics.

**Solving the exam shows what each paper answers.** Every problem states the question its paper asks and leads,
step by step, to the paper's answer. The appendices of the solutions then show what is established, what is
assumed, and what is still open.

## What you get

| Booklet | Content |
| --- | --- |
| Questions | General instructions; three independent problems of 10 points (30 points, 5 hours). Each problem: an introduction that ends with the question the paper answers, figures, given data, "Useful information", and parts A, B, ... with boxed subquestions and their points. Nothing that does not help to solve. |
| Answer Sheets | One box per subquestion and sub-part. |
| Solutions | Answers and marking scheme per problem, answer figures, then appendices: A paper map (what each paper answers, language map, chain of objects), B source, scope and open conditions of each question, C available and missing results, D teacher notes, E toolbox (the smallest worked example of every tool that the question paper states without proof). Each piece of a marking line is tagged (M) modelling or (C) computation. |
| Study guide | A checklist flowchart. The questions in exam order form the main line; beside each question, what it needs beyond a stated reader level: computation tools in blue frames, modelling ideas in orange frames, one resource each. |
| Research checklist | The same flowchart for the researcher: the chain of objects from the model to the measured quantity forms the main line, and its open links hang beside it, O-calc (a calculation is missing) in amber and O-theory (new theory is needed) in red, to be ticked off as results close them. |

A quick version has one problem of 10 points.

Both checklist pages come from one data-driven component: a self-contained HTML file with a main line of nodes, two
categories of items in their own colours, a checkbox per item, and progress per category and per group. Ticks are
saved in the browser; light and dark themes; it works on a phone. An author checklist (standards S1-S8 and the
verification steps) uses the same component.

## Olympiad standards built in

| # | Standard (source) | ResearchPhO rule | Checked by |
| --- | --- | --- | --- |
| S1 | Three theory problems, 30 marks, 5 hours (IPhO, APhO statutes) | three independent 10-point problems, 3-5 parts each | template, checker |
| S2 | Test creativity and understanding of physics, not mathematical virtuosity (IPhO syllabus) | every problem has modelling questions; most marks for physical steps | question plan; (M)/(C) marking tags, checker |
| S3 | Standard mathematics, no extensive numerical calculation; few marks for manipulation; partial credit for approximations (statutes, syllabus) | maths budget: only mathematics the reader has; anything else stated in one line under "Useful information" and worked in the toolbox appendix | cold read, trial solve, marking tags |
| S4 | Non-syllabus concepts explained in syllabus terms; concise texts (IPhO syllabus) | language map: standard words first, the paper's term in parentheses; definitions at first use | cold read |
| S5 | Context and data before each question; boxed subquestions with points; answer sheets; itemized marking (IPhO/APhO booklets) | LaTeX templates; marking lines add up to the points | checker, answer-sheet script |
| S6 | Research topics (PanPhO comprehensive test; IPhO 2016 LHC problem) | the papers are the problem source | workflow |
| S7 | Independent problems; one master text for translation (APhO) | each problem restates its model; fixed symbols and labels | cold read |
| S8 | Moderation by an international board (IPhO/APhO) | scripts, a cold read by a fresh agent, independent recomputation and sign checks; expert review when it matters | workflow |

## How the agent works

1. Writes, for each paper, the question it answers and its answer, in one sentence each.
2. Makes a language map: for each term of the paper, the physical process it names, the familiar equivalent the
   reader already knows, and how it is computed or measured. Terms with no familiar equivalent are marked as new
   concepts, and a question teaches each of them.
3. Maps the papers as a chain of objects from the model to the measured quantity, and splits it into three problems.
   Each open link is labelled O-calc (existing theory is enough; a calculation is missing) or O-theory (the closest
   existing theory needs a hypothesis that fails here). The O-theory links show where a larger theory has to enter.
4. Writes questions of nine types: modelling, bookkeeping, exact identity, solvable toy model, counterexample, bound
   chain, data interpretation, decision rule, synthesis.
5. Writes each introduction and its "Useful information", and runs a cold read: a fresh agent lists undefined terms,
   steps blocked by mathematics, and the question it thinks the paper answers.
6. Draws set-up figures (never answers), writes the solutions and a marking scheme tagged (M) modelling or (C)
   computation, moves all research context to the appendices, works the toolbox appendix, and generates the answer
   sheets.
7. Writes the study guide (for each question, the tools and modelling ideas it needs beyond the reader's level, with
   one resource each) and the research checklist (the open links of the chain of objects).
8. Verifies: labels, points per problem, marking sums, the modelling share of the marks per problem, answer sheets,
   study-guide labels, answer leaks, research notes in the question paper, problem structure, internal paths; a
   script for every derivable answer; independent sign checks; a trial solve by a fresh agent at the reader's level
   (where it gets stuck, what it misreads); a look at every rendered page.

The agent asks only what it cannot infer. Defaults: the reader is a scientist from another field (university physics
and mathematics, not the field's language); the study guide assumes an undergraduate who knows the four core physics
courses (classical mechanics, electromagnetism, quantum mechanics, thermal and statistical physics); a full exam; the
user's language; unpublished material stays out of public versions.

## Tutor mode

Ask the agent to tutor you through a problem. For each question it prepares a card: the purpose of the part, a
table that explains each element of the figure, the terms of the language map that the question uses, the steps with
one hint each, sanity checks (a limit, the units, a small case), likely misreadings with their corrections, and the
research step the question corresponds to. It then asks before it tells: you compute each step first, and it shows
no final answer until you ask for it. It names every symbol before using it, gives each object its own letter,
introduces pictures such as the Bloch vector before using them, writes every change of frame as a two-column table,
and gives a tiny worked example (a 3-site ring before a 5-site one) before a new piece of mathematics.

## Install

```bash
git clone https://github.com/DarrenWongKaWa/ResearchPhO.git
mkdir -p ~/.claude/skills
ln -sfn "$(pwd)/ResearchPhO/researchpho" ~/.claude/skills/researchpho
```

Or copy the folder instead of linking it. The LaTeX templates need TeX Live 2023 or newer (tikz, pgfplots, tcolorbox,
newtxmath, dsfont). The scripts need Python 3.10+; `render_sheets.py` also needs `pymupdf` and `pillow`. The study
guide is one HTML file that opens in any current browser, offline.

## Use

In Claude Code, attach or name the papers and ask, for example:

- "Use ResearchPhO: I work in X and want to understand these three papers on Y."
- "ResearchPhO quick version: one 10-point problem from this paper."
- "Turn my proposal into a ResearchPhO exam and give me the available/missing register."
- "Audit this exam against the ResearchPhO standards."
- "Tutor me through Problem 1, Part C. Let me try each step first."
- "What do I need to know before I start? Make the study guide for a second-year undergraduate."
- "Make the research checklist of the open links, so I can tick them off as the project closes them."

## Worked example

[`examples/mb1-fractional-pump`](examples/mb1-fractional-pump/): *How long can a two-cycle quantum conveyor operate?*
Built from [arXiv:2504.09338](https://arxiv.org/abs/2504.09338) (multi-band fractional Thouless pumps) and
[arXiv:2608.06777](https://arxiv.org/abs/2608.06777) (projectors on the Grassmannian). Three problems, 18 questions,
30 points; question paper 14 pages, answer sheets 7 pages, solutions 28 pages including the language map, the
open-link table and the toolbox; a study guide with 11 computation tools and 18 modelling ideas; a research
checklist with 2 O-calc and 4 O-theory links.

## Limits

- The quality of an exam depends on how well the agent understands the papers. The skill fixes the format and the
  checks; it cannot guarantee correct physics. Recompute every derivable answer by script, check every sign
  independently, and ask an expert of the field to review an exam that matters.
- Theory only; there is no experimental exam.
- A full 30-point exam is a large piece of work. For a first look at a field, start with the quick version.

## Contents

```
researchpho/                        the skill (link or copy this folder to ~/.claude/skills/)
  SKILL.md                          entry point: standards S1-S8, workflow, tutor mode, pitfalls
  references/olympiad_formats.md    IPhO, APhO, PanPhO comprehensive test: rules and sources
  references/question_design.md     what the paper answers, language map, chain, archetypes, maths budget
  references/booklet_layout.md      booklets, toolbox, checklist schema and uses
  references/verification.md        checker, cold read, trial solve, answer scripts, rendering, leaks
  references/proposal_mode.md       proposal -> chain -> register -> synthesis question
  references/tutor_mode.md          tutor cards, Socratic rules, notation rules, misreadings, a worked card
  references/case_study_mb1.md      how the worked example was built, revision by revision
  assets/questions_template.tex     question paper template
  assets/solutions_template.tex     solutions template with tagged marking, appendices and toolbox
  assets/checklist_template.html    checklist flowchart (data-driven, self-contained)
  assets/author_checklist.json      author checklist data: workflow steps, standards, checks
  scripts/check_booklets.py         consistency, structure, modelling-share and leak checks
  scripts/make_answer_sheets.py     answer sheets from the question paper
  scripts/make_checklist.py         checklist JSON -> HTML page
  scripts/render_sheets.py          PDF pages -> contact sheets
examples/mb1-fractional-pump/       worked example (PDF + LaTeX + checklist pages + checks)
```

## License

MIT. The example booklets cite the two arXiv papers; no text from them or from any exam is reproduced.
