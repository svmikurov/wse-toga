"""Foreign words page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from httpx import Response

from wse.boxes.base import BaseBox
from wse.constants import (
    FOREIGN_BOX,
    FOREIGN_CREATE_BOX,
    FOREIGN_DETAIL_PATH,
    FOREIGN_EXERCISE_BOX,
    FOREIGN_EXERCISE_PATH,
    FOREIGN_LIST_BOX,
    FOREIGN_PARAMS_BOX,
    FOREIGN_PARAMS_PATH,
    FOREIGN_PATH,
    FOREIGN_PROGRESS_PATH,
    FOREIGN_WORD,
    HOST_API,
    MAIN_BOX,
    NEXT,
    PREVIOUS,
    RESULTS,
    RUSSIAN_WORD,
)
from wse.contrib.http_requests import (
    request_get,
    request_post, request_delete_async,
)
from wse.contrib.utils import to_entries
from wse.forms.forms import (
    RequestCreateMixin,
    RequestHandler,
    RequestUpdateMixin, BaseForm,
)
from wse.sources.foreign import Word, WordSource
from wse.widgets.base import BtnApp, SmBtn, TableApp, TextInputApp
from wse.widgets.exercise import ExerciseBox, ExerciseParamsSelectionsBox


class ForeignMainPage(BaseBox):
    """Learning foreign words main box."""

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
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )
        btn_goto_create_box = BtnApp(
            'Добавить слово',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_CREATE_BOX),
        )
        btn_goto_list_box = BtnApp(
            'Словарь',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_LIST_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_main_box,
            btn_goto_params_box,
            btn_goto_create_box,
            btn_goto_list_box,
        )


class ForeignParamsPage(ExerciseParamsSelectionsBox):
    """Learning foreign words exercise parameters box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        btn_goto_foreign_exercise_box = BtnApp(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )
        btn_save_params = BtnApp(
            'Сохранить настройки',
            on_press=self.save_params_handler,
        )

        # Widget DOM.
        self.add(
            btn_goto_foreign_box,
            self.params_box,
            btn_save_params,
            btn_goto_foreign_exercise_box,
        )

    async def goto_exercise_box_handler(self, widget: toga.Widget) -> None:
        """Go to foreign exercise page box, button handler."""
        exercise_box = self.get_box(widget, FOREIGN_EXERCISE_BOX)
        exercise_box.task.params = self.lookup_conditions
        self.set_window_content(widget, exercise_box)
        await exercise_box.loop_task()

    def on_open(self) -> None:
        """Request and fill params data of box when box open."""
        url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
        response = request_get(url=url)
        if response.status_code == HTTPStatus.OK:
            self.lookup_conditions = response.json()

    def save_params_handler(self, _: toga.Widget) -> None:
        """Save Glossary Exercise parameters, button handler.

        Request to save user exercise parameters.
        """
        url = urljoin(HOST_API, FOREIGN_PARAMS_PATH)
        request_post(url, self.lookup_conditions)


class ForeignExercisePage(ExerciseBox):
    """Foreign exercise box.

    :ivar exercise_box: The ExerciseBox attr, container with exercise
        widgets.
    """

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.url_exercise = urljoin(HOST_API, FOREIGN_EXERCISE_PATH)
        self.url_progress = urljoin(HOST_API, FOREIGN_PROGRESS_PATH)

        # Buttons.
        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        btn_goto_params_box = BtnApp(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_foreign_box,
            btn_goto_params_box,
            self.exercise_box,
        )


class ForeignForm(BaseForm):
    """General form to create and update entries, the container."""

    btn_submit_name = 'Отправить'
    source_class = Word

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the container."""
        super().__init__(*args, **kwargs)

        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_LIST_BOX),
        )
        # Word data input widgets.
        self.russian_input = TextInputApp(placeholder='Слово на русском')
        self.foreign_input = TextInputApp(placeholder='Слово на иностранном')
        btn_submit = BtnApp(self.btn_submit_name, on_press=self.submit_handler)

        self.add(
            btn_goto_foreign_box,
            self.russian_input,
            self.foreign_input,
            btn_submit,
        )

    def on_open(self) -> None:
        """Focus to input field on open form."""
        self.input_field_focus()

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        self.russian_input.value = self.entry.russian_word
        self.foreign_input.value = self.entry.foreign_word

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        self.russian_input.clean()
        self.foreign_input.clean()

    def input_field_focus(self) -> None:
        """Focus to input field."""
        self.russian_input.focus()


class ForeignCreatePage(RequestCreateMixin, ForeignForm):
    """Add word to foreign dictionary."""

    url = urljoin(HOST_API, FOREIGN_PATH)
    success_http_status = HTTPStatus.CREATED
    btn_submit_name = 'Добавить'

    def get_form_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            FOREIGN_WORD: self.russian_input.value,
            RUSSIAN_WORD: self.foreign_input.value,
        }
        return submit_entry


class ForeignUpdatePage(RequestUpdateMixin, ForeignForm):
    """Update the foreign word the box."""

    url = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    btn_submit_name = 'Изменить'

    def handle_success(self, widget: toga.Widget) -> None:
        """Go to foreign list page, if success."""
        self.goto_box_handler(widget, FOREIGN_LIST_BOX)

    def get_form_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'id': str(self.entry.id),
            FOREIGN_WORD: self.russian_input.value,
            RUSSIAN_WORD: self.foreign_input.value,
        }
        return submit_entry


class ForeignListPage(BaseBox):
    """Foreign words list page."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # The table entries (data).
        self.term_source = WordSource()
        # The table entries source urls.
        self.source_url = urljoin(HOST_API, FOREIGN_PATH)
        self.delete_source_url = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
        self._next_pagination_url = None
        self.current_pagination_url = None
        self._previous_pagination_url = None

        # The navigation buttons.
        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
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

        # Table.
        self.table = TableApp(
            headings=['ID', 'Иностранный', 'Русский'],
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
        self.set_window_content(widget, self.root.app.foreign_create_box)

    def update_handler(self, widget: toga.Widget) -> None:
        """Update the entry, button handler."""
        entry = self.table.selection
        update_box = self.root.app.foreign_update_box
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
