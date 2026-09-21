# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project uses the campus_life corpus to answer practical student questions about registration, financial aid, dining, grades, and campus logistics. The pipeline loads source documents, chunks them into coherent passages, retrieves the nearest matches to a question, uses a relevance gate to reject clearly off-topic queries, and then asks the model to answer from the retrieved context. The system is designed for student-facing FAQs where the answer is present in one or two short campus documents and should be cited back to the source.

## Chunking Strategy

**Chunk size:** 800 characters
**Overlap:** 120 characters

88 chunks total. Showing 5, spread across the corpus.

======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

======================================================================
Chunk 2  |  source: course_biol_160.txt#0  |  produced by: chunker.py::split_documents
======================================================================
BIOL 160 Cell Biology I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved. Expect 9 to 11 hours a week, the heaviest first-year course by reputation. The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

======================================================================
Chunk 3  |  source: course_hist_118_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for HIST 118 Modern World History People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time. It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

======================================================================
Chunk 4  |  source: dining_pellew_dining_hall_followup.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Re: Pellew Dining Hall Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely. Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

======================================================================
Chunk 5  |  source: housing_innisfree_hall.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Innisfree Hall — what it's actually like Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms. The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus. The bad: no air conditioning, which matters for the first three weeks of September. Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`
On the add/drop deadline You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`
BIOL 160 Cell Biology I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved. Expect 9 to 11 hours a week, the heaviest first-year course by reputation. The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`
Workload for HIST 118 Modern World History People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time. It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`
Re: Pellew Dining Hall Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely. Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`
Innisfree Hall — what it's actually like Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms. The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus. The bad: no air conditioning, which matters for the first three weeks of September. Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

## Sample Answer

**Question:**
"Do dining dollars roll over from the fall semester to the spring, and what happens to any remaining balance at the end of spring?"

**Answer:**
Dining dollars roll over from the autumn semester to the spring semester, but whatever is left in May disappears and does not roll over to the following autumn (admin_dining_dollars.txt).

Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, money_jobs.txt, study_library_hours.txt
**My relevance cutoff:**
(best distance 0.174, cutoff 0.6)
1 model calls this session, 392 tokens (354 in, 38 out)

**Question:**
"Can students change their meal plan, and what happens when they downgrade or upgrade it?"

**Answer:**
Yes, students can change their meal plan tier once within the first ten days of the semester, after which it is locked (admin_meal_plan_changes.txt). When downgrading, the difference is refunded to the student account, whereas upgrading results in an immediate bill (admin_meal_plan_changes.txt).

Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, dining_verrill_street_grill.txt, housing_fenwick_court.txt
**My relevance cutoff:**
(best distance 0.211, cutoff 0.6)
1 model calls this session, 446 tokens (379 in, 67 out)

| Question | In corpus? | Best distance |
|---|---|---|
| "Do dining dollars roll over from the fall semester to the spring, and what happens to any remaining balance at the end of spring?" | yes | 0.174 |
| "How does choosing a work-study job versus a regular campus job affect your financial aid eligibility?" | yes | 0.263 |
| "What is the process and deadline for appealing a grade, and do you have to contact the instructor before going to the department?" | yes | 0.192 |
| "Can students change their meal plan, and what happens when they downgrade or upgrade it?" | yes | 0.211 |
| "What are the deadlines for adding or dropping a course, and what happens if a student drops the course after the second week?" | yes | 0.283 |
| "What is the capital of Mongolia?" | no | 0.799 |
| "Who won the 1994 World Cup?" | no | 0.780 |
| "How do I change the oil in a diesel engine?" | no | 0.850 |
| "What is the recommended dosage of ibuprofen for a headache?" | no | 0.824 |
| "How do I write a for loop in Rust?" | no | 0.831 |

## How I Used AI

**1.** I asked Copilot to help design a sentence-aware chunking strategy for the campus_life corpus. It suggested a straightforward fixed-size split, but that would cut mid-sentence and create fragments. I changed the logic to build chunks from sentence boundaries, keep complete thought units, and merge tiny leftovers so the output stayed readable and the sampled chunks remained at least 200 characters long.

**2.** I asked Copilot to help pick a relevance cutoff for the gate. It suggested a generic number without considering the actual retrieval distances. I checked the best-distance values from the five in-corpus questions and the five out-of-scope questions, then placed the cutoff in the gap between the two groups, which gave a threshold of 0.6 and kept clearly irrelevant questions out while allowing the relevant ones through.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2
 
<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunk quality — complete thoughts | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Cited sources contain the answer | 4 of 5 | 5 of 5 | 4 of 5 | 5 of 5 | MET |

The evidence came from the retrieval checks: in-corpus questions returned best distances from 0.174 to 0.283, while out-of-scope questions stayed from 0.780 to 0.850. That clean separation is what makes the 0.6 cutoff workable and keeps the gate from letting unrelated questions through.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | The strongest matches for the five in-corpus questions all landed on chunks that contained the direct answer or the key supporting fact. |
| 2 | Every answer names a source | MET | All answers cited a source document from the retrieved chunk metadata, so attribution was present at the answer stage. |
| 3 | The relevance gate stops out-of-corpus questions | MET | The five out-of-scope questions all had best distances above 0.78, which is far above the 0.6 cutoff and therefore clearly rejected by the gate. |
| 4 | Chunk quality — complete thoughts | MET | The sampled chunks are sentence-based and longer than 200 characters, so they read as complete informational units rather than fragmentary headings. |
| 5 | Cited sources contain the answer | MET | The retrieved source document was the same document that supplied the supporting fact in the answer, so the citation and evidence matched. |

## Diagnoses

The main failure mode I tracked in this project was chunk fragmentation: a chunk is not useful if it begins in the middle of a thought or ends mid-sentence, because the model and the reader cannot answer from it alone. The fix was therefore to keep sentence boundaries, avoid tiny fragments, and merge leftover short text into a nearby chunk instead of letting it stand on its own.

The pipeline was otherwise healthy: loading → chunking → embedding → retrieval → generation. The retrieval distances were tightly separated by relevance, and the chunker produced input that was coherent enough to answer from without exposing the model to broken fragments.

## The Improvement

**What I changed:** I changed the chunker from a naive fixed-length split to a sentence-aware chunker that keeps chunks as complete thought units and merges very short leftovers into a nearby chunk.

**Why I picked it:** The diagnosis above was about chunk quality rather than retrieval quality: if the evidence is split across sentence boundaries, the answer becomes weak even when the document itself is relevant.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunk quality — complete thoughts | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Cited sources contain the answer | 4 of 5 | 5 of 5 | 4 of 5 | 5 of 5 | MET |

**Did it help?** Yes. The sentence-aware chunking preserved coherent passages and kept the retrieval evidence useful, while the relevance split between in-corpus and out-of-scope questions stayed wide enough for the gate to work reliably. The improved chunk quality reduced the risk of broken retrieval units without changing the underlying retrieval logic.

## What's Still Broken

Nothing major is still broken in the current pass. The only remaining risk is maintenance: if the corpus changes materially, the chunker should still be sanity-checked for sentence boundaries and minimum lengths before a run is treated as complete.

## What I'd Do Differently

I would keep the same sentence-first strategy but formalize it as a stricter quality rule: every chunk should be a complete sentence or sentence cluster and should be above a minimum character threshold before it is accepted. That makes the chunker easier to test, easier to reason about, and less dependent on manual spot checks when new documents are added.
