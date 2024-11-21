"""Test of uer controllers."""

from unittest.mock import MagicMock, Mock, call, patch

from toga.handlers import simple_handler

from wse.app import WSE
from wse.controler.user import (
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
    assert wse.user is get_user(widget)


@patch('httpx.Client.post', return_value=RESPONSE_AUTH)
def test_login(
    post: MagicMock,
    wse: WSE,
) -> None:
    """Test the login."""
    box = wse.box_login
    box_next = wse.box_main
    button = box.btn_login
    credentials = {'username': 'name', 'password': 'pass'}

    # Assign the box-container to window content.
    wse.app.main_window.content = box

    async def handler(*args: object, **kwargs: object) -> None:
        """Set testing method."""
        await login(*args, **kwargs)

    wrapped = simple_handler(handler, button, credentials)

    # Invoke the handler, and run until it is complete.
    wse.loop.run_until_complete(wrapped('obj'))

    # Http request arguments are as expected.
    assert post.call_args_list == [
        call(
            'http://127.0.0.1/auth/token/login/',
            json={'username': 'name', 'password': 'pass'},
        ),
        call('http://127.0.0.1/api/v1/auth/users/me/'),
    ]

    # Window content was changed.
    assert wse.main_window.content is box_next
