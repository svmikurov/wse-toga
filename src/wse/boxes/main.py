"""Main box."""

from wse import constants as const
from wse.boxes.base import BaseBox
from wse.boxes.widgets.base import BaseButton


class MainBox(BaseBox):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()

        # Widgets.
        btn_goto_user_box = BaseButton(
            'Учетная запись',
            on_press=lambda _: self.goto_box_handler(_, const.USER_BOX),
        )
        btn_goto_glossary_box = BaseButton(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, const.GLOSSARY_BOX),
        )
        btn_goto_foreign_box = BaseButton(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, const.FOREIGN_BOX),
        )

        # DOM.
        self.add(
            btn_goto_user_box,
            btn_goto_foreign_box,
            btn_goto_glossary_box,
            btn_goto_foreign_box,
        )
