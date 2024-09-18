"""Word box."""

import toga

from wse import boxes, constants
from wse.boxes.base import BaseBox, goto_box_name


class WordBox(BaseBox):
    """Word box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = toga.Button(
            text='На главную',
            on_press=boxes.MainBox.goto_box_handler,
            style=self.btn_style,
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
        )

    @staticmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to current box, button handler."""
        goto_box_name(widget, constants.WORD_BOX)
