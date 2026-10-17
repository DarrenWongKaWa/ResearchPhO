# ResearchPhO: learn papers from outside your field by solving them

**Version 1.0.0** (17 October 2026). See the [changelog](CHANGELOG.md).

A [Claude Code](https://claude.com/claude-code) skill. Give it a few papers from a field that is not yours. It turns
the papers themselves into a physics-olympiad theory exam written to the standards of the International Physics
Olympiad (IPhO), the Asian Physics Olympiad (APhO) and the Pan Pearl River Delta Physics Olympiad (PanPhO): a question
paper, answer sheets, and solutions with a marking scheme and research appendices.

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
| Solutions | Answers and marking scheme per problem, answer figures, then appendices: A paper map (what each paper answers, language map, chain of objects), B source, scope and open conditions of each question, C available and missing results, D teacher notes. |

A quick version has one problem of 10 points.

## Olympiad standards built in

| # | Standard (source) | ResearchPhO rule | Checked by |
| --- | --- | --- | --- |
| S1 | Three theory problems, 30 marks, 5 hours (IPhO, APhO statutes) | three independent 10-point problems, 3-5 parts each | template, checker |
| S2 | Test creativity and understanding of physics, not mathematical virtuosity (IPhO syllabus) | every problem has modelling questions; most marks for physical steps | question plan, marking |
| S3 | Standard mathematics, no extensive numerical calculation; few marks for manipulation; partial credit for approximations (statutes, syllabus) | maths budget: only mathematics the reader has; anything else stated in one line under "Useful information" | cold read, marking |
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
4. Writes questions of nine types: modelling, bookkeeping, exact identity, solvable toy model, counterexample, bound
   chain, data interpretation, decision rule, synthesis.
5. Writes each introduction and its "Useful information", and runs a cold read: a fresh agent lists undefined terms,
   steps blocked by mathematics, and the question it thinks the paper answers.
6. Draws set-up figures (never answers), writes the solutions and marking scheme, moves all research context to
   the appendices, and generates the answer sheets.
7. Verifies: labels, points per problem, marking sums, answer sheets, answer leaks, research notes in the question
   paper, problem structure, internal paths; a script for every derivable answer; independent sign checks; a look
   at every rendered page.

The agent asks only what it cannot infer. Defaults: the reader is a scientist from another field (university physics
and mathematics, not the field's language); a full exam; the user's language; unpublished material stays out of
public versions.

## Install

```bash
git clone https://github.com/DarrenWongKaWa/ResearchPhO.git
mkdir -p ~/.claude/skills
ln -sfn "$(pwd)/ResearchPhO/researchpho" ~/.claude/skills/researchpho
```

Or copy the folder instead of linking it. The LaTeX templates need TeX Live 2023 or newer (tikz, pgfplots, tcolorbox,
newtxmath, dsfont). The scripts need Python 3.10+; `render_sheets.py` also needs `pymupdf` and `pillow`.

## Use

In Claude Code, attach or name the papers and ask, for example:

- "Use ResearchPhO: I work in X and want to understand these three papers on Y."
- "ResearchPhO quick version: one 10-point problem from this paper."
- "Turn my proposal into a ResearchPhO exam and give me the available/missing register."
- "Audit this exam against the ResearchPhO standards."

## Worked example

[`examples/mb1-fractional-pump`](examples/mb1-fractional-pump/): *How long can a two-cycle quantum conveyor operate?*
Built from [arXiv:2504.09338](https://arxiv.org/abs/2504.09338) (multi-band fractional Thouless pumps) and
[arXiv:2608.06777](https://arxiv.org/abs/2608.06777) (projectors on the Grassmannian). Three problems, 18 questions,
30 points; question paper 14 pages, answer sheets 7 pages, solutions 24 pages including the language map.

## Limits

- The quality of an exam depends on how well the agent understands the papers. The skill fixes the format and the
  checks; it cannot guarantee correct physics. Recompute every derivable answer by script, check every sign
  independently, and ask an expert of the field to review an exam that matters.
- Theory only; there is no experimental exam.
- A full 30-point exam is a large piece of work. For a first look at a field, start with the quick version.

## Contents

```
researchpho/                        the skill (link or copy this folder to ~/.claude/skills/)
  SKILL.md                          entry point: standards S1-S8, workflow, pitfalls
  references/olympiad_formats.md    IPhO, APhO, PanPhO comprehensive test: rules and sources
  references/question_design.md     what the paper answers, language map, chain, archetypes, maths budget
  references/booklet_layout.md      question paper, answer sheets, solutions and appendices; macros
  references/verification.md        checker, cold read, answer scripts, sign checks, rendering, leak review
  references/proposal_mode.md       proposal -> chain -> register -> synthesis question
  references/case_study_mb1.md      how the worked example was built, revision by revision
  assets/questions_template.tex     question paper template
  assets/solutions_template.tex     solutions template with appendices
  scripts/check_booklets.py         consistency, structure and leak checks
  scripts/make_answer_sheets.py     answer sheets from the question paper
  scripts/render_sheets.py          PDF pages -> contact sheets
examples/mb1-fractional-pump/       worked example (PDF + LaTeX + checks)
```

## License

MIT. The example booklets cite the two arXiv papers; no text from them or from any exam is reproduced.
