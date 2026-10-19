# Case study: a two-cycle quantum conveyor

The worked example in `examples/mb1-fractional-pump/` was built from two papers:

1. M. Jürgensen, J. Steiner, G. Refael, M. C. Rechtsman, *Multi-band fractional Thouless pumps*, arXiv:2504.09338.
   Repulsive fermions on a five-site-per-cell driven chain can follow one "flavor" of two-band Wannier orbitals;
   each flavor returns only after two periods, giving -1/2 particle per period at integer filling. The paper leaves
   the large-system lifetime open.
2. S.-M. Huang, *Quantum-State Projectors on Grassmannian: Geometry, Holonomy, and Topology*, arXiv:2608.06777.
   Band projectors, their tangent vectors and horizontal generators, geodesics, Wilson-loop determinants.

The research question behind the booklet: how long does the fractional pump keep its transport in a large system?
The full project version also used unpublished calculations; the public example keeps only what follows from the
two papers and from teaching models.

## Revision history and what each revision taught

| Revision | Change | Lesson |
| --- | --- | --- |
| 1 | 13 scored questions in six parts, 10 points, APhO layout | the chain A (target) -> B (geometry) -> C (correlations) -> D (current) -> E (local error) -> F (time) works as a skeleton |
| 2 | unscored supplements with project proofs and data | supplements without points get skipped; data without definitions cannot be used |
| 3 | six "modelling bridges" between objects (M.1, B.4, C.3, C.4, E.3, F.3) | the bridges carried most of the learning: why the next object is needed |
| 4 | everything scored (20 points); Background, Toolkit, Glossary; 16 set-up pictures; notation unified; answer leaks removed; teacher notes | a reader who had not read the papers could not start revision 3; a cold read finds this at once |
| 5 (ResearchPhO) | strict IPhO/APhO format: three independent problems of 10 points, boxed subquestions, answer sheets; every coloured frame, scope note and research-plan item moved to solution Appendices A-D; background and toolkit moved into each problem's introduction and "Useful information" | status frames are not olympiad style and distract the solver; the research context belongs at the end of the solutions |
| 6 (ResearchPhO 1.1.0) | marking lines tagged (M)/(C); toolbox appendix; study guide; the field direction of 1.C.1 defined in the text and the Bloch vector introduced before Figure 1.5 | the tags measure S2 instead of asserting it: 45%, 34% and 40% modelling, below the one-half target |

## Reader feedback that drove revisions 4 and 5

- "I do not know what the questions ask." -> pictures that show the set-up and say "X asks: ..." in plain words.
- "I want to solve it myself." -> remove every answer from the question booklet, including a box title with the
  numerical answer and status tables that listed the synthesis answers.
- "The booklet should give enough to think with, without the papers." -> Background, Toolkit, Glossary, plain
  definitions of report quantities, and a cold read.
- "Everything should be scored." -> keep the old marks, add marks to the rest, re-total, and check with a script.
- "These frames do not exist in APhO and are not for solving; they are research-plan information." -> strict
  format; three problems of 10 points; all research context in the solution appendices.
- "Call it ResearchPhO."

## Tutoring sessions that drove version 1.1.0

A reader worked through the exam with the agent as a tutor. The same needs came back in every session:

- "What is this part doing, and why?" -> the purpose sentence of each tutor card.
- "How do I read this figure?" (the Bloch-sphere cut of 1.C.1) -> the figure-reading table; every symbol of a figure
  also defined in the text.
- Lab frame versus rotating frame -> a two-column table for every change of frame.
- One letter for two fields, and a direction defined only in a caption -> one letter per object; symbols named
  before use.
- Unfamiliar mathematics (a determinant expansion, a product identity) -> the smallest worked example first; the
  toolbox appendix.
- Misreadings: "t^2 growth at short times means a divergence"; "a lower energy means it will happen"; "in the
  rotating frame the field is along z" -> the misreading list of the tutor cards, seeded from the trial solve.
- "What do I need to know first?" -> the study guide, drawn as a checklist flowchart.

## Audit findings on revision 3 (before the rewrite)

- All computed answers were correct (gap bound, contour constants, certificate time, classifications); the problems
  were in presentation.
- Editorial text addressed to the author ("Keep the 13 scored questions ...") sat in the student instructions.
- Sources were cited as private files "supplied in this conversation".
- Symbol clashes: K (amplitude, generator), F (frame matrix, polynomial, fidelity), J (hopping, local current,
  coupling, amplitude), I (current, identity).
- About ten red "scope" frames answered the question just above them.

## A physics check worth copying

The computed Wannier centres at K/J = -3/2 move +2 cells per period for band 1 and -1 cell per two periods for the
followed two-band flavor; an explicit time evolution of the filled band gave +2.00 per period through every bond.
These agree with the paper's figure values (+2 integer, -1/2 fractional) in a rightward-positive convention, while
the current expression printed in the paper is minus the rightward current for the printed Hamiltonian. Always
re-derive a sign before you set a target value in a problem.

## Reusable pieces (labels of the public example)

- The chain-of-objects picture (Appendix A): black arrows derived, amber dashed arrows O-calc, red dashed arrows
  O-theory; and the open-link table with the closest existing theory and the hypothesis that fails.
- A two-level "dressing" model (2.B.1) to show that short-time growth v^2 t^2 is not a decay rate.
- The counterexample det(i sigma_x) = det(1) (1.D.1) against reading internal exchange from a determinant.
- Global versus local fidelity for a product state (3.A.1).
- The certificate (3.B.1) and the pass/fail/undetermined rule (3.C.1) for any "how long does it last" proposal.
