# The Unofficial Guide

Monica — corpus: campus_life

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

**Chunk size:** 800 characters (maximum — most chunks land well under this)
**Overlap:** none

88 chunks total, average 315 characters, shortest 176, longest 545.

The starter's fixed 800-character window barely touched this corpus — almost
every post in `campus_life` is well under 800 characters, so it came out as
88 documents and 88 chunks with no real splitting happening. The actual
problem wasn't size, it was structure: a handful of posts pack more than one
distinct thought into a single file (a Q&A reply plus an aside, for example),
and a fixed-size cut has no way to know that.

I replaced it with a sentence-aware chunker (`chunker.py::split_documents`)
that builds chunks out of whole sentences, capped at 800 characters, and
merges any leftover piece under 200 characters into a neighboring chunk so
nothing ships as a bare fragment. Because it only ever cuts on a sentence
boundary — never mid-thought — there's no need for character overlap between
neighboring chunks the way a fixed-size window needs it: nothing gets sliced
in half in the first place, so there's nothing for overlap to stitch back
together.

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

**3. (Unit 2)** I used Claude Code to help audit this unit's eval before I treated any of it as evidence. It caught two things I would have graded past: the vector index (`chroma_db/`) was still built from before my sentence-aware chunking fix, so an earlier eval run had silently scored the old, fragmented chunker instead of the current one — and a hand-built criteria table I'd started (`results/scorer.py`) had numbers that didn't match a fresh read of the actual retrieved chunks. After I rebuilt the index and reran the eval, I had it lay out the real per-criterion numbers and distance margins — not decide MET/MISSED, which I did myself — and that margin data is what pointed Milestone 3's diagnosis at the gate threshold as the one criterion worth tightening. It also wrote the real `scorer.py::judge()` function once I confirmed I wanted it built, and flagged the false negative it produces on the parking-permits question.

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
 
Data below is copied from `results/run_2026-09-27_1402.md` (7 in-scope questions, 5 out-of-scope), run against the rebuilt index. 

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 6/7 | 6/7 | 6/7 |MET |
| 2. Every answer names a source | 5 of 5 | 7/7 | 7/7 | 7/7 | MET|
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 |MET |
| 4. Chunk quality — complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 |MET |
| 5. Cited sources contain the answer | 4 of 5 | 7/7 | 7/7 | 7/7 | MET|

Note on row 1: the one `judge()`-marked fail is the parking-permits question — its
answer is complete and correct but never uses the literal phrase "parking permits"
(it says "permits"), so the keyword-match scorer misses it. Worth deciding yourself
whether that's a real miss or a scorer artifact.

The evidence came from the retrieval checks: in-corpus questions returned best distances from 0.170 to 0.294, while out-of-scope questions stayed from 0.825 to 0.934. That clean separation is what makes the 0.6 cutoff workable and keeps the gate from letting unrelated questions through.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | 6 of 7 in-corpus questions passed the keyword-match scorer across all three runs. The seventh (parking permits) I checked by hand: the retrieved chunk and the answer built from it were both complete and correct, just phrased as "permits" instead of the literal "parking permits" the scorer looks for — a scorer wording issue, not a retrieval miss, so I'm counting all 7 as met. |
| 2 | Every answer names a source | MET | Every one of the 21 runs (7 questions × 3 runs) named a source document inline in the answer text — confirmed by scanning the run log for a cited filename in each. |
| 3 | The relevance gate stops out-of-corpus questions | MET | All five out-of-scope questions had best distances between 0.825 and 0.934, while every in-corpus question stayed between 0.170 and 0.294. That's a wide gap either side of the 0.6 cutoff, so this isn't a close call. |
| 4 | Chunk quality — complete thoughts | MET | Sampled the top-ranked retrieved chunk for 5 questions after rebuilding the index: all 5 were at least 200 characters and began and ended on sentence boundaries. The sentence-aware chunker now merges each document's title line into the paragraph that follows instead of leaving it as its own short fragment. |
| 5 | Cited sources contain the answer | MET | Checked all 7 cited source files against the specific claim each answer attributed to them, by searching the source document text directly. Every citation held up — no hallucinated or mismatched sources in any of the 21 runs. |

## Diagnoses

No criterion was missed against the rebuilt-index run (see Run Log — Before / Verdicts above), so there's nothing to trace back to a pipeline stage. That's a result worth being skeptical of rather than treating as a clean bill of health — a system that clears every target on the first try usually means the targets were safe, not that the system is excellent.

Looking at the margins instead of just the pass/fail:

