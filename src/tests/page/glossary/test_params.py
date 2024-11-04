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
    set_window_content(wse, wse.box_glossary_params)


def test_widget_order(wse: WSE) -> None:
    """Test the widget and containers orger at glossary params page."""
    box = wse.box_glossary_params

    assert box.children == [
        box.label_title,
        box.box_params,
        box.btn_goto_exercise,
        box.btn_save_params,
        box.btn_goto_glossary_main,
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
    title = wse.box_glossary_params.label_title
    assert title.text == 'Параметры изучения терминов'


def test_btn_goto_exercise(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the submit button."""
    btn = wse.box_glossary_params.btn_goto_exercise
    assert btn.text == 'Начать упражнение'

    # Button handler runs the http request the task of exercise
    # and start the loop_task of exercise,
    # assigns the exercise box to window content.
    goto = Mock(side_effect=set_window_content(wse, wse.box_foreign_exercise))
    monkeypatch.setattr(btn, 'on_press', goto)

    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_exercise


def test_btn_save_params(wse: WSE, monkeypatch: MonkeyPatch) -> None:
    """Test the save params button."""
    btn = wse.box_glossary_params.btn_save_params
    assert btn.text == 'Сохранить настройки'

    # Button handler runs the http request to save params.
    goto = Mock()
    monkeypatch.setattr(btn, 'on_press', goto)

    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_glossary_params


def test_btn_goto_glossary_main(wse: WSE) -> None:
    """Test button to go to glossary main page box."""
    btn = wse.box_glossary_params.btn_goto_glossary_main
    assert btn.text == 'Глоссарий'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_glossary_main
