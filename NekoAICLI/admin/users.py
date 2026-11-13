from core import state
from core.localization import t
from core.ui import (
    style,
    success,
    warning,
    error,
    title
)

from database.queries import (
    get_username_by_uuid,
    get_admin_users,
    get_admin_user,
    get_active_moderation,
    cleanup_expired_moderation,
    get_user_by_username,
    delete_user
)

from admin.access import admin_access


def format_user_status(status, chat_with_uuid):

    language = state.settings.get(
        "language",
        "ru"
    )

    if status == "chat":

        chat_username = get_username_by_uuid(
            chat_with_uuid
        )

        if chat_username is None:
            chat_username = "?"

        if language == "ru":
            return f"💬 В чате → {chat_username}"

        return f"💬 Chat → {chat_username}"

    if status == "interface":

        if language == "ru":
            return "⚙️ Интерфейс Neko AI"

        return "⚙️ Neko AI interface"

    if status == "online":

        return "🟢 Онлайн" if language == "ru" else "🟢 Online"

    return "⚫ Оффлайн" if language == "ru" else "⚫ Offline"


def admin_users():

    if not admin_access():
        return

    cleanup_expired_moderation()

    title(
        "ПОЛЬЗОВАТЕЛИ"
        if state.settings.get("language", "ru") == "ru"
        else "USERS"
    )

    users = get_admin_users()

    if users is None:

        error(
            t(
                "database_error",
                state.settings
            )
        )

        return

    if not users:

        print(
            style(
                "main",
                "Пользователей нет."
                if state.settings.get("language", "ru") == "ru"
                else "There are no users."
            )
        )

        return

    for (
        user_id,
        user_uuid,
        username,
        is_admin_value,
        created_at,
        status,
        chat_with_uuid,
        last_seen
    ) in users:

        if status is None:
            status = "offline"

        role = (
            "👑 Администратор"
            if is_admin_value
            else "👤 Пользователь"
        )

        if state.settings.get("language", "ru") != "ru":

            role = (
                "👑 Administrator"
                if is_admin_value
                else "👤 User"
            )

        ban = get_active_moderation(
            user_uuid,
            "ban"
        )

        mute = get_active_moderation(
            user_uuid,
            "mute"
        )

        ban_text = (
            "🚫 BAN"
            if ban is not None
            else "✓"
        )

        mute_text = (
            "🔇 MUTE"
            if mute is not None
            else "✓"
        )

        print(
            style(
                "main",
                f"""
╭─ #{user_id} {username} ─────────────
│ {format_user_status(status, chat_with_uuid)}
│ {role}
│ 📅 {created_at.strftime("%d.%m.%Y %H:%M")}
│ {ban_text}   {mute_text}
╰────────────────────────────────"""
            )
        )


def admin_user_info(username):

    if not admin_access():
        return

    cleanup_expired_moderation()

    user = get_admin_user(
        username
    )

    if user is None:

        error(
            "Пользователь не найден."
            if state.settings.get("language", "ru") == "ru"
            else "User not found."
        )

        return

    (
        user_id,
        user_uuid,
        username,
        is_admin_value,
        created_at,
        status,
        chat_with_uuid,
        last_seen
    ) = user

    ban = get_active_moderation(
        user_uuid,
        "ban"
    )

    mute = get_active_moderation(
        user_uuid,
        "mute"
    )

    title(
        "ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ"
        if state.settings.get("language", "ru") == "ru"
        else "USER INFORMATION"
    )

    role = (
        "Администратор"
        if is_admin_value
        else "Пользователь"
    )

    if state.settings.get("language", "ru") != "ru":

        role = (
            "Administrator"
            if is_admin_value
            else "User"
        )

    print(
        style(
            "main",
            f"""
│ Username: {username}
│ UUID: {user_uuid}
│ ID: {user_id}
│ Status: {format_user_status(status or "offline", chat_with_uuid)}
│ Role: {role}
│ Registered: {created_at.strftime("%d.%m.%Y %H:%M")}
│ Last seen: {last_seen.strftime("%d.%m.%Y %H:%M") if last_seen else "-"}"""
        )
    )

    if ban is None:

        print(
            style(
                "main",
                "│ Ban: No"
                if state.settings.get("language", "ru") != "ru"
                else "│ Ban: Нет"
            )
        )

    else:

        expires = (
            "Never"
            if ban[3] is None
            else ban[3].strftime("%d.%m.%Y %H:%M")
        )

        print(
            style(
                "error",
                f"│ Ban: YES | Until: {expires}"
            )
        )

        if ban[2]:

            print(
                style(
                    "main",
                    f"│ Reason: {ban[2]}"
                )
            )

    if mute is None:

        print(
            style(
                "main",
                "│ Mute: No"
                if state.settings.get("language", "ru") != "ru"
                else "│ Mute: Нет"
            )
        )

    else:

        expires = (
            "Never"
            if mute[3] is None
            else mute[3].strftime("%d.%m.%Y %H:%M")
        )

        print(
            style(
                "warning",
                f"│ Mute: YES | Until: {expires}"
            )
        )

        if mute[2]:

            print(
                style(
                    "main",
                    f"│ Reason: {mute[2]}"
                )
            )


def admin_delete_user(username):

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
            "Нельзя удалить самого себя."
            if state.settings.get("language", "ru") == "ru"
            else "You cannot delete yourself."
        )

        return

    confirmation = input(
        f"Удалить пользователя {username}? Введите DELETE: "
        if state.settings.get("language", "ru") == "ru"
        else f"Delete user {username}? Type DELETE: "
    )

    if confirmation != "DELETE":

        warning(
            "Удаление отменено."
            if state.settings.get("language", "ru") == "ru"
            else "Deletion cancelled."
        )

        return

    if not delete_user(
        user["uuid"]
    ):

        error(
            t(
                "database_error",
                state.settings
            )
        )

        return

    success(
        f"Пользователь {username} удалён."
        if state.settings.get("language", "ru") == "ru"
        else f"User {username} has been deleted."
    )