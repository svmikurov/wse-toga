"""Credentials container."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response
from toga.style import Pack

from wse.constants import (
    HOST_API,
    INPUT_HEIGHT,
    MAIN_BOX,
    PASSWORD,
    USERNAME,
)
from wse.contrib.http_requests import ErrorResponse, request_post
from wse.contrib.validator import validate_credentials
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.label import TitleLabel


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
    success_response_msg = ''
    """Success response message (`str`).
    """
    error_response_msg = ''
    """Error response message (`str`).
    """

    def __init__(self) -> None:
        """Construct the widgets."""
        super().__init__()

        # Styles.
        input_style = Pack(height=INPUT_HEIGHT)

        # Widgets.
        self.title_label = TitleLabel(text=self.title)
        self.username_input = toga.TextInput(
            placeholder='Имя', style=input_style
        )
        self.password_input = toga.PasswordInput(
            placeholder='Пароль', style=input_style
        )
        self.btn_submit = BtnApp(
            self.btn_submit_name, on_press=self._submit_handler
        )
        self.btn_goto_main_box = BtnApp(
            'На главную', lambda _: self.goto_box_handler(_, MAIN_BOX)
        )

        # Widgets DOM.
        self.add(
            self.title_label,
            self.username_input,
            self.password_input,
            self.btn_submit,
            self.btn_goto_main_box,
        )

    def on_open(self) -> None:
        """Clear fields."""
        self._clear_fields()

    ####################################################################
    # Button callback functions.

    async def _submit_handler(self, widget: toga.Widget) -> None:
        """Submit, button handler."""
        credentials: dict = await self.get_credentials()

        if bool(credentials):
            url = urljoin(HOST_API, self.url_path)
            response = await self.send_request(url, credentials)
            await self._show_response_message(response)

            if response.status_code == self.success_status_code:
                await self.handel_success(widget)

    ####################################################################
    # Auth.

    async def send_request(self, url: str, payload: dict) -> Response:
        """Send request."""
        return request_post(url, payload)

    def _extract_credentials(self) -> dict:
        """Extract user data from form, validate it."""
        credentials = {
            USERNAME: self.username_input.value,
            PASSWORD: self.password_input.value,
        }
        return credentials

    async def get_credentials(self) -> dict | None:
        """Extract user data from form, validate it."""
        credentials: dict = self._extract_credentials()
        errors = validate_credentials(credentials)
        if errors:
            await self.show_message('', '\n'.join(errors))
        return credentials

    async def handel_success(self, widget: toga.Widget) -> None:
        """Handel the success auth request."""
        self._clear_fields()
        self.goto_box_handler(widget, MAIN_BOX)

    def _clear_fields(self) -> None:
        """Clear the fields."""
        self.username_input.value = None
        self.password_input.value = None

    async def _show_response_message(
        self,
        response: Response | ErrorResponse,
    ) -> None:
        """Show response message."""
        if response.status_code == self.success_status_code:
            await self.show_message('', self.success_response_msg)
        elif response.status_code == HTTPStatus.BAD_REQUEST:
            await self.show_message('', self.error_response_msg)
        elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            await self.show_message('', response.conn_error_msg)
        else:
            await self.show_message('', 'Error')
