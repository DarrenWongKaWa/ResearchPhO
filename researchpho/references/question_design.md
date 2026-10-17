# Question design

## 0. What does each paper answer, and in which language?

Start with two short documents; both go to Appendix A of the solutions.

**The question each paper answers.** One sentence for the question and one for the answer, in plain physics.
Worked example: paper 1 asks "can repulsion turn an integer Thouless pump into one that carries half a particle per
period at integer filling, and how?" and answers "yes, at strong repulsion in small systems: the particles occupy one
of two localized two-band orbital types, which exchange every period, so each particle moves one cell in two periods;
in large systems this should last only for a finite (prethermal) time". Paper 2 asks "how
can one describe a moving group of bands without choosing a basis inside it?" and answers "with the band projector,
its derivative and the generator built from them". Each problem's introduction ends with such a question; its last
part reaches the paper's answer or the closest derivable form.

**The language map.** For every term of the paper: its meaning in standard physics, and where a physicist from
another field met the idea before. Many "new" words name familiar physics:

| Paper term | Standard physics | Where the reader met it |
| --- | --- | --- |
| Thouless pump | slow periodic modulation that moves charge; adiabatic transport | Berry phase, adiabatic theorem |
| Chern number of a band | integer winding of the Berry phase over (k, t) | Berry phase; quantum Hall effect |
| Wannier orbital, centre | localized orbital built from Bloch states; its mean position | tight binding; Fourier series |
| flavor A/B | the two localized orbital types built from bands 1 and 2 together | basis choice inside a degenerate subspace |
| composite bands, Gr(2,5) | a group of bands treated together; the set of planes in C^5 | degenerate perturbation theory; projectors |
| horizontal generator | the generator that moves a subspace without rotating inside it | adiabatic (Kato) generator, rotating frames |
| Wilson loop | ordered product of band-overlap matrices around the Brillouin zone | Berry phase on a closed path, discretized |
| prethermal lifetime | time during which a driven system stays in a long-lived non-equilibrium state | metastable states, false-vacuum decay |
| dressing e^S | a unitary change of basis that builds correlations into a reference state | Schrieffer-Wolff transformation |

In the question paper use the standard word and put the paper's term in parentheses at first use. The cold read
(section 3) checks that no term is left untranslated.

## 1. The chain of objects

Write the target as one sentence, then the chain of objects that leads to it. The chain is the skeleton of the
problem; each arrow becomes 1-3 questions.

Worked example (fractional Thouless pump, `examples/mb1-fractional-pump`; labels problem.part.number):

```
H_MFP(t)                         the real interacting chain                        S  [paper 1]
 -> h(k, phi)                    5x5 one-particle Bloch matrix                     D  1.B.1
 -> p12(k, phi)                  projector onto bands 1+2 (a moving plane)         D  1.B.2, 1.C.1
 -> flavor A/B, frame W(t)       one direction in the plane; following frame       D/O 1.D.1
 -> U = W e^S, K_ret             dressed frame; what is kept                       D/O 2.B.1-2.C.2
 -> sigma'_X(t), I'(t)           local state; physical current                     D  2.D.1, 2.D.2, 3.A.1-3.A.3
 -> Qhat(t) +- E(t)              charge prediction with error bar                  D/O 3.B.1, 3.C.1
 -> first failed window          the research goal                                 O  3.C.2
```

Labels: **S** stated in a source, **P** project result, **D** derivable exactly in the booklet, **O** open.
D/O means: the identity is derivable, its inputs for the real system are open. The chain, with its labels, becomes
Appendix A of the solutions; the O arrows are listed in Appendix C and feed the synthesis question. None of this
appears in the question paper.

## 1b. Split into three independent problems

Cut the chain into three problems of 10 points that can be solved in any order. In the worked example: Problem 1
(model, bands, projector, locality, flavors), Problem 2 (domains, dressing, frames, current), Problem 3 (local
errors, certificate, data, first failure). Keep dependencies inside a problem; when a problem needs a result from
another, state it as given. Each problem gets 3-5 parts and its own introduction.

How to find the chain in a paper: start from the quantity in the abstract or the main figure (here: charge per
period), ask "computed from what?", and repeat until you reach the model. Then ask, for each arrow, "which
assumption makes this step work?" - each assumption is a candidate counterexample question.

## 2. Question archetypes

