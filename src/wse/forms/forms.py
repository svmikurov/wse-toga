"""Form classes."""

from http import HTTPStatus

import toga
from httpx import Response
from toga.sources import Source

from wse.boxes.base import BaseBox
from wse.contrib.http_requests import (
    request_post_async,
    request_put_async,
)
from wse.widgets.base import BtnApp


class EntryManagement:
    """Entry form management.

    Override the methods:

        populate_entry_input()
        clear_entry_input()
        get_form_data()

    """

    source_class = Source
    """Set the custom entry source class (`toga.sources.Source`').
    """

    def __init__(self) -> None:
        """Construct the entry."""
        self._entry = None

    @property
    def entry(self) -> source_class:
        """The form entry data.

        Invoke the populate or clear the widget value.
        """
        return self._entry

    @entry.setter
    def entry(self, value: source_class) -> None:
        self._entry = value
        self.populate_entry_input()

    @entry.deleter
    def entry(self) -> None:
        del self.entry
        self.clear_entry_input()

    def input_field_focus(self) -> None:
        """Focus to field input.

        You may override this method.

        For example:
            self.russian_input.focus()

        """
        pass

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value.

        Override this method.

        For example:

            self.russian_input.value = self.entry.russian_word
            self.foreign_input.value = self._entry.foreign_word
        """
        raise NotImplementedError(
            'Subclasses must provide a populate_entry_input() method.'
        )

    def get_form_data(self) -> dict:
        """Get the entered into the form data.

        Override this method.

        For example:
            submit_entry = {
                FOREIGN_WORD: self.russian_input.value,
                RUSSIAN_WORD: self.foreign_input.value,
            }
        return submit_entry
        """
        raise NotImplementedError(
            'Subclasses must provide a get_form_data() method.'
        )

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value.

        Override this method.

        For example:

            self.russian_input.clean()
            self.foreign_input.clean()
        """
        raise NotImplementedError(
            'Subclasses must provide a populate_entry_input() method.'
        )


class RequestHandler(EntryManagement):
    """Request the form submit, the handler."""

    url = None
    """Entries url path to http requests (`str` | None).
    """
    success_http_status = None
    """Success http status (`int`).
    """
    btn_submit_name = 'Отправить'

    def __init__(self) -> None:
        """Construct."""
        super().__init__()
        btn_submit = BtnApp(self.btn_submit_name, on_press=self.submit_handler)

    async def submit_handler(self, widget: toga.Widget) -> None:
        """Submit, button handler."""
        form_data = self.get_form_data()
        response = await self.send_request_async(form_data)
        if response.status_code == self.success_http_status:
            self.clear_entry_input()
            self.handle_success(widget)
        self.input_field_focus()

    async def send_request_async(self, payload: dict) -> Response:
        """Send http async request.

        Override this method.

        For example:
            url = urljoin(HOST_API, ENTRY_PATH)
            success_http_status = HTTPStatus.CREATED
            ...
            async def send_request_async(self, payload) -> Response:
                return await request_post_async(self.url, payload)

        """
        raise NotImplementedError(
            'Subclasses must provide a send_request_async() method.'
        )

    def handle_success(self, widget: toga.Widget) -> None:
        """Invoke if success.

        Yoy may override this method to act.
        """
        pass


class RequestCreateMixin:
    """Request to create entry, the mixin."""

    url: str

    success_http_status = HTTPStatus.CREATED

    async def send_request_async(self, payload: dict) -> Response:
        """Send http request to create entry, POST method."""
        return await request_post_async(self.url, payload)


class RequestUpdateMixin:
    """Request to update entry, the mixin."""

    entry: Source
    url: str

    success_http_status = HTTPStatus.OK

    async def send_request_async(self, payload: dict) -> Response:
        """Send http request to update entry, PUT method."""
        url = self.url % self.entry.id
        return await request_put_async(url, payload)


class BaseForm(BaseBox, RequestHandler):
    """"""
