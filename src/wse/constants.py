"""App constants."""

########################################################################
# Box names
########################################################################

GLOS_BOX = 'glossary_box'
GLOS_EXE_BOX = 'glossary_exercise_box'
GLOS_PARAMS_BOX = 'glossary_exercise_params_box'
LOGIN_BOX = 'login_box'
MAIN_BOX = 'main_box'
USER_BOX = 'user_box'
WORD_BOX = 'word_box'

########################################################################
# Url and statuses
########################################################################

# Url
HOST_API = 'http://127.0.0.1/'
TOKEN_PATH = '/auth/token/login/'
"""Endpoint to obtain the user authentication token, allowed method: POST (`str`).
"""  # noqa: W505, E501
GLOS_EXE_PATH = '/api/v1/glossary/exercise/'
"""Glossary exercise path (`str`).
"""
GLOS_PARAMS_PATH = '/api/v1/glossary/exercise/parameters/'
"""Glossary exercise parameters path (`str`).
"""

# Statuses
HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_500_INTERNAL_SERVER_ERROR = 500

AUTH_TOKEN = 'auth_token'

########################################################################
# Attribute names
########################################################################

ACTION = 'action'
ALIAS = 'alias'
CATEGORY = 'category'
CATEGORIES = 'categories'
HUMANLY = 'humanly'
ID = 'id'
KNOW = 'know'
NAME = 'name'
NEXT = 'next'
NOT_KNOW = 'not_know'
PASSWORD = 'password'
PERIOD_END = 'period_end_date'
PERIOD_START = 'period_start_date'
PROGRES = 'progres'
TERM_ID = 'term_id'
USERNAME = 'username'
