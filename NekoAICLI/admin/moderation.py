from datetime import datetime, timedelta

from core import state
from core.localization import t
from core.ui import (
    style,
    success,
    warning,
    error
)

from database.queries import (
    get_user_by_username,
    get_active_moderation,
    create_moderation,
    delete_moderation
)

from admin.access import admin_access


def admin_apply_moderation(username, moderation_type):

    if not admin_access():
        return

    user = get_user_by_username(
        username
    )

    if user is None:

        error(
            "Пользователь не найден."
            if state.settings.get("language", "ru") == "ru"
            else "User not found."
        )

        return

    if user["uuid"] == state.current_user["uuid"]:

        error(
            "Нельзя применить это действие к себе."
            if state.settings.get("language", "ru") == "ru"
            else "You cannot apply this action to yourself."
        )

        return

    existing = get_active_moderation(
        user["uuid"],
        moderation_type
    )

    if existing is not None:

        error(
            "Наказание уже активно."
            if state.settings.get("language", "ru") == "ru"
            else "This punishment is already active."
        )

        return

    if moderation_type == "ban":

        action_name = (
            "BAN"
            if state.settings.get("language", "ru") != "ru"
            else "БАН"
        )

    else:

        action_name = (
            "MUTE"
            if state.settings.get("language", "ru") != "ru"
            else "МУТ"
        )

    print()

    print(
        style(
            "warning",
            f"{action_name}: {username}"
        )
    )

    duration = input(
        "Срок (0 = навсегда, минуты например 30): "
        if state.settings.get("language", "ru") == "ru"
        else "Duration (0 = permanent, minutes e.g. 30): "
    ).strip()

    try:

        duration_minutes = int(duration)

    except ValueError:

        error(
            "Некорректный срок."
            if state.settings.get("language", "ru") == "ru"
            else "Invalid duration."
        )

        return

    if duration_minutes < 0:

        error(
            "Срок не может быть отрицательным."
            if state.settings.get("language", "ru") == "ru"
            else "Duration cannot be negative."
        )

        return

    reason = input(
        "Причина: "
        if state.settings.get("language", "ru") == "ru"
        else "Reason: "
    ).strip()

    if duration_minutes == 0:

        expires_at = None

    else:

        expires_at = datetime.now() + timedelta(
            minutes=duration_minutes
        )

    if not create_moderation(
        user["uuid"],
        moderation_type,
        reason if reason else None,
        expires_at
    ):

        error(
            t(
                "database_error",
                state.settings
            )
        )

        return

    if moderation_type == "ban":

        success(
            f"Пользователь {username} заблокирован."
            if state.settings.get("language", "ru") == "ru"
            else f"User {username} has been banned."
        )

    else:

        success(
            f"Пользователь {username} замьючен."
            if state.settings.get("language", "ru") == "ru"
            else f"User {username} has been muted."
        )


def admin_remove_moderation(username, moderation_type):

    if not admin_access():
        return

    user = get_user_by_username(
        username
    )

    if user is None:

        error(
            "Пользователь не найден."
            if state.settings.get("language", "ru") == "ru"
            else "User not found."
        )

        return

    deleted = delete_moderation(
        user["uuid"],
        moderation_type
    )

    if deleted == 0:

        warning(
            "Активного наказания нет."
            if state.settings.get("language", "ru") == "ru"
            else "There is no active punishment."
        )

        return

    success(
        (
            f"Блокировка пользователя {username} снята."
            if moderation_type == "ban"
            else f"Мут пользователя {username} снят."
        )
        if state.settings.get("language", "ru") == "ru"
        else (
            f"Ban from {username} has been removed."
            if moderation_type == "ban"
            else f"Mute from {username} has been removed."
        )
    )