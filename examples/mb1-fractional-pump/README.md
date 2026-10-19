# Worked example: How long can a two-cycle quantum conveyor operate?

A ResearchPhO theory exam built from two arXiv papers with the `researchpho` skill, in strict IPhO/APhO format.

| File | Content |
| --- | --- |
| [questions.pdf](questions.pdf) | 14 pages: general instructions; three independent problems of 10 points (18 questions, 30 points); introductions, 13 figures, given data, "Useful information". No answers, no research notes. |
| [answersheets.pdf](answersheets.pdf) | 7 pages: one box per subquestion and sub-part. |
| [solutions.pdf](solutions.pdf) | 28 pages: answers, marking scheme with every piece tagged (M) modelling or (C) computation, 8 answer figures; Appendix A paper map (what each paper answers, research map with D, O-calc and O-theory links, language map, open-link table), Appendix B source/scope/open notes per question, Appendix C teacher notes, Appendix D toolbox (the smallest worked example of each tool the question paper states without proof). |
| [study_guide.html](study_guide.html) | Study guide for an undergraduate who knows the four core physics courses: the 18 questions in order, with 11 computation tools (blue) and 18 modelling ideas (orange) beyond that level, one resource each. Open it in a browser; ticks are saved in that browser. Built from [study_guide.json](study_guide.json). |
| [research_checklist.html](research_checklist.html) | Research checklist: the chain of objects from the model to the research target, with the 6 open links of Appendix A beside it (2 O-calc in amber, 4 O-theory in red), to tick off as results close them. Built from [research_checklist.json](research_checklist.json). |

## Sources

1. M. Jürgensen, J. Steiner, G. Refael, M. C. Rechtsman, *Multi-band fractional Thouless pumps*,
   [arXiv:2504.09338](https://arxiv.org/abs/2504.09338).
2. S.-M. Huang, *Quantum-State Projectors on Grassmannian: Geometry, Holonomy, and Topology*,
   [arXiv:2608.06777](https://arxiv.org/abs/2608.06777).

## Problems

| Problem | Parts | Archetypes |
| --- | --- | --- |
| 1. A two-cycle quantum conveyor: bands, projectors and flavors | A fractional transport; B lattice to projector; C following a moving projector; D a plane is not yet a flavor | bookkeeping, identity, toy model, counterexample |
| 2. Correlations and the physical current | A domains in a spin chain; B dressing a reference state; C exact frames and kept dynamics; D the physical current | toy model, identity, counterexample |
| 3. How long can the conveyor operate? | A local accuracy; B a conditional operating-time certificate; C prediction, error and first failure | bound chain, decision rule, synthesis |

This is a public excerpt of a 26-question version. Questions that used unpublished calculations of the underlying
research project were removed; the remaining questions were relabelled within each problem and their points
rescaled to 10 per problem.

## Rebuild and check

```bash
python3 figures.py                 # recompute bands and Wannier centres; rewrites the data block in both .tex files
pdflatex questions.tex && pdflatex questions.tex
pdflatex solutions.tex && pdflatex solutions.tex
python3 ../../researchpho/scripts/make_answer_sheets.py questions.tex answersheets.tex
pdflatex answersheets.tex
python3 ../../researchpho/scripts/make_checklist.py study_guide.json study_guide.html --profile study-guide
python3 ../../researchpho/scripts/make_checklist.py research_checklist.json research_checklist.html --profile research
python3 check_answers.py           # picture data, teaching algebra, toolbox examples -> check_answers.json
python3 ../../researchpho/scripts/check_booklets.py questions.tex solutions.tex --answers answersheets.tex \
    --total 30 --problem-total 10 --guide study_guide.json
```

The checker reports the modelling share of the tagged marks: 56% in Problem 1, 53% in Problem 2 and 52% in
Problem 3, above the one-half target (standards S2, S3). The first tagging gave 45%, 34% and 40%: the solvable
models (1.C.1, 2.B.1), the current identity (2.D.2) and the bound chain (3.A.2, 3.B.1) gave most of their points
to algebra. The marking lines were then rebalanced within each question, with every question's total unchanged:
algebra pieces lost weight, and the interpretation each solution already states gained it.
A later revision can move marks to the interpretation steps or add modelling sub-questions.

`figures.py` and `check_answers.py` need numpy and scipy. The figures are single-particle geometry at K/J = -3/2
(Wannier centres from the projected position operator on a 24-cell ring); they are not a many-body simulation.
