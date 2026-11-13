import os
import random
from datetime import datetime

from core import state
from core.localization import t, command_description
from core.ui import style, success, title
from core.response import Response
from admin.access import is_admin
from database.queries import set_user_offline


def say_hi(*args):
    return Response().text(
        t("greeting", state.settings), "main"
    )


def cmd_clear(*args):
    return Response().clear().success(
        t("console_cleared", state.settings)
    )


def cmd_time(*args):
    now = datetime.now()
    return Response().text(
        t("time", state.settings, time=f"{now:%H:%M:%S}"), "main"
    )


def cmd_date(*args):
    now = datetime.now()
    return Response().text(
        t("date", state.settings, date=f"{now:%d.%m.%Y}"), "main"
    )


def roll(*args):
    r = Response()

    try:
        if len(args) != 2:
            return r.warning(t("roll_usage", state.settings))

        minimum = int(args[0])
        maximum = int(args[1])

        if minimum > maximum:
            raise ValueError(t("min_greater_max", state.settings))

        result = random.randint(minimum, maximum)
        return r.success(t("roll_result", state.settings, result=result))

    except ValueError as exception:
        return r.error(t("error", state.settings, error=exception))


def choice(*args):
    if len(args) < 2:
        return Response().warning(t("choice_usage", state.settings))

    result = random.choice(args)
    return Response().success(t("choice_result", state.settings, result=result))


def count(*args):
    if not args:
        return Response().warning(t("count_usage", state.settings))

    return Response().success(t("count_result", state.settings, amount=len(args)))


def repeat(*args):
    r = Response()

    try:
        if len(args) < 2:
            return r.warning(t("repeat_usage", state.settings))

        amount = int(args[0])

        if amount < 1:
            raise ValueError(t("repeat_positive", state.settings))

        if amount > 1000:
            raise ValueError(t("repeat_max", state.settings))

        text = " ".join(args[1:])

        for _ in range(amount):
            r.text(text, "main")

        return r

    except ValueError as exception:
        return r.error(t("error", state.settings, error=exception))


def echo(*args):
    if not args:
        return Response().warning(t("echo_usage", state.settings))

    text = " ".join(args)
    return Response().text(
        t("echo_result", state.settings, text=text), "main"
    )


def say(*args):
    if not args:
        return Response().warning(t("say_usage", state.settings))

    return Response().text(" ".join(args), "main")


def joke(*args):
    return Response().text(t("joke", state.settings), "main")


def show_changelog(*args):
    r = Response()
    r.title(t("changelog_title", state.settings))
    r.text(
        f"""│ {t("changelog_new", state.settings)}
│
│ ✓ {t("changelog_01", state.settings)}
│ ✓ {t("changelog_02", state.settings)}
│ ✓ {t("changelog_03", state.settings)}
│ ✓ {t("changelog_04", state.settings)}
│ ✓ {t("changelog_05", state.settings)}
│ ✓ {t("changelog_06", state.settings)}
│ ✓ {t("changelog_07", state.settings)}
│ ✓ {t("changelog_08", state.settings)}
│ ✓ {t("changelog_09", state.settings)}
│ ✓ {t("changelog_10", state.settings)}
│ ✓ {t("changelog_11", state.settings)}
│ ✓ {t("changelog_12", state.settings)}
│ ✓ {t("changelog_13", state.settings)}
│ ✓ {t("changelog_14", state.settings)}""",
        "main"
    )
    return r


def cmd_exit(*args):
    set_user_offline()
    r = Response()
    r.success(t("exit", state.settings))
    r.exit()
    return r


def cmd_list(commands, command_categories, *args):
    r = Response()
    r.title(t("commands_title", state.settings))

    categorized = []

    for category, category_commands in command_categories.items():
        if category == "admin" and not is_admin():
            continue

        r.text(f"\n{t(f'category_{category}', state.settings)}", "title")

        for command in category_commands:
            if command not in commands:
                continue

            categorized.append(command)

            description = command_description(command, state.settings)

            r.text(f"│ {command:<12} — {description}", "main")

    plugin_commands = [
        cmd for cmd in commands if cmd not in categorized
    ]

    if plugin_commands:
        r.text(f"\n{t('category_plugins', state.settings)}", "title")

        for command in plugin_commands:
            description = command_description(command, state.settings)
            r.text(f"│ {command:<12} — {description}", "main")

    return r
