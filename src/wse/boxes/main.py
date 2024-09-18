"""Main box."""

import toga

from wse import constants
from wse.boxes.base import BaseBox, get_box, set_window_content, goto_box_name


class MainBox(BaseBox):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()

        # Box widgets.
        btn_goto_word_box = toga.Button(
            'Словарь',
            on_press=self.goto_word_box_handler,
            style=self.btn_style,
        )
        btn_goto_user_box = toga.Button(
            'Учетная запись',
            on_press=self.goto_user_box_handler,
            style=self.btn_style,
        )
        btn_goto_glossary_box = toga.Button(
            'Глоссарий',
            on_press=self.goto_glossary_box_handler,
            style=self.btn_style,
        )

        # Widget DOM.
        self.add(
            btn_goto_user_box,
            btn_goto_word_box,
            btn_goto_glossary_box,
        )

    @staticmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to current box, button handler."""
        goto_box_name(widget, constants.MAIN_BOX)

    def goto_user_box_handler(self, widget: toga.Button) -> None:
        """Go to User box, button handler."""
        self.goto_box(widget, constants.USER_BOX)

    def goto_word_box_handler(self, widget: toga.Button) -> None:
        """Go to Word box, button handler."""
        self.goto_box(widget, constants.WORD_BOX)

    def goto_glossary_box_handler(self, widget: toga.Button) -> None:
        """Go to Glossary box, button handler."""
        self.goto_box(widget, constants.GLOSSARY_BOX)
