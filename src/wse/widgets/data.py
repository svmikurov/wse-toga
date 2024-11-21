"""Managing widget values."""

import toga
from httpx import Response
from toga.sources import Source

from wse.widgets.button import BtnApp


class ManagingWidgetData:
    """Managing widget data.

    .. important::

        Override the methods:
            * populate_entry_input()
            * clear_entry_input()
            * get_widget_data()

        Override the attrs:
            * url
            * success_http_status

    """

    source_class = Source
    """Set the custom entry source class (`toga.sources.Source`').
    """

    def __init__(self) -> None:
        """Construct the entry."""
        self._entry = None

    @property
    def entry(self) -> source_class:
        """The widget entry data.

        The setter invokes methods to populate or clear the widget's
        attr value.

        :setter value: the item of Source data to set to widget
            value.
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

    def focus_to_input_field(self) -> None:
        """Focus to field input.

        Currently, nothing is being implemented.
        You may **override** this method, for example::

            def focus_to_input_field(self) -> None:
                self.field_name_input.focus()
        """
        pass

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value.

        Currently, nothing is being implemented.
        **Override** this method, for example::

            def populate_entry_input(self) -> None:
                self.field_name_input.value = self.entry.some_value
                ...

        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError(
            'Subclasses must provide a populate_entry_input() method.'
        )

    def get_widget_data(self) -> dict:
        """Get the entered into the widget data.

        Currently, nothing is being implemented.
        **Override** this method, for example::

            def get_widget_data(self) -> dict:
                submit_entry = {
                    'some_value': self.field_name_input.value,
                    ...
                }
                return submit_entry

        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError(
            'Subclasses must provide a get_widget_data() method.'
        )

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value.

        Currently, nothing is being implemented.
        **Override** this method, for example::

             def clear_entry_input(self) -> None:
                self.field_name_input.clean()
                ...

        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError(
            'Subclasses must provide a clear_entry_input() method.'
        )


class ManagingWidgetDataFromResponse(ManagingWidgetData):
    """Managing widget data received from a response request.

    .. important::

        Override the methods:
            * send_request_async()

        Override the attrs:
            * url
            * success_http_status

    """

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
        self.btn_submit = BtnApp(
            self.btn_submit_name, on_press=self.submit_handler
        )

    async def submit_handler(self, widget: toga.Widget) -> None:
        """Submit, button handler."""
        self.focus_to_input_field()

        widget_data = self.get_widget_data()
        item_id = widget_data.get('id')
        url = self.url % item_id if bool(item_id) else self.url

        response = await self.request_post_async(url, widget_data)
        if response.status_code == self.success_http_status:
            self.clear_entry_input()
            self.handle_success(widget)

    @classmethod
    async def request_post_async(cls, url: str, payload: dict) -> Response:
        """Send http async request.

        Currently, nothing is being implemented.
        **Override** this method.

        :param str url: Url to request.
        :param dict payload: Data to assign.
        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError(
            'Subclasses must provide a request_post_async method.'
        )

    def handle_success(self, widget: toga.Widget) -> None:
        """Invoke if success.

        Currently, nothing is being implemented.
        Yoy may **override** this method to act.
        """
        pass
