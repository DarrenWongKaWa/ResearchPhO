# Proposal mode

Use this when the input is a research proposal (or a project plan) rather than finished papers. The aim is to
learn what the proposal needs and to see, question by question, which steps can be done now.

## Steps

1. **Target.** Rewrite the proposal's goal as one measurable sentence. Example: "predict when the original
   interacting pump leaves a charge tolerance of 0.005 per period, and the process that controls it".
2. **Chain of objects** with S/P/D/O labels (see question design). The O arrows are the research.
3. **Tools that exist now.** For each D arrow, one exact question (identity, toy model, bound). These teach the
   methods the proposal will use.
4. **Conditional result.** One question that shows how the final answer would follow *if* the open inputs were
   given (worked example: 3.B.1 turns assumed growth bounds into a certified operating time). State the assumed
   inputs plainly ("Assume that ...") and call the numbers "illustrative inputs"; their status goes to Appendix B.
5. **Decision rule.** One question with error bars and three outcomes: certified pass, certified fail,
   undetermined (worked example: 3.C.1 in the public example).
6. **Synthesis question** (last part of problem 3). "List the inputs that must be derived from the model and a specified initial state
   before the tests can be applied. Why does certifying individual windows not, by itself, locate the first
   failure?" Mark it on fixed items.
7. **Register** (Appendix C of the solutions): a table "item - available now - still missing". Keep it out of the
   question paper: it answers the synthesis question.

## Output for a proposal review

Besides the booklets, give the author a one-page summary: the chain with labels, the open arrows ranked by how much
of the target depends on them, and for each open arrow the smallest calculation that would close it.

## Guardrails

- Do not turn an assumed bound into a result: invented numbers are called illustrative in the text, never in a
  title that could leak the answer.
- A solved toy model is not evidence for the real system; say so in Appendix B.
- A certified lower bound is not a prediction of the failure time; ask the reader to state this distinction.
