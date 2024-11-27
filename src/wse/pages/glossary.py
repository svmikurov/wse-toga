"""Glossary page boxes."""

from urllib.parse import urljoin

import toga

from wse.constants import (
    BTN_GOTO_GLOSSARY_CREATE,
    BTN_GOTO_GLOSSARY_LIST,
    BTN_GOTO_GLOSSARY_MAIN,
    BTN_GOTO_GLOSSARY_PARAMS,
    BTN_GOTO_MAIN,
    GLOSSARY_DETAIL_PATH,
    GLOSSARY_EXERCISE_PATH,
    GLOSSARY_PARAMS_PATH,
    GLOSSARY_PATH,
    GLOSSARY_PROGRESS_PATH,
    HOST_API,
    TITLE_GLOSSARY_CREATE,
    TITLE_GLOSSARY_EXERCISE,
    TITLE_GLOSSARY_LIST,
    TITLE_GLOSSARY_MAIN,
    TITLE_GLOSSARY_PARAMS,
    TITLE_GLOSSARY_UPDATE,
)
from wse.container.exercise import (
    ExerciseBox,
    ExerciseParamSelectionsBox,
)
from wse.contrib.http_requests import (
    HttpPostMixin,
    HttpPutMixin,
)
from wse.handlers.goto_handler import (
    goto_glossary_create_handler,
    goto_glossary_exercise_handler,
    goto_glossary_list_handler,
    goto_glossary_main_handler,
    goto_glossary_params_handler,
    goto_main_handler,
)
from wse.source.glossary import Term, TermSource
from wse.widgets.box_page import (
    BoxApp,
)
from wse.widgets.button import BtnApp
from wse.widgets.form import BaseForm
from wse.widgets.label import TitleLabel
from wse.widgets.table import TableApp
from wse.widgets.text_input import MulTextInpApp


class MainGlossaryPage(BoxApp):
    """Glossary main box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        self.label_title = TitleLabel(TITLE_GLOSSARY_MAIN)
        self.btn_goto_main = BtnApp(BTN_GOTO_MAIN, on_press=goto_main_handler)
        self.btn_goto_params = BtnApp(
            BTN_GOTO_GLOSSARY_PARAMS,
            on_press=goto_glossary_params_handler,
        )
        self.btn_goto_create = BtnApp(
            BTN_GOTO_GLOSSARY_CREATE,
            on_press=goto_glossary_create_handler,
        )
        self.btn_goto_list = BtnApp(
            BTN_GOTO_GLOSSARY_LIST,
            on_press=goto_glossary_list_handler,
        )

        # Widget DOM.
        self.add(
            self.label_title,
            self.btn_goto_main,
            self.btn_goto_params,
            self.btn_goto_create,
            self.btn_goto_list,
        )


class ParamGlossaryPage(ExerciseParamSelectionsBox):
    """Glossary page box."""

    title = TITLE_GLOSSARY_PARAMS
    url = urljoin(HOST_API, GLOSSARY_PARAMS_PATH)
    """Learning glossary term exercise parameters url (`str`).
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        self.btn_goto_glossary_main = BtnApp(
            BTN_GOTO_GLOSSARY_MAIN,
            on_press=goto_glossary_main_handler,
        )

        # Widget DOM.
        self.insert(4, self.btn_goto_glossary_main)

    async def goto_box_exercise_handler(self, widget: toga.Widget) -> None:
        """Go to glossary exercise, button handler."""
        await goto_glossary_exercise_handler(widget)


