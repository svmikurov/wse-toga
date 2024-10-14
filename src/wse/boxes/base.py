"""Base box."""

import httpx
import toga
from httpx import Response
from travertino.constants import (
    CENTER,
    COLUMN,
)
from typing_extensions import Self

from wse.http_requests import app_auth


class GoToBoxMixin:
    """Go to page box mixin."""

    @classmethod
    def get_box(cls, widget: toga.Button, box_name: str) -> Self:
        """Get the page box by box name.

        Get the page box that was initialized in the app.
        """
        return widget.root.app.__getattribute__(box_name)

    @classmethod
    def set_window_content(cls, widget: toga.Button, box: Self) -> None:
        """Set page box to window content."""
        widget.window.content = box

    def goto_box_handler(self, widget: toga.Button, box_name: str) -> None:
        """Go to page box by box name, button handler.

        Invoke the :py:meth:`on_open` method when the current page box is
        assigned to the window content.

        :param toga.Button widget: The widget that generated the event.
        :param str box_name: The page box name to go.
        """
        box = self.get_box(widget, box_name)
        self.set_window_content(widget, box)
        box.on_open()

    @classmethod
    def on_open(cls) -> None:
        """Runs when the current box is assigned to the window content.

        Override it if it necessary to run same actions, then the
        current box is assigned to :term:`window content`.
        """
        pass


class MessageBoxMixin:
    """Dialog message mixin."""

    app: toga.App

    async def show_message(self, title: str, message: str) -> None:
        """Show dialog message."""
        await self.app.main_window.dialog(
            toga.InfoDialog(str(title), str(message))
        )


class HttpRequestMixin:
    """Http request mixin."""

    auth = app_auth

    @classmethod
    def request_get(cls, url: str) -> Response:
        """Send GET request."""
        with httpx.Client(auth=cls.auth) as client:
            response = client.get(url=url)
        return response

    @classmethod
    def request_post(cls, url: str, payload: dict) -> Response:
        """Send POST request."""
        with httpx.Client(auth=cls.auth) as client:
            response = client.post(url=url, json=payload)
        return response


class BaseBox(
    MessageBoxMixin,
    GoToBoxMixin,
    toga.Box,
):
    """Base page box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
        self.style.update(direction=COLUMN)


class BaseButton(toga.Button):
    """Base button.

    Assigns a common style to derived buttons.
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the button."""
        super().__init__(*args, **kwargs)
        self.style.update(flex=1)
        self.style.update(height=60)


class BaseLabel(toga.Label):
    """Base label.

    Assigns a common style to derived labels.
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the label."""
        super().__init__(*args, **kwargs)
        self.style.update(height=35)
        self.style.update(text_align=CENTER)
