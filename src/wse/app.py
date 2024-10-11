"""WSE application."""

import toga

from wse import boxes, constants

BOXES = {
    constants.MAIN_BOX: boxes.MainBox,
    # Foreign language study page boxes.
    constants.FOREIGN_BOX: boxes.ForeignBox,
    constants.FOREIGN_EXERCISE_BOX: boxes.ForeignExerciseBox,
    constants.FOREIGN_PARAMS_BOX: boxes.ForeignParamsBox,
    # Glossary study page boxes.
    constants.GLOS_BOX: boxes.GlossaryBox,
    constants.GLOS_PARAMS_BOX: boxes.GlossaryParamsBox,
    constants.GLOS_EXE_BOX: boxes.GlossaryExerciseBox,
    # User management page boxes.
    constants.LOGIN_BOX: boxes.LoginBox,
    constants.USER_CREATE_BOX: boxes.UserCreateBox,
    constants.USER_UPDATE_BOX: boxes.LoginBox,
    constants.USER_BOX: boxes.UserBox,
}
"""Boxes to add to ``main_window.content`` (`dict[str, toga.Box]`).

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
