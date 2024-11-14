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
    box_main: page.MainBox
    # Foreign language study page boxes.
    box_foreign_main: page.MainForeignPage
    box_foreign_params: page.ParamForeignPage
    box_foreign_exercise: page.ExerciseForeignPage
    box_foreign_create: page.CreateWordPage
    box_foreign_update: page.UpdateWordPage
    box_foreign_list: page.ListForeignPage
    # Glossary study page boxes.
    box_glossary_main: page.MainGlossaryPage
    box_glossary_params: page.ParamGlossaryPage
    box_glossary_exercise: page.ExerciseGlossaryPage
    box_glossary_create: page.CreateTermPage
    box_glossary_update: page.UpdateTermPage
    box_glossary_list: page.ListTermPage
    # Login box.
    box_login: page.LoginBox

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
        self.box_main = page.MainBox()
        # Foreign language study page boxes.
        self.box_foreign_main = page.MainForeignPage()
        self.box_foreign_params = page.ParamForeignPage()
        self.box_foreign_exercise = page.ExerciseForeignPage()
        self.box_foreign_create = page.CreateWordPage()
        self.box_foreign_update = page.UpdateWordPage()
        self.box_foreign_list = page.ListForeignPage()
        # Glossary study page boxes.
        self.box_glossary_main = page.MainGlossaryPage()
        self.box_glossary_params = page.ParamGlossaryPage()
        self.box_glossary_exercise = page.ExerciseGlossaryPage()
        self.box_glossary_create = page.CreateTermPage()
        self.box_glossary_update = page.UpdateTermPage()
        self.box_glossary_list = page.ListTermPage()
        # Login box.
        self.box_login = page.LoginBox()

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
        self.box_main.setup_user_status()
        self.box_main.update_widget_values()
        self.main_window.content = self.box_main
        self.main_window.show()

    def move_to_page(self, box: BoxApp) -> None:
        """Move to page box."""
        self.main_window.content = box
        box.on_open(box)

    def goto_main(self, _: toga.Widget, **kwargs: object) -> None:
        """Goto main box, command handler."""
        self.move_to_page(self.box_main)

    def goto_glossary(self, _: toga.Widget, **kwargs: object) -> None:
        """Goto glossary box, command handler."""
        self.move_to_page(self.box_glossary_main)

    def goto_foreign(self, _: toga.Widget, **kwargs: object) -> None:
        """Goto foreign box, command handler."""
        self.move_to_page(self.box_foreign_main)


def main() -> WSE:
    """Return the app instance."""
    return WSE()
