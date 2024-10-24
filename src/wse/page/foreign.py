"""Foreign words page boxes."""

from http import HTTPStatus
from urllib.parse import urljoin

import toga
from toga import MultilineTextInput
from toga.style import Pack

from wse.constants import (
    ASSESSMENT,
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
    TITLE_FOREIGN_CREATE,
    TITLE_FOREIGN_EXERCISE,
    TITLE_FOREIGN_LIST,
    TITLE_FOREIGN_MAIN,
    TITLE_FOREIGN_PARAMS,
    TITLE_FOREIGN_UPDATE,
)
from wse.container.exercise import ExerciseBox, ExerciseParamSelectionsBox
from wse.contrib.http_requests import (
    HttpPostMixin,
    HttpPutMixin,
    request_get,
    request_post,
)
from wse.general.box_page import BoxApp
from wse.general.button import BtnApp
from wse.general.form import BaseForm
from wse.general.label import TitleLabel
from wse.general.table import TableApp
from wse.general.text_input import TextInputApp
from wse.source.foreign import Word, WordSource


class MainForeignPage(BoxApp):
    """Learning foreign words main box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_main = BtnApp(
            text='На главную',
            on_press=lambda _: self.goto_box_handler(_, MAIN_BOX),
        )
        btn_goto_params = BtnApp(
            'Упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )
        btn_goto_create = BtnApp(
            'Добавить слово',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_CREATE_BOX),
        )
        btn_goto_list = BtnApp(
            'Словарь',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_LIST_BOX),
        )

        # Widget DOM.
        self.add(
            TitleLabel(TITLE_FOREIGN_MAIN),
            btn_goto_main,
            btn_goto_create,
            btn_goto_params,
            btn_goto_list,
        )


class ParamForeignPage(ExerciseParamSelectionsBox):
    """Learning foreign words exercise parameters box."""

    title = TITLE_FOREIGN_PARAMS

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Box widgets.
        btn_goto_foreign = BtnApp(
            'Меню словаря',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )

        # Widget DOM.
        self.insert(4, btn_goto_foreign)

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


class ExerciseForeignPage(ExerciseBox):
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
        btn_goto_params_box = BtnApp(
            'Настроить упражнение',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_PARAMS_BOX),
        )

        # TextPanel
        textpanel_label = toga.Label('Информация об упражнении:')
        textpanel_label.style = Pack(padding=(2, 0, 2, 7))
        self.textpanel = MultilineTextInput()

        # Widget DOM.
        self.add(
            TitleLabel(TITLE_FOREIGN_EXERCISE),
            self.exercise_box,
            self.textpanel,
            btn_goto_params_box,
        )
        self.exercise_box.insert(4, textpanel_label)
        self.exercise_box.insert(5, self.textpanel)

    def populate_textpanel(self) -> None:
        """Populate the text panel."""
        self.textpanel.value = (
            f'Найдено слов: {self.task.data["item_count"]}\n'
            f'Оценка знания слова: {self.task.data[ASSESSMENT]}'
        )

    def show_question(self) -> None:
        """Add populate items."""
        super().show_question()
        self.populate_textpanel()


class FormForeign(BaseForm):
    """General form to create and update entries, the container."""

    title = ''
    """Bage box title (`str`).
    """

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
            TitleLabel(text=self.title),
            self.russian_input,
            self.foreign_input,
            btn_submit,
            btn_goto_foreign_box,
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


class CreateWordPage(HttpPostMixin, FormForeign):
    """Add word to foreign dictionary."""

    title = TITLE_FOREIGN_CREATE
    url = urljoin(HOST_API, FOREIGN_PATH)
    btn_submit_name = 'Добавить'

    def get_widget_data(self) -> dict:
        """Get the entered into the form data."""
        submit_entry = {
            FOREIGN_WORD: self.foreign_input.value,
            RUSSIAN_WORD: self.russian_input.value,
        }
        return submit_entry


class UpdateWordPage(HttpPutMixin, FormForeign):
    """Update the foreign word the box."""

    title = TITLE_FOREIGN_UPDATE
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


class ListForeignPage(TableApp):
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
            'Оглавление словаря',
            on_press=lambda _: self.goto_box_handler(_, FOREIGN_BOX),
        )

        # Page widgets DOM.
        self.add(
            TitleLabel(TITLE_FOREIGN_LIST),
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
