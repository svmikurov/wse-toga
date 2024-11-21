"""Test start app.

Testing:
 * that the main window will exist, and has content;
 * that the WSE app has specific sources;
 * that the WSE app has specific box-container attrs.

.. todo::

   * that specific methods has been invoked on start app;
   * add test that start app with error;
   * add test that wse app has menu with specific commands;
   * add test of handlers of menu command.
"""

from asyncio import AbstractEventLoop
from unittest import skip
from unittest.mock import MagicMock, patch

from wse.app import WSE


@patch('httpx.Client.get')
def test_main_window(
    _: MagicMock,
    event_loop: AbstractEventLoop,
) -> None:
    """Test that main window will exist, and has content.

    Mock:
    * ``get`` method of httpx.Client, otherwise http request.
    """
    app = WSE(formal_name='Test App', app_id='org.example.test')

    # The main window will exist, and has content.
    assert app.main_window.content == app.box_main


def test_has_source(wse: WSE) -> None:
    """Test that WSE app has specific sources."""
    assert hasattr(wse, 'source_user')
    assert hasattr(wse, 'source_main_info_panel')


def test_has_page(wse: WSE) -> None:
    """Test that WSE app has specific box-container attrs."""
    assert hasattr(wse, 'box_main')
    assert hasattr(wse, 'box_foreign_main')
    assert hasattr(wse, 'box_foreign_params')
    assert hasattr(wse, 'box_foreign_exercise')
    assert hasattr(wse, 'box_foreign_create')
    assert hasattr(wse, 'box_foreign_update')
    assert hasattr(wse, 'box_foreign_list')
    assert hasattr(wse, 'box_glossary_main')
    assert hasattr(wse, 'box_glossary_params')
    assert hasattr(wse, 'box_glossary_exercise')
    assert hasattr(wse, 'box_glossary_create')
    assert hasattr(wse, 'box_glossary_update')
    assert hasattr(wse, 'box_glossary_list')
    assert hasattr(wse, 'box_login')


@skip
def test_invoke_methods_on_startup() -> None:
    """Test that specific methods has been invoked on start app."""
    # Initializing the app.
    WSE(formal_name='Test App', app_id='org.example.test')

    # Methods has been invoked on start app.
    ...
