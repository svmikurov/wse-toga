"""Mocks."""

import json
import os
import pathlib


class MockClient:
    """Mock httpx.Client functionality.

    :param str fixture: The fixture file name.
    """

    module_dir = pathlib.Path(__file__).parent
    """Current module dir path (`str`).
    """

    def __init__(self, fixture: str) -> None:
        """Construct the mocking."""
        self.fixture = fixture

    @property
    def fixture_path(self) -> str:
        """Return the path to fixture."""
        return os.path.join(self.module_dir, f'fixtures/{self.fixture}')

    @staticmethod
    def url() -> str:
        """Mock the url."""
        return ''

    def json(self) -> dict:
        """Mock the json method.

        :return: the fixture data to mocking the response json.
        """
        with open(self.fixture_path, 'r') as file:
            fixture = json.load(file)
        return fixture
