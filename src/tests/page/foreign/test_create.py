"""Test widgets of create foreign word page box.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget order at page.
"""

from unittest.mock import AsyncMock, patch

import pytest

from tests.utils import run_until_complete
from wse.app import WSE
from wse.page import CreateWordPage, ListForeignPage


@pytest.fixture(autouse=True)
def goto_foreign_create_page(wse: WSE) -> None:
    """Assign the foreign create box to main window content."""
    wse.main_window.content = wse.box_foreign_create


def test_widget_order(wse: WSE) -> None:
    """Test the widget orger at foreign create page box."""
    box = wse.box_foreign_create
    expected_widget_order = [
        box.label_title,
        box.input_native,
        box.input_foreign,
        box.btn_submit,
        box.btn_goto_foreign_list,
        box.btn_goto_foreign_main,
    ]
    assert box.children == expected_widget_order


def test_input_native(wse: WSE) -> None:
    """Test the native word input field."""
    input_native = wse.box_foreign_create.input_native
    assert input_native.placeholder == 'Слово на русском'
    assert input_native.enabled is True


def test_input_foreign(wse: WSE) -> None:
    """Test the foreign word input field."""
    input_foreign = wse.box_foreign_create.input_foreign
    assert input_foreign.placeholder == 'Слово на иностранном'
    assert input_foreign.enabled is True


@patch.object(CreateWordPage, 'request_post_async', new_callable=AsyncMock)
def test_btn_submit(
    request_post_async: AsyncMock,
    wse: WSE,
) -> None:
    """Test the submit button."""
    btn = wse.box_foreign_create.btn_submit
    btn._impl.simulate_press()

    run_until_complete(wse)

    assert btn.text == 'Добавить'
    assert wse.main_window.content == wse.box_foreign_create

    request_post_async.assert_awaited()


def test_btn_goto_foreign_main(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.box_foreign_create.btn_goto_foreign_main
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Иностранный'

    assert wse.main_window.content == wse.box_foreign_main


@patch.object(ListForeignPage, 'on_open')
def test_btn_goto_foreign_list(
    on_open: AsyncMock,
    wse: WSE,
) -> None:
    """Test button to go to foreign list page box.

    Mock:
     * ``on_open`` method of ListForeignPage, otherwise http request.
    """
    btn = wse.box_foreign_create.btn_goto_foreign_list

    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Словарь иностранных слов'

    assert wse.main_window.content == wse.box_foreign_list
