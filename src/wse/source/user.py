"""User data source."""

from toga.sources import Source


class UserSource(Source):
    """User data source."""

    def __init__(self) -> None:
        """Construct the source."""
        super().__init__()
        self._username: str | None = None
        self._is_auth: bool = False

    @property
    def username(self) -> str:
        """The username (`str`)."""
        return self._username

    @property
    def is_auth(self) -> bool:
        """The user auth status (`bool`)."""
        return self._is_auth

    def set_auth_data(self, username: str | None = None) -> None:
        """Set auth data.

        If username is None then set data as not auth.

        :param username: The username (optionally)
        :type username: str or None
        """
        self._username = username
        self._is_auth = True if username else False
