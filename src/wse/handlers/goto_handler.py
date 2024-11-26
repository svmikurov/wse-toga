"""Button handlers to go to specific page box."""

import toga

from wse.widgets.box_page import BoxApp


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


async def goto_main_handler(widget: toga.Widget) -> None:
    """Go to main, button handler."""
    box = widget.root.app.box_main
    await set_window_content(widget, box)


async def goto_login_handler(widget: toga.Widget) -> None:
    """Go to log in, button handler."""
    box = widget.root.app.box_login
    await set_window_content(widget, box)


########################################################################
# Foreign


async def goto_foreign_main_handler(widget: toga.Widget) -> None:
    """Go to foreign main, button handler."""
    box = widget.root.app.box_foreign_main
    await set_window_content(widget, box)


async def goto_foreign_create_handler(widget: toga.Widget) -> None:
    """Go to foreign create, button handler."""
    box = widget.root.app.box_foreign_create
    await set_window_content(widget, box)


async def goto_foreign_update_handler(widget: toga.Widget) -> None:
    """Go to foreign update, button handler."""
    box = widget.root.app.box_foreign_update
    await set_window_content(widget, box)


async def goto_foreign_params_handler(widget: toga.Widget) -> None:
    """Go to foreign params, button handler."""
    box = widget.root.app.box_foreign_params
    await set_window_content(widget, box)


async def goto_foreign_list_handler(widget: toga.Widget) -> None:
    """Go to foreign list, button handler."""
    box = widget.root.app.box_foreign_list
    await set_window_content(widget, box)


async def goto_foreign_exercise_handler(widget: toga.Widget) -> None:
    """Go to foreign exercise, button handler."""
    box = widget.root.app.box_foreign_exercise
    await set_window_content(widget, box)


########################################################################
# Glossary


async def goto_glossary_main_handler(widget: toga.Widget) -> None:
    """Go to glossary main, button handler."""
    box = widget.root.app.box_glossary_main
    await set_window_content(widget, box)


async def goto_glossary_params_handler(widget: toga.Widget) -> None:
    """Go to glossary params, button handler."""
    box = widget.root.app.box_glossary_params
    await set_window_content(widget, box)


async def goto_glossary_create_handler(widget: toga.Widget) -> None:
    """Go to glossary create, button handler."""
    box = widget.root.app.box_glossary_create
    await set_window_content(widget, box)


async def goto_glossary_list_handler(widget: toga.Widget) -> None:
    """Go to glossary list, button handler."""
    box = widget.root.app.box_glossary_list
    await set_window_content(widget, box)


async def goto_glossary_exercise_handler(widget: toga.Widget) -> None:
    """Go to glossary exercise, button handler."""
    box = widget.root.app.box_glossary_exercise
    await set_window_content(widget, box)
