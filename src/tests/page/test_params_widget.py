"""Test widgets of foreign exercise params page box.

Testing:
 * Text representation of widgets in the window content
   (text on widget, placeholder text).
 * Changing window contents when pressing move buttons.
 * Control the order of widget and widget containers at page.

.. todo::

   * add test the inputs of box.box_params;
   * add test the populate of param widgets.

"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.monkeypatch import MonkeyPatch
from toga import NumberInput

from wse.app import WSE
from wse.general.button import BtnApp
from wse.general.selection import BaseSelection
from wse.page import ParamForeignPage, ParamGlossaryPage


def get_attr(
    instance: WSE | ParamForeignPage,
    attr_name: str,
) -> ParamForeignPage | ParamGlossaryPage | BtnApp | NumberInput:
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


def test_foreign_widget_order(
    wse: WSE,
    box_foreign: ParamForeignPage,
) -> None:
    """Test the widget and containers orger at params page."""
    box = box_foreign
    set_window_content(wse, box)

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

    # Selection widgets are parent box-container attr to flex layout.
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


def test_glossary_widget_order(
    wse: WSE,
    box_glossary: ParamGlossaryPage,
) -> None:
    """Test the widget and containers orger at params page."""
    box = box_glossary
    set_window_content(wse, box)

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


@pytest.mark.parametrize(
    'box_name, title_text',
    [
        ('box_foreign_params', 'Параметры изучения слов'),
        ('box_glossary_params', 'Параметры изучения терминов'),
    ],
)
def test_label_title(box_name: str, title_text: str, wse: WSE) -> None:
    """Test page box title.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * that label has a specific text.

    """
    box = get_attr(wse, box_name)

    # The label has a specific text.
    assert box.label_title.text == title_text


@pytest.mark.parametrize(
    'label_name, label_text',
    [
        ('label_start', 'Начало периода:'),
        ('label_end', 'Конец периода:'),
        ('label_category', 'Категория:'),
        ('label_progres', 'Стадия изучения:'),
    ],
)
def test_selections(
    label_name: str,
    label_text: str,
    box: ParamForeignPage | ParamGlossaryPage,
) -> None:
    """Test the selection widgets.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * test that label of selection has specific text.

    """
    label = get_attr(box, label_name)

    # Label of selection has specific text.
    assert label.text == label_text


@pytest.mark.parametrize(
    'switch_name, switch_text',
    [
        ('count_first_switch', 'Первые'),
        ('count_last_switch', 'Последние'),
    ],
)
def test_switches(
    switch_name: str,
    switch_text: str,
    box: ParamForeignPage | ParamGlossaryPage,
) -> None:
    """Test the switch widgets.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * test that switch has specific text.

    """
    switch = get_attr(box, switch_name)

    # Switch has specific text.
    assert switch.text == switch_text


def test_switch_toggles(box: ParamForeignPage | ParamGlossaryPage) -> None:
    """Test the switching.

    Test the switches to add item count (number input) to exercise
    params.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * test that switch is off by default;
     * test that toggle of first switch to set True;
     * test that toggle of last switch to set True;
     * test that toggle of last switch to set False.

    """
    # A switch is off by default.
    assert not box.count_first_switch.value
    assert not box.count_last_switch.value

    # Toggle the first switch to set True.
    box.count_first_switch.toggle()
    assert box.count_first_switch.value
    assert not box.count_last_switch.value

    # Toggle the last switch to True.
    box.count_last_switch.toggle()
    assert not box.count_first_switch.value
    assert box.count_last_switch.value

    # Toggle the last switch to set False.
    box.count_last_switch.toggle()
    assert not box.count_first_switch.value
    assert not box.count_last_switch.value


@pytest.mark.parametrize(
    'input_name',
    [
        ('input_count_first'),
        ('input_count_last'),
    ],
)
def test_number_inputs(
    input_name: str,
    box: ParamForeignPage | ParamGlossaryPage,
) -> None:
    """Test a number input widgets.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * that a number input has not initial value;
     * that a number input has an increment/decrement step of ten;
     * that a number input has a minimal value.

    """
    switch = get_attr(box, input_name)

    # A number input has not initial value.
    assert switch.value is None

    # A number input has an increment/decrement step of ten.
    assert switch.step == 10

    # A number input has a minimal value.
    assert switch.min == 0


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

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * that button has specific text;
     * that loop task of exercise was awaited;
     * that window content has been refreshed.

    Mocking:
     * get values from param selection widgets;
     * loop task of exercise.

    .. todo::

       Foreign params:
        * add test exercise_box.clean_text_panel()
        * add test exercise_box.task.status = None
        * add test exercise_box.task.params = self.lookup_conditions

       Glossary params:
        * add test exercise_box.task.params = self.lookup_conditions

    """
    box_params = get_attr(wse, box_name)
    box_exercise = get_attr(wse, box_togo)
    btn = box_params.btn_goto_exercise

    # Set the test box in the content window.
    set_window_content(wse, box_params)

    # Mock the get param value from widgets, otherwise test failed.
    monkeypatch.setattr(BaseSelection, 'get_alias', Mock(return_value=dict()))

    # Simulate a button press.
    btn._impl.simulate_press()

    # Run a fake main loop.
    wse.loop.run_until_complete(asyncio.sleep(0.5))

    # Button has specific text.
    assert btn.text == 'Начать упражнение'

    # The loop task of exercise was awaited.
    loop_task.assert_awaited()

    # The window content has been refreshed.
    assert wse.main_window.content == box_exercise


def test_btn_save_params(
    wse: WSE,
    box: ParamForeignPage | ParamGlossaryPage,
    monkeypatch: MonkeyPatch,
) -> None:
    """Test the save params button.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * that button has specific text;
     * that window content has not been refreshed.

    .. todo::

       Foreign params:
        * add test payload = self.lookup_conditions
        * add test self.request_put_async(url, payload)

       Glossary params:
        * add test payload = self.lookup_conditions
        * add test request_post(url, payload)

        * add test the call the functions in button handler.

    """
    btn = box.btn_save_params
    set_window_content(wse, box)

    # Mock the getting param value from widgets,
    # otherwise AttributeError.
    monkeypatch.setattr(BaseSelection, 'get_alias', Mock(return_value=dict()))

    # Simulate a button press.
    btn._impl.simulate_press()

    # Button has specific text.
    assert btn.text == 'Сохранить настройки'

    # The window content has not been refreshed.
    assert wse.main_window.content == box


@pytest.mark.parametrize(
    'box_name, box_togo, btn_name, btn_text',
    [
        (
            'box_foreign_params',
            'box_foreign_main',
            'btn_goto_foreign_main',
            'Иностранный',
        ),
        (
            'box_glossary_params',
            'box_glossary_main',
            'btn_goto_glossary_main',
            'Глоссарий',
        ),
    ],
)
def test_btn_goto_sub_main(
    box_name: str,
    box_togo: str,
    btn_name: str,
    btn_text: str,
    wse: WSE,
) -> None:
    """Test button to go to sub main page box.

    Test a go to foreign main and glossary main box-containers.

    Testing:
     * ParamForeignPage and ParamGlossaryPage classes;
     * that button has specific text;
     * that window content has not been refreshed.

    """
    box = get_attr(wse, box_name)
    box_next = get_attr(wse, box_togo)
    btn = get_attr(box, btn_name)

    # Set the test box in the content window.
    set_window_content(wse, box)

    # Simulate a button press.
    btn._impl.simulate_press()

    # The button has a specific text.
    assert btn.text == btn_text

    # The window content has not been refreshed.
    assert wse.main_window.content == box_next
