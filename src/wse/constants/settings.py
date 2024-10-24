"""The application widget settings constants."""

from travertino.constants import ITALIC

DEFAULT_TIMEOUT = 5
"""Time to answer on task question in exercises (`int`).
"""

########################################################################
# Widget constants
########################################################################

SCREEN_SIZE = (440, 700)
PADDING_NO = 0
PADDING_SM = 2
PADDING_SIDE = (PADDING_NO, PADDING_SM, PADDING_NO, PADDING_SM)
PADDING_AROUND_WIDGET = (PADDING_SM, PADDING_SM, PADDING_SM, PADDING_SM)
FONT_SIZE_APP = 11
BUTTON_HEIGHT = 60
INPUT_HEIGHT = 60

#########################################################################
# TextDisplay
TEXT_DISPLAY_FONT_SIZE = 18
TEXT_DISPLAY_FONT_STYLE = ITALIC
TEXT_DISPLAY_PADDING = (2, 2, 2, 2)

#########################################################################
# Titles

TITLE_LABEL_FONT_SIZE = 16
TITLE_LABEL_HEIGHT = 35
TITLE_LABEL_PADDING = (5, 0, 10, 0)
# Main
TITLE_MAIN = 'WSELFEDU'
# User
TITLE_USER_MAIN = 'Учетная запись'
USER_UPDATE_TITLE = 'Изменить имя'
USER_CREATE_TITLE = 'Регистрация'
LOGIN_TITLE = 'Вход в учетную запись'
# Glossary
TITLE_GLOSSARY_MAIN = 'Глоссарий'
TITLE_GLOSSARY_CREATE = 'Добавить термин'
TITLE_GLOSSARY_UPDATE = 'Изменить термин'
TITLE_GLOSSARY_LIST = 'Список терминов'
TITLE_GLOSSARY_PARAMS = 'Параметры изучения терминов'
TITLE_GLOSSARY_EXERCISE = 'Изучение терминов'
# Foreign
TITLE_FOREIGN_MAIN = 'Иностранный словарь'
TITLE_FOREIGN_CREATE = 'Добавить термин'
TITLE_FOREIGN_UPDATE = 'Изменить термин'
TITLE_FOREIGN_LIST = 'Список иностранных слов'
TITLE_FOREIGN_PARAMS = 'Параметры изучения слов'
TITLE_FOREIGN_EXERCISE = 'Изучение иностранных слов'

#########################################################################
# Messages

LOGIN_MSG = 'Вы вошли в учетную записи'
LOGIN_BAD_MSG = 'Неверный логин или пароль'
LOGOUT_MSG = 'Вы вышли из учетной записи'
USER_CREATE_MESSAGE = 'Вы создали учетную запись'
USER_UPDATE_MESSAGE = 'Вы изменили имя'
CONNECTION_ERROR_MSG = 'Ошибка соединения с сервером'
