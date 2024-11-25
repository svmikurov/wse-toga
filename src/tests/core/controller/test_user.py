"""Test of user controllers."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

from _pytest.monkeypatch import MonkeyPatch
from toga.handlers import simple_handler

from wse.app import WSE
from wse.contrib.http_requests import AppAuth
from wse.controller.user import (
    get_user,
    login,
)

RESPONSE_AUTH = Mock(
    status_code=200,
    json=Mock(return_value={'username': 'name', 'auth_token': 'token'}),
)
RESPONSE_UNAUTH = Mock(
    status_code=401,
    json=Mock(return_value={'detail': ''}),
)


def test_get_user(wse: WSE) -> None:
    """Test get user source instance."""
    widget = wse.box_main
    assert wse.source_user is get_user(widget)


@patch('httpx.Client.get')
@patch('httpx.Client.post', return_value=RESPONSE_AUTH)
def test_login(
    post: MagicMock,
    get: MagicMock,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the login.

    Mock:
     * http request to obtain token;
     * http request to get user data.

    Test:
     * that the http request arguments are as expected;
     * that window content was changed.
    """
    box = wse.box_login
    box_next = wse.box_main
    button = box.btn_submit
    credentials = {'username': 'name', 'password': 'pass'}
    path_src = Path(__file__).parent.parent.parent.parent
    path_token = os.path.join(path_src, 'wse/resources/')

    # Assign the box-container to window content.
    wse.app.main_window.content = box

    async def handler(*args: object, **kwargs: object) -> None:
        """Set testing method."""
        await login(*args, **kwargs)

    wrapped = simple_handler(handler, button, credentials)

    with tempfile.TemporaryDirectory(dir=path_token) as tmpdir:
        path_token_temp = os.path.join(tmpdir, 'token.txt')

        # Mock the token file path.
        monkeypatch.setattr(AppAuth, 'token_path', path_token_temp)

        # Invoke the handler, and run until it is complete.
        wse.loop.run_until_complete(wrapped('obj'))

        # Http request arguments are as expected.
        assert post.call_args == (
            call(
                'http://127.0.0.1/auth/token/login/',
                json={'username': 'name', 'password': 'pass'},
            )
        )
        assert get.call_args == call('http://127.0.0.1/api/v1/auth/users/me/')

        # The window content was changed.
        assert wse.main_window.content is box_next
