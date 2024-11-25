"""Test start app.

Testing:
 * that the main window will exist, and has content;
 * that the WSE app has specific sources;
 * that the WSE app has specific box-container attrs;
 * that request user data with saved token.

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
from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

from _pytest.monkeypatch import MonkeyPatch

from wse.app import WSE
from wse.constants import HOST_API
from wse.contrib.http_requests import AppAuth, request_user_data


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
def test_request_with_token(
    client: MagicMock,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test request user data with saved token."""
    test_token = 'token'
    path_src = Path(__file__).parent.parent.parent
    path_token = os.path.join(path_src, 'wse/resources/')
    # greetings = 'Добро пожаловать name!'

    with tempfile.TemporaryDirectory(dir=path_token) as tmpdir:
        path_token_temp = os.path.join(tmpdir, 'token.txt')

        # Save token.
        with open(path_token_temp, 'w') as save_token:
            save_token.write(test_token)

        # Mock the file path to reade token.
        monkeypatch.setattr(AppAuth, 'token_path', path_token_temp)

        # Invoke http request of user data.
        request_user_data()

        # The http request is called with a token.
        assert client.call_args.kwargs['auth'].token == test_token

        # The info panel has greetings.
        # assert wse.box_main.info_panel.value == greetings


@patch('httpx.Client.get')
def test_request_user_data(
    get: MagicMock,
) -> None:
    """Test request user data."""
    url = urljoin(HOST_API, '/api/v1/auth/users/me/')

    # Invoke http request of user data.
    request_user_data()

    # The http request is called with url.
    get.assert_called_once_with(url)
