"""Base page widget."""

import toga
from toga.style.pack import COLUMN


class ColBox(toga.Box):
    """Column style box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
        self.style.direction = COLUMN


class FlexBox(toga.Box):
    """Flex style box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
        self.style.flex = 1
        self.style.direction = COLUMN
