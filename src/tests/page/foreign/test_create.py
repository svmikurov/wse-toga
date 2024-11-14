"""Test widgets of create foreign word page box.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget order at page.
"""

import pytest
from _pytest.monkeypatch import MonkeyPatch

from tests.utils import run_until_complete
from wse.app import WSE
from wse.general.table import TableApp


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


def test_btn_submit(wse: WSE) -> None:
    """Test the submit button."""
    btn = wse.box_foreign_create.btn_submit
    assert btn.text == 'Добавить'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_create


def test_btn_goto_foreign_main(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.box_foreign_create.btn_goto_foreign_main
    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Иностранный'

    assert wse.main_window.content == wse.box_foreign_main


def request_entries(obj: object, url: str) -> list[tuple[str, ...]]:
    """Return entries to insert at table."""
    return [
        ('id', 'foreign', 'native'),
    ]


def test_btn_goto_foreign_list(
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test button to go to foreign list page box."""
    btn = wse.box_foreign_create.btn_goto_foreign_list

    monkeypatch.setattr(TableApp, 'request_entries', request_entries)

    btn._impl.simulate_press()

    # Run a fake main loop.
    run_until_complete(wse)

    assert btn.text == 'Словарь иностранных слов'

    assert wse.main_window.content == wse.box_foreign_list
