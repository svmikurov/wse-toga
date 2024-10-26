"""Main box."""

import toga
from toga.style import Pack

from wse import constants as const
from wse.constants import TITLE_MAIN
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.label import TitleLabel


class MainBox(BoxApp):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    def __init__(self) -> None:
        """Construct the Main box."""
        super().__init__()

        # Widgets.
        btn_goto_user_box = BtnApp(
            'Учетная запись',
            on_press=lambda _: self.goto_box_handler(_, const.USER_MAIN_BOX),
        )
        btn_goto_glossary_box = BtnApp(
            'Глоссарий терминов',
            on_press=lambda _: self.goto_box_handler(_, const.GLOSSARY_BOX),
        )
        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, const.FOREIGN_BOX),
        )

        # Debug
        btn_debug = BtnApp('Test request', on_press=self.debug_handler)
        self.debug_panel = toga.MultilineTextInput(
            readonly=True,
            placeholder='Ready ...',
            style=Pack(flex=1),
        )

        # DOM.
        self.add(
            TitleLabel(TITLE_MAIN),
            btn_goto_user_box,
            btn_goto_foreign_box,
            btn_goto_glossary_box,
            self.debug_panel,
            btn_debug,
        )

    def debug_handler(self, _: toga.Widget) -> None:
        """Test thr request, button handler."""
        pass
