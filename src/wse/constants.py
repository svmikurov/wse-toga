"""App constants."""

from http import HTTPStatus

########################################################################
# Box names
########################################################################

FOREIGN_BOX = 'foreign_box'
FOREIGN_EXERCISE_BOX = 'foreign_exercise_box'
FOREIGN_PARAMS_BOX = 'foreign_params_box'
GLOS_BOX = 'glossary_box'
GLOS_EXE_BOX = 'glossary_exercise_box'
GLOS_PARAMS_BOX = 'glossary_exercise_params_box'
LOGIN_BOX = 'login_box'
MAIN_BOX = 'main_box'
USER_BOX = 'user_box'

########################################################################
# Url and statuses
########################################################################

# Url
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
FOREIGN_PARAMS_PATH = '/api/v1/foreign/exercise/params/'
"""Learning foreign word exercise parameters path (`str`).
"""
GLOS_EXE_PATH = '/api/v1/glossary/exercise/'
"""Glossary exercise path (`str`).
"""
GLOS_PARAMS_PATH = '/api/v1/glossary/exercise/parameters/'
"""Glossary exercise parameters path (`str`).
"""
GLOS_PROGRESS = '/api/v1/glossary/progress/'
"""Glossary progress update path (`str`).
"""

HTTP_400_BAD_REQUEST = HTTPStatus.BAD_REQUEST
HTTP_401_UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
HTTP_500_INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR

AUTH_TOKEN = 'auth_token'

RESPONSE_ERROR_MSGS = {
    HTTP_400_BAD_REQUEST: ('', 'Предоставлены неверные данные'),
    HTTP_401_UNAUTHORIZED: ('', 'Необходимо авторизоваться'),
    HTTP_500_INTERNAL_SERVER_ERROR: ('', 'Ошибка сервера'),
}

########################################################################
# Attribute names
########################################################################

ACTION = 'action'
ALIAS = 'alias'
ANSWER = 'answer'
ANSWER_TEXT = 'answer_text'
CATEGORIES = 'categories'
CATEGORY = 'category'
DEFAULT_TIMEOUT = 5
DETAIL = 'detail'
EDGE_PERIOD_ITEMS = 'edge_period_items'
ERROR = 'error'
EXERCISE_CHOICES = 'exercise_choices'
HUMANLY = 'humanly'
ID = 'id'
KNOW = 'know'
LOOKUP_CONDITIONS = 'lookup_conditions'
NAME = 'name'
NEXT = 'next'
NOT_KNOW = 'not_know'
PASSWORD = 'password'
PERIOD_END = 'period_end_date'
PERIOD_START = 'period_start_date'
PROGRESS = 'progress'
QUESTION = 'question'
QUESTION_TEXT = 'question_text'
TERM_ID = 'term_id'
TIMEOUT = 'timeout'
USERNAME = 'username'
