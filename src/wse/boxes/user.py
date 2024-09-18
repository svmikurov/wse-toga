"""User box."""

import toga

from wse import base, boxes, constants


class UserBox(base.BaseBox):
    """User box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = base.BaseButton(
            text='На главную',
            on_press=boxes.MainBox.goto_box_handler,
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
        )

    @staticmethod
    def goto_box_handler(widget: toga.Button) -> None:
        """Go to User box, button handler."""
        base.goto_box_name(widget, constants.USER_BOX)
