"""WSE application."""

import toga

from wse import constants, page

BOXES = {
    constants.MAIN_BOX: page.MainBox,
    # Foreign language study page boxes.
    constants.FOREIGN_BOX: page.MainForeignPage,
    constants.FOREIGN_PARAMS_BOX: page.ParamsForeignPage,
    constants.FOREIGN_EXERCISE_BOX: page.ForeignExercisePage,
    constants.FOREIGN_CREATE_BOX: page.CreateForeignPage,
    constants.FOREIGN_UPDATE_BOX: page.UpdateForeignPage,
    constants.FOREIGN_LIST_BOX: page.ListForeignPage,
    # Glossary study page boxes.
    constants.GLOSSARY_BOX: page.MainGlossaryPage,
    constants.GLOSSARY_PARAMS_BOX: page.ParamsGlossaryBox,
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


def main() -> WSE:
    """Return the app instance."""
    return WSE()
