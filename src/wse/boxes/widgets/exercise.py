"""General exercise box widgets."""

from http import HTTPStatus

import toga
from httpx import Response
from toga.style import Pack
from travertino.constants import COLUMN

from wse import base
from wse.constants import (
    ALIAS,
    CATEGORIES,
    CATEGORY,
    EDGE_PERIOD_ITEMS,
    EXERCISE_CHOICES,
    HUMANLY,
    ID,
    LOOKUP_CONDITIONS,
    NAME,
    PERIOD_END,
    PERIOD_START,
    PROGRESS,
)
from wse.tools import set_selection_item


class ExerciseParamChoicesBox(base.BaseBox):
    """Exercise parameter choices box."""

    def __init__(self) -> None:
        """Construct the box."""
        super().__init__()

        # Styles.
        label_style = Pack(padding=(7, 0, 7, 20))
        pair_box_style = Pack(flex=1, direction=COLUMN)

        # Parameter widgets.
        # labels
        start_date_label = toga.Label('Начало периода:', style=label_style)
        end_date_label = toga.Label('Конец периода:', style=label_style)
        category_label = toga.Label('Категория:', style=label_style)
        progress_label = toga.Label('Стадия изучения:', style=label_style)
        # selections
        self.start_period_selection = toga.Selection(accessor=HUMANLY)
        self.end_period_selection = toga.Selection(accessor=HUMANLY)
        self.category_selection = toga.Selection(accessor=NAME)
        self.progress_selection = toga.Selection(accessor=HUMANLY)
        # boxes
        box_pair = toga.Box()
        box_left = toga.Box(style=pair_box_style)
        box_right = toga.Box(style=pair_box_style)

        # Widget DOM.
        self.add(
            box_pair,
        )
        box_pair.add(box_left, box_right)
        box_left.add(
            start_date_label,
            end_date_label,
            category_label,
            progress_label,
        )
        box_right.add(
            self.start_period_selection,
            self.end_period_selection,
            self.category_selection,
            self.progress_selection,
        )

    @property
    def lookup_conditions(self) -> dict[str, str | list]:
        """User lookup conditions (`dict`, reade-only)."""
        # selection.value is None if not is set
        period_start = self.start_period_selection.value
        period_end = self.end_period_selection.value
        category = self.category_selection.value
        progres = self.progress_selection.value
        lookup_conditions = {
            PERIOD_START: period_start.alias if period_start else None,
            PERIOD_END: period_end.alias if period_end else None,
            CATEGORY: category.id if category else None,
            PROGRESS: progres.alias if progres else None,
        }
        return lookup_conditions

    def fill_params(self, response: Response) -> None:
        """Fill exercise parameters.

        Parameters
        ----------
        response : `httpx.Response`
            Server response with choices and current exercise parameters
            as choice by default.

        """
        if response.status_code == HTTPStatus.OK:
            payload = response.json()
            exercise_choices = payload[EXERCISE_CHOICES]

            # Choices.
            edge_period_items = exercise_choices[EDGE_PERIOD_ITEMS]
            category_items = exercise_choices[CATEGORIES]
            progress_items = exercise_choices[PROGRESS]

            # Default choice.
            defaults = payload[LOOKUP_CONDITIONS]
            start_period_alias = defaults[PERIOD_START]
            end_period_alias = defaults[PERIOD_END]
            default_category = defaults[CATEGORY]
            default_progress = defaults[PROGRESS]

            # Assign the choices to selection.
            self.start_period_selection.items = edge_period_items
            self.end_period_selection.items = edge_period_items
            self.category_selection.items = category_items
            self.progress_selection.items = progress_items

            # Assign the default choice to selection.
            set_selection_item(
                key=ALIAS,
                value=start_period_alias,
                items=edge_period_items,
                selection=self.start_period_selection,
            )
            set_selection_item(
                key=ALIAS,
                value=end_period_alias,
                items=edge_period_items,
                selection=self.end_period_selection,
            )
            set_selection_item(
                key=ID,
                value=default_category,
                items=category_items,
                selection=self.category_selection,
            )
            set_selection_item(
                key=ALIAS,
                value=default_progress,
                items=progress_items,
                selection=self.progress_selection,
            )
