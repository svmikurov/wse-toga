"""The user pages for window content."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
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
from wse.contrib.http_requests import app_auth, request_post
from wse.page.base import BaseBox
from wse.widget.base import BtnApp, MulTextInpApp


class Credentials(BaseBox):
    """Credentials input widgets."""

    page_box_title = ''
    """Page box title (`str`).
    """
    page_box_path = ''
    """Url path to page box (`str`).
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
            'Назад',
            on_press=lambda _: self.goto_box_handler(_, const.USER_BOX),
        )
        self.username_input = toga.TextInput(
            placeholder='Имя',
            style=input_style,
        )
        self.password_input = toga.PasswordInput(
            placeholder='Пароль',
            style=input_style,
        )
        btn_submit = BtnApp(
            self.btn_submit_name,
            on_press=self.submit_handler,
        )

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
        url = urljoin(HOST_API, self.page_box_path)
        credentials = {
            USERNAME: self.username_input.value,
            PASSWORD: self.password_input.value,
        }
        response = request_post(url=url, payload=credentials)

        if response.status_code == HTTPStatus.OK:
            self.username_input.value = None
            self.password_input.value = None
            app_auth.set_token(response)
            self.goto_box_handler(widget, USER_BOX)


class UserBox(BaseBox):
    """The general user page box.

    Contains buttons for move to user page boxes.
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
        self.user_data = self.USER_DATA

        # Box widgets.
        btn_goto_main_box = BtnApp(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )
        btn_goto_register_form = BtnApp(
            'Зарегистрироваться',
            on_press=lambda _: self.goto_box_handler(_, const.USER_CREATE_BOX),
        )
        btn_goto_login_box = BtnApp(
            'Войти в учетную запись',
            on_press=lambda _: self.goto_box_handler(_, const.LOGIN_BOX),
        )
        btn_goto_update_user_box = BtnApp(
            'Изменить учетную запись',
            on_press=lambda _: self.goto_box_handler(_, const.USER_UPDATE_BOX),
        )
        btn_delete_user = BtnApp(
            'Удалить учетную запись',
            on_press=lambda _: self.delete_handler,
        )
        self.btn_logout = BtnApp(
            'Выйти',
            on_press=self.logout_handler,
        )

        # User info display
        self.user_info_display = MulTextInpApp()

        # Widget DOM.
        self.add(
            self.user_info_display,
            btn_goto_main_box,
            btn_goto_login_box,
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
    # User info display.

    def display_user_info(self) -> None:
        """Display the user info."""
        self.populate_display_info()

    def populate_display_info(self) -> None:
        """Populate the user info display."""
        user_name = self.user_data.get('username')
        info_text = self.user_info_text % user_name
        self.user_info_display.value = info_text


class UserCreateBox(Credentials):
    """User registration page box."""

    page_box_title = 'Регистрация пользователя'
    page_box_path = ''
    btn_submit_name = 'Зарегистрироваться'


class UserUpdateBox(Credentials):
    """User update page box."""

    page_box_title = 'Изменение учетных данных'
    page_box_path = ''
    btn_submit_name = 'Изменить'


class LoginBox(Credentials):
    """Login page box."""

    page_box_title = 'Вход в учетную запись'
    page_box_path = ''
    btn_submit_name = 'Войти'
