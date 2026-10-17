# ResearchPhO: learn a field by writing its olympiad exam

A [Claude Code](https://claude.com/claude-code) skill that turns research papers, the literature of a new field, or a
research proposal into a **research-based physics-olympiad theory exam written strictly in the IPhO/APhO format**:
a question paper, answer sheets, and solutions with marking scheme and research appendices.

[中文说明见下方](#中文说明)

## Why the olympiad format

An IPhO/APhO theory problem introduces an unfamiliar topic in a few paragraphs, then breaks it into small steps, each
with points, given data and a checkable answer. The IPhO syllabus requires that any concept outside the syllabus be
"explained in terms of topics in the Syllabus". A newcomer to a field needs exactly this: the few calculations that
carry the field, in an order that can be solved, with a clear line between what is established and what is open.

## What a ResearchPhO exam looks like

| Booklet | Content |
| --- | --- |
| Questions | General instructions; three independent problems of 10 points (30 points, 5 hours). Each problem: introduction, figures, given data, "Useful information", parts A, B, ... with boxed subquestions A.1, A.2, ... and points. **Nothing else**: no status frames, source boxes or research notes. |
| Answer Sheets | One box per subquestion and sub-part. |
| Solutions | Answers and marking scheme per problem (marking lines add up to the points), answer figures, then Appendices: A research map, B source/scope/open notes per question, C register of available and missing results, D teacher notes. |

## What the skill does

1. Maps the papers as a **chain of objects** from the model to the measured quantity; labels each step as stated,
   derivable, or open (this becomes Appendix A).
2. Splits the chain into **three independent problems** of 10 points, each with its own introduction.
3. Writes questions of eight types: bookkeeping, exact identity, solvable toy model, counterexample, bound chain,
   data interpretation, pass/fail/undetermined decision rule, synthesis.
4. Makes every problem **self-contained** (definitions at first use, "Useful information", a cold read by a fresh
   agent) and draws set-up figures, never answers.
5. Writes solutions with marking, then moves all research context to the appendices.
6. **Verifies**: labels, points per problem, marking sums, answer sheets, answer leaks, research material in the
   question paper, internal paths; a script for every derivable answer; independent sign checks; page renders.
7. **Proposal mode**: a conditional result, a decision rule, a synthesis question, and the available/missing register.

## Contents

```
researchpho/                        the skill (copy or link this folder to ~/.claude/skills/)
  SKILL.md                          entry point: two main rules, workflow, top pitfalls
  references/olympiad_formats.md    IPhO, APhO, PanPhO comprehensive test: rules and what to copy (with sources)
  references/question_design.md     chain of objects, splitting into problems, archetypes, points, cold read
  references/booklet_layout.md      question paper, answer sheets, solutions and appendices; macros; page codes
  references/verification.md        checker, answer scripts, sign checks, rendering, leak review
  references/proposal_mode.md       proposal -> chain -> register -> synthesis question
  references/case_study_mb1.md      how the worked example was built, revision by revision
  assets/questions_template.tex     strict IPhO/APhO question paper
  assets/solutions_template.tex     solutions, marking scheme, Appendices A-D
  scripts/check_booklets.py         labels, points, marking sums, leaks, research material in the question paper
  scripts/make_answer_sheets.py     answer sheets from the question paper
  scripts/render_sheets.py          PDF pages -> contact sheets
examples/mb1-fractional-pump/       worked example: questions, answer sheets, solutions (PDF + LaTeX), checks
```

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

- "Use ResearchPhO: make a 30-point exam from these two papers so that I can learn the field."
- "Quick version: one 10-point problem from this review."
- "Turn my proposal into a ResearchPhO exam and give me the available/missing register."
- "Audit this exam: research notes in the question paper, answer leaks, points, layout."

## Worked example

[`examples/mb1-fractional-pump`](examples/mb1-fractional-pump/): *How long can a two-cycle quantum conveyor operate?*
Built from [arXiv:2504.09338](https://arxiv.org/abs/2504.09338) (multi-band fractional Thouless pumps) and
[arXiv:2608.06777](https://arxiv.org/abs/2608.06777) (projectors on the Grassmannian). Three problems, 18 questions,
30 points; question paper 14 pages, answer sheets 7 pages, solutions 23 pages.

---

## 中文说明

**ResearchPhO** 是"用科研文献出的物理奥赛"：把论文、新领域的文献或研究 proposal 写成一套严格按 IPhO/APhO 理论考格式的试卷，让人通过做题快速学会一个领域。

一套 ResearchPhO 包括三本：

- **题目册（Questions）**：完全按 IPhO/APhO 理论考的格式。总说明之后是 3 道独立的大题，每题 10 分，共 30 分、5 小时。每道题由引言、图、已知条件、"Useful information"和若干部分组成，每部分是带分值的小题框（A.1、A.2……）。**只有做题需要的内容**，不放任何状态框、出处框或研究说明。
- **答题纸（Answer Sheets）**：每个小题、每个分问各一个作答框。
- **答案册（Solutions）**：每道题的解答和评分细则，每条细则的分值加起来等于该题分值；附答案图。最后是附录：A 研究地图、B 每道题的出处与适用范围及未解决条件、C"已有 / 缺失"清单、D 教师说明。

**两条最重要的规则：**

1. 题目册里只放做题用得上的东西。研究计划、"尚未证明"之类的说明一律放到答案册附录。
2. 每道大题自成一体：在引言里讲清模型，概念在第一次出现的地方就定义，需要的数学事实写进"Useful information"，不依赖其他大题。

**参照的比赛：** IPhO、APhO 理论考（3 道题 × 10 分），以及 PanPhO 综合试（香港科技大学主办，会结合科研最新进展）。

**例子：** `examples/mb1-fractional-pump` 用两篇 arXiv 论文出了 3 道大题、18 道小题、共 30 分。这是一个更大题目的公开节选，依赖未发表数据的题目已经删掉。

## License

MIT. The example booklets cite the two arXiv papers; no text from them or from any exam is reproduced.
