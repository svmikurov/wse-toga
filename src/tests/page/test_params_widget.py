"""Test widgets of foreign exercise params page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

.. todo::

   * add test the populate of param widgets.
"""

import asyncio
from unittest import skip
from unittest.mock import Mock, MagicMock, patch, AsyncMock

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch

from wse.app import WSE
from wse.general.selection import BaseSelection
from wse.page import ParamForeignPage, ParamGlossaryPage


def get_attr(
    instance: object,
    attr_name: str,
) -> ParamForeignPage | ParamGlossaryPage:
    """Get instance attribute by attribute name."""
    attr = instance.__getattribute__(attr_name)
    return attr


def set_window_content(
    wse: WSE,
    box: ParamForeignPage | ParamGlossaryPage,
) -> None:
    """Assign the box with widgets to window content."""
    wse.main_window.content = box


@pytest.fixture
def box_foreign(wse: WSE) -> ParamForeignPage:
    """Return the instance of ParamForeignPage, fixture."""
    box = wse.box_foreign_params
    return box


@pytest.fixture
def box_glossary(wse: WSE) -> ParamGlossaryPage:
    """Return the instance of ParamGlossaryPage, fixture."""
    box = wse.box_glossary_params
    return box


@pytest.fixture(params=['box_foreign', 'box_glossary'])
def box(request: FixtureRequest) -> ParamForeignPage | ParamGlossaryPage:
    """Return the box fixtures one by one."""
    return request.getfixturevalue(request.param)


# def mock_get_alias() -> dict:
#     """Mock th get alias from selection widgets."""
#     return


def test_widget_order(
    wse: WSE,
    box: ParamForeignPage | ParamGlossaryPage,
) -> None:
    """Test the widget and containers orger at params page."""
    box = wse.box_foreign_params

    assert box.children == [
        box.label_title,
        box.box_params,
        box.btn_goto_exercise,
        box.btn_save_params,
        box.btn_goto_foreign_main,
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


@pytest.mark.parametrize(
    'box_name, label_title',
    [
        ('box_foreign_params', 'Параметры изучения слов'),
        ('box_glossary_params', 'Параметры изучения терминов'),
    ],
)
def test_label_title(box_name: str, label_title: str, wse: WSE) -> None:
    """Test page box title."""
    box = get_attr(wse, box_name)
    assert box.label_title.text == label_title


@pytest.mark.parametrize(
    'box_name, box_togo',
    [
        ('box_foreign_params', 'box_foreign_exercise'),
        ('box_glossary_params', 'box_glossary_exercise'),
    ],
)
@patch('wse.container.exercise.ExerciseBox.loop_task', new_callable=AsyncMock)
def test_btn_goto_exercise(
    loop_task: AsyncMock,
    box_name: str,
    box_togo: str,
    wse: WSE,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the button to go to foreign exercise.

    Mocking:
    * get selection values from param selection widgets;
    * loop task of exercise.
    """
    box_params = get_attr(wse, box_name)
    box_exercise = get_attr(wse, box_togo)
    set_window_content(wse, box_params)
    btn = box_params.btn_goto_exercise

    # Mock the get param value from widgets, otherwise test failed.
    monkeypatch.setattr(BaseSelection, 'get_alias', Mock(return_value=dict()))

    # Simulate a button press.
    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.5))

    # Button has specific text.
    assert btn.text == 'Начать упражнение'

    # The loop task has been invoked.
    loop_task.assert_awaited()

    # The window content has been refreshed.
    assert wse.main_window.content == box_exercise


@skip
def test_btn_save_params(wse: WSE) -> None:
    """Test the save params button."""
    btn = wse.box_foreign_params.btn_save_params
    assert btn.text == 'Сохранить настройки'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_params


@skip
def test_btn_goto_foreign(wse: WSE) -> None:
    """Test button to go to foreign main page box."""
    btn = wse.box_foreign_params.btn_goto_foreign_main
    assert btn.text == 'Иностранный'
    btn._impl.simulate_press()
    assert wse.main_window.content == wse.box_foreign_main
