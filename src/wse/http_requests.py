"""Requests module."""

import typing

import httpx
from httpx import Request, Response

import wse.constants as const


def get_message(
    messages: dict[int, tuple[str, str]],
    status_code: int,
) -> tuple[str, str]:
    """Get message by response."""
    default_message = ('Необработанная ошибка', '')
    title, message = messages.get(status_code, default_message)
    return title, message


class AppAuth(httpx.Auth):
    """Authentication."""

    def __init__(self) -> None:
        """Construct."""
        self.token = None

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


def send_post_request(
    url: str,
    payload: dict | None = None,
    auth: AppAuth | None = None,
) -> Response | ErrorResponse:
    """Send POST request."""
    with httpx.Client(auth=auth) as client:
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
