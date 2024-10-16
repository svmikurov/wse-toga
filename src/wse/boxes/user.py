"""The user pages for window content."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from toga import Button
from toga.style import Pack
from travertino.constants import CENTER

from wse import constants as const
from wse.boxes.base import BaseBox
from wse.boxes.widgets.base import BaseButton
from wse.constants import (
    HOST_API,
    INPUT_HEIGHT,
    PASSWORD,
    TITLE_LABEL_HEIGHT,
    USER_BOX,
    USERNAME,
)
from wse.http_requests import app_auth, request_post


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
        btn_goto_user_box = BaseButton(
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
        btn_submit = BaseButton(
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

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = BaseButton(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )
        btn_goto_register_form = BaseButton(
            'Зарегистрироваться',
            on_press=lambda _: self.goto_box_handler(_, const.USER_CREATE_BOX),
        )
        btn_goto_login_box = BaseButton(
            'Войти в учетную запись',
            on_press=lambda _: self.goto_box_handler(_, const.LOGIN_BOX),
        )
        btn_goto_update_user_box = BaseButton(
            'Изменить учетную запись',
            on_press=lambda _: self.goto_box_handler(_, const.USER_UPDATE_BOX),
        )
        btn_delete_user = BaseButton(
            'Удалить учетную запись',
            on_press=lambda _: self.delete_handler,
        )
        self.btn_logout = BaseButton(
            'Выйти',
            on_press=self.logout_handler,
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_login_box,
            btn_goto_register_form,
            btn_goto_update_user_box,
            btn_delete_user,
        )

    def delete_handler(self, _: toga.Button) -> None:
        """Send the http request to delete the user, button handler."""
        pass

    def logout_handler(self, _: toga.Button) -> None:
        """Send the http request to user logout, button handler."""
        pass


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