| Archetype | Purpose | Example in the public worked example | Answer type |
| --- | --- | --- | --- |
| Modelling | the reader sets up the model or picks the relevant physics | 1.B.1(a) derive the Bloch matrix from the lattice; 2.A.1 energy bookkeeping of a domain; 2.C.1(c) where does the approximation enter? | model + reason |
| Bookkeeping | fix definitions and units | 1.A.1 charge from centre displacements; 1.B.1(c) Hilbert-space dimensions 4845, 70, 16 | number |
| Exact identity | the reader derives the paper's formula | 1.B.2 projector generator; 2.C.1 generator after W e^S; 2.D.2 current after a change of frame; 3.A.3 reduced-state equation | formula |
| Solvable toy model | isolate one mechanism with an exact answer | 2.A.1 domain energy; 1.C.1 spin in a turning field; 2.B.1 two-level dressing; 2.C.2 transverse-field chain | formula + number |
| Counterexample | block a tempting inference | 1.D.1 det(i sigma_x) = det(1) yet A -> B; 3.A.1 global vs local fidelity; 2.D.1 same probability, opposite currents; 2.C.2 nothing dropped, state still moves | statement + example |
| Bound chain | turn small errors into a guaranteed statement | 3.A.2 trace-distance current bound; 3.B.1 certificate time | inequality + number |
| Data interpretation | read a table honestly | which claim does a reported table support? (full version) | yes/no + reason |
| Decision rule | pass / fail / undetermined with error bars | 3.C.1 three windows | classification |
| Synthesis | list what is still missing | 3.C.2 inputs before a lifetime can be predicted | list |

Rules for every question:

- One verb per sentence: Find, Prove, Show, Evaluate, Explain, State. Avoid "discuss".
- The answer is checkable: a number, a formula, a classification, or a list with fixed items.
- 0.2-2.5 points. Algebra-heavy steps get few points (IPhO syllabus); the physical judgement gets the rest.
- Every problem has at least one modelling question (standard S2): the reader builds or chooses the model, not
  only manipulates a given formula.
- Add "Does this establish X?" only when X is a real temptation, and never answer it in a nearby box.
- State toy models plainly ("Consider the spin chain ..."). Their scope note (what they are not) goes to
  Appendix B. Never identify a toy model's parameters with the real model's unless a reduction is derived.
- Data from a paper or report goes in plain text or a table, with every quantity defined in plain words.
- Each question box repeats the conventions it needs (signs, units, which state is meant).

## 3. Self-containedness

The IPhO syllabus allows out-of-syllabus concepts only if they are explained in syllabus terms. In ResearchPhO this
happens inside each problem, never on separate pages:

1. **Introduction**: the system, the mechanism in plain words, the model with all conventions, and the question the
   problem builds towards; a footnote may cite the source papers.
2. **Useful information**: the facts this problem needs (frame change, Heisenberg rule, Pauli algebra, norm
   inequalities, partial trace, fermion operators, resolvent, Fourier contour shift, Wannier centres, ...), one line each.
3. **Definitions at first use**: every technical word ("Wannier orbital", "Slater determinant", "external weight")
   is defined in the sentence where it first appears.
4. **One symbol, one meaning**: calligraphic letters for generators, blackboard 1 for the identity; rename before
   writing the solutions.

**Cold read.** Give one problem alone to a fresh agent: "Do not solve the problem. List (a) every term, symbol,
number or assumption you cannot interpret from this text alone; (b) every step that needs mathematics not provided
in the text; (c) in your own words, the question this problem says the paper answers." Repeat until (a) and (b) are
empty and (c) matches the sentence written in section 0.

## 3b. Mathematics budget (standard S3)

The olympiad rule is that mathematics must not be the obstacle: standard mathematics, no extensive numerical
calculation, a small share of marks for manipulation, partial credit for approximate routes. In ResearchPhO:

- "Standard" means mathematics the chosen reader already has (default: university physics mathematics: linear
  algebra, calculus, Fourier series, complex numbers, basic probability).
- Any other tool (contour integrals of resolvents, trace norms, partial traces, Lie-algebra identities) is stated in
  one line under "Useful information", in a form that can be used without proof.
- No step requires a computer; numbers are chosen so that a calculator suffices.
- When a derivation is long, split it into questions and give the intermediate result as a target ("Show that ...").
- Marking: at most about one third of a question's points for pure algebra; give partial credit for a correct
  approximate argument.

The cold read reports every step "blocked by mathematics that is not provided"; fix each one by adding a line to
"Useful information", a target result, or a hint.

## 4. Points

- A full exam: three problems of 10 points (30 points, 5 hours). Within a problem, parts of 1-4 points and
  questions of 0.2-2.5 points.
- Marking lines use 0.05 or 0.1 units and sum exactly to the question's points.
- When questions are regrouped, rescale points within each problem to 10 (largest-remainder rounding in 0.1),
  rescale every marking line in 0.05 steps, relabel cross-references with a map, and run the checker.

## 5. Hints

A hint names the tool, not the step: "Differentiate p^2 = p" is acceptable for a 0.5-point question; "Multiply by
p from both sides to get p p' p = 0" is the answer. Prefer pointing to an item of the problem's "Useful information" over writing new hints.

## 6. Quick version

For a fast start (1-2 hours of solving): one problem of 10 points with 3 parts, the same strict layout, its answer
sheet and solutions. Keep the chain of objects in the appendix; it is the part that makes the learning stick.
