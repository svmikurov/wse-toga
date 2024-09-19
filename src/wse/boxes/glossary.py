"""Glossary box."""

import toga

from wse import base, boxes, constants


class GlossaryBox(base.BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = base.BaseButton(
            text='На главную',
            on_press=lambda _: self.app.main_box.goto_box_handler(_),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
        )

    @classmethod
    def goto_box_handler(cls, widget: toga.Button) -> None:
        """Go to Glossary box, button handler."""
        base.goto_box_name(widget, constants.GLOSSARY_BOX)
