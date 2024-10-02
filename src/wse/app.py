"""WSE application."""

import toga

from wse import boxes, constants

BOXES = {
    constants.FOREIGN_BOX: boxes.EnglishBox,
    constants.FOREIGN_EXERCISE_BOX: boxes.EnglishExerciseBox,
    constants.FOREIGN_PARAMS_BOX: boxes.EnglishParamsBox,
    constants.GLOS_BOX: boxes.GlossaryBox,
    constants.GLOS_PARAMS_BOX: boxes.GlossaryParamsBox,
    constants.GLOS_EXE_BOX: boxes.GlossaryExerciseBox,
    constants.LOGIN_BOX: boxes.LoginBox,
    constants.MAIN_BOX: boxes.MainBox,
    constants.USER_BOX: boxes.UserBox,
    constants.WORD_BOX: boxes.WordBox,
}


class WSE(toga.App):
    """WSE application."""

    main_box: toga.Box

    def startup(self) -> None:
        """Construct the main window and initialize the boxes."""
        # Initialize the box widgets.
        for box_name, box_class in BOXES.items():
            setattr(self, box_name, box_class())

        # Application start with Main box content.
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()


def main() -> WSE:
    """Return the app instance."""
    return WSE()
