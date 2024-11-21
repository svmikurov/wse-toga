"""Test Login widgets."""

import os
import tempfile
from unittest.mock import MagicMock, Mock, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from tests.utils import run_until_complete
from wse.app import WSE
from wse.contrib import http_requests
from wse.handlers.goto_handler import goto_login_handler
from wse.pages import LoginBox, MainBox
from wse.source import user

WIDGET_COUNT = 5
"""Widget count at testing box container (int).
"""


@pytest.fixture(autouse=True)
def move_login_page(wse: WSE) -> None:
    """Assign the login box to main window content, fixture."""
    wse.main_window.content = wse.box_login


@pytest.fixture
def box_login(wse: WSE) -> LoginBox:
    """Return log in box-container."""
    return wse.box_login


@pytest.fixture
def box_main(wse: WSE) -> MainBox:
    """Return main box-container."""
    return wse.box_main


def test_widget_count(box_login: LoginBox) -> None:
    """Test of widget count."""
    assert WIDGET_COUNT == len(box_login.children)


def test_title(box_login: LoginBox) -> None:
    """Test widgets at login box-container."""
    assert box_login.label_title.text == 'Вход в учетную запись'
    assert box_login.input_username.placeholder == 'Имя'
    assert box_login.input_password.placeholder == 'Пароль'
    assert box_login.btn_login.text == 'Войти в учетную запись'
    assert box_login.btn_login.on_press._raw == box_login.login_handler
    assert box_login.btn_goto_main.text == 'На главную'


def test_main_box_btns(box_main: MainBox) -> None:
    """Test the auth button at main box-container."""
    assert box_main.btn_goto_login.text == 'Вход в учетную запись'
    assert box_main.btn_goto_login.on_press._raw == goto_login_handler
    assert box_main.btn_logout.text == 'Выйти из учетной записи'
    assert box_main.btn_logout.on_press._raw == box_main.logout_handler


RESPONSE_AUTH_POST = Mock(
    name='Response',
    status_code=200,
    json=Mock(return_value={'auth_token': 'token'}),
)
RESPONSE_AUTH_GET = Mock(
    name='Response',
    status_code=200,
    json=Mock(return_value={'id': 1, 'username': 'name', 'email': 'email'}),
)


@patch('httpx.Client.post', return_value=RESPONSE_AUTH_POST)
@patch('httpx.Client.get', return_value=RESPONSE_AUTH_GET)
def test_login(
    get: MagicMock,
    post: MagicMock,
    box_login: LoginBox,
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

        # Main box-container include button to log in.
        assert wse.box_main.btn_goto_login in wse.box_main.children
        assert wse.box_main.btn_logout not in wse.box_main.children

        # Input username and password.
        box_login.input_username.value = 'name'
        box_login.input_password.value = 'password'

        # Press the login button.
        box_login.btn_login._impl.simulate_press()

        # Run a fake main loop.
        run_until_complete(wse)

        # Assert request the token.
        post.assert_called_once_with(
            'http://127.0.0.1/auth/token/login/',
            json={'username': 'name', 'password': 'password'},
        )
        # Assert request the user data.
        get.assert_called_once_with('http://127.0.0.1/api/v1/auth/users/me/')

        # Main window content has been changed.
        assert wse.main_window.content is wse.box_main

        # Main box-container include button to log out.
        assert wse.box_main.btn_logout in wse.box_main.children
        assert wse.box_main.btn_goto_login not in wse.box_main.children

        # The user data has been updated.
        assert wse.source_user.is_auth is True
        assert wse.source_user.username == 'name'

        # The main information panel contains user greetings.
        assert wse.box_main.info_panel.value == 'Добро пожаловать, name!'

        # The username and password input fields have been cleared.
        assert box_login.input_username.value == ''
        assert box_login.input_password.value == ''
