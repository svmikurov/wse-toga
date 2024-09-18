"""Base box."""

import toga
from toga import Box, Button
from toga.style import Pack
from travertino.constants import (
    CENTER,
    COLUMN,
)

from wse import constants


class BaseBox(toga.Box):
    """Base box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box style.
        self.style.update(direction=COLUMN)

        # Widget styles.
        self.btn_style = Pack(
            flex=1,
            height=60,
        )
        self.label_style = Pack(
            height=35,
            text_align=CENTER,
        )

    @staticmethod
    def goto_box(widget: Button, box_name: str) -> None:
        """Show current box content in window.

        Switching between windows may require additional operations,
        such as retrieving data from the server to display it in the
        content. Add this method along with these operations to the
        switch button handler.

        Parameters
        ----------
        widget : `toga.Button`
            The widget that generated the event.
        box_name : `str`
            The name of current box.

        """
        box = get_box(widget, box_name)
        set_window_content(widget, box)

    @staticmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to current box, button handler."""
        pass


def get_box(widget: Button, box_name: str) -> BaseBox:
    """Get the box that was initialized in the app."""
    return widget.root.app.__getattribute__(box_name)

def set_window_content(widget: toga.Button, box: Box) -> None:
    """Set box to window content."""
    widget.window.content = box

def goto_box_name(widget, box_name) -> None:
    box = get_box(widget, box_name)
    set_window_content(widget, box)