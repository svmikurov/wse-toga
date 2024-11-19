"""Test invoke the user methods.

Test:
 * the refresh user authentication status;
 * the update widgets value with user auth status.

.. todo::

   Add tests:
    * save and delete the token;
    * auth_attrs property;
    * login;
    * logout;
    * widgets and handlers of login box;
    * display a messages.
"""

from unittest.mock import MagicMock, Mock, patch, AsyncMock, call
from urllib.parse import urljoin

import pytest
from toga.handlers import simple_handler, wrapped_handler

from tests.utils import FixtureReader, run_until_complete
from wse.app import WSE
from wse.constants import HOST_API
from wse.general.goto_handler import goto_login_handler
from wse.page.user import UserAuthMixin, Credentials

REQUEST_ARGS = call(
    urljoin(HOST_API, '/auth/token/login/'),
    json={'username': 'user name', 'password': 'password'},
)
FIXTURE = 'user_detail.json'
PARAMS = FixtureReader(FIXTURE).json()
RESPONSE_AUTH = Mock(
    name='Response',
    status_code=200,
    json=Mock(return_value=PARAMS),
)
RESPONSE_UNAUTH = Mock(
    name='Response',
    status_code=401,
    json=Mock(return_value={'detail': ''}),
)


@pytest.mark.parametrize(
    'response, username, is_auth',
    [
        (RESPONSE_AUTH, 'user name', True),
        (RESPONSE_UNAUTH, None, False),
    ],
)
@patch('httpx.Client.get')
def test_refresh_user_auth_status(
    request: MagicMock,
    response: dict,
    username: str,
    is_auth: bool,
    wse: WSE,
) -> None:
    """Test a refresh user authentication status.

    Test:
     * that http request method has been invoked;
     * the refreshing the authentication data.
    """
    user_detail_url = urljoin(HOST_API, '/api/v1/auth/users/me/')

    # Set response to mock of request.
    request.return_value = response

    def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method to invoke."""
        wse.box_main.refresh_user_auth_status()

    wrapped = simple_handler(handler)

    # Invoke the handler as if it were a method handler (i.e., with the
    # extra "widget" argument)
    wrapped('widget')

    # Http request method has been invoked once.
    request.assert_called_once_with(url=user_detail_url)

    # Assert about refreshing the authentication data.
    assert wse.box_main._username == username
    assert wse.box_main._is_auth is is_auth


@pytest.mark.parametrize(
    'username, is_auth, btn_text, btn_handler, info_text',
    [
        (
            'user name',
            True,
            'Выход из учетной записи',
            UserAuthMixin.logout_handler,
            'Добро пожаловать, user name!',
        ),
        (
            None,
            False,
            'Вход в учетную запись',
            goto_login_handler,
            'Ready for connect to http://127.0.0.1/',
        ),
    ],
)
def test_update_widgets(
    username: str,
    is_auth: bool,
    btn_text: str,
    btn_handler: str,
    info_text: str,
    wse: WSE,
) -> None:
    """Test the update widgets value with user auth status.

    Test:
     * the text of authentication button and info panel;
     * that the text of authentication button has been updated;
     * that the info panel has been updated.

    .. todo:

       * Fix AssertionError of test that handler of authentication
         button has been updated.
    """
    box = wse.box_main
    box.set_username(username)
    box._is_auth = is_auth

    def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method to invoke."""
        box.update_widgets()

    wrapped = simple_handler(handler)

    # Invoke the handler as if it were a method handler (i.e., with the
    # extra "widget" argument)
    wrapped('widget')

    # The text of authentication button has been updated.
    assert box.btn_goto_login.text == btn_text

    # The handler of authentication button has been updated.
    # TODO: Fix AssertionError  # noqa: TD003, TD002
    # assert logout_handler is
    # <function UserAuthMixin.logout_handler at 0x7af62bf66cb0>
    # assert box.btn_goto_login.on_press._raw is btn_handler

    # The info panel has been updated.
    assert box.info_panel.value == info_text


def test_btn_login_callback_assign(wse: WSE) -> None:
    """Test the assign of callback to a button."""
    button = wse.box_login.btn_login
    assert button.on_press._raw == wse.box_login.login_handler


@pytest.mark.parametrize(
    'username, password, was_awaited, request_args',
    [
        ('user name', None, False, None),
        (None, 'password', False, None),
        ('user name', 'password', True, REQUEST_ARGS),
    ]
)
@patch('httpx.AsyncClient.post', new_callable=AsyncMock)
@patch.object(Credentials, '_show_response_message')
@patch.object(Credentials, 'success_handler')
def test_login_handler(
    success_handler: AsyncMock,
    _show_response_message: MagicMock,
    response: AsyncMock,
    username: str | None,
    password: str | None,
    was_awaited: bool,
    request_args,
    wse: WSE,
) -> None:
    """Test a log in handler.

    Mock:
     * ``httpx.AsyncClient.post``, to set response;
     * ``_show_response_message`` method of ``Credentials``,
       otherwise RuntimeError.
     * ``success_handler`` method of ``Credentials`` to was awaited.
    """
    wse.main_window.content = wse.box_login
    button = wse.box_login.btn_login

    # Mock http response.
    response.return_value = RESPONSE_AUTH

    # Input credentials to login fields.
    wse.box_login.input_username.value = username
    wse.box_login.input_password.value = password

    # Invoke the callback.
    button._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    # Http request awaited if credentials has been input.
    assert response.await_count == was_awaited

    # The handler of success login was awaited.
    assert success_handler.await_count == was_awaited

    # Http request call args.
    assert response.call_args == request_args


def test_success_handler(wse: WSE) -> None:
    """Test the handler of success login."""
    box_login = wse.box_login
    button = box_login.btn_login
    wse.main_window.content = wse.box_login

    async def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method."""
        await wse.box_login.success_handler(*args, **kwargs)

    wrapped = simple_handler(handler, button, RESPONSE_AUTH)

    # Invoke the handler.
    wse.loop.run_until_complete(wrapped(RESPONSE_AUTH))

    # Set the username for greetings.
    assert wse.box_main._username == RESPONSE_AUTH.json()['username']

    # Clear the fields with user credentials.
    assert not box_login.input_username.value
    assert not box_login.input_password.value

    # Switch to main page.
    assert wse.main_window.content == wse.box_main
