"""Table classes."""

import toga
from httpx import Response
from toga.style import Pack
from travertino.constants import ITALIC

from wse.contrib.http_requests import request_delete_async, request_get
from wse.contrib.utils import to_entries
from wse.widgets.box_page import BoxApp
from wse.widgets.button import BtnApp, SmBtn


class BaseTable(toga.Table):
    """General table app.

    Defines a common style for derived table widgets.
    """

    def __init__(self, *arge: object, **kwargs: object) -> None:
        """Construct the table."""
        style = Pack(
            flex=1,
            font_style=ITALIC,
        )
        kwargs['style'] = kwargs.get('style', style)
        super().__init__(*arge, **kwargs)


class TableApp(BoxApp):
    """Base table, the container.

    In the derived class:
        * Assign source class.
        * Add source urls (list-create, detail).
        * Add table column head names.
        * Add the necessary page widgets.
        * Construct the page DOM.

    .. important::

        Override the methods:
            * create_handler()
            * update_handler()

        Override the attrs:
            * source_class
            * source_url
            * source_url_detail
            * headings

    :cvar source_class: The widget entries data source class.
    :cvar source_url: Url to request the widget entries data.
    :cvar source_url_detail: Url to request the widget entry.
    :cvar headings: The entries table column name.

    :ivar btns_manage: The box of buttons for managing of entries.
    :ivar table: The table of entries list.
    :ivar btns_paginate: The box of buttons for managing of pagination.
    """

    source_class = None
    source_url = None
    source_url_detail = None
    headings = None

    def __init__(self) -> None:
        """Construct the table."""
        super().__init__()

        # The table entries (data).
        self.entry = self.source_class

        # The pagination urls.
        self._next_pagination_url = None
        self.current_pagination_url = None
        self._previous_pagination_url = None
        # The pagination buttons.
        self._btn_previous = BtnApp('<', on_press=self.previous_handler)
        self._btn_table_reload = BtnApp(
            'Обновить', on_press=self.reload_handler
        )
        self._btn_next = BtnApp('>', on_press=self.next_handler)
        # By default, the pagination buttons is disabled.
        self._btn_previous.enabled = False
        self._btn_next.enabled = False
        # Pagination buttons group.
        self.btns_paginate = toga.Box(
            children=[
                self._btn_previous, self._btn_table_reload, self._btn_next
            ]
        )  # fmt: skip

        # The table entries management buttons.
        self._btn_create = SmBtn('Добавить', on_press=self.create_handler)
        self._btn_update = SmBtn('Изменить', on_press=self.update_handler)
        self._btn_delete = SmBtn('Удалить', on_press=self.delete_handler)
        # Buttons group.
        self.btns_manage = toga.Box(
            children=[self._btn_create, self._btn_update, self._btn_delete],
        )

        # The table.
        self.table = BaseTable(
            headings=self.headings,
            data=self.entry,
            accessors=self.entry.accessors,
        )

    ####################################################################
    # Callback functions.

    def create_handler(self, widget: toga.Widget) -> None:
        """Create the entry, button handler.

        :param Widget widget: Widget that called the handler.
        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError(
            'Subclasses must provide a create_handler() method.'
        )

    def update_handler(self, widget: toga.Widget) -> None:
        """Update the entry, button handler.

        :param Widget widget: Widget that called the handler.
        :raises NotImplementedError: if the method is not overridden.
        """
        raise NotImplementedError(
            'Subclasses must provide a update_handler() method.'
        )

    async def delete_handler(self, _: toga.Widget) -> None:
        """Delete the entry, button handler."""
        try:
            entry = self.table.selection
        except IndexError:
            print('\nDEBUG: The entry is empty')
        else:
            url = self.source_url_detail % entry.id
            await request_delete_async(url)
            self.populate_table(self.current_pagination_url)

    def reload_handler(self, _: toga.Widget) -> None:
        """Update the table, button handler."""
        self.populate_table()

    def previous_handler(self, _: toga.Widget) -> None:
        """Populate the table by previous pagination, button handler."""
        self.populate_table(self.previous_pagination_url)

    def next_handler(self, _: toga.Widget) -> None:
        """Populate the table by next pagination, button handler."""
        self.populate_table(self.next_pagination_url)

    ####################################################################
    # Any methods.

    async def on_open(self, widget: toga.Widget) -> None:
        """Invoke the populate the table when the table opens."""
        if bool(self.current_pagination_url):
            self.populate_table(self.current_pagination_url)
        else:
            self.populate_table()

    def populate_table(self, url: str | None = None) -> None:
        """Populate the table on url request."""
        self.clear_table()
        entries = self.request_entries(url)
        for entry in entries:
            self.entry.add_entry(entry)

    def clear_table(self) -> None:
        """Clear the table."""
        self.table.data.clear()

    ####################################################################
    # Url methods.

    def request_entries(
        self,
        pagination_url: str | None = None,
    ) -> list[tuple[str, ...]]:
        """Request the entries to populate the table."""
        response = request_get(pagination_url or self.source_url)
        self.set_pagination_urls(response)
        payload = response.json()
        entries = to_entries(payload['results'])
        return entries

    def set_pagination_urls(self, response: Response) -> None:
        """Set pagination urls."""
        payload = response.json()
        self.next_pagination_url = payload['next']
        self.current_pagination_url = response.url
        self.previous_pagination_url = payload['previous']

    @property
    def next_pagination_url(self) -> str:
        """Next pagination url (`str`).

        Controls the active state of the previous pagination button.
        """
        return self._next_pagination_url

    @next_pagination_url.setter
    def next_pagination_url(self, value: str | None) -> None:
        self._next_pagination_url = value
        self._btn_next.enabled = bool(value)

    @property
    def previous_pagination_url(self) -> str:
        """Previous pagination url (`str`).

        Controls the active state of the previous pagination button.
        """
        return self._previous_pagination_url

    @previous_pagination_url.setter
    def previous_pagination_url(self, value: str | None) -> None:
        self._previous_pagination_url = value
        self._btn_previous.enabled = bool(value)
