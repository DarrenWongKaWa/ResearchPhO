# Worked example 2 (sources): How does disorder enter a model, a Hall current and a pump?

A ResearchPhO theory exam built with the `researchpho` skill, in strict IPhO/APhO format, for an undergraduate who
knows the four core physics courses. The research question behind it: how is a microscopic disorder model built for
a real material, and how is it then used for a response (the nonlinear Hall effect, nonlinear optics) and for a
Thouless pump in a large system? This folder holds the sources. The deliverables are in
[`../DisorderInducedNonlinearHallEffect_RPhO`](../DisorderInducedNonlinearHallEffect_RPhO/):

| Deliverable | Content |
| --- | --- |
| [questions.pdf](../DisorderInducedNonlinearHallEffect_RPhO/questions.pdf) | 18 pages: general instructions; three independent problems of 10 points (33 questions, 30 points); introductions, 9 figures, given data, "Useful information". No answers, no research notes. |
| [solutions.pdf](../DisorderInducedNonlinearHallEffect_RPhO/solutions.pdf) | 24 pages: answers, marking scheme with every number tagged (M) or (C); Appendix A paper map (what each source answers, language map, chain of objects, open-link table), B source/scope/open notes, C register of available and missing results, D teacher notes (checks, interpretations to confirm, a priority list of disorder sources in real materials), E toolbox. |
| [checklist.html](../DisorderInducedNonlinearHallEffect_RPhO/checklist.html) | One page: the 33 questions with 15 computation tools (blue) and 31 modelling ideas (orange), each with a linked reference; then the research segment with 4 O-calc (amber) and 5 O-theory (red) open links. Built from [checklist.json](checklist.json). |

## Sources

1. N. Nagaosa, J. Sinova, S. Onoda, A. H. MacDonald, N. P. Ong, *Anomalous Hall effect*,
   [Rev. Mod. Phys. 82, 1539 (2010)](https://doi.org/10.1103/RevModPhys.82.1539).
2. Z. Z. Du, C. M. Wang, S. Li, H.-Z. Lu, X. C. Xie, *Disorder-induced nonlinear Hall effect with time-reversal
   symmetry*, [Nat. Commun. 10, 3047 (2019)](https://doi.org/10.1038/s41467-019-10941-3).
3. Z. Z. Du, C. M. Wang, H.-P. Sun, H.-Z. Lu, X. C. Xie, *Quantum theory of the nonlinear Hall effect*,
   [Nat. Commun. 12, 5038 (2021)](https://doi.org/10.1038/s41467-021-25273-4) (used for the sign revision of the
   collision terms).
4. L. Hertkorn, Y. Oreg, *Topology from disorder*, [Nat. Phys. 22, 1534 (2026)](https://www.nature.com/articles/s41567-026-03459-1),
   on Z. Yue et al., [arXiv:2505.06286](https://arxiv.org/abs/2505.06286), and L. Su et al.,
   [arXiv:2505.17009](https://arxiv.org/abs/2505.17009). The body of the commentary was not available; the
   average-symmetry questions use the two original papers.
5. M. Jürgensen, J. Steiner, G. Refael, M. C. Rechtsman, *Multi-band fractional Thouless pumps*,
   [arXiv:2504.09338](https://arxiv.org/abs/2504.09338), and its ref. 14, Q. Niu, D. J. Thouless,
   [J. Phys. A 17, 2453 (1984)](https://doi.org/10.1088/0305-4470/17/12/016).

## Problems

| Problem | Parts | Archetypes |
| --- | --- | --- |
| 1. From a dirty crystal to a random Hamiltonian | A impurity to lattice parameters; B displaced atoms; C correlations to rates; D which random term first? | modelling, bookkeeping, solvable toy model, counterexample, decision rule, synthesis |
| 2. Impurities and the second-order Hall current | A three sources of a Hall current; B a dipole of curvature; C collisions at the same order; D one broadening, many ensembles | exact identity, toy model, data interpretation, counterexample, synthesis |
| 3. Disorder in a two-cycle quantum pump | A topology from disorder in a dimer chain; B counting the pumped charge; C what a random potential does to the flavors; D domains in a long disordered chain | exact identity, bookkeeping, toy model, bound chain, synthesis |

The modelling share of the tagged marks is 57%, 64% and 64%.

## Rebuild and check

```bash
pdflatex questions.tex && pdflatex questions.tex
pdflatex solutions.tex && pdflatex solutions.tex
python3 check_answers.py           # every derivable answer, independent numerics, toolbox -> check_answers.json
python3 build_checklist_json.py    # writes checklist.json
python3 ../../researchpho/scripts/check_booklets.py questions.tex solutions.tex \
    --total 30 --problem-total 10 --checklist checklist.json
D=../DisorderInducedNonlinearHallEffect_RPhO
cp questions.pdf solutions.pdf $D/
python3 ../../researchpho/scripts/make_checklist.py checklist.json $D/checklist.html
```

`check_answers.py` needs numpy and scipy (about 15 s). Besides the answers it checks the golden-rule rate against the
exact decay of a plane wave on a 3000-site ring, the localization length against a transfer-matrix Lyapunov
exponent, the Berry curvature dipole against a two-dimensional integration, and computes the two-band flavor orbitals
of the clean five-site pump (single-particle geometry at K/J = -3/2, 24-cell ring) that give Figure 3.3 and the bias
and mixing values of 3.C.2.

## What the cold read and trial solve changed

A cold read by fresh agents found an inconsistency (the neglected orbital overlap was larger than the bond term asked
for in 1.A.1; fixed by a/b = 4 and a stated model), about twenty symbol clashes (renamed), and missing tools in
Problem 3's "Useful information" (added). The trial solve reproduced every final answer and led to four changes: the
validity of a noise rate when the correlation time exceeds the observation time (1.D.1), a corrected answer to 2.C.2(b)
(the two theories' totals keep their signs for all Fermi energies, so only an independent dipole value separates
them), an accepted alternative input in 2.D.3, and clearer wording in 3.C.2–3.C.3.
