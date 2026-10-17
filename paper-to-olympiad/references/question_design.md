# Question design

## 1. The chain of objects

Write the target as one sentence, then the chain of objects that leads to it. The chain is the skeleton of the
problem; each arrow becomes 1-3 questions.

Worked example (fractional Thouless pump, `examples/mb1-fractional-pump`):

```
H_MFP(t)                         the real interacting chain                        S  [paper 1]
 -> h(k, phi)                    5x5 one-particle Bloch matrix                     D  M.1
 -> p12(k, phi)                  projector onto bands 1+2 (a moving plane)         D  B.1, B.2
 -> flavor A/B, frame W(t)       one direction in the plane; following frame       D/O B.4
 -> U = W e^S, K_ret             dressed frame; what is kept                       D/O C.1-C.4
 -> sigma'_X(t), I'(t)           local state; physical current                     D  D.1, D.2, E.1-E.3
 -> Qhat(t) +- E(t)              charge prediction with error bar                  D/O F.1, F.3
 -> first failed window          the research goal                                 O  X.1
```

Labels: **S** stated in a source, **P** project result, **D** derivable exactly in the booklet, **O** open.
D/O means: the identity is derivable, its inputs for the real system are open. The O arrows are where the problem
must say clearly "not established" (red frames) and where the synthesis question lives.

How to find the chain in a paper: start from the quantity in the abstract or the main figure (here: charge per
period), ask "computed from what?", and repeat until you reach the model. Then ask, for each arrow, "which
assumption makes this step work?" - each assumption is a candidate counterexample question.

## 2. Question archetypes

| Archetype | Purpose | Example in the worked problem | Answer type |
| --- | --- | --- | --- |
| Bookkeeping | fix definitions and units | A.1 charge from centre displacements; M.1(c) Hilbert-space dimensions 4845, 70, 16 | number |
| Exact identity | the reader derives the paper's formula | B.1 projector generator; C.3 generator after W e^S; D.2 current after a change of frame; E.3 reduced-state equation | formula |
| Solvable toy model (red ADDED MODEL) | isolate one mechanism with an exact answer | A.2 domain energy; B.2 spin in a turning field; C.1 two-level dressing; C.4 transverse-field chain | formula + number |
| Counterexample | block a tempting inference | B.4 det(i sigma_x) = det(1) yet A -> B; E.1 global vs local fidelity; D.1 same probability, opposite currents; C.4 nothing dropped, state still moves | statement + example |
| Bound chain | turn small errors into a guaranteed statement | E.2 trace-distance current bound; F.1 certificate time | inequality + number |
| Data interpretation | read a table honestly | which claim does a reported table support? | yes/no + reason |
| Decision rule | pass / fail / undetermined with error bars | F.3 three windows | classification |
| Synthesis | list what is still missing | X.1 inputs before a lifetime can be predicted | list |

Rules for every question:

- One verb per sentence: Find, Prove, Show, Evaluate, Explain, State. Avoid "discuss".
- The answer is checkable: a number, a formula, a classification, or a list with fixed items.
- 0.2-1.5 points. Algebra-heavy steps get few points (IPhO syllabus); the physical judgement gets the rest.
- Add "Does this establish X?" only when X is a real temptation, and never answer it in a nearby box.
- Toy models carry a red ADDED MODEL frame that says what they are not. Parameters of a toy model are never
  identified with the real model's parameters unless a reduction is derived.
- Data from a paper or report goes in a green frame that defines every quantity in plain words.
- Each question box repeats the conventions it needs (signs, units, which state is meant).

## 3. Self-containedness

The IPhO syllabus allows out-of-syllabus concepts only if they are explained in syllabus terms. Translate that
into four sections that come before the questions:

1. **Background** (2-3 pages): what the system is, the mechanism in plain words, why it matters, the open question,
   and how the parts of the problem attack it. Two or three computed pictures.
2. **Toolkit**: numbered facts usable without proof (frame change, Heisenberg rule for time-dependent operators,
   Pauli algebra, norm inequalities, partial trace, fermion operators, resolvent, Fourier contour shift, Wannier
   centres). Cite them as T1, T2, ... in the questions.
3. **Glossary**: every technical word, and every label of a source the reader cannot open (e.g. "C1, R2a: two
   numerical calculations of the project; only the printed numbers are needed").
4. **Notation table**: one symbol, one meaning. Use calligraphic letters for generators, blackboard 1 for identity,
   and rename before you write the solutions.

**Cold read.** Give the question booklet alone to a fresh agent: "List every term, symbol, number or assumption you
cannot interpret from this booklet alone. Do not solve the problems." Repeat until the list is empty.

## 4. Points

- One IPhO problem: 10 points. Within it, parts of 1-3 points, questions of 0.2-1.5 points.
- Marking lines use 0.05 or 0.1 units and sum exactly to the question's points.
- When an existing set gains scored questions, keep the old marks and add new ones; update the cover table, the
  part titles and the solution totals together, then run the checker.

## 5. Hints

A hint names the tool, not the step: "Differentiate p^2 = p" is acceptable for a 0.5-point question; "Multiply by
p from both sides to get p p' p = 0" is the answer. Prefer pointing to the Toolkit (T3) over writing new hints.

## 6. Lite mode

For a quick start (1-2 hours): Background (one page), Glossary, 8-12 questions in Markdown, answers in a folded
section, optional 5 multiple-choice vocabulary checks in PanPhO basic-test style. Keep the chain of objects; it is
the part that makes the learning stick.
