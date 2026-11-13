from core import state
from core.localization import t
from core.ui import style, error, title

from database.queries import (
    cleanup_expired_moderation,
    get_admin_statistics
)

from admin.access import admin_access


def admin_statistics():

    if not admin_access():
        return

    cleanup_expired_moderation()

    statistics = get_admin_statistics()

    if statistics is None:

        error(
            t(
                "database_error",
                state.settings
            )
        )

        return

    users_count = statistics["users_count"]
    admins_count = statistics["admins_count"]
    online_count = statistics["online_count"]
    banned_count = statistics["banned_count"]
    muted_count = statistics["muted_count"]
    messages_count = statistics["messages_count"]
    messages_today = statistics["messages_today"]
    notes_count = statistics["notes_count"]
    tasks_count = statistics["tasks_count"]
    completed_tasks = statistics["completed_tasks"]
    new_users_today = statistics["new_users_today"]
    new_users_week = statistics["new_users_week"]

    title(
        "СТАТИСТИКА"
        if state.settings.get("language", "ru") == "ru"
        else "STATISTICS"
    )

    print(
        style(
            "main",
            f"""
╭─ USERS ─────────────────────╮
│ Total:             {users_count}
│ Online:            {online_count}
│ Admins:            {admins_count}
│ Banned:            {banned_count}
│ Muted:             {muted_count}
╰─────────────────────────────╯

╭─ MESSENGER ─────────────────╮
│ Messages:          {messages_count}
│ Today:             {messages_today}
╰─────────────────────────────╯

╭─ DATA ──────────────────────╮
│ Notes:             {notes_count}
│ Tasks:             {tasks_count}
│ Completed tasks:   {completed_tasks}
╰─────────────────────────────╯

╭─ ACTIVITY ──────────────────╮
│ New users today:   {new_users_today}
│ New users / 7 days:{new_users_week}
╰─────────────────────────────╯
"""
        )
    )