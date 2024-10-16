"""Test convert http response data to Source Toga model."""

from wse.contrib.utils import to_entries

http_response_data = [
    {'id': 6, 'name': 'apple', 'color': 'green'},
    {'id': 7, 'name': 'tomato', 'color': 'red'},
]

source_data = [
    ('6', 'apple', 'green'),
    ('7', 'tomato', 'red'),
]


def test_to_entries() -> None:
    """Test to entries."""
    entries = to_entries(http_response_data)
    assert source_data == entries
