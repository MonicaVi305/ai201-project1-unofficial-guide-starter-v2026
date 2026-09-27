"""
Milestone 2's scoring rule.

`judge(question, expects, answer, results) -> bool` decides whether one run's
answer counts as correct. `run_eval.py` finds this file automatically and,
once it exists, fills the Run columns of your run log with its verdicts
instead of leaving them blank.

The rule: an answer is correct if the gate didn't refuse it and the answer
text mentions the phrase you wrote down in `expects` when you set the
question up in questions.py, before you'd seen any results.
"""

from gate import REFUSAL


def judge(question: str, expects: str, answer: str, results) -> bool:
    if answer.strip() == REFUSAL:
        return False
    if not expects:
        return True
    return expects.lower() in answer.lower()
