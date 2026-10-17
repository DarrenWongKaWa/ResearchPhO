# Worked example: How long can a two-cycle quantum conveyor operate?

A ResearchPhO theory exam built from two arXiv papers with the `researchpho` skill, in strict IPhO/APhO format.

| File | Content |
| --- | --- |
| [questions.pdf](questions.pdf) | 14 pages: general instructions; three independent problems of 10 points (18 questions, 30 points); introductions, 13 figures, given data, "Useful information". No answers, no research notes. |
| [answersheets.pdf](answersheets.pdf) | 7 pages: one box per subquestion and sub-part. |
| [solutions.pdf](solutions.pdf) | 25 pages: answers, marking scheme, 8 answer figures; Appendix A paper map (what each paper answers, research map with D, O-calc and O-theory links, language map, open-link table), Appendix B source/scope/open notes per question, Appendix C teacher notes. |

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
python3 check_answers.py           # picture data and teaching algebra -> check_answers.json
python3 ../../researchpho/scripts/check_booklets.py questions.tex solutions.tex --answers answersheets.tex \
    --total 30 --problem-total 10
```

`figures.py` and `check_answers.py` need numpy and scipy. The figures are single-particle geometry at K/J = -3/2
(Wannier centres from the projected position operator on a 24-cell ring); they are not a many-body simulation.
