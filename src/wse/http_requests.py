"""Requests module."""

import os
import typing

import httpx
from dotenv import load_dotenv
from httpx import Request, Response

import wse.constants as const

load_dotenv()

TOKEN = os.getenv('TOKEN')


class AppAuth(httpx.Auth):
    """Authentication."""

    def __init__(self) -> None:
        """Construct the authentication."""
        # self.token = None
        self.token = TOKEN

    def auth_flow(
        self,
        request: Request,
    ) -> typing.Generator[Request, Response, None]:
        """Execute the authentication flow."""
        request.headers['Authorization'] = f'Token {self.token}'
        yield request

    def set_token(self, response: Response) -> None:
        """Set auth token."""
        self.token = response.json()[const.AUTH_TOKEN]

    def delete_token(self) -> None:
        """Delete current auth token."""
        self.token = None

    @property
    def is_authenticated(self) -> bool:
        """Return user authentication status."""
        return True if self.token else False


app_auth = AppAuth()


class ErrorResponse:
    """Stub to response with errors.

    Used to intercept errors of the HTTPX library.
    https://www.python-httpx.org/exceptions/
    """

    def __init__(self, status_code: int, message: str) -> None:
        """Construct response."""
        self.status_code = const.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message


def request_get(url: str) -> Response:
    """Send GET request."""
    with httpx.Client(auth=app_auth) as client:
        response = client.get(url=url)
    return response


def request_post(
    url: str,
    payload: dict | None = None,
) -> Response | ErrorResponse:
    """Send POST request."""
    with httpx.Client(auth=app_auth) as client:
        try:
            response = client.post(url=url, json=payload)
        except httpx.ConnectError as exc:
            print(f'\nINFO: HTTP Exception for {exc.request.url} - {exc}')
            return ErrorResponse(
                const.HTTP_500_INTERNAL_SERVER_ERROR,
                'Не удалось установить соединение',
            )
        else:
            return response


async def request_get_async(url: str) -> Response:
    """Request async the get method."""
    async with httpx.AsyncClient(auth=app_auth) as client:
        response = await client.get(url)
    return response


async def request_post_async(url: str, payload: dict) -> Response:
    """Request async the post method."""
    async with httpx.AsyncClient(auth=app_auth) as client:
        response = await client.post(url, json=payload)
    return response
