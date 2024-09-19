"""WSE application."""

import toga

from wse import boxes, constants

BOXES = {
    constants.GLOSSARY_BOX: boxes.GlossaryBox,
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
