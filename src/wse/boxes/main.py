"""Main box."""

from wse import base
from wse import constants as const


class MainBox(base.BaseBox):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()

        # Widgets.
        btn_goto_user_box = base.BaseButton(
            'Учетная запись',
            on_press=lambda _: self.goto_box_handler(_, const.USER_BOX),
        )
        btn_goto_glossary_box = base.BaseButton(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, const.GLOS_BOX),
        )
        btn_goto_foreign_box = base.BaseButton(
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
