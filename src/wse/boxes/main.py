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
            on_press=lambda _: self.app.word_box.goto_box_handler(_),
        )
        btn_goto_user_box = base.BaseButton(
            'Учетная запись',
            on_press=lambda _: self.app.user_box.goto_box_handler(_),
        )
        btn_goto_glossary_box = base.BaseButton(
            'Глоссарий',
            on_press=lambda _: self.app.glossary_box.goto_box_handler(_),
        )

        # Widget DOM.
        self.add(
            btn_goto_user_box,
            btn_goto_word_box,
            btn_goto_glossary_box,
        )

    @classmethod
    def goto_box_handler(cls, widget: toga.Button) -> None:
        """Go to Main box, button handler."""
        base.goto_box_name(widget, constants.MAIN_BOX)
