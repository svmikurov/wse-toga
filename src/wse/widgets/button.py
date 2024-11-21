"""General app buttons."""

import toga
from toga.style import Pack

from wse.constants import BUTTON_HEIGHT, FONT_SIZE_APP


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
