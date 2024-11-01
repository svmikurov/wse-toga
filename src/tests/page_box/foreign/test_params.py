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
    wse.main_window.content = wse.foreign_params_box


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at foreign params page."""
    box = wse.foreign_params_box

    assert box.children == [
        box.title_label,
        box.param_box,
        box.btn_goto_foreign_exercise,
        box.btn_save_params,
        box.btn_goto_foreign,
    ]

    assert box.param_box.children == [
        box.selection_start_box,
        box.selection_end_box,
        box.selection_category_box,
        box.selection_progress_box,
        box.input_first_box,
        box.input_last_box,
    ]

    # Selection widgets are included in the parent box to flex layout.
    assert box.selection_start_box.children == [
        box.label_start.parent,
        box.start_period_selection.parent,
    ]
    assert box.selection_end_box.children == [
        box.label_end.parent,
        box.end_period_selection.parent,
    ]
    assert box.selection_category_box.children == [
        box.label_category.parent,
        box.category_selection.parent,
    ]
    assert box.selection_progress_box.children == [
        box.label_progres.parent,
        box.progress_selection.parent,
    ]
    assert box.input_first_box.children == [
        box.count_first_switch.parent,
        box.count_first_input.parent,
    ]
    assert box.input_last_box.children == [
        box.count_last_switch.parent,
        box.count_last_input.parent,
    ]


def test_title(wse: WSE) -> None:
    """Test page box title."""
    title = wse.foreign_params_box.title_label
    assert title.text == 'Параметры изучения слов'


def test_btn_goto_foreign_exercise(wse: WSE) -> None:
    """Test the submit button."""
    btn = wse.foreign_params_box.btn_goto_foreign_exercise
    assert btn.text == 'Начать упражнение'
    # btn._impl.simulate_press()
    # assert wse.main_window.content == wse.foreign_exercise_box


def test_btn_save_params(wse: WSE) -> None:
    """Test the save params button."""
    btn = wse.foreign_params_box.btn_save_params
    assert btn.text == 'Сохранить настройки'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_params_box


def test_btn_goto_foreign_box(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.foreign_params_box.btn_goto_foreign
    assert btn.text == 'Меню словаря'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_box
