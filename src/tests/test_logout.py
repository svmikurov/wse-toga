"""Test logout."""

import json
import os
import tempfile
from unittest.mock import MagicMock, Mock, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from tests.test_login import USER_DATA
from tests.utils import run_until_complete
from wse.app import WSE
from wse.constants import HOST_API
from wse.contrib import http_requests
from wse.pages import MainBox
from wse.source import user


@pytest.fixture
def box_main(wse: WSE) -> MainBox:
    """Return main box-container."""
    return wse.box_main


@patch('httpx.Client.post', return_value=Mock(status_code=204))
def test_logout(
    post: MagicMock,
    box_main: MainBox,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test login."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path_userdata = os.path.join(tmpdir, 'userdata.json')
        path_token = os.path.join(tmpdir, 'token.txt')

        # Mock paths.
        monkeypatch.setattr(user, 'PATH_USERDATA_FILE', path_userdata)
        monkeypatch.setattr(http_requests, 'PATH_TOKEN_FILE', path_token)

        # Save files.
        with open(path_userdata, 'w', encoding='utf-8') as fp:
            json.dump(USER_DATA, fp, ensure_ascii=False)
        with open(path_token, 'w') as fp:
            fp.write('token')

        # Set widgets and user source.
        wse.main_window.content = wse.box_main
        wse.source_user._username = 'name'
        wse.source_user._is_auth = True
        box_main.update_widgets()

        box_main.btn_logout._impl.simulate_press()

        run_until_complete(wse)

        post.assert_called_once_with(
            url='http://127.0.0.1/auth/token/logout/', json=None
        )

        assert box_main.info_panel.value == f'Ready for connect to {HOST_API}'
