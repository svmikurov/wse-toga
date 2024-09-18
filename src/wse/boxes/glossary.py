"""Glossary box."""

import toga

from wse import boxes, constants
from wse.boxes.base import BaseBox, goto_box_name


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

    @staticmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to Glossary box, button handler."""
        goto_box_name(widget, constants.GLOSSARY_BOX)
