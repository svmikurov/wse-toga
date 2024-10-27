"""WSE application."""

import toga

from wse import page
from wse.constants import (
    SCREEN_SIZE,
)
from wse.general.box_page import BoxApp


class WSE(toga.App):
    """WSE application."""

    # Page boxes.
    main_box: page.MainBox
    # Foreign language study page boxes.
    foreign_box: page.MainForeignPage
    foreign_params_box: page.ParamForeignPage
    foreign_exercise_box: page.ExerciseForeignPage
    foreign_create_box: page.CreateWordPage
    foreign_update_box: page.UpdateWordPage
    foreign_list_box: page.ListForeignPage
    # Glossary study page boxes.
    glossary_box: page.MainGlossaryPage
    glossary_params_box: page.ParamGlossaryBox
    glossary_exercise_box: page.ExerciseGlossaryBox
    glossary_create_box: page.CreateTermPage
    glossary_update_box: page.UpdateTermPage
    glossary_list_box: page.ListTermPage
    # Login box.
    login_box: page.LoginBox

    # Menu.
    menu: toga.Group
    cmd_goto_main: toga.Command
    cmd_goto_foreign: toga.Command
    cmd_goto_glossary: toga.Command

    def startup(self) -> None:
        """Initialise widgets to start application.

        * Initialises the page boxes.
        * Creates the app command menu.
        * Define the main window.
        """
        # Page boxes.
        self.main_box = page.MainBox()
        # Foreign language study page boxes.
        self.foreign_box = page.MainForeignPage()
        self.foreign_params_box = page.ParamForeignPage()
        self.foreign_exercise_box = page.ExerciseForeignPage()
        self.foreign_create_box = page.CreateWordPage()
        self.foreign_update_box = page.UpdateWordPage()
        self.foreign_list_box = page.ListForeignPage()
        # Glossary study page boxes.
        self.glossary_box = page.MainGlossaryPage()
        self.glossary_params_box = page.ParamGlossaryBox()
        self.glossary_exercise_box = page.ExerciseGlossaryBox()
        self.glossary_create_box = page.CreateTermPage()
        self.glossary_update_box = page.UpdateTermPage()
        self.glossary_list_box = page.ListTermPage()
        # Login box.
        self.login_box = page.LoginBox()

        # Menu.
        self.menu = toga.Group('Menu')
        # Menu commands.
        self.cmd_goto_main = toga.Command(
            self.goto_main,
            text='Главная страница',
            group=self.menu,
            order=1,
        )
        self.cmd_goto_foreign = toga.Command(
            self.goto_foreign,
            text='Иностранный словарь',
            group=self.menu,
            order=2,
        )
        self.cmd_goto_glossary = toga.Command(
            self.goto_glossary,
            text='Глоссарий',
            group=self.menu,
            order=3,
        )
        self.commands.add(
            self.cmd_goto_main,
            self.cmd_goto_glossary,
            self.cmd_goto_foreign,
        )

        # Main window.
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=toga.Size(*SCREEN_SIZE),
        )
        # Application start with Main page box content.
        self.main_window.content = self.main_box
        self.main_window.show()

    def move_to_page(self, box: BoxApp) -> None:
        """Move to page box."""
        self.main_window.content = box
        box.on_open()

    def goto_main(self, _: toga.Widget, **kwargs: object) -> None:
        """Goto main box, command handler."""
        self.move_to_page(self.main_box)

    def goto_glossary(self, _: toga.Widget, **kwargs: object) -> None:
        """Goto glossary box, command handler."""
        self.move_to_page(self.glossary_box)

    def goto_foreign(self, _: toga.Widget, **kwargs: object) -> None:
        """Goto foreign box, command handler."""
        self.move_to_page(self.foreign_box)


def main() -> WSE:
    """Return the app instance."""
    return WSE()
