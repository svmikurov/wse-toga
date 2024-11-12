"""Button handlers to go to specific page box."""

import toga


def set_window_content(widget: toga.Widget, box: toga.Box) -> None:
    """Set page box to window content."""
    widget.app.main_window.content = box


def goto_main(widget: toga.Widget) -> None:
    """Go to main."""
    box = widget.root.app.box_main
    set_window_content(widget, box)


def goto_login(widget: toga.Widget) -> None:
    """Go to login."""
    box = widget.root.app.box_login
    set_window_content(widget, box)


########################################################################
# Glossary


def goto_foreign_main(widget: toga.Widget) -> None:
    """Go to foreign main."""
    box = widget.root.app.box_foreign_main
    set_window_content(widget, box)


def goto_foreign_create(widget: toga.Widget) -> None:
    """Go to foreign create."""
    box = widget.root.app.box_foreign_create
    set_window_content(widget, box)


def goto_foreign_params(widget: toga.Widget) -> None:
    """Go to foreign params."""
    box = widget.root.app.box_foreign_params
    set_window_content(widget, box)


def goto_foreign_list(widget: toga.Widget) -> None:
    """Go to foreign list."""
    box = widget.root.app.box_foreign_list
    set_window_content(widget, box)


########################################################################
# Glossary


def goto_glossary_main(widget: toga.Widget) -> None:
    """Go to glossary main."""
    box = widget.root.app.box_glossary_main
    set_window_content(widget, box)


def goto_glossary_params(widget: toga.Widget) -> None:
    """Go to glossary params."""
    box = widget.root.app.box_glossary_params
    set_window_content(widget, box)


def goto_glossary_create(widget: toga.Widget) -> None:
    """Go to glossary create."""
    box = widget.root.app.box_glossary_create
    set_window_content(widget, box)


def goto_glossary_list(widget: toga.Widget) -> None:
    """Go to glossary list."""
    box = widget.root.app.box_glossary_list
    set_window_content(widget, box)
