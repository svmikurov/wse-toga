"""Application utils."""


def to_entries(items: list[dict]) -> list[tuple[str, ...]]:
    """Convert http response data to app source data.

    For example:

    >>> from wse.contrib.utils import to_entries
    >>> http_response_data = [
    ...     {'id': 6, 'name': 'apple', 'color': 'green'},
    ...     {'id': 7, 'name': 'tomato', 'color': 'red'},
    ... ]
    >>> to_entries(http_response_data)
    [('6', 'apple', 'green'), ('7', 'tomato', 'red')]
    """
    return [tuple(map(str, d.values())) for d in items]
