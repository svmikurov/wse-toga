"""Utils for testing.."""

import json
import os
import pathlib


class FixtureReader:
    """Reader of fixtures.

    :param str fixture: The fixture file name.
    """

    module_dir = pathlib.Path(__file__).parent
    """Current module dir path (`str`).
    """

    def __init__(self, fixture: str) -> None:
        """Construct the reader."""
        self.fixture = fixture

    @property
    def fixture_path(self) -> str:
        """Return the path to fixture (`str`, reade-only)."""
        return os.path.join(self.module_dir, f'fixtures/{self.fixture}')

    @staticmethod
    def url() -> str:
        """Return the url."""
        return ''

    def json(self) -> dict:
        """Reade the fixture.

        :return: the fixture data.
        """  # noqa: D401
        with open(self.fixture_path, 'r') as file:
            fixture = json.load(file)
        return fixture
