"""Tests of button handlers to go to specific page box."""

from toga.handlers import simple_handler

from wse.app import WSE
from wse.general.goto_handler import goto_foreign_exercise_handler


def test_goto_foreign_exercise(wse: WSE) -> None:
    """Test button handler to go to foreign exercise box-container."""
    button = wse.box_main.btn_goto_foreign_exercise

    async def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method to invoke."""
        await goto_foreign_exercise_handler(*args, **kwargs)

    wrapped = simple_handler(handler, button)

    # Invoke the handler.
    wse.loop.run_until_complete(wrapped('btn'))

    # Window switching.
    assert wse.main_window.content == wse.box_foreign_exercise


def test_goto_foreign_exercise(wse: WSE) -> None:
    """Test button handler to go to foreign exercise box-container."""
    button = wse.box_main.btn_goto_foreign_exercise

    async def handler(*args: object, **kwargs: object) -> None:
        """Set the tested method to invoke."""
        await goto_foreign_exercise_handler(*args, **kwargs)

    wrapped = simple_handler(handler, button)

    # Invoke the handler.
    wse.loop.run_until_complete(wrapped('btn'))

    # Window switching.
    assert wse.main_window.content == wse.box_foreign_exercise
