# Tutor mode

Use tutor mode when a reader works through a ResearchPhO exam with the agent: "tutor me through Problem 1", "explain
Part C", "what does Figure 1.5 show?". The booklets stay as they are. The agent prepares one tutor card per question,
then leads the reader through it.

Inputs: the question paper, the solutions with Appendix A (language map, chain of objects, open links), the toolbox
appendix, the study guide, and the trial-solve records (see [verification](verification.md), section 1c).

## 1. The tutor card (prepare before the reader starts the question)

| Field | Content | Source |
| --- | --- | --- |
| Purpose | One sentence: what this part establishes and why the problem needs it next. | the chain of objects |
| Figure reading | A table: each element of the set-up figure (axis, symbol, colour, arrow, shaded area), what it means, and which question uses it. | the figure and its caption |
| Language map | The rows of the language map that this question uses: paper term, picture, familiar equivalent. | Appendix A |
| Steps and hints | The steps of the solution in order. Each step has one hint that names the tool, never the result. | the solution |
| Sanity checks | A limit (nu -> 0, N -> infinity), units or dimensions, and a small case that the reader can compute by hand (N = 1, two sites, one spin). | the solution; the toolbox appendix |
| Misreadings | Likely misreadings, each with its correction and the computation or counterexample that shows it. | trial solve; the seed list in section 4 |
| Research step | The arrow of the chain that this question corresponds to, its label (D, O-calc, O-theory), and what is still open there. | Appendix A, open-link table |

Keep the card private until it is needed. Show one field at a time, when the reader reaches it.

## 2. Rules during the session

1. **Lead with questions.** Ask what the reader would try first. Let the reader compute each step before you show
   it. Use this order of help, one rung at a time:
   1. ask the next question ("Which term in K comes from the motion of the frame?");
   2. point to the line of "Useful information" or the hint;
   3. give the smallest worked example from the toolbox appendix;
   4. show the step.
2. **Never show a boxed answer before the reader asks for it.** "I give up" or "show me the answer" is a request;
   "I am stuck" is not.
3. **Name every symbol before you use it.** Give each object one letter for the whole session, and keep a symbol
   table. If the exam uses one letter for two objects, rename one of them and say so. Two cases that confused a
   reader in practice:
   - B for the total field in one sentence and for the applied (real) field in the next. Write B_lab for the
     applied field and B_eff for the field in the rotating frame.
   - n(t) defined only in a figure caption. Define it in a sentence of the text before the figure uses it.
4. **Introduce a picture before you use it.** Example: "The state of one spin-1/2 is a point on a sphere. Its Bloch
   vector is r = <sigma>; r has length 1 for a pure state. The ground state of H = -(Delta/2) n . sigma has r = n."
   Only then talk about the vector "lagging" or "precessing".
5. **Tabulate every change of frame or representation.** Use the columns "quantity | description 1 | description
   2 | relation". Example: section 5.
6. **Give a tiny worked example for each pure-mathematics tool** before the reader uses it in the exam: a 3-site
   ring determinant before the 5-site one; the N = 2 case of a product identity before the general N.
7. **Correct a misreading at once and explicitly.** State the misreading, say why it is tempting, and show the
   computation or counterexample that refutes it. Do not only restate the correct result.
8. **Close each part with a two-sentence recap**: what was found, and what it means for the question the paper
   answers.
9. **Prerequisites on request.** When the reader asks "what do I need to know for this?", show the study guide, or
   the items of the current question from it.

## 3. Preparing the cards

