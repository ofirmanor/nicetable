from typing import Any


def coalesce(*args: Any) -> Any:
    """ Return the first non-None argument."""
    return next((x for x in args if x is not None), None)
