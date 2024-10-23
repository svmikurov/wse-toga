"""WSE application."""

import toga

from wse import constants, page

BOXES = {
    constants.MAIN_BOX: page.MainBox,
    # Foreign language study page boxes.
    constants.FOREIGN_BOX: page.MainForeignPage,
    constants.FOREIGN_PARAMS_BOX: page.ParamForeignPage,
    constants.FOREIGN_EXERCISE_BOX: page.ExerciseForeignPage,
    constants.FOREIGN_CREATE_BOX: page.CreateWordPage,
    constants.FOREIGN_UPDATE_BOX: page.UpdateWordPage,
    constants.FOREIGN_LIST_BOX: page.ListForeignPage,
    # Glossary study page boxes.
    constants.GLOSSARY_BOX: page.MainGlossaryPage,
    constants.GLOSSARY_PARAMS_BOX: page.ParamGlossaryBox,
    constants.GLOSSARY_EXERCISE_BOX: page.ExerciseGlossaryBox,
    constants.GLOSSARY_CREATE_BOX: page.CreateTermPage,
    constants.GLOSSARY_UPDATE_BOX: page.UpdateTermPage,
    constants.GLOSSARY_LIST_BOX: page.ListTermPage,
    # User management page boxes.
    constants.USER_MAIN_BOX: page.MainUserBox,
    constants.USER_CREATE_BOX: page.CreateUserBox,
    constants.USER_UPDATE_BOX: page.UpdateUserBox,
    constants.LOGIN_BOX: page.LoginBox,
}
"""The box-container contents to add to ``main_window.content``
(`dict[str, toga.Box]`).

Fields:
  - box name: box instance
"""


class WSE(toga.App):
    """WSE application."""

    main_box: toga.Box

    def startup(self) -> None:
        """Construct the main window and initialize the page boxes."""
        # Initialize the page box widgets.
        for box_name, box_class in BOXES.items():
            setattr(self, box_name, box_class())

        # Application start with Main page box content.
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Commands
        menu = toga.Group('Menu')
        cmd_goto_main = toga.Command(
            self.goto_main,
            text='Главная страница',
            group=menu,
            order=1,
        )
        cmd_goto_user = toga.Command(
            self.goto_user,
            text='Учетная запись',
            group=menu,
            order=2,
        )
        cmd_goto_foreign = toga.Command(
            self.goto_foreign,
            text='Иностранный словарь',
            group=menu,
            order=3,
        )
        cmd_goto_glossary = toga.Command(
            self.goto_glossary,
            text='Глоссарий',
            group=menu,
            order=4,
        )
        self.app.commands.add(
            cmd_goto_main, cmd_goto_user, cmd_goto_glossary, cmd_goto_foreign
        )

    def set_window_content(self, box: toga.Box) -> None:
        self.main_window.content = box

    def goto_main(self, widget, **kwargs) -> None:
        self.set_window_content(self.main_box)

    def goto_glossary(self, widget, **kwargs) -> None:
        self.set_window_content(self.glossary_box)

    def goto_user(self, widget, **kwargs) -> None:
        self.set_window_content(self.user_box)

    def goto_foreign(self, widget, **kwargs) -> None:
        self.set_window_content(self.foreign_box)

def main() -> WSE:
    """Return the app instance."""
    return WSE()
