"""The application url endpoints."""

from http import HTTPStatus

HOST_API = 'http://127.0.0.1/'
"""Host to conect (`str`).
"""
TOKEN_PATH = '/auth/token/login/'
"""Endpoint to obtain the user authentication token, allowed method: POST (`str`).
"""  # noqa: W505, E501
FOREIGN_EXERCISE_PATH = '/api/v1/foreign/exercise/'
"""Learning foreign word exercise path (`str`).
"""
FOREIGN_PROGRESS_PATH = '/api/v1/foreign/progress/'
"""Learning foreign word progress path (`str`).
"""
FOREIGN_PARAMS_PATH = '/api/v1/foreign/params/'
"""Learning foreign word exercise parameters path (`str`).
"""
FOREIGN_PATH = '/api/v1/foreign/'
"""Create foreign word and list of foreign word the url path(`str`).
"""
FOREIGN_DETAIL_PATH = '/api/v1/foreign/%s/'
"""Detail foreign word the url path(`str`).
"""
GLOSSARY_EXERCISE_PATH = '/api/v1/glossary/exercise/'
"""Glossary exercise path (`str`).
"""
GLOSSARY_PARAMS_PATH = '/api/v1/glossary/params/'
"""Glossary exercise parameters path (`str`).
"""
GLOSSARY_PROGRESS_PATH = '/api/v1/glossary/progress/'
"""Glossary progress update path (`str`).
"""

HTTP_400_BAD_REQUEST = HTTPStatus.BAD_REQUEST
HTTP_401_UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
HTTP_500_INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

RESPONSE_ERROR_MSGS = {
    HTTP_400_BAD_REQUEST: ('', 'Предоставлены неверные данные'),
    HTTP_401_UNAUTHORIZED: ('', 'Необходимо авторизоваться'),
    HTTP_500_INTERNAL_SERVER_ERROR: ('', 'Ошибка сервера'),
}
