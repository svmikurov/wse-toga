"""Application utils."""


def to_entries(items: list[dict]) -> list[tuple[str, ...]]:
    """Convert http response data to app source data."""
    return [tuple(map(str, d.values())) for d in items]
