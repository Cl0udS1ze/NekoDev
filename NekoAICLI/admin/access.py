from core import state
from core.response import Response, render_cli


def is_admin():
    return (
        state.current_user is not None
        and state.current_user.get("is_admin") is True
    )


def admin_access():

    if not is_admin():
        render_cli(
            Response().error(
                "Доступ разрешён только администраторам."
                if state.settings.get("language", "ru") == "ru"
                else "Access is restricted to administrators."
            )
        )
        return False

    if state.db is None or not state.db.is_connected():
        render_cli(
            Response().error(
                "Для админ-панели необходимо подключение к серверу."
                if state.settings.get("language", "ru") == "ru"
                else "A server connection is required for the admin panel."
            )
        )
        return False

    return True
