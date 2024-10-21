"""General app text input."""

import toga
from toga.style import Pack
from travertino.constants import ITALIC

from wse.constants import (
    BUTTON_HEIGHT,
    FONT_SIZE_APP,
    TEXT_DISPLAY_FONT_SIZE,
    TEXT_DISPLAY_FONT_STYLE,
)


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
        style = Pack(
            padding=(2, 0, 2, 0),
            font_style=ITALIC,
        )
        kwargs['style'] = kwargs.get('style', style)
        super().__init__(*args, **kwargs)

    def clean(self) -> None:
        """Clear the text input widget value."""
        self.value = None


class TextDisplay(toga.MultilineTextInput):
    """Exercise text display widget.

    :param str value: The initial content to display in the widget.
    :param bool readonly: Can the text be modified by the user?
    """

    def __init__(self, **kwargs: object) -> None:
        """Construct the widget."""
        style = Pack(
            padding=(2, 2, 2, 2),
            font_size=TEXT_DISPLAY_FONT_SIZE,
            font_style=TEXT_DISPLAY_FONT_STYLE,
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
        self.value = None
