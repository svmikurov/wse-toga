"""Tests button handlers to switch window to specific box-container."""

import typing
from typing import Callable
from unittest.mock import Mock

import httpx
import pytest
from _pytest.monkeypatch import MonkeyPatch
from toga.handlers import simple_handler

from tests.utils import FixtureReader
from wse.app import WSE
from wse.handlers import goto_handler

MOCK_REQUEST_GET_SIMPLE = [httpx.Client, 'get']
"""To mock ``get`` method of ``httpx.Client`` (`list[object, str]`).
"""

MOCK_REQUEST_FOREIGN_LIST = [
    *MOCK_REQUEST_GET_SIMPLE,
    Mock(return_value=FixtureReader('pagination_foreign_center.json')),
]
MOCK_REQUEST_GLOSSARY_LIST = [
    *MOCK_REQUEST_GET_SIMPLE,
    Mock(return_value=FixtureReader('pagination_foreign_center.json')),
]


@pytest.mark.parametrize(
    """
    handler,
    box_container_name,
    box_target_name,
    button_name,
    mock_http_request
    """,
    [
        (
            goto_handler.goto_main_handler,
            'box_foreign_main',
            'box_main',
            'btn_goto_main',
            None,
        ),
        (
            goto_handler.goto_login_handler,
            'box_main',
            'box_login',
            'btn_goto_login',
            None,
        ),
        # Foreign
        (
            goto_handler.goto_foreign_main_handler,
            'box_main',
            'box_foreign_main',
            'btn_goto_foreign_main',
            '',
        ),
        (
            goto_handler.goto_foreign_create_handler,
            'box_foreign_main',
            'box_foreign_create',
            'btn_goto_create',
            None,
        ),
        (
            goto_handler.goto_foreign_update_handler,
            'box_foreign_list',
            'box_foreign_update',
            'btn_goto_update',
            None,
        ),
        (
            goto_handler.goto_foreign_params_handler,
            'box_foreign_main',
            'box_foreign_params',
            'btn_goto_params',
            None,
        ),
        (
            goto_handler.goto_foreign_list_handler,
            'box_foreign_main',
            'box_foreign_list',
            'btn_goto_list',
            MOCK_REQUEST_FOREIGN_LIST,
        ),
        (
            goto_handler.goto_foreign_exercise_handler,
            'box_foreign_params',
            'box_foreign_exercise',
            'btn_goto_exercise',
            None,
        ),
        # Glossary
        (
            goto_handler.goto_glossary_main_handler,
            'box_main',
            'box_glossary_main',
            'btn_goto_glossary_main',
            None,
        ),
        (
            goto_handler.goto_glossary_create_handler,
            'box_glossary_main',
            'box_glossary_create',
            'btn_goto_create',
            None,
        ),
        (
            goto_handler.goto_glossary_params_handler,
            'box_glossary_main',
            'box_glossary_params',
            'btn_goto_params',
            None,
        ),
        (
            goto_handler.goto_glossary_list_handler,
            'box_glossary_main',
            'box_glossary_list',
            'btn_goto_list',
            MOCK_REQUEST_GLOSSARY_LIST,
        ),
        (
            goto_handler.goto_glossary_exercise_handler,
            'box_glossary_params',
            'box_glossary_exercise',
            'btn_goto_exercise',
            None,
        ),
    ],
)
def test_goto_handler(
    handler: Callable,
    box_container_name: str,
    box_target_name: str,
    button_name: str,
    mock_http_request: typing.Iterable,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test button handlers to go to box-container.

    Test:
     * switching of window.
    """
    box = getattr(wse, box_container_name)
    box_togo = getattr(wse, box_target_name)
    button = getattr(box, button_name)
    wse.main_window.content = box

    if mock_http_request:
        monkeypatch.setattr(*mock_http_request)

    async def set_handler(*args: object, **kwargs: object) -> None:
        """Set the tested handler to invoke."""
        await handler(*args, **kwargs)

    wrapped = simple_handler(set_handler, button)

    # Invoke the handler.
    wse.loop.run_until_complete(wrapped(button))

    # The switching of window.
    assert wse.main_window.content == box_togo
