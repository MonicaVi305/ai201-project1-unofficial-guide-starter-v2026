# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
The corpus is small and some facts appear in only one or two documents, so
occasional misses are expected. Requiring 4 of 5 balances being strict enough
to catch systematic retrieval failures while allowing for one hard or ambiguous
query where the exact answer may not be present in any single chunk.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Source attribution is essential for trust and grading; the pipeline already
attaches document identifiers to retrieved chunks, so naming at least one
source for every answer is achievable. Failing to name a source indicates a
bug in the retrieval→generation handoff rather than a borderline relevance
decision, so we require it for all answers.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
We observed a modest separation between in-corpus and out-of-corpus distances
but some overlap at the margin. A 4-of-5 target tests the gate's robustness:
it must reject most clearly out-of-scope questions while tolerating occasional
borderline cases caused by semantically similar phrasing or noisy embeddings.

---

## 4. Chunk quality — complete thoughts

For at least 4 of 5 sampled chunks, the chunk text begins and ends at sentence
boundaries and is at least 200 characters long (so it reads as a complete
thought rather than a heading fragment).

**Why this target:**
In Milestone 3 sampling showed short fragments and cut-off sentences reduced
answer quality. Requiring 4 of 5 chunks to be full sentences and length >=200
chars ensures chunks are likely to contain meaningful context while allowing
one problematic sample.

---

## 5. Cited sources contain the answer

For at least 4 of my 5 test questions, the source document(s) named in the
system's answer actually contain the information used to produce that answer
(i.e., the cited document includes the supporting sentence or fact).

**Why this target:**
Correct attribution is more than naming a document; the cited source must
actually contain the supporting evidence. Checking 4 of 5 verifies that
attribution is reliable while allowing for one edge case caused by noisy
retrieval or borderline citations.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
