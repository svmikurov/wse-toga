"""Custom app widget."""

import toga
from toga.style.pack import Pack
from travertino.constants import ITALIC

from wse.constants import (
    ALIAS,
    BUTTON_HEIGHT,
    FONT_SIZE_APP,
    HUMANLY,
)


class TableApp(toga.Table):
    """General table app."""

    def __init__(self, *arge: object, **kwargs: object) -> None:
        """Construct the table."""
        super().__init__(*arge, **kwargs)
        self.style.padding = (14, 7, 7, 7)
        self.style.flex = 1
        self.font_style = ITALIC


class TextDisplay(toga.MultilineTextInput):
    """Exercise text display widget.

    :param str value: The initial content to display in the widget.
    :param bool readonly: Can the text be modified by the user?
    """

    def __init__(self, **kwargs: object) -> None:
        """Construct the widget."""
        style = Pack(
            padding=(0, 5, 0, 5),
        )
        kwargs['readonly'] = True
        kwargs['style'] = kwargs.get('style', style)
        super().__init__(**kwargs)

    def update(self, text: str | None) -> None:
        """Update text widget value.

        :param str text: Text to set as widget value.
        """
        self.value = text

    def clean(self) -> None:
        """Clear the value of the text widget."""
        self.value = ''


class TextInputApp(toga.TextInput):
    """Text input widget."""

    def __init__(self, **kwargs: object) -> None:
        """Construct the widget."""
        style = Pack(
            padding=(0, 0, 0, 0),
            height=BUTTON_HEIGHT,
            font_size=FONT_SIZE_APP,
        )
        kwargs['style'] = kwargs.get('style', style)
        super().__init__(**kwargs)

    def clean(self) -> None:
        """Clear the text input widget value."""
        self.value = None


class MulTextInpApp(toga.MultilineTextInput):
    """MultilineTextInput application widget."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the table."""
        super().__init__(*args, **kwargs)

    def clean(self) -> None:
        """Clear the text input widget value."""
        self.value = None


class BtnApp(toga.Button):
    """Custom button widget."""

    def __init__(
        self,
        text: str | None = None,
        on_press: toga.widgets.button.OnPressHandler | None = None,
        **kwargs: object,
    ) -> None:
        """Construct the box."""
        style = Pack(
            flex=1,
            height=BUTTON_HEIGHT,
            font_size=FONT_SIZE_APP,
        )
        kwargs['style'] = kwargs.get('style', style)
        super().__init__(text, on_press=on_press, **kwargs)


class SmBtn(toga.Button):
    """Small button app widget."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the button."""
        super().__init__(*args, **kwargs)
        self.style.flex = 1
        self.style.height = 45


class BaseSelection(toga.Selection):
    """Custom selection widget.

    :param list[dict] items: Initial items to display for selection.
    :param value: Initial value for the selection.
    :type value: str or None.
    :param str accessor: The accessor to use to extract display values
        from the list of items.
    :param str alias: Key for attribute on the selected item.
    """

    def __init__(self, **kwargs: object) -> None:
        """Construct the widget."""
        kwargs['accessor'] = HUMANLY
        super().__init__(**kwargs)
        self.alias = ALIAS

    def set_items(self, items: list[dict], value: str | None) -> None:
        """Set selection initial items and initial value to display.

        :param list[dict] items: Initial items to display for selection.
        :param value: Initial value for the selection.
        :type value: str or None.
        """
        # Set Selection items attr.
        self.items = items
        # Set Selection value attr.
        for index, selection in enumerate(items):
            if selection[self.alias] == value:
                self.value = self.items[index]

    def get_alias(self) -> str | int | list | None:
        """Get displayed value from selection."""
        return self.value.alias
