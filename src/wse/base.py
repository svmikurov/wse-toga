"""Base box."""

import abc

import toga
from travertino.constants import (
    CENTER,
    COLUMN,
)


def get_box(widget: toga.Button, box_name: str) -> toga.Box:
    """Get the box that was initialized in the app."""
    return widget.root.app.__getattribute__(box_name)


def set_window_content(widget: toga.Button, box: toga.Box) -> None:
    """Set box to window content."""
    widget.window.content = box


def goto_box_name(widget: toga.Button, box_name: str) -> None:
    """Go to box by box name, button handler.

    Parameters
    ----------
    widget : `toga.Button`
        The widget that generated the event.
    box_name : `str`
        The name of box.

    """
    box = get_box(widget, box_name)
    set_window_content(widget, box)


class GoToBoxMixin(abc.ABC):
    """Go to current box mixin."""

    @staticmethod
    @abc.abstractmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to current box by box name, button handler.

        Override this method.

        Switching between windows may require additional operations,
        such as retrieving data from the server to display it in the
        content. Add this method along with these operations to the
        switch button handler.

        Parameters
        ----------
        widget : `toga.Button`
            The widget that generated the event.

        Example
        -------
        @staticmethod
        def goto_box_handler(widget: toga.Button) -> None:
            goto_box_name(widget, constants.MAIN_BOX)

        """
        pass


class BaseBox(
    GoToBoxMixin,
    toga.Box,
    abc.ABC,
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
