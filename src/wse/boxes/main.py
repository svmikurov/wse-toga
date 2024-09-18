"""Main box."""

import toga

from wse import base, boxes, constants


class MainBox(base.BaseBox):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()

        # Box widgets.
        btn_goto_word_box = base.BaseButton(
            'Словарь',
            on_press=boxes.WordBox.goto_box_handler,
        )
        btn_goto_user_box = base.BaseButton(
            'Учетная запись',
            on_press=boxes.UserBox.goto_box_handler,
        )
        btn_goto_glossary_box = base.BaseButton(
            'Глоссарий',
            on_press=boxes.GlossaryBox.goto_box_handler,
        )

        # Widget DOM.
        self.add(
            btn_goto_user_box,
            btn_goto_word_box,
            btn_goto_glossary_box,
        )

    @staticmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to Main box, button handler."""
        base.goto_box_name(widget, constants.MAIN_BOX)
