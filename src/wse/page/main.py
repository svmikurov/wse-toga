"""Main box."""

import toga
from toga.style import Pack

from wse.constants import (
    BTN_GOTO_FOREIGN_MAIN,
    BTN_GOTO_GLOSSARY_MAIN,
    FOREIGN_MAIN_BOX,
    GLOSSARY_MAIN_BOX,
    HOST_API,
    TITLE_MAIN,
)
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
        self.label_title = TitleLabel(TITLE_MAIN)
        self.btn_goto_glossary_main = BtnApp(
            BTN_GOTO_GLOSSARY_MAIN,
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_MAIN_BOX),  # noqa: E501
        )
        self.btn_goto_foreign_main = BtnApp(
            BTN_GOTO_FOREIGN_MAIN,
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_MAIN_BOX),  # noqa: E501
        )

        # Quick start of exercise.
        self.label_chapter_exercises = toga.Label(
            'Упражнения:',
            style=Pack(padding=(4, 0, 2, 2)),
        )
        self.btn_goto_foreign_exercise = BtnApp(
            'Изучение слов',
            on_press= self.goto_foreign_exercise_handler,
        )
        self.btn_goto_glossary_exercise = BtnApp(
            'Изучение терминов',
            on_press= self.goto_glossary_exercise_handler,
        )

        # Info panel
        self.info_panel = toga.MultilineTextInput(
            readonly=True,
            placeholder=self.welcome,
            style=Pack(flex=1),
        )

        # DOM.
        self.add(
            self.label_title,
            self.info_panel,
            self.btn_goto_auth,  # UserAuth attr
            self.btn_goto_foreign_main,
            self.btn_goto_glossary_main,
            self.label_chapter_exercises,
            self.btn_goto_foreign_exercise,
            self.btn_goto_glossary_exercise,
        )

    async def goto_foreign_exercise_handler(self, widget: toga.Widget) -> None:
        """Start foreign exercise, button handler."""
        box_params = widget.root.app.box_foreign_params
        box_params.on_open()
        await box_params.goto_box_exercise_handler(widget)

        box_exercise = widget.root.app.box_foreign_exercise
        self.set_window_content(widget, box_exercise)
        await box_exercise.loop_task()

    async def goto_glossary_exercise_handler(self, widget: toga.Widget) -> None:
        """Start foreign exercise, button handler."""
        box_params = widget.root.app.box_glossary_params
        box_params.on_open()
        await box_params.goto_box_exercise_handler(widget)

        box_exercise = widget.root.app.box_glossary_exercise
        self.set_window_content(widget, box_exercise)
        await box_exercise.loop_task()