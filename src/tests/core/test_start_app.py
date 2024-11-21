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
import os
import tempfile
from asyncio import AbstractEventLoop
from pathlib import Path
from unittest import skip
from unittest.mock import MagicMock, patch

import httpx
from _pytest.monkeypatch import MonkeyPatch

from tests.test_user_auth_request import URL_ME
from wse.app import WSE
from wse.contrib.http_requests import AppAuth, app_auth, request_user_data

PATH_SRC = Path(__file__).parent.parent.parent
PATH_TOKEN = os.path.join(PATH_SRC, 'wse/resources/')


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


@patch('httpx.Client')
def test_request_token_exist(
    mock_client: MagicMock,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the request with saved token."""
    test_token = 'token543'

    with tempfile.TemporaryDirectory(dir=PATH_TOKEN) as tmpdir:
        path_test_token = os.path.join(tmpdir, 'token.txt')

        # Save token.
        with open(path_test_token, 'w') as save_token:
            save_token.write(test_token)

        # Mock the file path to reade token.
        monkeypatch.setattr(AppAuth, 'token_path', path_test_token)

        # The http request of user data.
        request_user_data()

        # The http request is called with a token.
        assert mock_client.call_args.kwargs['auth'].token == test_token


@skip
def test_invoke_methods_on_startup() -> None:
    """Test that specific methods has been invoked on start app."""
    # Initializing the app.
    WSE(formal_name='Test App', app_id='org.example.test')

    # Methods has been invoked on start app.
    ...
