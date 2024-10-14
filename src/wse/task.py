"""Task."""

from wse.constants import ANSWER_TEXT, ID, QUESTION_TEXT


class Task:
    """Task.

    :ivar params: Item lookup parameters to create  task by item.
        Are sent to the server.
    :vartype params: dict[str, object] or None
    :ivar status: The task status, may be 'question' or 'answer'.
    :vartype status: str or None
    """

    def __init__(self) -> None:
        """Construct the task."""
        self._data = None
        self.params = None
        self.status = None

    @property
    def data(self) -> dict[str, str | int | None]:
        """Task data for its execution (`dict[str, str | int | None]`).

        Received from server.
        """
        return self._data

    @data.setter
    def data(self, value: dict[str, str | int | None]) -> None:
        self._data = value

    @property
    def question(self) -> str:
        """The text of the task question (`str`, reade-only)."""
        return self.data[QUESTION_TEXT]

    @property
    def answer(self) -> str:
        """The text of the task answer (`str`, reade-only)."""
        return self.data[ANSWER_TEXT]

    @property
    def item_id(self) -> int:
        """Item ID on task (`int`, reade-only)."""
        return self.data[ID]
