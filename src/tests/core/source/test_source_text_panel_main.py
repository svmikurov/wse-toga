"""Unit tests of source info text panel at main page."""

from wse.app import WSE
from wse.constants import HOST_API


def test_display_on_start_app() -> None:
    """Test the text display on start app, source_user not auth."""
    welcome = f'Ready for connect to {HOST_API}'

    # Create app instance on start app.
    wse = WSE(formal_name='Test app', app_id='com.com')

    # Info panel text for not auth source_user.
    assert wse.box_main.info_panel.value == welcome
