"""Unit tests of source info text panel at main page."""

import pytest


@pytest.fixture
def source() ->  TextPanelMain:
    """Return the info text panel instance, fixture."""
    return TextPanelMain()
