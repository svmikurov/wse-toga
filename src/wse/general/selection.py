"""General app selection."""

import toga

from wse.constants import ALIAS, HUMANLY


class BaseSelection(toga.Selection):
    """Custom selection widget.

    :param list[dict] items: Initial items to display for selection.
    :param value: Initial value for the selection.
    :type value: str or None.
    :param str accessor: The accessor to use to extract display values
        from the list of items.
    :param str alias: Key for attribute on the selected item.
    """

    def __init__(self, **kwargs: object) -> None:
        """Construct the widget."""
        kwargs['accessor'] = HUMANLY
        super().__init__(**kwargs)
        self.alias = ALIAS

    def set_items(self, items: list[dict], value: str | None) -> None:
        """Set selection initial items and initial value to display.

        :param list[dict] items: Initial items to display for selection.
        :param value: Initial value for the selection.
        :type value: str or None.
        """
        # Set Selection items attr.
        self.items = items
        # Set Selection value attr.
        for index, selection in enumerate(items):
            if selection[self.alias] == value:
                self.value = self.items[index]

    def get_alias(self) -> str | int | list | None:
        """Get displayed value from selection."""
        return self.value.alias
