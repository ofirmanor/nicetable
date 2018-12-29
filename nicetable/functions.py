from typing import Any


def coalesce(*args: Any) -> Any:
    """ Return the first non-None argument."""
    return next((x for x in args if x is not None), None)


def non_printable_to_space(s: str) -> str:
    """ Return the input string, with non-printable characters replaced with a space (Unicode-friendly) """
    return s  # TODO implement and double-check
