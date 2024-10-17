"""Glossary page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response

from wse.boxes.base import (
    BaseBox,
)
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
    NEXT,
    PREVIOUS,
    RESULTS,
)
from wse.contrib.http_requests import (
    request_delete_async,
    request_get,
    request_post,
)
from wse.contrib.utils import to_entries
from wse.forms.forms import (
    RequestCreateMixin,
    RequestUpdateMixin, BaseForm,
)
from wse.sources.glossary import Term, TermSource
from wse.widgets.base import BtnApp, MulTextInpApp, SmBtn, TableApp
from wse.widgets.exercise import (
    ExerciseBox,
    ExerciseParamsSelectionsBox,
)


class GlossaryMainPage(BaseBox):
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


class GlossaryParamsBox(BaseBox):
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


class GlossaryExerciseBox(ExerciseBox):
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


class GlossaryFormContainer(BaseForm):
    """General form to create and update entries, the container."""

    btn_submit_name = 'Отправить'
    source_class = Term

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the container."""
        super().__init__(*args, **kwargs)

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

    def on_open(self) -> None:
        """Focus to input field on open form."""
        self.input_field_focus()

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        self.term.value = self.entry.term
        self.definition.value = self.entry.definition

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        self.term.clean()
        self.definition.clean()

    def input_field_focus(self) -> None:
        """Focus to input field."""
        self.term.focus()


class CreateTermPage(RequestCreateMixin, GlossaryFormContainer):
    """Glossary create page."""

    url = urljoin(HOST_API, GLOSSARY_PATH)
    success_http_status = HTTPStatus.CREATED
    btn_submit_name = 'Добавить'

    def get_form_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'term': self.term.value,
            'definition': self.definition.value,
        }
        return submit_entry


class UpdateTermPage(RequestUpdateMixin, GlossaryFormContainer):
    """Glossary update page."""

    url = urljoin(HOST_API, GLOSSARY_DETAIL_PATH)
    btn_submit_name = 'Изменить'

    def handle_success(self, widget: toga.Widget) -> None:
        """Go to foreign list page, if success."""
        self.goto_box_handler(widget, GLOSSARY_LIST_BOX)

    def get_form_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'id': str(self.entry.id),
            'term': self.term.value,
            'definition': self.definition.value,
        }
        return submit_entry


class ListTermPage(BaseBox):
    """Glossary list page."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # The table entries (data).
        self.term_source = TermSource()
        # The table entries source urls.
        self.source_url = urljoin(HOST_API, GLOSSARY_PATH)
        self.delete_source_url = urljoin(HOST_API, GLOSSARY_DETAIL_PATH)
        self._next_pagination_url = None
        self.current_pagination_url = None
        self._previous_pagination_url = None

        # The navigation buttons.
        btn_goto_foreign_box = BtnApp(
            'Словарь терминов',
            on_press=lambda _: self.goto_box_handler(_, GLOSSARY_BOX),
        )

        # The pagination buttons.
        self.btn_previous = BtnApp('<', on_press=self.previous_handler)
        btn_table_reload = BtnApp('Обновить', on_press=self.reload_handler)
        self.btn_next = BtnApp('>', on_press=self.next_handler)
        # By default, the pagination buttons is disabled.
        self.btn_previous.enabled = False
        self.btn_next.enabled = False
        # Buttons group.
        btns_paginate = [
            self.btn_previous, btn_table_reload, self.btn_next
        ]  # fmt: skip

        # The table entries management buttons.
        btn_create = SmBtn('Добавить', on_press=self.create_handler)
        btn_update = SmBtn('Изменить', on_press=self.update_handler)
        btn_delete = SmBtn('Удалить', on_press=self.delete_handler)
        # Buttons group.
        btns_manage = toga.Box(children=[btn_create, btn_update, btn_delete])

        # The table.
        self.table = TableApp(
            headings=['ID', 'Термин', 'Толкование'],
            data=self.term_source,
            accessors=self.term_source.accessors,
        )

        # Page widgets DOM.
        self.add(
            btn_goto_foreign_box,
            btns_manage,
            self.table,
            toga.Box(children=btns_paginate),
        )

    def on_open(self) -> None:
        """Populate the table when the table opens."""
        if bool(self.current_pagination_url):
            self.populate_table(self.current_pagination_url)
        else:
            self.populate_table()

    ####################################################################
    # Callback functions.

    def create_handler(self, widget: toga.Widget) -> None:
        """Create the entry, button handler."""
        self.set_window_content(widget, self.root.app.glossary_create_box)

    def update_handler(self, widget: toga.Widget) -> None:
        """Update the entry, button handler."""
        entry = self.table.selection
        update_box = self.root.app.glossary_update_box
        update_box.entry = entry
        self.set_window_content(widget, update_box)

    async def delete_handler(self, _: toga.Widget) -> None:
        """Delete the entry, button handler."""
        entry = self.table.selection
        url = self.delete_source_url % entry.id
        await request_delete_async(url)
        self.populate_table(self.current_pagination_url)

    def reload_handler(self, _: toga.Widget) -> None:
        """Update the table, button handler."""
        self.populate_table()

    def previous_handler(self, _: toga.Widget) -> None:
        """Populate the table by previous pagination, button handler."""
        self.populate_table(self.previous_pagination_url)

    def next_handler(self, _: toga.Widget) -> None:
        """Populate the table by next pagination, button handler."""
        self.populate_table(self.next_pagination_url)

    def populate_table(self, url: str | None = None) -> None:
        """Populate the table on url request."""
        self.clear_table()
        entries = self.request_entries(url)
        for entry in entries:
            self.term_source.add_entry(entry)

    def clear_table(self) -> None:
        """Clear the table."""
        self.table.data.clear()

    def is_table_populated(self) -> bool:
        """Check table is populated."""
        return bool(self.table.data)

    ####################################################################
    # Url

    def request_entries(
        self,
        pagination_url: str | None = None,
    ) -> list[tuple[str, ...]]:
        """Request the entries to populate the table."""
        response = request_get(pagination_url or self.source_url)
        self.set_pagination_urls(response)
        payload = response.json()
        return to_entries(payload[RESULTS])

    def set_pagination_urls(self, response: Response) -> None:
        """Set pagination urls."""
        payload = response.json()
        self.next_pagination_url = payload[NEXT]
        self.current_pagination_url = response.url
        self.previous_pagination_url = payload[PREVIOUS]

    @property
    def next_pagination_url(self) -> str:
        """Next pagination url (`str`).

        Controls the active state of the previous pagination button.
        """
        return self._next_pagination_url

    @next_pagination_url.setter
    def next_pagination_url(self, value: str | None) -> None:
        self._next_pagination_url = value
        self.btn_next.enabled = bool(value)

    @property
    def previous_pagination_url(self) -> str:
        """Previous pagination url (`str`).

        Controls the active state of the previous pagination button.
        """
        return self._previous_pagination_url

    @previous_pagination_url.setter
    def previous_pagination_url(self, value: str | None) -> None:
        self._previous_pagination_url = value
        self.btn_previous.enabled = bool(value)
