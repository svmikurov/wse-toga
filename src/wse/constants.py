"""App constants."""

########################################################################
# Box names
########################################################################

GLOSSARY_BOX = 'glossary_box'
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

# Statuses
HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_500_INTERNAL_SERVER_ERROR = 500

########################################################################
# Attribute names
########################################################################

AUTH_TOKEN = 'auth_token'
PASSWORD = 'password'
USERNAME = 'username'
