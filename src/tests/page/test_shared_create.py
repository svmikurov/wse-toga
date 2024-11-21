"""Test widgets of create page boxes.

Testing:
 * Text representation of widgets in the window content.
 * Changing window contents when pressing move buttons.
 * Control the widget order at page.
"""

import pytest
from _pytest.fixtures import FixtureRequest

from wse.app import WSE
from wse.pages import CreateTermPage, CreateWordPage


def set_window_content(
    wse: WSE,
    box: CreateWordPage | CreateTermPage,
) -> None:
    """Assign the box with widgets to window content."""
    wse.main_window.content = box


@pytest.fixture
def box_foreign(wse: WSE) -> CreateWordPage:
    """Return the instance of CreateWordPage, fixture."""
    box = wse.box_foreign_create
    return box


@pytest.fixture
def box_glossary(wse: WSE) -> CreateTermPage:
    """Return the instance of CreateTermPage, fixture."""
    box = wse.box_glossary_create
    return box


@pytest.fixture(params=['box_foreign', 'box_glossary'])
def box(request: FixtureRequest) -> CreateWordPage | CreateTermPage:
    """Return the box fixtures one by one."""
    return request.getfixturevalue(request.param)


def test_foreign_widget_order(wse: WSE) -> None:
    """Test the widget orger at foreign create page box."""
    box = wse.box_foreign_create
    set_window_content(wse, box)

    expected_widget_order = [
        box.label_title,
        box.input_native,
        box.input_foreign,
        box.btn_submit,
        box.btn_goto_foreign_list,
        box.btn_goto_foreign_main,
    ]
    assert box.children == expected_widget_order


def test_glossary_widget_order(wse: WSE) -> None:
    """Test the widget order at glossary term create page box."""
    box = wse.box_glossary_create
    set_window_content(wse, box)

    assert box.children == [
        box.label_title,
        box.input_term,
        box.input_definition,
        box.btn_submit,
        box.btn_goto_glossary_list,
        box.btn_goto_glossary_main,
    ]


@pytest.mark.parametrize(
    'box_name, label_text',
    [
        ('box_foreign_create', 'Добавить слово'),
        ('box_glossary_create', 'Добавить термин'),
    ],
)
def test_label_title(box_name: str, label_text: str, wse: WSE) -> None:
    """Test the label title.

    Testing:
     * CreateWordPage and CreateTermPage classes;
     * that label has a specific text.

    """
    box: CreateWordPage | CreateTermPage = getattr(wse, box_name)

    # The label has a specific text.
    assert box.label_title.text == label_text