class ExerciseGlossaryPage(ExerciseBox):
    """Glossary exercise page box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.url_exercise = urljoin(HOST_API, GLOSSARY_EXERCISE_PATH)
        self.url_progress = urljoin(HOST_API, GLOSSARY_PROGRESS_PATH)

        # Widgets.
        self.label_title = TitleLabel(TITLE_GLOSSARY_EXERCISE)
        self.btn_goto_params = BtnApp(
            'Параметры упражнения',
            on_press=goto_glossary_params_handler,
        )

        # Widget DOM.
        self.add(
            self.label_title,
            self.box_exercise,
            self.btn_goto_params,
        )

    def get_box_params(self) -> ParamGlossaryPage:
        """Get box instance with exercise params."""
        return self.root.app.box_glossary_params


class FormGlossary(BaseForm):
    """General form to create and update entries, the container."""

    title = ''
    """Page box title (`str`).
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the glossary form."""
        super().__init__(*args, **kwargs)
        self._entry = Term

        # Widgets.
        self.label_title = TitleLabel(text=self.title)
        self.btn_goto_glossary_list = BtnApp(
            BTN_GOTO_GLOSSARY_LIST,
            on_press=goto_glossary_list_handler,
        )
        self.btn_goto_glossary_main = BtnApp(
            BTN_GOTO_GLOSSARY_MAIN,
            on_press=goto_glossary_main_handler,
        )

        # Data input widgets.
        self.input_term = MulTextInpApp(placeholder='Термин')
        self.input_term.style.padding_bottom = 1
        self.input_definition = MulTextInpApp(placeholder='Определение')
        self.btn_submit = BtnApp(
            self.btn_submit_text, on_press=self.submit_handler
        )

        self.add(
            self.label_title,
            self.input_term,
            self.input_definition,
            self.btn_submit,
            self.btn_goto_glossary_list,
            self.btn_goto_glossary_main,
        )

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        self.input_term.value = self.entry.input_term
        self.input_definition.value = self.entry.input_definition

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        self.input_term.clean()
        self.input_definition.clean()

    def focus_to_input_field(self) -> None:
        """Focus to input field."""
        self.input_term.focus()


class CreateTermPage(HttpPostMixin, FormGlossary):
    """Glossary create page."""

    title = TITLE_GLOSSARY_CREATE
    url = urljoin(HOST_API, GLOSSARY_PATH)
    btn_submit_text = 'Добавить'

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'term': self.input_term.value,
            'definition': self.input_definition.value,
        }
        return submit_entry


class UpdateTermPage(HttpPutMixin, FormGlossary):
    """Glossary update page."""

    title = TITLE_GLOSSARY_UPDATE
    url = urljoin(HOST_API, GLOSSARY_DETAIL_PATH)
    btn_submit_name = 'Изменить'

    def handle_success(self, widget: toga.Widget) -> None:
        """Go to glossary list page, if success."""
        goto_glossary_list_handler(widget)

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'id': str(self.entry.id),
            'term': self.input_term.value,
            'definition': self.input_definition.value,
        }
        return submit_entry


class ListTermPage(TableApp):
    """Table of list of glossary terms, the page.

    :ivar Button label_title: The page title.
    :ivar Button btn_goto_glossary_main: Button go to Glossary Main
        page.
    """

    source_class = TermSource()
    source_url = urljoin(HOST_API, GLOSSARY_PATH)
    source_url_detail = urljoin(HOST_API, GLOSSARY_DETAIL_PATH)
    headings = [
        'ID',
        'Термин',
        'Толкование',
    ]

    def __init__(self) -> None:
        """Construct the page."""
        super().__init__()

        # Widgets.
        self.label_title = TitleLabel(TITLE_GLOSSARY_LIST)
        self.btn_goto_glossary_main = BtnApp(
            BTN_GOTO_GLOSSARY_MAIN,
            on_press=goto_glossary_main_handler,
        )

        # Page widgets DOM.
        self.add(
            self.label_title,
            self.btn_goto_glossary_main,
            self.btns_manage,
            self.table,
            self.btns_paginate,
        )

    def create_handler(self, widget: toga.Widget) -> None:
        """Go to create the term form, button handler."""
        goto_glossary_create_handler(widget)

    def update_handler(self, widget: toga.Widget) -> None:
        """Go to update the term form, button handler."""
        entry = self.table.selection
        box = self.root.app.box_glossary_update
        box.entry = entry
        self.set_window_content(widget, box)
