"""Foreign words page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga

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
    RUSSIAN_WORD,
)
from wse.contrib.http_requests import (
    HttpPostMixin,
    HttpPutMixin,
    request_get,
    request_post,
)
from wse.general.form import BaseForm
from wse.general.table import BaseTable
from wse.page.base import BoxApp
from wse.source.foreign import Word, WordSource
from wse.widget.base import BtnApp, TextInputApp
from wse.widget.exercise import ExerciseBox, ExerciseParamsSelectionsBox


class MainForeignPage(BoxApp):
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


class ParamsForeignPage(ExerciseParamsSelectionsBox):
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
        """Save Foreign Exercise parameters, button handler.

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


class FormForeign(BaseForm):
    """General form to create and update entries, the container."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the foreign form."""
        super().__init__(*args, **kwargs)
        self._entry = Word

        btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_LIST_BOX),
        )
        # Word data input widgets.
        self.russian_input = TextInputApp(placeholder='Слово на русском')
        self.russian_input.style.padding_bottom = 1
        self.foreign_input = TextInputApp(placeholder='Слово на иностранном')
        btn_submit = BtnApp(self.btn_submit_name, on_press=self.submit_handler)

        self.add(
            btn_goto_foreign_box,
            self.russian_input,
            self.foreign_input,
            btn_submit,
        )

    def populate_entry_input(self) -> None:
        """Populate the entry input widgets value."""
        self.russian_input.value = self.entry.russian_word
        self.foreign_input.value = self.entry.foreign_word

    def clear_entry_input(self) -> None:
        """Clear the entry input widgets value."""
        self.russian_input.clean()
        self.foreign_input.clean()

    def focus_to_input_field(self) -> None:
        """Focus to input field."""
        self.russian_input.focus()


class CreateForeignPage(HttpPostMixin, FormForeign):
    """Add word to foreign dictionary."""

    url = urljoin(HOST_API, FOREIGN_PATH)
    btn_submit_name = 'Добавить'

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            FOREIGN_WORD: self.foreign_input.value,
            RUSSIAN_WORD: self.russian_input.value,
        }
        return submit_entry


class UpdateForeignPage(HttpPutMixin, FormForeign):
    """Update the foreign word the box."""

    url = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    btn_submit_name = 'Изменить'

    def handle_success(self, widget: toga.Widget) -> None:
        """Go to foreign list page, if success."""
        self.goto_box_handler(widget, FOREIGN_LIST_BOX)

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            'id': str(self.entry.id),
            FOREIGN_WORD: self.foreign_input.value,
            RUSSIAN_WORD: self.russian_input.value,
        }
        return submit_entry


class ListForeignPage(BaseTable):
    """Table of list of foreign words, the page.

    :ivar Button btn_goto_foreign_box: Button go to Foreign Main page.
    """

    source_class = WordSource()
    source_url = urljoin(HOST_API, FOREIGN_PATH)
    source_url_detail = urljoin(HOST_API, FOREIGN_DETAIL_PATH)
    headings = ['ID', 'Иностранный', 'Русский']

    def __init__(self) -> None:
        """Construct the page."""
        super().__init__()

        # The navigation buttons.
        self.btn_goto_foreign_box = BtnApp(
            'Словарь иностранных слов',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )

        # Page widgets DOM.
        self.add(
            self.btn_goto_foreign_box,
            self.btns_manage,
            self.table,
            self.btns_paginate,
        )

    def create_handler(self, widget: toga.Widget) -> None:
        """Go to create the word form, button handler."""
        self.goto_box_handler(widget, FOREIGN_CREATE_BOX)

    def update_handler(self, widget: toga.Widget) -> None:
        """Go to create the word form, button handler."""
        entry = self.table.selection
        update_box = self.root.app.foreign_update_box
        update_box.entry = entry
        self.set_window_content(widget, update_box)
