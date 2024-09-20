"""Base box."""

import toga
from travertino.constants import (
    CENTER,
    COLUMN,
)
from typing_extensions import Self


class GoToBoxMixin:
    """Go to box mixin."""

    @classmethod
    def get_box(cls, widget: toga.Button, box_name: str) -> Self:
        """Get the box that was initialized in the app."""
        return widget.root.app.__getattribute__(box_name)

    @classmethod
    def set_window_content(cls, widget: toga.Button, box: Self) -> None:
        """Set box to window content."""
        widget.window.content = box

    def goto_box_handler(self, widget: toga.Button, box_name: str) -> None:
        """Go to box by box name, button handler.

        Runs the ``on_open`` method when the current field
        is assigned to the window content.

        Parameters
        ----------
        widget : `toga.Button`
            The widget that generated the event.
        box_name : `str`
            Box name to go.

        """
        box = self.get_box(widget, box_name)
        self.set_window_content(widget, box)
        box.on_open()

    @classmethod
    def on_open(cls) -> None:
        """Run when the current box is assigned to the window content.

        Override to run box method then box assigned to window content.
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


class BaseBox(
    GoToBoxMixin,
    toga.Box,
):
    """Base box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
        self.style.update(direction=COLUMN)


class BaseButton(toga.Button):
    """Base button."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the button."""
        super().__init__(*args, **kwargs)
        self.style.update(flex=1)
        self.style.update(height=60)


class BaseLabel(toga.Label):
    """Base label."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the label."""
        super().__init__(*args, **kwargs)
        self.style.update(height=35)
        self.style.update(text_align=CENTER)