1. Read the solution of the question; split it into steps of one idea each.
2. For each step, write the hint as a tool name or a question ("Differentiate p^2 = p"; "Which states does the
   current operator connect?").
3. Take the figure-reading rows from the set-up figure. Every symbol in the figure must also be defined in the text
   (rule 3); if it is not, add the definition to the question paper.
4. Take the misreadings from the trial-solve records first, then from section 4.
5. Take the research step from the chain of objects; quote its label, not a summary of the research.

## 4. Seed list of misreadings

| Misreading | Correction | Shown by (worked example) |
| --- | --- | --- |
| "Quadratic growth at short times, v^2 t^2, means the population runs away or decays at a rate." | Every quantum transition probability starts as t^2. The exact two-level result oscillates and returns to zero; a rate needs a continuum of final states. | 2.B.1, 2.C.2 |
| "A lower energy means it will happen." | An eigenstate only acquires a phase. A transition needs a matrix element to the other state and a way to remove the energy difference. | 2.A.1 |
| "In the rotating frame the field is always along z." | K = W^dagger H W - i W^dagger dW/dt. The second term is a fictitious field along the rotation axis of the frame; in 1.C.1 it points along y. | 1.C.1 |
| "Equal determinants mean the same action." | det(i sigma_x) = det(1) = 1, but i sigma_x exchanges A and B. | 1.D.1(c) |
| "A closed projector path means the endpoint term of the current vanishes." | A closed path fixes a subspace, not a frame. The endpoint term and the bulk term are each frame-dependent; only their sum is physical. | 2.D.2 |
| "Low global fidelity means poor local accuracy." | For a product state, F_N = (1 - p)^N goes to 0 while every m-cell region keeps F_m = (1 - p)^m. | 3.A.1 |
| "The certificate ends, so the pump fails there." | A sufficient bound stops certifying; it says nothing about failure after that time. | 3.B.1 |

Add every misreading that a trial solve or a reader produces, with the question where it appeared.

## 5. Worked tutor card: question 1.C.1 of the example

**Purpose.** Show, with a spin that can be solved exactly, that following a moving ground-state projector depends
on the gap Delta and the turning rate nu, although the projector path p(t) does not depend on Delta.

**Figure reading (Figure 1.5).**

| Element | Meaning | Used in |
| --- | --- | --- |
| circle | cut of the Bloch sphere in the x-z plane; a pure spin state is a point on it | whole question |
| blue arrow n(t) | field direction (sin nu t, 0, cos nu t); the ground state of H points along it | p(t), H(t) |
| angle nu t | angle of n(t) from the z axis; it grows at rate nu | W(t) |
| orange arrow and ellipse | the actual state; it may lag behind n(t) and precess around it | P_ex(t) |
| dashed arc | the field keeps turning in the same direction | the frame W(t) |

**Language map.** Moving projector -> instantaneous ground state of a slowly turning field; following -> adiabatic
following; horizontal generator -> the rotation that carries the frame along with the field.

**Lab frame and rotating frame.**

| Quantity | Lab frame | Rotating frame | Relation |
| --- | --- | --- | --- |
| state | psi(t) | Xi(t) | Xi = W^dagger psi |
| field direction | n(t), turns about y | z, fixed | n(t) . sigma = W sigma_z W^dagger |
| Hamiltonian | H(t) = -(Delta/2) n(t) . sigma | K = -(1/2)(Delta sigma_z + nu sigma_y), constant | K = W^dagger H W - i W^dagger dW/dt |
| effective field | along n(t) | in the y-z plane: Delta along z plus nu along y | the frame motion adds nu along y |
| ground state | along n(t) | spin up along z | W maps up to the ground state |
| excited state | opposite to n(t) | spin down along z | P_ex = abs(<down\|Xi>)^2 |

**Steps and hints.**

1. Compute W^dagger H W. Hint: W rotates about y by the angle nu t.
2. Compute -i W^dagger dW/dt. Hint: W is an exponential of a constant matrix times t.
3. Solve i dXi/dt = K Xi from spin up. Hint: K is constant; use the Pauli exponential of "Useful information".
4. Find the probability of spin down in the rotating frame. Hint: which state of the rotating frame is the
   instantaneous excited state?
5. Explain the role of Delta. Hint: compare nu/Delta small and large.

**Sanity checks.** nu -> 0: P_ex -> 0 (an infinitely slow turn is followed exactly). Delta -> 0: P_ex = sin^2(nu
t/2) (no field; the state stays at rest while n(t) turns away). Units: Delta and nu are both frequencies (hbar = 1).
Small case: Delta = nu gives a largest P_ex of exactly one half.

**Misreadings.** "In the rotating frame the field is along z": no, the frame motion adds -(nu/2) sigma_y.
"P_ex grows like t^2 at first, so it keeps growing": no, it oscillates with angular frequency
sqrt(Delta^2 + nu^2) and returns to zero.

**Research step.** Projector -> following frame (chain of objects, D). Open beyond the booklet: in the real
pump the following of one flavor needs a gap that the composite bands do not provide (O-theory).
