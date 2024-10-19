"""Glossary page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga

from wse.constants import (
    GLOSSARY_BOX,
    GLOSSARY_CREATE_BOX,
    GLOSSARY_DETAIL_PATH,
    GLOSSARY_EXERCISE_BOX,
    GLOSSARY_EXERCISE_PATH,
    GLOSSARY_LIST_BOX,
    GLOSSARY_PARAMS_BOX,
    GLOSSARY_PARAMS_PATH,
    GLOSSARY_PATH,
    GLOSSARY_PROGRESS_PATH,
    HOST_API,
    MAIN_BOX,
)
from wse.contrib.http_requests import (
    HttpPostMixin,
    HttpPutMixin,
    request_get,
    request_post,
)
from wse.general.form import BaseForm
from wse.general.table import BaseTable
from wse.page.base import (
    BaseBox,
)
from wse.source.glossary import Term, TermSource
from wse.widget.base import BtnApp, MulTextInpApp
from wse.widget.exercise import (
    ExerciseBox,
    ExerciseParamsSelectionsBox,
)


class MainGlossaryPage(BaseBox):
    """Glossary main box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = BtnApp(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        btn_goto_params_box = BtnApp(
            'Упражнение',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_PARAMS_BOX),
        )
        btn_goto_create_box = BtnApp(
            'Добавить термин',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_CREATE_BOX),
        )
        btn_goto_list_box = BtnApp(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_LIST_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_params_box,
            btn_goto_create_box,
            btn_goto_list_box,
        )


class ParamsGlossaryBox(BaseBox):
    """Glossary box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_glossary_box = BtnApp(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_BOX),
        )
        btn_goto_glossary_exercise_box = BtnApp(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )
        btn_save_params = BtnApp(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )
        self.params_box = ExerciseParamsSelectionsBox()

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            self.params_box,
            btn_save_params,
            btn_goto_glossary_exercise_box,
        )

    async def goto_exercise_box_handler(self, widget: toga.Widget) -> None:
        """Go to glossary exercise, button handler."""
        exercise_box = self.get_box(widget, GLOSSARY_EXERCISE_BOX)
        try:
            exercise_box.lookup_conditions = self.params_box.lookup_conditions
        except AttributeError as error:
            await self.show_message('', 'Войдите в учетную запись')
            raise error
        else:
            self.set_window_content(widget, exercise_box)
            await exercise_box.show_task()

    def on_open(self) -> None:
        """Request and fill params data."""
        url = urljoin(HOST_API, GLOSSARY_PARAMS_PATH)
        response = request_get(url=url)
        if response.status_code == HTTPStatus.OK:
            self.params_box.fill_params(response.json())

    def save_params_handler(self, _: toga.Widget) -> None:
        """Save Glossary Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(HOST_API, GLOSSARY_PARAMS_PATH)
        request_post(url, self.params_box.lookup_conditions)


class ExerciseGlossaryBox(ExerciseBox):
    """English exercise box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.url_exercise = urljoin(HOST_API, GLOSSARY_EXERCISE_PATH)
        self.url_progress = urljoin(HOST_API, GLOSSARY_PROGRESS_PATH)

        # Buttons.
        btn_goto_glossary_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_BOX),
        )
        btn_goto_params_box = BtnApp(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_glossary_box,
            btn_goto_params_box,
            self.exercise_box,
        )


class FormGlossary(BaseForm):
    """General form to create and update entries, the container."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the clossary form."""
        super().__init__(*args, **kwargs)
        self._entry = Term

        btn_goto_foreign_box = BtnApp(
            'Глоссарий',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_LIST_BOX),
        )

        # Data input widgets.
        self.term = MulTextInpApp(placeholder='Терин')
        self.term.style.padding_bottom = 1
        self.definition = MulTextInpApp(placeholder='Определение')
        btn_submit = BtnApp(self.btn_submit_name, on_press=self.submit_handler)

        self.add(
            btn_goto_foreign_box,
            self.term,
            self.definition,
            btn_submit,
        )

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        self.term.value = self.entry.term
        self.definition.value = self.entry.definition

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        self.term.clean()
        self.definition.clean()

    def focus_to_input_field(self) -> None:
        """Focus to input field."""
        self.term.focus()


class CreateTermPage(HttpPostMixin, FormGlossary):
    """Glossary create page."""

    url = urljoin(HOST_API, GLOSSARY_PATH)
    btn_submit_name = 'Добавить'

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'term': self.term.value,
            'definition': self.definition.value,
        }
        return submit_entry


class UpdateTermPage(HttpPutMixin, FormGlossary):
    """Glossary update page."""

    url = urljoin(HOST_API, GLOSSARY_DETAIL_PATH)
    btn_submit_name = 'Изменить'

    def handle_success(self, widget: toga.Widget) -> None:
        """Go to glossary list page, if success."""
        self.goto_box_handler(widget, GLOSSARY_LIST_BOX)

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'id': str(self.entry.id),
            'term': self.term.value,
            'definition': self.definition.value,
        }
        return submit_entry


class ListTermPage(BaseTable):
    """Table of list of glossary terms, the page.

    :ivar Button btn_goto_foreign_box: Button go to Glossary Main page.
    """

    source_class = TermSource()
    source_url = urljoin(HOST_API, GLOSSARY_PATH)
    source_url_detail = urljoin(HOST_API, GLOSSARY_DETAIL_PATH)
    headings = ['ID', 'Термин', 'Толкование']

    def __init__(self) -> None:
        """Construct the page."""
        super().__init__()

        # The navigation buttons.
        self.btn_goto_foreign_box = BtnApp(
            'Словарь терминов',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_BOX),
        )

        # Page widgets DOM.
        self.add(
            self.btn_goto_foreign_box,
            self.btns_manage,
            self.table,
            self.btns_paginate,
        )

    def create_handler(self, widget: toga.Widget) -> None:
        """Go to create the term form, button handler."""
        self.goto_box_handler(widget, GLOSSARY_CREATE_BOX)

    def update_handler(self, widget: toga.Widget) -> None:
        """Go to update the term form, button handler."""
        entry = self.table.selection
        update_box = self.root.app.glossary_update_box
        update_box.entry = entry
        self.set_window_content(widget, update_box)
