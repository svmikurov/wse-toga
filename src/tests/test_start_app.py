"""Tests of start app.

Testing:
 * that the main window will exist, and has content;
 * that the WSE app has specific box-container attrs;
 * that specific methods has been invoked on start app.

.. todo::

   * add test that start app with error;
   * add test that wse app has menu with specific commands;
   * add test of handlers of menu command.

"""

from asyncio import AbstractEventLoop
from unittest.mock import MagicMock, patch

from wse.app import WSE
from wse.page.user import UserAuth


@patch('httpx.Client.get')
def test_main_window(
    get: MagicMock,
    event_loop: AbstractEventLoop,
) -> None:
    """Test that main window will exist, and has content.

    Mock:
    * ``get`` method of httpx.Client, otherwise http request.
    """
    app = WSE(formal_name='Test App', app_id='org.example.test')

    # The main window will exist, and has content.
    assert app.main_window.content == app.box_main


@patch.object(UserAuth, 'refresh_user_auth_status')
@patch.object(UserAuth, 'update_widget_values')
def test_invoke_methods_on_startup(
    refresh_user_auth_status: MagicMock,
    update_widget_values: MagicMock,
) -> None:
    """Test that specific methods has been invoked on start app."""
    # Initializing the app.
    WSE(formal_name='Test App', app_id='org.example.test')

    # Methods has been invoked on start app.
    refresh_user_auth_status.assert_called_once()
    update_widget_values.assert_called_once()


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
