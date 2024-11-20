"""App http requests module."""

import os.path
import typing
from http import HTTPStatus
from pathlib import Path
from urllib.parse import urljoin

import httpx
from httpx import Request, Response

from wse.constants import (
    CONNECTION_ERROR_MSG,
    HOST_API,
    TOKEN_PATH,
    USER_ME_PATH,
)

url_obtain_token = urljoin(HOST_API, TOKEN_PATH)
url_authorization = urljoin(HOST_API, USER_ME_PATH)


class AppAuth(httpx.Auth):
    """Authentication.

    :ivar token: User authentication token.
    :vartype token: str or None
    """

    token_path = os.path.join(
        Path(__file__).parent.parent,
        'resources/token.txt',
    )
    """Path to reade or save token (`str`).
    """

    def __init__(self) -> None:
        """Construct the token auth."""
        self._token: str | None = None

    def auth_flow(
        self,
        request: Request,
    ) -> typing.Generator[Request, Response, None]:
        """Execute the authentication flow."""
        request.headers['Authorization'] = f'Token {self.token}'
        yield request

    @property
    def token(self) -> str | None:
        """The user authentication token."""
        if self._token:
            return self._token

        try:
            with open(self.token_path, 'r') as file:
                token = file.read()
        except FileNotFoundError:
            return None
        else:
            self.token = token
            return token

    @token.setter
    def token(self, token: str) -> None:
        with open(self.token_path, 'w') as file:
            file.write(token)
        self._token = token

    @token.deleter
    def token(self) -> None:
        try:
            os.unlink(self.token_path)
        except FileNotFoundError:
            pass
        self._token = None


app_auth = AppAuth()


class ErrorResponse(Response):
    """Stub to response with errors.

    Used to intercept errors of the HTTPX library.
    https://www.python-httpx.org/exceptions/
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct response."""
        super().__init__(*args, **kwargs)
        self.conn_error_msg = CONNECTION_ERROR_MSG


def obtain_token(credentials: dict) -> Response:
    """Obtain the user token."""
    with httpx.Client() as client:
        response = client.post(url_obtain_token, json=credentials)

        if response.status_code == HTTPStatus.OK:
            token = response.json()['auth_token']
            app_auth.token = token

            return response


#########################################################################
# Request
#########################################################################


def request_get(url: str) -> Response:
    """Send GET request."""
    with httpx.Client(auth=app_auth) as client:
        try:
            response = client.get(url=url)
        except httpx.ConnectError:
            print('Connection error')
            return ErrorResponse(HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            return response


def request_post(
    url: str,
    payload: dict | None = None,
    token: bool = True,
) -> Response | ErrorResponse:
    """Send POST request."""
    auth = app_auth if token else None

    with httpx.Client(auth=auth) as client:
        try:
            response = client.post(url=url, json=payload)
        except httpx.ConnectError:
            print('Connection error')
            return ErrorResponse(HTTPStatus.INTERNAL_SERVER_ERROR)
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


async def request_token_async(
    url: str, payload: dict | None = None
) -> Response:
    """Request the async POST method."""
    async with httpx.AsyncClient() as client:
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
    async def request_get_async(cls, url: str, payload: dict) -> Response:
        """Send http request, GET method."""
        return await request_put_async(url, payload)


class HttpPostMixin:
    """Request POST method, the mixin."""

    success_http_status = HTTPStatus.CREATED

    @classmethod
    async def request_post_async(cls, url: str, payload: dict) -> Response:
        """Send http request, POST method."""
        return await request_post_async(url, payload)


class HttpPutMixin:
    """Request PUT method, the mixin."""

    success_http_status = HTTPStatus.OK

    @classmethod
    async def request_put_async(cls, url: str, payload: dict) -> Response:
        """Send http request, PUT method."""
        return await request_put_async(url, payload)
