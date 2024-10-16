"""Foreign words page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from toga.style import Pack

from wse.boxes.base import BaseBox
from wse.boxes.sources.foreign import WordSource
from wse.boxes.widgets.base import BaseButton, SmBtn, TextDisplay, TextInputApp
from wse.boxes.widgets.exercise import (
    ExerciseBox,
    ExerciseParamsSelectionsBox,
)
from wse.constants import (
    FOREIGN_BOX,
    FOREIGN_CREATE_BOX,
    FOREIGN_EXERCISE_BOX,
    FOREIGN_EXERCISE_PATH,
    FOREIGN_LIST_BOX,
    FOREIGN_PATH,
    FOREIGN_PARAMS_BOX,
    FOREIGN_PARAMS_PATH,
    FOREIGN_PROGRESS_PATH,
    FOREIGN_WORD,
    HOST_API,
    MAIN_BOX,
    NEXT,
    PREVIOUS,
    RESULTS,
    RUSSIAN_WORD,
    FOREIGN_DETAIL_PATH,
)
from wse.http_requests import (
    request_get,
    request_post,
    request_post_async,
)
from wse.utils import to_entries


class ForeignMainPage(BaseBox):
    """Learning foreign words main box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main_box = BaseButton(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        btn_goto_params_box = BaseButton(
            'Упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )
        btn_goto_create_box = BaseButton(
            'Добавить слово',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_CREATE_BOX),
        )
        btn_goto_list_box = BaseButton(
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
        btn_goto_foreign_box = BaseButton(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        btn_goto_foreign_exercise_box = BaseButton(
            'Начать упражнение',
            on_press=self.goto_exercise_box_handler,
        )
        btn_save_params = BaseButton(
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

    async def goto_exercise_box_handler(self, widget: toga.Button) -> None:
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

    def save_params_handler(self, _: toga.Button) -> None:
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
        btn_goto_foreign_box = BaseButton(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        btn_goto_params_box = BaseButton(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )

        # Widget DOM.
        self.add(
            btn_goto_foreign_box,
            btn_goto_params_box,
            self.exercise_box,
        )


class ForeignFormPage(BaseBox):
    """General edit foreign box."""

    url = ''
    """Entries source url path (`str`).
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)

        btn_goto_foreign_box = BaseButton(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )
        # Word data input widgets.
        self.russian_input = TextInputApp(placeholder='Слово на русском')
        self.foreign_input = TextInputApp(placeholder='Слово на иностранном')
        btn_submit = BaseButton('Добавить', on_press=self.submit_handler)

        self.add(
            btn_goto_foreign_box,
            self.russian_input,
            self.foreign_input,
            btn_submit,
        )

    async def submit_handler(self, _: toga.Widget) -> None:
        """Submit, button handler."""
        word_data = {
            FOREIGN_WORD: self.russian_input.value,
            RUSSIAN_WORD: self.foreign_input.value,
        }
        await request_post_async(self.url, word_data)
        self.clear_entry_input()
        self.russian_input.focus()

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        self.russian_input.clean()
        self.foreign_input.clean()


class ForeignCreatePage(ForeignFormPage):
    """Add word to foreign dictionary."""

    url = urljoin(HOST_API, FOREIGN_PATH)
    """Create foreign word the url path (`str`). 
    """


class ForeignUpdatePage(ForeignFormPage):
    """Update the foreign word the box."""

    url = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    """Update foreign word the url path (`str`). 
    """


class ForeignListPage(BaseBox):
    """Foreign words list page."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()
        self.source_url = urljoin(HOST_API, FOREIGN_PATH)
        self._next_pagination_url = None
        self._previous_pagination_url = None
        source_impl = WordSource()

        # Buttons.
        btn_goto_foreign_box = BaseButton(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )

        # Entry info display.
        self.info = TextDisplay()
        self.info.placeholder = 'Информация о выбранном слове'

        # Tha manage of entries.
        btn_create = SmBtn('Добавить', on_press=self.create_handler)
        btn_update = SmBtn('Изменить', on_press=self.update_handler)
        btn_delete = SmBtn('Удалить', on_press=self.delete_handler)
        btns_manage = toga.Box(children=[btn_create, btn_update, btn_delete])

        # Pagination.
        self.btn_previous = BaseButton('<', on_press=self.previous_handler)
        btn_table_reload = BaseButton('Обновить', on_press=self.reload_handler)
        btn_table_clear = BaseButton('Очистить', on_press=self.clear_handler)
        self.btn_next = BaseButton('>', on_press=self.next_handler)
        # By default, the pagination buttons is disabled.
        self.btn_previous.enabled = False
        self.btn_next.enabled = False

        # The bottom grope of buttons.
        btns_paginate = [
            self.btn_previous, btn_table_reload, btn_table_clear, self.btn_next
        ]  # fmt: skip

        # Table.
        self.table = toga.Table(
            headings=['ID', 'Иностранный', 'Русский'],
            data=source_impl,
            accessors=source_impl.accessors,
            style=Pack(flex=1),
            on_select=self.on_select_handler,
        )

        # Page widgets DOM.
        self.add(
            btn_goto_foreign_box,
            self.info,
            btns_manage,
            self.table,
            toga.Box(children=btns_paginate),
        )

    def on_open(self) -> None:
        """Populate the table when the table opens."""
        if not self.is_table_populated():
            self.populate_table()

    def previous_handler(self, _: toga.Button) -> None:
        """Populate the table by previous pagination, button handler."""
        self.populate_table(self.previous_pagination_url)

    def next_handler(self, _: toga.Button) -> None:
        """Populate the table by next pagination, button handler."""
        self.populate_table(self.next_pagination_url)

    def reload_handler(self, _: toga.Button) -> None:
        """Update the table."""
        self.populate_table()

    def clear_handler(self, _: toga.Button) -> None:
        """Clear the table."""
        self.clear_table()

    def populate_table(self, url: str | None = None) -> None:
        """Populate the table by url request."""
        self.clear_table()
        entries = self.request_entries(url)
        for entry in entries:
            self.table.data.add(entry)

    def clear_table(self) -> None:
        """Clear the table."""
        self.table.data.clear()

    def is_table_populated(self) -> bool:
        """Check table is populated."""
        return bool(self.table.data)

    ####################################################################
    # Tha manage of entries.

    def on_select_handler(self, widget: toga.Table, **kwargs: object) -> None:
        """Get entry on select event, button handler."""
        row = widget.selection
        self.info.value = (
            f'You selected row: {row.id}'
            if row is not None
            else 'No row selected'
        )

    def create_handler(self, widget: toga.Button) -> None:
        """Create the entry, button handler."""
        # Ahe mobile app change window content, desktop - open the new
        # window. NOTE: DD (Development Diversity)
        # Mobile:
        self.set_window_content(widget, self.root.app.foreign_create_box)

    def update_handler(self, widget: toga.Button) -> None:
        """Create the entry, button handler."""
        # Ahe mobile app change window content, desktop - open the new
        # window. NOTE: DD (Development Diversity)
        # Mobile:
        self.set_window_content(widget, self.root.app.foreign_update_box)

    def delete_handler(self, widget: toga.Button) -> None:
        """Create the entry, button handler."""
        pass

    ####################################################################
    # URL functions

    def request_entries(
        self,
        pagination_url: str | None = None,
    ) -> list[tuple[str, ...]]:
        """Request the entries to populate the table."""
        payload = request_get(pagination_url or self.source_url).json()
        self.next_pagination_url = payload[NEXT]
        self.previous_pagination_url = payload[PREVIOUS]
        return to_entries(payload[RESULTS])

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

    # End URL functions
    ###################
