"""Contribute in app."""

import wse.constants as const


def get_response_error_msg(status_code: int) -> tuple[str, str]:
    """Get message by response."""
    default_msg = ('Необработанная ошибка', '')
    title, msg = const.RESPONSE_ERROR_MSGS.get(status_code, default_msg)
    return title, msg
