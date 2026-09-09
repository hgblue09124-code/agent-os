"""Module Contract facet.

Protocol only in PR-01. Implementation belongs to PR-02.
"""

BOUNDARY = "module.contract"
IMPLEMENTED = False

CONTRACT_QUESTIONS: tuple[str, ...] = (
    "what_is_the_module",
    "identity",
    "capability",
    "input",
    "output",
    "lifecycle",
    "dependencies",
    "verification",
)
