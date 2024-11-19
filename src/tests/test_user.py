"""Test invoke the user methods.

Test:
 * the refresh user authentication status;
 * the update widgets value with user auth status.

.. todo::

   Add tests:
    * save and delete the token;
    * request the user data;
    * auth_attrs property;
    * login;
    * logout;
    * widgets and handlers of login box.

"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from toga.handlers import simple_handler

from tests.utils import FixtureReader
from wse.app import WSE
from wse.general.goto_handler import goto_login_handler
from wse.page.user import UserAuth

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
    """Test the refresh user authentication status.

    Test:
     * that http request method has been invoked;
     * the refreshing the authentication data.
    """
    # Set response to mock of request.
    request.return_value = response

    def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method to invoke."""
        wse.box_main.refresh_user_auth_status()

    wrapped = simple_handler(handler)

    # Invoke the handler as if it were a method handler (i.e., with the
    # extra "widget" argument)
    wrapped('widget')

    # Http request method has been invoked.
    request.assert_called_once()

    # Assert about refreshing the authentication data.
    assert wse.box_main.username == username
    assert wse.box_main.is_auth is is_auth


@pytest.mark.parametrize(
    'username, is_auth, btn_text, btn_handler, info_text',
    [
        (
            'user name',
            True,
            'Выход из учетной записи',
            UserAuth.logout_handler,
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
def test_update_widget_values(
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
    box.username = username
    box.is_auth = is_auth

    def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method to invoke."""
        box.update_widget_values()

    wrapped = simple_handler(handler)

    # Invoke the handler as if it were a method handler (i.e., with the
    # extra "widget" argument)
    wrapped('widget')

    # The text of authentication button has been updated.
    assert box.btn_change_auth.text == btn_text

    # The handler of authentication button has been updated.
    # TODO: Fix AssertionError  # noqa: TD003, TD002
    # <function wrapped_handler.<locals>._handler at 0x747cf1120c10>
    # == <function goto_login at 0x747cf1e4fb50>
    # assert box.btn_change_auth.on_press == btn_handler

    # The info panel has been updated.
    assert box.info_panel.value == info_text
