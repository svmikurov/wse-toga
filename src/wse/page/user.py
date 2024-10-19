"""The user pages for window content."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response
from toga.style.pack import CENTER, Pack

from wse.constants import (
    AUTH_BOX,
    HOST_API,
    INPUT_HEIGHT,
    LOGIN_PATH,
    LOGOUT_PATH,
    MAIN_BOX,
    PASSWORD,
    TITLE_LABEL_HEIGHT,
    USER_BOX,
    USER_ME,
    USER_REGISTER_PATH,
    USER_UPDATE_BOX,
    USERNAME, USER_UPDATE_PATH,
)
from wse.contrib.http_requests import app_auth, request_get, request_post
from wse.contrib.validator import validate_credentials
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
            'Назад', lambda _: self.goto_box_handler(_, USER_BOX)
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

    ####################################################################
    # Button callback functions.

    async def submit_handler(self, widget: toga.Widget) -> None:
        """Submit, button handler."""
        url = urljoin(HOST_API, self.url_path)
        await self.request_auth(widget, url)

    ####################################################################
    # Auth.

    async def request_auth(self, widget: toga.Widget, url: str) -> None:
        """Request login."""
        credentials: dict = await self.get_credentials()
        if not bool(credentials):
            return

        response = request_post(url, credentials, token=False)
        if response.status_code == HTTPStatus.OK:
            app_auth.set_token(response)
            self.handel_success(widget, response)

    def extract_credentials(self) -> dict:
        """Extract user data from form, validate it."""
        credentials = {
            USERNAME: self.username_input.value,
            PASSWORD: self.password_input.value,
        }
        return credentials

    async def get_credentials(self) -> dict:
        """Extract user data from form, validate it."""
        credentials = self.extract_credentials()
        errors = validate_credentials(credentials)
        if not errors:
            return credentials
        else:
            await self.show_message('', '\n'.join(errors))


    def handel_success(self, widget: toga.Widget, response: Response) -> None:
        """Handel the success auth request."""
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
    user_info_text = 'Username: %s'
    """User info template (`str`).
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.user_id: int | None = None
        self.username: str | None = None
        self.is_auth: bool = False

        # Box widgets.
        btn_goto_main = BtnApp(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        self.btn_goto_auth = BtnApp(
            self.values['btn_auth']['text'],
            on_press=self.values['btn_auth']['on_press'],
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
        self.info_display = MulTextInpApp()
        self.info_display.style.flex = 1

        # Widget DOM.
        self.add(
            self.info_display,
            btn_goto_main,
            self.btn_goto_auth,
            self.btn_goto_update,
            self.btn_delete,
        )

    def on_open(self) -> None:
        """Call widget setup by user authentication status."""
        self.setup_user_status()
        self.update_widget_values()

    ####################################################################
    # Button callback functions.

    def logout_handler(self, _: toga.Widget) -> None:
        """Send the http request to user logout, button handler."""
        url = urljoin(HOST_API, LOGOUT_PATH)
        response = request_post(url=url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            self.is_auth = False
            self.update_widget_values()
            app_auth.delete_token()

    async def delete_handler(self, _: toga.Widget) -> None:
        """Send the http request to delete the user, button handler."""
        pass

    ####################################################################
    # Widget managing.

    def update_widget_values(self) -> None:
        """Update widget values by user auth status."""
        # Display info.
        self.info_display.value = self.values['info_text']
        # Button auth user.
        self.btn_goto_auth.text = self.values['btn_auth']['text']
        self.btn_goto_auth.on_press = self.values['btn_auth']['on_press']
        # Button update user.
        self.btn_goto_update.enabled = self.is_auth
        # Button delete user.
        self.btn_delete.enabled = self.is_auth

    ####################################################################
    # User info.

    @property
    def values(self) -> dict:
        """Widget attr values by user auth status."""
        move_to = self.goto_box_handler
        widget_values = {
            True: {
                'btn_auth': {
                    'text': 'Выход',
                    'on_press': self.logout_handler,
                },
                'info_text': self.user_info_text % self.username,
            },
            False: {
                'btn_auth': {
                    'text': 'Вход / Регистрация',
                    'on_press': lambda _: move_to(_, AUTH_BOX),
                },
                'info_text': self.user_info_text % 'Anonymous',
            },
        }
        return widget_values[self.is_auth]

    def setup_user_status(self) -> None:
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


class UserUpdateBox(Credentials):
    """User update page box."""

    page_box_title = 'Изменение учетных данных'
    url_path = USER_UPDATE_PATH
    btn_submit_name = 'Изменить'

    async def request_auth(self, widget: toga.Widget, url: str) -> None:
        """Request login."""
        credentials: dict = await self.get_credentials()
        payload = {
            'new_username': credentials['username'],
            'current_password': credentials['password'],
        }

        response = request_post(url, payload)
        if response.status_code == HTTPStatus.NO_CONTENT:
            self.handel_success(widget, response)


class AuthBox(Credentials):
    """Login page box."""

    url_path = LOGIN_PATH
    page_box_title = 'Вход в учетную запись'
    btn_submit_name = 'Войти'

    def __init__(self) -> None:
        """Construct the page box."""
        super().__init__()

        btn_registration = BtnApp(
            'Зарегистрироваться', self.registration_handler
        )

        # Update DOM.
        self.add(btn_registration)

    def registration_handler(self, widget: toga.Widget) -> None:
        """Submit registration, button handler."""
        url = urljoin(HOST_API, USER_REGISTER_PATH)
        self.request_auth(widget, url)
