# paper-to-olympiad: learn a field by writing its exam

A [Claude Code](https://claude.com/claude-code) skill that turns research papers, the literature of a new field, or
a research proposal into a self-contained **IPhO / APhO / PanPhO-style guided problem set**: a question booklet that
a reader can solve without the papers, and a solution booklet with marking scheme and teacher notes.

[中文说明见下方](#中文说明)

## Why the olympiad format

A physics-olympiad theory problem introduces an unfamiliar topic in a few paragraphs and then breaks it into 15-25
small steps, each with points, given data and a checkable answer. The IPhO syllabus even requires that any concept
outside the syllabus be "explained in terms of topics in the Syllabus". That is exactly what a newcomer to a field
needs: a map of the field, the few calculations that carry it, and a clear line between what is established and
what is still open.

## What the skill does

1. Maps the papers as a **chain of objects** from the model to the measured quantity and labels each step:
   stated in a source, derivable here, or open.
2. Turns each step into questions of eight types: bookkeeping, exact identity, solvable toy model, counterexample,
   bound chain, data interpretation, pass/fail/undetermined decision rule, synthesis.
3. Makes the question booklet **self-contained**: Background, Toolkit (facts usable without proof), Glossary,
   one-symbol-one-meaning notation table, and a "cold read" by a fresh agent to find anything undefined.
4. Draws **set-up pictures** (never answers) with TikZ/pgfplots, including figures computed from the model.
5. Writes solutions with marking breakdowns, answer pictures and teacher notes on provenance.
6. **Verifies**: label/point/marking consistency, answer-leak and internal-path scans, a script for every derivable
   answer, independent sign checks, and contact sheets of every page.
7. **Proposal mode**: adds a conditional result, a decision rule, a synthesis question and an available/missing
   register.

## Contents

```
paper-to-olympiad/                  the skill (copy this folder to ~/.claude/skills/)
  SKILL.md                          entry point: workflow, colour code, top pitfalls
  references/olympiad_formats.md    IPhO, APhO, PanPhO rules and what to copy (with sources)
  references/question_design.md     chain of objects, question archetypes, points, cold read, Lite mode
  references/booklet_layout.md      page order, macros, pictures, page-break control
  references/verification.md        checker, answer scripts, sign checks, rendering, leak review
  references/proposal_mode.md       proposal -> chain -> register -> synthesis question
  references/case_study_mb1.md      how the worked example was built, revision by revision
  assets/questions_template.tex     self-contained LaTeX question booklet
  assets/solutions_template.tex     matching solution booklet
  scripts/check_booklets.py         labels, points, marking sums, answer leaks, forbidden text
  scripts/render_sheets.py          PDF pages -> contact sheets
examples/mb1-fractional-pump/       worked example (questions.pdf, solutions.pdf, sources, checks)
```

## Install

```bash
git clone https://github.com/DarrenWongKaWa/paper-to-olympiad-skill.git
mkdir -p ~/.claude/skills
ln -sfn "$(pwd)/paper-to-olympiad-skill/paper-to-olympiad" ~/.claude/skills/paper-to-olympiad
```

Or copy the folder instead of linking it. The LaTeX templates need TeX Live 2023 or newer (tikz, pgfplots,
tcolorbox, newtxmath, dsfont). The scripts need Python 3.10+, and `render_sheets.py` needs `pymupdf` and `pillow`.

## Use

In Claude Code, attach or name the papers and ask, for example:

- "Use paper-to-olympiad: make an APhO-style problem (10 points) from these two papers so that I can learn the field."
- "Turn my proposal into a guided problem set and give me the available/missing register."
- "Lite mode: one page of background and 10 questions with answers from this review."
- "Audit this question booklet for answer leaks, undefined terms and notation clashes."

## Worked example

[`examples/mb1-fractional-pump`](examples/mb1-fractional-pump/) - *How long can a two-cycle quantum conveyor
operate?* Built from [arXiv:2504.09338](https://arxiv.org/abs/2504.09338) (multi-band fractional Thouless pumps)
and [arXiv:2608.06777](https://arxiv.org/abs/2608.06777) (projectors on the Grassmannian). 18 questions,
15 points, 14 set-up pictures, 8 answer pictures.

---

## 中文说明

**目标：** 让大家接触一个新领域的文献、或者写/读一个 proposal 时，能像做一套奥赛题一样快速学会它。

这个 skill 把论文或 proposal 改写成 IPhO / APhO / PanPhO 风格的引导式题目：

- **题目册**：不读原文也能直接做。开头有背景知识、工具箱（可直接引用的数学事实）、术语表和符号表；每道题配一张"这题在问什么"的图；题目册里不出现任何答案。
- **答案册**：完整解答、逐项评分细则、答案图，以及教师说明（数据出处、哪些内容从题目册里移走了、为什么移走）。

**做法：**

1. 把领域画成一条"对象链"：从模型一路走到可测量的量。每一步标明是文献已有、可在题中推出，还是尚未解决。
2. 每一步出 1–3 道题。题型有八种：记账、恒等式推导、可精确求解的玩具模型、反例、估计链、读数据、通过/失败/待定判据、综合题。
3. 自足性检查：把题目册单独交给一个新的 agent，让它列出所有看不懂的词、符号和数字，直到列表为空。
4. 自动检查：分值是否一致、评分细则加起来是否等于分值、有没有泄露答案或内部路径；每个能推导的答案都用脚本复算；符号约定另做一次独立验证；逐页渲染检查版面。
5. Proposal 模式：额外加一道"条件结论"题、一条判定规则和一道综合题，并在答案册里给出"已有 / 缺失"清单。

**三个比赛的特点（详见 `references/olympiad_formats.md`）：**

- **IPhO / APhO**：理论 3 题共 30 分、5 小时，实验 20 分；只用高中数学；允许出现大纲外的概念，但必须用大纲内的知识解释清楚。
- **PanPhO**：由香港科技大学主办，分基础试（只考力学）和综合试（接近 IPhO 难度，会涉及科研最新进展）。

**例子：** `examples/mb1-fractional-pump` 用两篇 arXiv 论文（多带分数 Thouless 泵、Grassmann 流形上的投影算子）出了 18 道题、共 15 分。这是一个更大题目的公开节选，依赖未发表数据的题目已经删掉。

## License

MIT. The example booklets cite the two arXiv papers; no text from them or from any exam is reproduced.
