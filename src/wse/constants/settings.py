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
TEXT_DISPLAY_PADDING = (0, 2, 0, 2)

#########################################################################
# Titles

TITLE_LABEL_FONT_SIZE = 16
TITLE_LABEL_HEIGHT = 35
TITLE_LABEL_PADDING = (5, 0, 10, 0)
# Main
TITLE_MAIN = 'WSELFEDU'
BTN_GOTO_MAIN = 'На главную'
# User
TITLE_LOGIN = 'Вход в учетную запись'
TITLE_USER_MAIN = 'Учетная запись'
TITLE_USER_UPDATE = 'Изменить имя'
TITLE_USER_CREATE = 'Регистрация'
BTN_GOTO_LOGIN = 'Вход в учетную запись'
BTN_LOGIN = 'Войти в учетную запись'
BTN_LOGOUT = 'Выйти из учетной записи'
# Glossary
TITLE_GLOSSARY_MAIN = 'Глоссарий'
TITLE_GLOSSARY_CREATE = 'Добавить термин'
TITLE_GLOSSARY_UPDATE = 'Изменить термин'
TITLE_GLOSSARY_LIST = 'Список терминов'
TITLE_GLOSSARY_PARAMS = 'Параметры изучения терминов'
TITLE_GLOSSARY_EXERCISE = 'Изучение терминов'
BTN_GOTO_GLOSSARY_MAIN = 'Глоссарий'
BTN_GOTO_GLOSSARY_LIST = 'Словарь терминов'
BTN_GOTO_GLOSSARY_EXERCISE = 'Начать упражнение'
BTN_GOTO_GLOSSARY_PARAMS = 'Упражнение'
BTN_GOTO_GLOSSARY_CREATE = 'Добавить термин'
# Foreign
TITLE_FOREIGN_MAIN = 'Иностранный словарь'
TITLE_FOREIGN_CREATE = 'Добавить слово'
TITLE_FOREIGN_UPDATE = 'Изменить термин'
TITLE_FOREIGN_LIST = 'Словарь иностранных слов'
TITLE_FOREIGN_PARAMS = 'Параметры изучения слов'
TITLE_FOREIGN_EXERCISE = 'Изучение иностранных слов'
BTN_GOTO_FOREIGN_MAIN = 'Иностранный'
BTN_GOTO_FOREIGN_CREATE = 'Добавить слово'
BTN_GOTO_FOREIGN_LIST = 'Словарь иностранных слов'
BTN_GOTO_FOREIGN_EXERCISE = 'Начать упражнение'
BTN_GOTO_FOREIGN_PARAMS = 'Упражнение'

#########################################################################
# Messages

LOGIN_MSG = 'Вы вошли в учетную записи'
LOGIN_BAD_MSG = 'Неверный логин или пароль'
LOGOUT_MSG = 'Вы вышли из учетной записи'
USER_CREATE_MESSAGE = 'Вы создали учетную запись'
USER_UPDATE_MESSAGE = 'Вы изменили имя'
CONNECTION_ERROR_MSG = 'Ошибка соединения с сервером'
NO_TASK_MSG = 'По заданным условия задание не сформировано'
TASK_ERROR_MSG = 'Ошибка формирования задания'
