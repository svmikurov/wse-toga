"""The page handlers of user data."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response
from toga.style import Pack

from wse.constants import (
    BTN_GOTO_LOGIN,
    BTN_LOGIN,
    BTN_LOGOUT,
    HOST_API,
    INPUT_HEIGHT,
    LOGIN_BAD_MSG,
    LOGIN_MSG,
    LOGIN_PATH,
    LOGOUT_MSG,
    LOGOUT_PATH,
    TITLE_LOGIN,
    USER_ME_PATH,
)
from wse.contrib.http_requests import (
    ErrorResponse,
    app_auth,
    request_get,
    request_post,
    request_post_async, request_token_async,
)
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.goto_handler import goto_login_handler, goto_main_handler
from wse.general.label import TitleLabel


class UserAuthMixin(BoxApp):
    """Handlers to control the user authentication status, mixin.

    Displays the user authentication status at main page.
    """

    welcome: str
    info_panel: toga.MultilineTextInput

    text_user_info = 'Добро пожаловать, %s!'
    """User info text (`str`).
    """
    url_user_detail = urljoin(HOST_API, USER_ME_PATH)
    """User detail url, allowed GET method (`str`).
    """
    url_logout = urljoin(HOST_API, LOGOUT_PATH)
    """User logout url, allowed POST method (`str`).
    """

    def __init__(self) -> None:
        """Construct the widget."""
        super().__init__()
        self._is_auth: bool = False
        self._username: str | None = None
        self._index_btn_auth = 2

        self.btn_goto_login = BtnApp(
            BTN_GOTO_LOGIN,
            on_press=goto_login_handler,
        )
        self.btn_logout = BtnApp(
            BTN_LOGOUT,
            on_press=self.logout_handler,
        )

    ####################################################################
    # Authentication

    async def logout_handler(self, _: toga.Widget) -> None:
        """Send the http request to user logout, button handler."""
        response = request_post(url=self.url_logout)

        if response.status_code == HTTPStatus.NO_CONTENT:
            self._is_auth = False
            self.update_widgets()
            app_auth.delete_token()
            await self.show_message('', LOGOUT_MSG)

    def update_widgets(self) -> None:
        """Update widgets by user auth status."""
        if self._is_auth:
            self.info_panel.value = self.text_user_info % self._username
            self.children[self._index_btn_auth] = self.btn_logout
        else:
            self.info_panel.value = self.welcome
            self.children[self._index_btn_auth] = self.btn_goto_login

    def refresh_user_auth_status(self) -> None:
        """Refresh the user authentication status."""
        # Request the user detail.
        response = request_get(self.url_user_detail)

        # Update the user authentication data.
        if response.status_code == HTTPStatus.OK:
            username = response.json()['username']
            self.set_username(username)
            self._is_auth = True
        else:
            self.set_username(None)
            self._is_auth = False

    def set_username(self, username: str | None) -> None:
        """Set the username."""
        self._username = username


class Credentials(BoxApp):
    """Credentials input widgets container."""

    title = ''
    """Page box title (`str`).
    """
    url_path = ''
    """Submit url path (`str`).
    """
    btn_submit_name = 'Отправить'
    """Name of the "Submit" button (`str`).
    """
    success_status_code = HTTPStatus.OK
    """Success status code (`int`).
    """
    msg_success_response = ''
    """Success response message (`str`).
    """
    msg_error_response = ''
    """Error response message (`str`).
    """

    def __init__(self) -> None:
        """Construct the widgets."""
        super().__init__()

        # Styles.
        style_input = Pack(height=INPUT_HEIGHT)

        # Widgets.
        self.label_title = TitleLabel(text=self.title)
        self.input_username = toga.TextInput(
            placeholder='Имя', style=style_input
        )
        self.input_password = toga.PasswordInput(
            placeholder='Пароль', style=style_input
        )
        self.btn_login = BtnApp(
            BTN_LOGIN,
            on_press=self.login_handler,
        )
        self.btn_goto_main = BtnApp('На главную', on_press=goto_main_handler)

        # Widgets DOM.
        self.add(
            self.label_title,
            self.input_username,
            self.input_password,
            self.btn_login,
            self.btn_goto_main,
        )

    async def on_open(self, widget: toga.Widget) -> None:
        """Clear fields."""
        self._clear_fields()

    ####################################################################
    # Button callback functions.

    async def login_handler(self, widget: toga.Widget) -> None:
        """Submit login, button handler."""
        credentials: dict = self.get_credentials()

        if credentials:
            url = urljoin(HOST_API, self.url_path)
            response = await request_token_async(url, credentials)
            print(f'{response = }')
            await self._show_response_message(response)

            if response.status_code == self.success_status_code:
                await self.success_handler(widget, response)

    ####################################################################
    # Auth.

    def get_credentials(self) -> dict:
        """Extract user data from form."""
        username = self.input_username.value
        password = self.input_password.value
        if username and password:
            return {'username': username, 'password': password}
        else:
            print('INFO: введены не полные данные для входа в учетную запись')

    async def success_handler(
        self,
        widget: toga.Widget,
        response: Response,
    ) -> None:
        """Handel the success auth request."""
        username = response.json()['username']
        main_box = widget.root.app.box_main
        main_box.set_username(username)
        self._clear_fields()
        await goto_main_handler(widget)

    def _clear_fields(self) -> None:
        """Clear the fields with credentials."""
        self.input_username.value = None
        self.input_password.value = None

    async def _show_response_message(
        self,
        response: Response | ErrorResponse,
    ) -> None:
        """Show response message."""
        if response.status_code == self.success_status_code:
            await self.show_message('', self.msg_success_response)
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            await self.show_message('', self.msg_error_response)
        elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            await self.show_message('', response.conn_error_msg)
        else:
            await self.show_message('', 'Error')


class LoginBox(Credentials):
    """Login page box."""

    title = TITLE_LOGIN
    url_path = LOGIN_PATH
    btn_submit_name = 'Войти'
    msg_success_response = LOGIN_MSG
    msg_error_response = LOGIN_BAD_MSG

    async def send_request(self, url: str, payload: dict) -> Response:
        """Request login without token, save token."""
        response = request_post(url, payload, token=False)
        if response.status_code == HTTPStatus.OK:
            app_auth.set_token(response)
        return response