- **Criterion 3 (gate)** cleared its 4-of-5 target at 5 of 5, and the underlying numbers show why it wasn't close: in-corpus distances ran 0.170–0.294 and out-of-scope distances ran 0.825–0.934, a gap of more than 0.5 with nothing near the 0.6 cutoff on either side. A 4-of-5 tolerance was set before I had real distance data to calibrate against; with a gap this wide, **this is the criterion I'd tighten, to 5 of 5.**
- **Criterion 1 (retrieval contains the answer)** cleared 6 of 7 even under a scorer that penalizes exact wording — the seventh, checked by hand, was also correct, just phrased differently than the keyword match expected. The true pass rate is 7 of 7, which suggests this target also had slack, though I'd want a less brittle scorer before tightening it.
- **Criteria 2, 4, and 5** cleared at 7/7, 5/5, and 7/7 respectively, with no borderline cases in the chunks or citations I inspected — nothing here forced a close call.

The one genuine risk this run surfaced wasn't a criterion at all: the vector index had gone stale relative to the chunker (built before the sentence-aware chunking fix landed), so an earlier eval pass was silently scoring the old chunker's output. That's a process gap — rebuilding the index isn't automatic after a chunker change — worth a note for future units rather than a chunk-fragmentation fix, since the fragmentation itself turned out to already be fixed.

## The Improvement

**What I changed:** Lowered `config.THRESHOLD` from 0.6 to 0.5 (`config.py`).

**Why I picked it:** Milestone 3's diagnosis found criterion 3 (the gate) cleared its 4-of-5 target with the widest margin of any criterion — in-corpus distances topped out at 0.294 and out-of-scope distances started at 0.825, leaving 0.6 sitting in the middle of a gap over 0.5 wide. That's the criterion the diagnosis actually pointed at tightening, so I moved the cutoff to 0.5: still comfortably above every in-corpus distance I have, but meaningfully less permissive toward a future out-of-scope question that lands closer to the corpus than these five examples did.

### Run Log — After

Data from `results/run_2026-09-27_1519_after.md`, same 7 in-corpus / 5 out-of-scope questions, `THRESHOLD = 0.5`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 6/7 | 6/7 | 6/7 | MET |
| 2. Every answer names a source | 5 of 5 | 7/7 | 7/7 | 7/7 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk quality — complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Cited sources contain the answer | 4 of 5 | 7/7 | 7/7 | 7/7 | MET |

**Did it help?** Not measurably, on this test set — and I want to be honest about that rather than dress it up. Every distance came out identical to the before run (retrieval doesn't depend on the threshold), and since the closest in-corpus question (0.294) and the closest out-of-scope question (0.825) were both already far from 0.6, moving the cutoff to 0.5 didn't flip a single verdict. What it did do is remove slack from the gate for cases this test set doesn't cover — a future out-of-scope question landing between 0.5 and 0.6 would now correctly get refused instead of let through. That's a real improvement to the gate's robustness, just not one these five out-of-scope questions were positioned to demonstrate. A more honest test of this change would need out-of-scope questions deliberately chosen to sit closer to the corpus.

## What's Still Broken

No criterion is currently missed, but two things are genuinely unresolved, not just tidy:

- **`scorer.py`'s `judge()` is a brittle keyword-substring check.** It produced a false negative on the parking-permits question — a fully correct answer that said "permits" instead of the literal "parking permits" — and I have no reason to think that's the only phrasing it'll ever misjudge. I didn't fix this here because this unit's time went into finding the stale-index bug and testing the threshold change instead; a better scorer (checking for the underlying fact rather than exact wording) is its own piece of work.
- **The Milestone 4 threshold change (0.6 → 0.5) is unverified against anything that actually tests it.** None of my five out-of-scope questions land between 0.5 and 0.6 — they're all comfortably above 0.8 — so I can't yet point to a real question this change caught that the old threshold would have let through. I stopped here rather than construct an artificial near-boundary question, because a made-up example proves less than a real one and I'd rather flag the gap honestly than fake the evidence for it.

## What I'd Do Differently

Two of my five criteria, in hindsight, were written before I had real distance data to calibrate against:

- **Criterion 3 (the gate)** should have targeted 5 of 5, not 4 of 5. A margin this wide (0.294 vs. 0.825) means the 4-of-5 tolerance was never actually being tested — it just never got the chance to matter.
- **Criterion 1 (retrieved chunk contains the answer)**, as written, is scored by a literal keyword match against `expects`, which is too strict a proxy for "the answer is correct." I'd rewrite it to judge whether the retrieved chunk supports the actual fact asked for, not whether one specific phrase shows up verbatim — or pick `expects` phrases I'm certain any correct answer would restate exactly. 
