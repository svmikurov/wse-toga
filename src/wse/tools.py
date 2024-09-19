"""Application tools."""

from toga import Selection


def set_selection_item(
    key: str,
    value: str,
    items: list[dict],
    selection: Selection,
) -> None:
    """Set default selection item.

    Parameters
    ----------
    key : `str`
        Item key name.
    value : `str`
        Item value to set.
    items : `list[dict]`
        List of items.
    selection : `toga.Selection`
        Toga selection widget, whose default selection item is set.

    Example
    -------
    .. code-block:: python
       set_selection_item(
           key='id',
           value='2',
           items='categories',
           selection=self.category_selection,
       )

    """
    for index, period in enumerate(items):
        if period[key] == value:
            selection.value = selection.items[index]
