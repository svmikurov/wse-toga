"""Test the request the auth."""

import os
import tempfile
from http import HTTPStatus
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.parse import urljoin

import httpx
from _pytest.monkeypatch import MonkeyPatch
from toga.handlers import simple_handler

from wse.app import WSE
from wse.constants import HOST_API
from wse.contrib.http_requests import AppAuth, app_auth, obtain_token

URL_OBTAIN_TOKEN = urljoin(HOST_API, '/auth/token/login/')
URL_ME = urljoin(HOST_API, '/api/v1/auth/users/me/')
TOKEN = 'token12321'
CREDENTIALS = {
    'username': 'name',
    'password': 'password',
}
RESPONSE = httpx.Response(HTTPStatus.OK, json={'auth_token': 'token123333'})

path_src = Path(__file__).parent.parent
path_token = os.path.join(path_src, 'wse/resources/')


@patch('httpx.Client.post', return_value=RESPONSE)
def test_obtain_token(
    post: MagicMock,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test obtain the user auth token.

    Mock:
     * ``httpx.Client.post`` to set response;
     * temp dir to save token.

    Test:
     * that token request was called with attrs;
     * that token has been saved.
    """
    with tempfile.TemporaryDirectory(dir=path_token) as tmpdir:
        path_temp_token = os.path.join(tmpdir, 'token.txt')
        monkeypatch.setattr(AppAuth, 'token_path', path_temp_token)

        def handler(*args: object, **kwargs: object) -> httpx.Response:
            """Set the testing func."""
            return obtain_token(*args, **kwargs)

        wrapped = simple_handler(handler, CREDENTIALS)

        # Invoke the token request.
        wrapped(CREDENTIALS)

        # The token request was called with attrs.
        post.assert_called_once_with(URL_OBTAIN_TOKEN, json=CREDENTIALS)

        # The token has been saved.
        assert os.path.isfile(path_temp_token)


@patch('httpx.Client')
def test_request_with_token(
    mock_client: MagicMock,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the request with saved token.

    Mock:
     * ``httpx.Client``;
     * path to token file.

    Test:
     * that token can be setts;
     * that token was saved to the file;
     * that token is stored as an attribute;
     * that http request is called with a token.
    """
    with tempfile.TemporaryDirectory(dir=path_token) as tmpdir:
        path_temp_token = os.path.join(tmpdir, 'token.txt')
        # Mock the token file path.
        monkeypatch.setattr(AppAuth, 'token_path', path_temp_token)

        # The token can be setts.
        app_auth.token = TOKEN

        # The token was saved to the file.
        assert os.path.exists(path_temp_token)

        # The token is stored as an attribute.
        assert app_auth.token == TOKEN

        # The HTTP request contains a token.
        with httpx.Client(auth=app_auth) as client:
            client.get(URL_ME)

            # The http request is called with a token.
            assert mock_client.call_args.kwargs['auth'].token == TOKEN
