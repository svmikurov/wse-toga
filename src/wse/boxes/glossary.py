"""Glossary box."""

import toga

from wse import constants, boxes
from wse.boxes.base import BaseBox


class GlossaryBox(BaseBox):
    """Glossary box."""

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

    def goto_main_box_handler(self, widget: toga.Button) -> None:
        """Go to Main box, button handler."""
        self.goto_box(widget, constants.MAIN_BOX)
