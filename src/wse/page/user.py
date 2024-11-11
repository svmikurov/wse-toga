"""The page handlers of user data."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response

from wse.constants import (
    BTN_GOTO_LOGIN,
    BTN_LOGOUT,
    HOST_API,
    LOGIN_BAD_MSG,
    LOGIN_MSG,
    LOGIN_PATH,
    LOGOUT_MSG,
    LOGOUT_PATH,
    TITLE_LOGIN,
    USER_ME_PATH,
)
from wse.container.credentials import Credentials
from wse.contrib.http_requests import (
    app_auth,
    request_get,
    request_post,
)
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.goto_handler import goto_login


class UserAuth(BoxApp):
    """Handlers to control the user authentication status.

    Displays the user authentication status.
    """

    welcome: str
    info_panel: toga.MultilineTextInput

    user_info_text = 'Добро пожаловать, %s!'
    """User info text (`str`).
    """
    user_detail_url = urljoin(HOST_API, USER_ME_PATH)
    """User detail url, allowed GET method (`str`).
    """

    def __init__(self) -> None:
        """Construct the widget."""
        super().__init__()
        self.is_auth: bool = False
        self.username: str | None = None

        self.btn_goto_auth = BtnApp(
            self.auth_attrs['btn_auth']['text'],
            on_press=self.auth_attrs['btn_auth']['on_press'],
        )

    def on_open(self) -> None:
        """Update the widgets on opening page."""
        super().on_open()
        self.setup_user_status()
        self.update_widget_values()

    ####################################################################
    # Authentication

    @property
    def auth_attrs(self) -> dict:
        """Setup widget attr values by user auth status."""
        widget_values = {
            True: {
                'btn_auth': {
                    'text': BTN_LOGOUT,
                    'on_press': self.logout_handler,
                },
                'info_text': self.user_info_text % self.username,
            },
            False: {
                'btn_auth': {
                    'text': BTN_GOTO_LOGIN,
                    'on_press': goto_login,
                },
                'info_text': self.welcome,
            },
        }
        return widget_values[self.is_auth]

    async def logout_handler(self, _: toga.Widget) -> None:
        """Send the http request to user logout, button handler."""
        url = urljoin(HOST_API, LOGOUT_PATH)
        response = request_post(url=url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            self.is_auth = False
            self.update_widget_values()
            app_auth.delete_token()
            await self.show_message('', LOGOUT_MSG)

    def update_widget_values(self) -> None:
        """Update widget values by user auth status."""
        # Display info.
        self.info_panel.value = self.auth_attrs['info_text']
        # Button auth user.
        self.btn_goto_auth.text = self.auth_attrs['btn_auth']['text']
        self.btn_goto_auth.on_press = self.auth_attrs['btn_auth']['on_press']

    def setup_user_status(self) -> None:
        """Request and set user data for information."""
        user_data = request_get(self.user_detail_url)
        # Update user data.
        if user_data.status_code == HTTPStatus.OK:
            self.username = user_data.json()['username']
            self.is_auth = True
        else:
            self.username = None
            self.is_auth = False


class LoginBox(Credentials):
    """Login page box."""

    title = TITLE_LOGIN
    url_path = LOGIN_PATH
    btn_submit_name = 'Войти'
    success_response_msg = LOGIN_MSG
    error_response_msg = LOGIN_BAD_MSG

    async def send_request(self, url: str, payload: dict) -> Response:
        """Request login without token, save token."""
        response = request_post(url, payload, token=False)
        if response.status_code == HTTPStatus.OK:
            app_auth.set_token(response)
        return response
