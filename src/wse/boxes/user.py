"""User boxes."""

from urllib.parse import urljoin

import toga
from toga.style import Pack

from wse import base
from wse import constants as const
from wse.http_requests import app_auth, get_message, send_post_request


class UserBox(base.BaseBox):
    """User box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = base.BaseButton(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )
        btn_goto_login_box = base.BaseButton(
            'Войти в учетную запись',
            on_press=lambda _: self.goto_box_handler(_, const.LOGIN_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_login_box,
        )


class LoginBox(
    base.MessageBoxMixin,
    base.BaseBox,
):
    """Log in box."""

    LOGIN_MESSAGES = {
        const.HTTP_200_OK: ('Вы вошли в учетную запись', ''),
        const.HTTP_400_BAD_REQUEST: ('Неверные имя или пароль', ''),
        const.HTTP_500_INTERNAL_SERVER_ERROR: ('Ошибка сервера', ''),
    }

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Styles.
        input_style = Pack(
            height=60,
        )

        # Box widgets.
        title_label = base.BaseLabel('Вход в приложение')
        btn_goto_user_box = base.BaseButton(
            'На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )
        self.username_input = toga.TextInput(
            placeholder='Имя',
            style=input_style,
        )
        self.password_input = toga.PasswordInput(
            placeholder='Пароль',
            style=input_style,
        )
        btn_submit = base.BaseButton(
            'Войти',
            on_press=self.login_handler,
        )

        # Widget DOM.
        self.add(
            title_label,
            btn_goto_user_box,
            self.username_input,
            self.password_input,
            btn_submit,
        )

    async def login_handler(self, widget: toga.Button) -> None:
        """Submit log in, button handler.

        Send an authorization request, if success then update widgets.
        """
        url = urljoin(const.HOST_API, const.TOKEN_PATH)
        authorization_data = {
            const.USERNAME: self.username_input.value,
            const.PASSWORD: self.password_input.value,
        }

        response = await send_post_request(url=url, payload=authorization_data)

        if response.status_code == const.HTTP_200_OK:
            self.username_input.value = None
            self.password_input.value = None
            app_auth.set_token(response)
            self.goto_box_handler(widget, const.MAIN_BOX)

        title, message = get_message(self.LOGIN_MESSAGES, response.status_code)
        await self.show_message(title, message)
