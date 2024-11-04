"""Test widgets of foreign exercise params page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

.. todo::

   * add test foreign exercise params - selection handlers;
   * add test foreign exercise params - start foreign exercise;
   * add test foreign exercise params - save params handler.
"""

import pytest

from wse.app import WSE


@pytest.fixture(autouse=True)
def goto_foreign_params_page(wse: WSE) -> None:
    """Assign the foreign params box to main window content, fixture."""
    wse.main_window.content = wse.box_foreign_params


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at foreign params page."""
    box = wse.box_foreign_params

    assert box.children == [
        box.label_title,
        box.box_params,
        box.btn_goto_exercise,
        box.btn_save_params,
        box.btn_goto_foreign,
    ]

    assert box.box_params.children == [
        box.box_selection_start,
        box.box_selection_end,
        box.box_selection_category,
        box.box_selection_progress,
        box.box_input_first,
        box.box_input_last,
    ]

    # Selection widgets are included in the parent box to flex layout.
    assert box.box_selection_start.children == [
        box.label_start.parent,
        box.selection_start_period.parent,
    ]
    assert box.box_selection_end.children == [
        box.label_end.parent,
        box.selection_end_period.parent,
    ]
    assert box.box_selection_category.children == [
        box.label_category.parent,
        box.selection_category.parent,
    ]
    assert box.box_selection_progress.children == [
        box.label_progres.parent,
        box.selection_progress.parent,
    ]
    assert box.box_input_first.children == [
        box.count_first_switch.parent,
        box.input_count_first.parent,
    ]
    assert box.box_input_last.children == [
        box.count_last_switch.parent,
        box.input_count_last.parent,
    ]


def test_label_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.box_foreign_params.label_title
    assert title.text == 'Параметры изучения слов'


def test_btn_goto_exercise(wse: WSE) -> None:
    """Test the button to go to foreign exercise."""
    btn = wse.box_foreign_params.btn_goto_exercise
    assert btn.text == 'Начать упражнение'
    # btn._impl.simulate_press()
    # assert wse.main_window.content == wse.box_foreign_exercise


def test_btn_save_params(wse: WSE) -> None:
    """Test the save params button."""
    btn = wse.box_foreign_params.btn_save_params
    assert btn.text == 'Сохранить настройки'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_params


def test_btn_goto_foreign(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.box_foreign_params.btn_goto_foreign
    assert btn.text == 'Меню словаря'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_main
