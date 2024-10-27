"""Main box."""

import toga
from toga.style import Pack

from wse import constants as const
from wse.constants import TITLE_MAIN, HOST_API
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.label import TitleLabel
from wse.page.user import UserAuth


class MainBox(UserAuth, BoxApp):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    welcome = f'Ready for connect to {HOST_API}'
    """Welcome text on the information display (`str`).
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()

        # Widgets.
        btn_goto_glossary_box = BtnApp(
            'Глоссарий терминов',
            on_press=lambda _: self.goto_box_handler(_, const.GLOSSARY_BOX),
        )
        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, const.FOREIGN_BOX),
        )

        # Info panel
        self.info_panel = toga.MultilineTextInput(
            readonly=True,
            placeholder=self.welcome,
            style=Pack(flex=1),
        )

        # DOM.
        self.add(
            TitleLabel(TITLE_MAIN),
            self.btn_goto_auth,  # UserAuth attr
            btn_goto_foreign_box,
            btn_goto_glossary_box,
            self.info_panel,
        )
