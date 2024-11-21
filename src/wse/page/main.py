"""Main box."""

import toga
from toga.style import Pack

from wse.constants import (
    BTN_GOTO_FOREIGN_MAIN,
    BTN_GOTO_GLOSSARY_MAIN,
    TITLE_MAIN,
)
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.goto_handler import (
    goto_foreign_exercise_handler,
    goto_foreign_main_handler,
    goto_glossary_exercise_handler,
    goto_glossary_main_handler,
)
from wse.general.label import TitleLabel
from wse.page.user import UserAuthMixin
from wse.source.text_panel_main import MainTextPanelSource
from wse.source.user import UserSource


class MainBox(UserAuthMixin, BoxApp):
    """Main box.

    Contains content that is displayed to the user
    when the application is launched.
    """

    def __init__(
        self,
        user: UserSource,
        input_info_main: MainTextPanelSource,
    ) -> None:
        """Construct the Main box."""
        super().__init__()
        self.user = user
        self.input_info_main = input_info_main

        # Widgets.
        self.label_title = TitleLabel(TITLE_MAIN)
        self.btn_goto_glossary_main = BtnApp(
            BTN_GOTO_GLOSSARY_MAIN,
            on_press=goto_glossary_main_handler,
        )
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN,
            on_press=goto_foreign_main_handler,
        )

        # Quick start of exercise.
        self.label_chapter_exercises = toga.Label(
            'Упражнения:',
            style=Pack(padding=(4, 0, 2, 2)),
        )
        self.btn_goto_foreign_exercise = BtnApp(
            'Изучение слов',
            on_press=goto_foreign_exercise_handler,
        )
        self.btn_goto_glossary_exercise = BtnApp(
            'Изучение терминов',
            on_press=goto_glossary_exercise_handler,
        )

        # Info panel
        self.info_panel = toga.MultilineTextInput(
            readonly=True, style=Pack(flex=1), value=self.input_info_main.value
        )

        # DOM.
        self.add(
            self.label_title,
            self.info_panel,
            self.btn_goto_login,  # attr from UserAuthMixin
            self.btn_goto_foreign_main,
            self.btn_goto_glossary_main,
            self.label_chapter_exercises,
            self.btn_goto_foreign_exercise,
            self.btn_goto_glossary_exercise,
        )
