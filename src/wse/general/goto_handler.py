"""Button handlers to go to specific page box."""

import toga

from wse.general.box_page import BoxApp


async def set_window_content(
    widget: toga.Widget,
    box: BoxApp | toga.Box,
) -> None:
    """Set page box in window content."""
    widget.app.main_window.content = box
    try:
        await box.on_open(widget)
    except AttributeError:
        pass


async def goto_main(widget: toga.Widget) -> None:
    """Go to main."""
    box = widget.root.app.box_main
    await set_window_content(widget, box)


async def goto_login(widget: toga.Widget) -> None:
    """Go to log in."""
    box = widget.root.app.box_login
    await set_window_content(widget, box)


########################################################################
# Glossary


async def goto_foreign_main(widget: toga.Widget) -> None:
    """Go to foreign main."""
    box = widget.root.app.box_foreign_main
    await set_window_content(widget, box)


async def goto_foreign_create(widget: toga.Widget) -> None:
    """Go to foreign create."""
    box = widget.root.app.box_foreign_create
    await set_window_content(widget, box)


async def goto_foreign_params(widget: toga.Widget) -> None:
    """Go to foreign params."""
    box = widget.root.app.box_foreign_params
    await set_window_content(widget, box)


async def goto_foreign_list(widget: toga.Widget) -> None:
    """Go to foreign list."""
    box = widget.root.app.box_foreign_list
    await set_window_content(widget, box)


async def goto_foreign_exercise(widget: toga.Widget) -> None:
    """Go to foreign exercise."""
    box = widget.root.app.box_foreign_exercise
    await set_window_content(widget, box)


########################################################################
# Glossary


async def goto_glossary_main(widget: toga.Widget) -> None:
    """Go to glossary main."""
    box = widget.root.app.box_glossary_main
    await set_window_content(widget, box)


async def goto_glossary_params(widget: toga.Widget) -> None:
    """Go to glossary params."""
    box = widget.root.app.box_glossary_params
    await set_window_content(widget, box)


async def goto_glossary_create(widget: toga.Widget) -> None:
    """Go to glossary create."""
    box = widget.root.app.box_glossary_create
    await set_window_content(widget, box)


async def goto_glossary_list(widget: toga.Widget) -> None:
    """Go to glossary list."""
    box = widget.root.app.box_glossary_list
    await set_window_content(widget, box)


async def goto_glossary_exercise(widget: toga.Widget) -> None:
    """Go to glossary exercise."""
    box = widget.root.app.box_glossary_exercise
    await set_window_content(widget, box)
