from core import state
from core.ui import (
    style,
    warning,
    title
)

from database.queries import (
    cleanup_expired_moderation,
    set_user_status
)

from admin.access import admin_access
from admin.users import (
    admin_users,
    admin_user_info,
    admin_delete_user
)
from admin.moderation import (
    admin_apply_moderation,
    admin_remove_moderation
)
from admin.statistics import admin_statistics


def admin_panel(*args):

    if not admin_access():
        return

    while True:

        cleanup_expired_moderation()

        set_user_status(
            "interface"
        )

        print()

        title(
            "ADMIN PANEL"
        )

        print(
            style(
                "main",
                """
│
│ 1. 👥 Users
│ 2. 🔎 User info
│ 3. 🚫 Ban user
│ 4. 🔓 Unban user
│ 5. 🔇 Mute user
│ 6. 🔊 Unmute user
│ 7. 🗑️ Delete user
│ 8. 📊 Statistics
│
│ 0. ← Exit
│"""
            )
        )

        choice_value = input(
            "Select: "
        ).strip()

        if choice_value == "1":

            admin_users()

            input(
                "\nPress Enter..."
            )

        elif choice_value == "2":

            username = input(
                "Username: "
            ).strip()

            if username:
                admin_user_info(username)

            input(
                "\nPress Enter..."
            )

        elif choice_value == "3":

            username = input(
                "Username to ban: "
            ).strip()

            if username:
                admin_apply_moderation(
                    username,
                    "ban"
                )

            input(
                "\nPress Enter..."
            )

        elif choice_value == "4":

            username = input(
                "Username to unban: "
            ).strip()

            if username:
                admin_remove_moderation(
                    username,
                    "ban"
                )

            input(
                "\nPress Enter..."
            )

        elif choice_value == "5":

            username = input(
                "Username to mute: "
            ).strip()

            if username:
                admin_apply_moderation(
                    username,
                    "mute"
                )

            input(
                "\nPress Enter..."
            )

        elif choice_value == "6":

            username = input(
                "Username to unmute: "
            ).strip()

            if username:
                admin_remove_moderation(
                    username,
                    "mute"
                )

            input(
                "\nPress Enter..."
            )

        elif choice_value == "7":

            username = input(
                "Username to delete: "
            ).strip()

            if username:
                admin_delete_user(username)

            input(
                "\nPress Enter..."
            )

        elif choice_value == "8":

            admin_statistics()

            input(
                "\nPress Enter..."
            )

        elif choice_value == "0":

            return

        else:

            warning(
                "Неизвестный пункт."
                if state.settings.get("language", "ru") == "ru"
                else "Unknown option."
            )