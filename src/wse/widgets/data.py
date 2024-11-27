"""Managing widget values."""

import toga
from httpx import Response
from toga.sources import Source

from wse.widgets.button import BtnApp


class ManagingWidgetData:
    """Managing widget data."""

    source_class = Source
    """Set the custom entry source class (`toga.sources.Source`').
    """

    def __init__(self) -> None:
        """Construct the entry."""
        self._entry = None

    @property
    def entry(self) -> source_class:
        """The widget entry data."""
        return self._entry

    @entry.setter
    def entry(self, value: source_class) -> None:
        self._entry = value
        self.populate_entry_input()

    @entry.deleter
    def entry(self) -> None:
        del self.entry
        self.clear_entry_input()

    def focus_to_input_field(self) -> None:
        """Focus to field input."""
        pass

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        raise NotImplementedError(
            'Subclasses must provide a populate_entry_input() method.'
        )

    def get_widget_data(self) -> dict:
        """Get the entered into the widget data."""
        raise NotImplementedError(
            'Subclasses must provide a get_widget_data() method.'
        )

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        raise NotImplementedError(
            'Subclasses must provide a clear_entry_input() method.'
        )


class HandleSuccessResponse(ManagingWidgetData):
    """Managing widget data received from a response request."""

    url = None
    success_http_status = None
    btn_submit_text = 'Отправить'

    def __init__(self) -> None:
        """Construct."""
        super().__init__()
        self.btn_submit = BtnApp(
            self.btn_submit_text, on_press=self.submit_handler
        )

    async def submit_handler(self, widget: toga.Widget) -> None:
        """Submit, button handler."""
        widget_data = self.get_widget_data()
        item_id = widget_data.get('id')
        url = self.url % item_id if bool(item_id) else self.url

        response = await self.request_async(url, widget_data)
        if response.status_code == self.success_http_status:
            self.clear_entry_input()
            await self.handle_success(widget)

    @classmethod
    async def request_async(cls, url: str, payload: dict) -> Response:
        """Send http async request."""
        raise NotImplementedError(
            'Subclasses must provide a request_async method.'
        )

    async def handle_success(self, widget: toga.Widget) -> None:
        """Invoke if success."""
        pass
