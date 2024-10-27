"""The user pages for window content."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response

from wse.constants import (
    HOST_API,
    LOGIN_BAD_MSG,
    LOGIN_BOX,
    LOGIN_MSG,
    LOGIN_PATH,
    LOGIN_TITLE,
    LOGOUT_MSG,
    LOGOUT_PATH,
    MAIN_BOX,
    PASSWORD,
    TITLE_USER_MAIN,
    USER_CREATE_BOX,
    USER_CREATE_PATH,
    USER_ME,
    USER_UPDATE_BOX,
    USER_UPDATE_MESSAGE,
    USER_UPDATE_PATH,
    USER_UPDATE_TITLE,
    USERNAME,
)
from wse.constants.settings import (
    USER_CREATE_MESSAGE,
    USER_CREATE_TITLE,
)
from wse.container.credentials import Credentials
from wse.contrib.http_requests import app_auth, request_get, request_post
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.label import TitleLabel
from wse.general.text_input import TextPanel


class UserAuth(BoxApp):
    """User authentication control widget."""

    welcome: str
    info_panel: toga.MultilineTextInput

    user_info_text = 'Добро пожаловать, %s!'
    """User info template (`str`).
    """
    user_detail_url = urljoin(HOST_API, USER_ME)
    """User detail url, allowed GET method (`str`).
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()
        self.is_auth: bool = False
        self.username: str | None = None

        self.btn_goto_auth = BtnApp(
            self.auth_attrs['btn_auth']['text'],
            on_press=self.auth_attrs['btn_auth']['on_press'],
        )

    def on_open(self) -> None:
        """Call widget setup by user authentication status."""
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
                    'text': 'Выход из учетной записи',
                    'on_press': self.logout_handler,
                },
                'info_text': self.user_info_text % self.username,
            },
            False: {
                'btn_auth': {
                    'text': 'Вход в учетную запись',
                    'on_press': lambda _: self.goto_box_handler(_, LOGIN_BOX),
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
        """Set user info."""
        response = request_get(self.user_detail_url)
        if response.status_code == HTTPStatus.OK:
            self.username = response.json()['username']
            self.is_auth = True
        else:
            self.username = None
            self.is_auth = False


class MainUserBox(BoxApp):
    """The main user page box.

    **DEPRECATED**

    Contains buttons for move to user page boxes.
    """

    title = TITLE_USER_MAIN
    """Page box title (`str`).
    """
    user_detail_url = urljoin(HOST_API, USER_ME)
    """User detail url, allowed GET method (`str`).
    """
    user_info_text = 'Username: %s'
    """User info template (`str`).
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.username: str | None = None
        self.is_auth: bool = False

        # Box widgets.
        btn_goto_main = BtnApp(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        self.btn_goto_auth = BtnApp(
            self.auth_attrs['btn_auth']['text'],
            on_press=self.auth_attrs['btn_auth']['on_press'],
        )
        self.btn_goto_create = BtnApp(
            'Создать учетную запись',
            on_press=lambda _: self.goto_box_handler(_, USER_CREATE_BOX),
        )
        self.btn_goto_update = BtnApp(
            'Изменить имя',
            on_press=lambda _: self.goto_box_handler(_, USER_UPDATE_BOX),
            enabled=not self.is_auth,
        )
        self.btn_delete = BtnApp(
            'Удалить учетную запись',
            on_press=lambda _: self.delete_handler,
            enabled=not self.is_auth,
        )

        # User info display
        self.info_display = TextPanel()
        self.info_display.style.flex = 1

        # Widget DOM.
        self.add(
            TitleLabel(self.title),
            self.info_display,
            self.btn_goto_auth,
            self.btn_goto_create,
            self.btn_goto_update,
            self.btn_delete,
            btn_goto_main,
        )

    def on_open(self) -> None:
        """Call widget setup by user authentication status."""
        self.setup_user_status()
        self.update_widget_values()

    ####################################################################
    # Button callback functions.

    async def logout_handler(self, _: toga.Widget) -> None:
        """Send the http request to user logout, button handler."""
        url = urljoin(HOST_API, LOGOUT_PATH)
        response = request_post(url=url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            self.is_auth = False
            self.update_widget_values()
            app_auth.delete_token()
            await self.show_message('', LOGOUT_MSG)

    async def delete_handler(self, _: toga.Widget) -> None:
        """Send the http request to delete the user, button handler."""
        pass

    ####################################################################
    # Widget managing.

    def update_widget_values(self) -> None:
        """Update widget values by user auth status."""
        # Display info.
        self.info_display.value = self.auth_attrs['info_text']
        # Button auth user.
        self.btn_goto_auth.text = self.auth_attrs['btn_auth']['text']
        self.btn_goto_auth.on_press = self.auth_attrs['btn_auth']['on_press']
        # Button create user.
        self.btn_goto_create.enabled = not self.is_auth
        # Button update user.
        self.btn_goto_update.enabled = self.is_auth
        # Button delete user.
        self.btn_delete.enabled = self.is_auth

    ####################################################################
    # User info.

    @property
    def auth_attrs(self) -> dict:
        """Setup widget attr values by user auth status."""
        move_to = self.goto_box_handler
        widget_values = {
            True: {
                'btn_auth': {
                    'text': 'Выход из учетной записи',
                    'on_press': self.logout_handler,
                },
                'info_text': self.user_info_text % self.username,
            },
            False: {
                'btn_auth': {
                    'text': 'Вход в учетную запись',
                    'on_press': lambda _: move_to(_, LOGIN_BOX),
                },
                'info_text': self.user_info_text % 'Anonymous',
            },
        }
        return widget_values[self.is_auth]

    def setup_user_status(self) -> None:
        """Set user info."""
        response = request_get(self.user_detail_url)
        if response.status_code == HTTPStatus.OK:
            self.username = response.json()['username']
            self.is_auth = True
        else:
            self.username = None
            self.is_auth = False


class CreateUserBox(Credentials):
    """Create user page box."""

    title = USER_CREATE_TITLE
    url_path = USER_CREATE_PATH
    btn_submit_name = 'Создать учетную запись'
    success_status_code = HTTPStatus.CREATED
    success_response_msg = USER_CREATE_MESSAGE

    async def send_request(self, url: str, payload: dict) -> Response:
        """Request login, without token."""
        return request_post(url, payload, token=False)


class UpdateUserBox(Credentials):
    """Update user page box."""

    title = USER_UPDATE_TITLE
    url_path = USER_UPDATE_PATH
    btn_submit_name = 'Изменить'
    success_status_code = HTTPStatus.NO_CONTENT
    success_response_msg = USER_UPDATE_MESSAGE

    async def get_credentials(self) -> dict | None:
        """Rename credential payload field names."""
        credentials: dict = await super().get_credentials()
        if bool(credentials):
            credentials['new_username'] = credentials.pop(USERNAME)
            credentials['current_password'] = credentials.pop(PASSWORD)
            return credentials


class LoginBox(Credentials):
    """Login page box."""

    title = LOGIN_TITLE
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
