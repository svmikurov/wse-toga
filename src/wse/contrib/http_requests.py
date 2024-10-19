"""App http requests module."""

import os
import typing
from http import HTTPStatus

import httpx
from dotenv import load_dotenv
from httpx import Request, Response

import wse.constants as const

load_dotenv()

TOKEN = os.getenv('TOKEN')


class AppAuth(httpx.Auth):
    """Authentication.

    :ivar token: User authentication token.
    :vartype token: str
    """

    def __init__(self) -> None:
        """Construct the authentication."""
        # self.token = None
        self.token = TOKEN

    def auth_flow(
        self,
        request: Request,
    ) -> typing.Generator[Request, Response, None]:
        """Execute the authentication flow.

        Adds auth ``token`` to "Authorization" header.
        """
        request.headers['Authorization'] = f'Token {self.token}'
        yield request

    def set_token(self, response: Response) -> None:
        """Set auth token from login response."""
        self.token = response.json()[const.AUTH_TOKEN]

    def delete_token(self) -> None:
        """Delete current auth token."""
        self.token = None


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


#########################################################################
# Request
#########################################################################


def request_get(url: str) -> Response:
    """Send GET request."""
    with httpx.Client(auth=app_auth) as client:
        response = client.get(url=url)
    return response


def request_post(
    url: str,
    payload: dict | None = None,
    token: bool = True,
) -> Response:
    """Send POST request."""
    auth = app_auth if token else None
    with httpx.Client(auth=auth) as client:
        response = client.post(url=url, json=payload)
    return response


#########################################################################
# Async request
#########################################################################


async def request_get_async(url: str) -> Response:
    """Request the async GET method."""
    async with httpx.AsyncClient(auth=app_auth) as client:
        response = await client.get(url)
    return response


async def request_post_async(
    url: str, payload: dict | None = None
) -> Response:  # noqa: E501
    """Request the async POST method."""
    async with httpx.AsyncClient(auth=app_auth) as client:
        response = await client.post(url, json=payload)
    return response


async def request_put_async(url: str, payload: dict) -> Response:
    """Request the async POST method."""
    async with httpx.AsyncClient(auth=app_auth) as client:
        response = await client.put(url, json=payload)
    return response


async def request_delete_async(url: str) -> Response:
    """Request the async DELETE method."""
    async with httpx.AsyncClient(auth=app_auth) as client:
        response = await client.delete(url)
    return response


#########################################################################
# Request mixins
#########################################################################


class HttpGetMixin:
    """Request GET method, the mixin."""

    success_http_status = HTTPStatus.OK

    @classmethod
    async def send_request_async(cls, url: str, payload: dict) -> Response:
        """Send http request PUT method."""
        return await request_put_async(url, payload)


class HttpPostMixin:
    """Request POST method, the mixin."""

    success_http_status = HTTPStatus.CREATED

    @classmethod
    async def send_request_async(cls, url: str, payload: dict) -> Response:
        """Send http request, POST method."""
        return await request_post_async(url, payload)


class HttpPutMixin:
    """Request PUT method, the mixin."""

    success_http_status = HTTPStatus.OK

    @classmethod
    async def send_request_async(cls, url: str, payload: dict) -> Response:
        """Send http request PUT method."""
        return await request_put_async(url, payload)
