"""Login box-container."""

from http import HTTPStatus

import toga
from toga.style import Pack

from wse.constants import (
    BTN_LOGIN,
    INPUT_HEIGHT,
    LOGIN_PATH,
    TITLE_LOGIN,
)
from wse.contrib.http_requests import obtain_token, request_user_data
from wse.handlers.goto_handler import goto_main_handler
from wse.source.user import UserSource
from wse.widgets.box_page import BoxApp
from wse.widgets.button import BtnApp
from wse.widgets.label import TitleLabel


class LoginBox(BoxApp):
    """Credentials input widgets container."""

    title = TITLE_LOGIN
    """Box-container title (`str`).
    """
    url_path = LOGIN_PATH
    """Url to login (`str`).
    """

    def __init__(self, source_user: UserSource) -> None:
        """Construct the widgets."""
        super().__init__()
        self.source_user = source_user

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
        self._clear_input_fields()

    async def login_handler(self, widget: toga.Widget) -> None:
        """Submit login, button handler."""
        credentials = self.get_credentials()

        if credentials:
            response_token = obtain_token(credentials)

            if response_token.status_code == HTTPStatus.OK:
                response_userdata = request_user_data()

                if response_userdata.status_code == HTTPStatus.OK:
                    payload = response_userdata.json()
                    # Save user data.
                    self.source_user.set_source_user(payload)
                    self.source_user.save_userdata(payload)

                    # Update widgets.
                    self._clear_input_fields()
                    widget.root.app.box_main.update_widgets()
                    await goto_main_handler(widget)

        else:
            # TODO: Add error message
            pass

    def get_credentials(self) -> dict | None:
        """Extract source_user data from form."""
        username = self.input_username.value
        password = self.input_password.value

        if username and password:
            return {'username': username, 'password': password}
        else:
            print('INFO: введены не полные данные для входа в учетную запись')

    def _clear_input_fields(self) -> None:
        """Clear the fields with credentials."""
        self.input_username.value = None
        self.input_password.value = None
