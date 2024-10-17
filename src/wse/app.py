"""WSE application."""

import toga

from wse import boxes, constants

BOXES = {
    constants.MAIN_BOX: boxes.MainBox,
    # Foreign language study page boxes.
    constants.FOREIGN_BOX: boxes.ForeignMainPage,
    constants.FOREIGN_PARAMS_BOX: boxes.ForeignParamsPage,
    constants.FOREIGN_EXERCISE_BOX: boxes.ForeignExercisePage,
    constants.FOREIGN_CREATE_BOX: boxes.ForeignCreatePage,
    constants.FOREIGN_UPDATE_BOX: boxes.ForeignUpdatePage,
    constants.FOREIGN_LIST_BOX: boxes.ForeignListPage,
    # Glossary study page boxes.
    constants.GLOSSARY_BOX: boxes.GlossaryMainPage,
    constants.GLOSSARY_PARAMS_BOX: boxes.GlossaryParamsBox,
    constants.GLOSSARY_EXERCISE_BOX: boxes.GlossaryExerciseBox,
    constants.GLOSSARY_CREATE_BOX: boxes.CreateTermPage,
    constants.GLOSSARY_UPDATE_BOX: boxes.UpdateTermPage,
    constants.GLOSSARY_LIST_BOX: boxes.ListTermPage,
    # User management page boxes.
    constants.LOGIN_BOX: boxes.LoginBox,
    constants.USER_CREATE_BOX: boxes.UserCreateBox,
    constants.USER_UPDATE_BOX: boxes.LoginBox,
    constants.USER_BOX: boxes.UserBox,
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
