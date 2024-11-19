"""Tests of button handlers to go to specific page box."""

from typing import Callable

import pytest
from toga.handlers import simple_handler

from wse.app import WSE
from wse.general import goto_handler as hl


@pytest.mark.parametrize(
    'handler, box_name, box_target, button_name',
    [
        (
            hl.goto_main_handler,
            'box_foreign_main',
            'box_main',
            'btn_goto_main',
        ),
        (
            hl.goto_login_handler,
            'box_main',
            'box_login',
            'btn_change_auth',
        ),
        # Foreign
        (
            hl.goto_foreign_main_handler,
            'box_main',
            'box_foreign_main',
            'btn_goto_foreign_main',
        ),
        (
            hl.goto_foreign_create_handler,
            'box_foreign_main',
            'box_foreign_create',
            'btn_goto_create',
        ),
        (
            hl.goto_foreign_params_handler,
            'box_foreign_main',
            'box_foreign_params',
            'btn_goto_params',
        ),
        (
            hl.goto_foreign_list_handler,
            'box_foreign_main',
            'box_foreign_list',
            'btn_goto_list',
        ),
        (
            hl.goto_foreign_exercise_handler,
            'box_foreign_params',
            'box_foreign_exercise',
            'btn_goto_exercise',
        ),
        # Glossary
        (
            hl.goto_glossary_main_handler,
            'box_main',
            'box_glossary_main',
            'btn_goto_glossary_main',
        ),
        (
            hl.goto_glossary_create_handler,
            'box_glossary_main',
            'box_glossary_create',
            'btn_goto_create',
        ),
        (
            hl.goto_glossary_params_handler,
            'box_glossary_main',
            'box_glossary_params',
            'btn_goto_params',
        ),
        (
            hl.goto_glossary_list_handler,
            'box_glossary_main',
            'box_glossary_list',
            'btn_goto_list',
        ),
        (
            hl.goto_glossary_exercise_handler,
            'box_glossary_params',
            'box_glossary_exercise',
            'btn_goto_exercise',
        ),
    ],
)
def test_goto_handler(
    handler: Callable,
    box_name: str,
    box_target: str,
    button_name: str,
    wse: WSE,
) -> None:
    """Test button handlers to go to main box-container.

    Test:
     * window switching.
    """
    box = getattr(wse, box_name)
    box_togo = getattr(wse, box_target)
    button = getattr(box, button_name)
    wse.main_window.content = box

    async def set_handler(*args: object, **kwargs: object) -> None:
        """Set the tested handler to invoke."""
        await handler(*args, **kwargs)

    wrapped = simple_handler(set_handler, button)

    # Invoke the handler.
    wse.loop.run_until_complete(wrapped(button))

    # Window switching.
    assert wse.main_window.content == box_togo
