"""Test widgets of glossary exercise params page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

.. todo::

   * add test glossary exercise params - selection handlers;
   * add test glossary exercise params - save params handler.
"""

from unittest.mock import Mock

import pytest
import toga
from _pytest.monkeypatch import MonkeyPatch

from wse.app import WSE


def set_window_content(app: toga.App, box: toga.Widget) -> None:
    """Assign the specific page box to main window content."""
    app.main_window.content = box


@pytest.fixture(autouse=True)
def goto_glossary_params_page(wse: WSE) -> None:
    """Assign the glossary params box to main window content, fixture."""  # noqa: W505
    set_window_content(wse, wse.glossary_params_box)


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at glossary params page."""
    box = wse.glossary_params_box

    assert box.children == [
        box.title_label,
        box.param_box,
        box.btn_goto_exercise,
        box.btn_save_params,
        box.btn_goto_glossary,
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
    title = wse.glossary_params_box.title_label
    assert title.text == 'Параметры изучения терминов'


def test_btn_goto_foreign_exercise(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the submit button."""
    btn = wse.glossary_params_box.btn_goto_exercise
    assert btn.text == 'Начать упражнение'

    # Button handler runs the http request the task of exercise
    # and start the loop_task of exercise,
    # assigns the exercise box to window content.
    goto = Mock(side_effect=set_window_content(wse, wse.foreign_exercise_box))
    monkeypatch.setattr(btn, 'on_press', goto)

    btn._impl.simulate_press()
    assert wse.main_window.content == wse.foreign_exercise_box


def test_btn_save_params(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the save params button."""
    btn = wse.glossary_params_box.btn_save_params
    assert btn.text == 'Сохранить настройки'

    # Button handler runs the http request to save params.
    goto = Mock()
    monkeypatch.setattr(btn, 'on_press', goto)

    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_params_box


def test_btn_goto_glossary_box(wse: WSE) -> None:
    """Test button to go to glossary main page box."""
    btn = wse.glossary_params_box.btn_goto_glossary
    assert btn.text == 'Меню глоссария'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.glossary_box
