# Worked example: How long can a two-cycle quantum conveyor operate?

An APhO-style guided problem built from two arXiv papers with the `paper-to-olympiad` skill.

- [questions.pdf](questions.pdf) - 26 pages, 18 scored questions, 15.0 points. Self-contained: Background, Toolkit,
  Glossary, 14 set-up pictures. Contains no answers.
- [solutions.pdf](solutions.pdf) - 27 pages: worked answers, marking breakdowns, 8 answer pictures, teacher notes.

## Sources

1. M. Jürgensen, J. Steiner, G. Refael, M. C. Rechtsman, *Multi-band fractional Thouless pumps*,
   [arXiv:2504.09338](https://arxiv.org/abs/2504.09338).
2. S.-M. Huang, *Quantum-State Projectors on Grassmannian: Geometry, Holonomy, and Topology*,
   [arXiv:2608.06777](https://arxiv.org/abs/2608.06777).

## What it shows

| Part | Topic | Archetypes |
| --- | --- | --- |
| A | fractional transport; domain energy | bookkeeping, toy model |
| M | from the lattice to the Bloch matrix and the band projector | exact derivation, counting |
| B | projector kinematics; a spin in a turning field; plane versus flavor | identity, toy model, counterexample |
| C | dressing, overlapping corrections, exact frame change, "kept" versus "harmless" | toy model, identity, counterexample |
| D | current needs a phase; the current after a change of frame | counterexample, identity |
| E | global versus local fidelity; a local current-error bound; the reduced-state equation | counterexample, bound, identity |
| F | a conditional operating-time certificate; pass / fail / undetermined | bound chain, decision rule |
| X | what a real prediction still needs | synthesis |

This is a public excerpt of a 26-question, 20-point version. Questions that used unpublished calculations of the
underlying research project were removed; labels were kept, so they skip (no B.3, B.G1, B.G2, R.1, R.2, E.G1, E.G2,
F.2).

## Rebuild and check

```bash
python3 figures.py            # recompute bands and Wannier centres; rewrites the data block in both .tex files
pdflatex questions.tex && pdflatex questions.tex
pdflatex solutions.tex && pdflatex solutions.tex
python3 check_answers.py      # picture data and teaching algebra -> check_answers.json
python3 ../../paper-to-olympiad/scripts/check_booklets.py questions.tex solutions.tex --total 15
```

`figures.py` and `check_answers.py` need numpy and scipy. The pictures are single-particle geometry at
K/J = -3/2 (Wannier centres from the projected position operator on a 24-cell ring); they are not a many-body
simulation.
