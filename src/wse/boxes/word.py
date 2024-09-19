"""Word box."""

from wse import base
from wse import constants as const


class WordBox(base.BaseBox):
    """Word box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = base.BaseButton(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, const.MAIN_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
        )
