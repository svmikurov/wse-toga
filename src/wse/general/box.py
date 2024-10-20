"""Base box widgets and methods."""

import toga
from toga.style.pack import COLUMN
from typing_extensions import Self

from wse.constants.settings import PADDING_SM


class BaseBox(toga.Box):
    """Base page box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
        self.style.direction = COLUMN
        self.style.padding = PADDING_SM
        self.style.flex = 1


class GoToBoxMixin:
    """Go to page box mixin."""

    @classmethod
    def get_box(cls, widget: toga.Widget, box_name: str) -> Self:
        """Get the page box by box name.

        Get the page box that was initialized in the app.
        """
        return widget.root.app.__getattribute__(box_name)

    @classmethod
    def set_window_content(cls, widget: toga.Widget, box: Self) -> None:
        """Set page box to window content."""
        widget.window.content = box

    def goto_box_handler(self, widget: toga.Widget, box_name: str) -> None:
        """Go to page box by box name, button handler.

        Invoke the :py:meth:`on_open` method when the current page box
        is assigned to the window content.

        :param toga.Button widget: The widget that generated the event.
        :param str box_name: The page box name to go.
        """
        box = self.get_box(widget, box_name)
        self.set_window_content(widget, box)
        box.on_open()

    def on_open(self) -> None:
        """Run when the current box is assigned to the window content.

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


class BoxApp(MessageBoxMixin, GoToBoxMixin, BaseBox):
    """Base page box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
