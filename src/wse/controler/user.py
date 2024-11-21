"""User controllers."""

from http import HTTPStatus

import toga

from wse.contrib.http_requests import obtain_token, request_user_data
from wse.general.goto_handler import goto_main_handler
from wse.source.user import UserSource


def get_user(widget: toga.Widget) -> UserSource:
    """Return user source instance."""
    return widget.app.user


async def login(widget: toga.Widget, credentials: dict[str, str]) -> None:
    """Login, controller."""
    response_token = obtain_token(credentials)
    user = get_user(widget)

    if response_token.status_code == HTTPStatus.OK:
        username = request_user_data()['username']
        user.set_auth_data(username)

        # Go to next box-container.
        await goto_main_handler(widget)
