"""Base application page box with methods."""

import toga
from toga.style.pack import COLUMN
from typing_extensions import Self

from wse.constants.settings import PADDING_SM


class BaseBox(toga.Box):
    """Base page box.

    Defines a common style for derived box widgets.
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
        self.style.direction = COLUMN
        self.style.padding = PADDING_SM
        self.style.flex = 1


class GoToBoxMixin:
    """Go to page box mixin.

    Mixin methods for switching between application pages.
    """

    @classmethod
    def get_box(cls, widget: toga.Widget, box_name: str) -> Self:
        """**DEPRECATED** - Use wse.general.goto_handler module.

        Get the page box that was initialized in the app.
        """  # noqa: D401
        return widget.root.app.__getattribute__(box_name)

    @classmethod
    def set_window_content(cls, widget: toga.Widget, box: Self) -> None:
        """**DEPRECATED** - Use wse.general.goto_handler module.

        Set page box to window content.
        """  # noqa: D401
        widget.window.content = box

    def on_open(self, widget: toga.Widget) -> None:
        """Run when the current box is assigned to the window content.

        Override it if it necessary to run same actions, then the
        current box is assigned to :term:`window content`.
        """
        pass


class MessageBoxMixin:
    """Dialog message mixin."""

    app: toga.App

    async def show_message(self, title: str, message: str) -> None:
        """Show dialog message.

        :param str title: The message title.
        :param str message: The message text.
        """
        await self.app.main_window.dialog(
            toga.InfoDialog(str(title), str(message))
        )


class BoxApp(MessageBoxMixin, GoToBoxMixin, BaseBox):
    """General application page box."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the box."""
        super().__init__(*args, **kwargs)
