"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # {"question": "...", "expects": "..."},
    {"question": "What are the deadlines for adding or dropping a course, and what happens if a student drops the course after the second week?","expects": "week"},
    {"question": "How does choosing a work-study job versus a regular campus job affect your financial aid eligibility?","expects": "financial aid"},
    {"question": "Do dining dollars roll over from the fall semester to the spring, and what happens to any remaining balance at the end of spring?","expects": "semester"},
    {"question": "What is the process and deadline for appealing a grade, and do you have to contact the instructor before going to the department?","expects": "grade appeal"},
    {"question": "What are the graduation requirements, including the writing-intensive requirement, and when should students check that they have completed them?","expects": "requirements"},
    {"question": "Can students change their meal plan, and what happens when they downgrade or upgrade it?","expects": "meal plan"},
    {"question": "When do student parking permits go on sale, which lots tend to sell out, and what options are available if students miss the sales window?","expects": "parking permits"},
]

OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
