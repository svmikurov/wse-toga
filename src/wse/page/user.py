"""The user pages for window content."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response
from toga import Button
from toga.style.pack import Pack
from travertino.constants import CENTER

from wse import constants as const
from wse.constants import (
    HOST_API,
    INPUT_HEIGHT,
    PASSWORD,
    TITLE_LABEL_HEIGHT,
    USER_BOX,
    USERNAME,
)
from wse.constants.page import AUTH_BOX
from wse.constants.url import USER_ME, USER_REGISTER_PATH
from wse.contrib.http_requests import app_auth, request_get, request_post
from wse.page.base import BoxApp
from wse.widget.base import BtnApp, MulTextInpApp


class Credentials(BoxApp):
    """Credentials input widgets."""

    url_path = ''
    """Submit url path (`str`).
    """
    page_box_title = ''
    """Page box title (`str`).
    """
    btn_submit_name = 'Отправить'
    """Name of the "Submit" button (`str`).
    """

    def __init__(self) -> None:
        """Construct the widgets."""
        super().__init__()

        # Styles.
        input_style = Pack(height=INPUT_HEIGHT)
        title_style = Pack(height=TITLE_LABEL_HEIGHT, text_align=CENTER)

        # Widgets.
        title_label = toga.Label(self.page_box_title, style=title_style)
        btn_goto_user_box = BtnApp(
            'Назад', lambda _: self.goto_box_handler(_, const.USER_BOX)
        )
        self.username_input = toga.TextInput(
            placeholder='Имя', style=input_style
        )
        self.password_input = toga.PasswordInput(
            placeholder='Пароль', style=input_style
        )
        btn_submit = BtnApp(self.btn_submit_name, on_press=self.submit_handler)

        # Widgets DOM.
        self.add(
            title_label,
            btn_goto_user_box,
            self.username_input,
            self.password_input,
            btn_submit,
        )

    def submit_handler(self, widget: Button) -> None:
        """Submit, button handler."""
        url = urljoin(HOST_API, self.url_path)
        self.request_auth(widget, url)

    def request_auth(self, widget: toga.Widget, url: str) -> None:
        """Request login."""
        response = request_post(url, payload=self.get_credentials())
        if response.status_code == HTTPStatus.OK:
            self.handel_success(widget, response)

    @staticmethod
    def validate_credentials(credentials: dict) -> bool:
        """Validate the user credentials."""
        return True

    def get_credentials(self) -> dict:
        """Extract user data from form, validate it."""
        credentials = {
            USERNAME: self.username_input.value,
            PASSWORD: self.password_input.value,
        }
        if self.validate_credentials(credentials):
            return credentials

    def handel_success(self, widget: toga.Widget, response: Response) -> None:
        """Handel the success auth request."""
        app_auth.set_token(response)
        self.username_input.value = None
        self.password_input.value = None
        self.goto_box_handler(widget, USER_BOX)


class UserBox(BoxApp):
    """The general user page box.

    Contains buttons for move to user page boxes.
    """

    user_detail_url = urljoin(HOST_API, USER_ME)
    """User detail url, allowed GET method (`str`).
    """
    USER_DATA = {
        'username': 'Test name',
    }
    """Test user info data (`dict`q).
    """
    user_info_text = 'Username: %s'
    """User info template (`str`).
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.user_data: dict = self.USER_DATA
        self.user_id: int | None = None
        self.username: str | None = None
        self.is_auth: bool = False

        # Box widgets.
        btn_goto_main_box = BtnApp(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )
        btn_goto_register_form = BtnApp(
            'Вход / Регистрация',
            on_press=lambda _: self.goto_box_handler(_, AUTH_BOX),
        )
        btn_goto_update_user_box = BtnApp(
            'Изменить учетную запись',
            on_press=lambda _: self.goto_box_handler(_, const.USER_UPDATE_BOX),
        )
        btn_delete_user = BtnApp(
            'Удалить учетную запись',
            on_press=lambda _: self.delete_handler,
        )
        self.btn_logout = BtnApp('Выйти', on_press=self.logout_handler)

        # User info display
        self.user_info_display = MulTextInpApp()

        # Widget DOM.
        self.add(
            self.user_info_display,
            btn_goto_main_box,
            btn_goto_register_form,
            btn_goto_update_user_box,
            btn_delete_user,
        )

    def on_open(self) -> None:
        """Invoke display of user information."""
        self.display_user_info()

    ####################################################################
    # Button callback functions.

    def delete_handler(self, _: toga.Widget) -> None:
        """Send the http request to delete the user, button handler."""
        pass

    def logout_handler(self, _: toga.Widget) -> None:
        """Send the http request to user logout, button handler."""
        pass

    ####################################################################
    # User info.

    def display_user_info(self) -> None:
        """Display the user info."""
        self.set_user_info()
        self.username = self.username or 'anonymous'
        self.populate_display_info()

    def set_user_info(self) -> None:
        """Set user info."""
        response = request_get(self.user_detail_url)

        if response.status_code == HTTPStatus.OK:
            self.user_id = response.json()['id']
            self.username = response.json()['username']
            self.is_auth = True
        else:
            self.user_id = None
            self.username = None
            self.is_auth = False

        self.update_auth_widgets()

    def populate_display_info(self) -> None:
        """Populate the user info display."""
        info_text = self.user_info_text % self.username
        self.user_info_display.value = info_text

    def update_auth_widgets(self) -> None:
        """Update auth widgets."""
        pass


class UserUpdateBox(Credentials):
    """User update page box."""

    page_box_title = 'Изменение учетных данных'
    page_box_path = ''
    btn_submit_name = 'Изменить'


class AuthBox(Credentials):
    """Login page box."""

    page_box_title = 'Вход в учетную запись'
    btn_submit_name = 'Войти'

    def __init__(self) -> None:
        """Construct the page box."""
        super().__init__()

        btn_registration = BtnApp(
            'Зарегистрироваться', self.registration_handler
        )
        self.add(btn_registration)

    def registration_handler(self, widget: toga.Widget) -> None:
        """Submit registration, button handler."""
        url = urljoin(HOST_API, USER_REGISTER_PATH)
        self.request_auth(widget, url)
