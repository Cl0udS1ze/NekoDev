# =========================================================
# IMPORTS
# =========================================================
from core.requirements import ensure_requirements
from core.updater import check_updates

import os
import json

from core import state
from core.response import Response, render_cli
from core.config import (
    PLUGINS_DIR,
    default_settings,
)
from core.ui import (
    style,
    warning,
    error,
    title
)
from core.localization import t

ensure_requirements()

from database.connection import (
    connect_db,
    reconnect
)
from database.queries import (
    set_user_status,
    set_user_offline,
    cleanup_expired_moderation
)

from account.register import register
from account.login import login
from account.logout import logout
from account.profile import show_profile

from admin.panel import admin_panel

from commands.system import (
    say_hi,
    cmd_clear,
    cmd_time,
    cmd_date,
    roll,
    choice,
    count,
    repeat,
    echo,
    say,
    joke,
    show_changelog,
    cmd_exit,
    cmd_list,
)

from commands.calculator import calculator
from commands.info import show_info
from commands.plugins import show_plugins

from messenger.chat import chat
from messenger.messages import newmessages
from messenger.blocks import (
    block,
    unblock
)

from commands.notes import (
    note_add,
    note_get,
    note_del,
    load_notes,
)

from commands.tasks import (
    task_add,
    show_tasks,
    complete,
    del_task,
    load_tasks
)

from commands.settings import (
    load_settings,
    show_settings,
    set_setting
)

from commands.registry import (
    command_categories,
    aliases
)

from plugins.loader import load_plugins

from ai.fallback import ai_fallback
from ai.chat import ai_ask, ai_clear, ai_status



# =========================================================
# INITIAL STATE
# =========================================================

state.settings = default_settings.copy()

check_updates()


# =========================================================
# PLUGINS
# =========================================================

state.plugins = os.listdir(PLUGINS_DIR)
state.loaded_plugins = []


# =========================================================
# ЛОКАЛИЗАЦИЯ
# =========================================================

def command_description(command):
    return t(f"desc_{command}", state.settings)


# =========================================================
# ЗАГРУЗКА ДАННЫХ
# =========================================================

try:
    state.settings = load_settings()
except json.JSONDecodeError:
    state.settings = default_settings.copy()

try:
    state.notes = load_notes()
except json.JSONDecodeError:
    state.notes = {}

try:
    state.tasks = load_tasks()
except json.JSONDecodeError:
    state.tasks = {}


# =========================================================
# КОМАНДЫ
# =========================================================

commands = {

    "clear": cmd_clear,
    "settings": show_settings,
    "changelog": show_changelog,
    "set": set_setting,
    "profile": show_profile,

    "addtask": task_add,
    "tasks": show_tasks,
    "complete": complete,
    "deltask": del_task,

    "plugins": show_plugins,

    "hi": say_hi,
    "info": show_info,
    "joke": joke,
    "cmds": None,
    "reconnect": reconnect,

    "say": say,
    "echo": echo,
    "count": count,
    "repeat": repeat,

    "calc": calculator,
    "roll": roll,
    "time": cmd_time,
    "date": cmd_date,
    "choice": choice,

    "remember": note_add,
    "notes": note_get,
    "forget": note_del,

    "register": register,
    "login": login,
    "logout": logout,

    "ask": ai_ask,
    "clearai": ai_clear,
    "nekogpt": ai_status,


    "chat": chat,
    "newmessages": newmessages,
    "block": block,
    "unblock": unblock,

    "admin": admin_panel,
    "exit": cmd_exit
}

commands["cmds"] = lambda *args: cmd_list(
    commands,
    command_categories,
    *args
)


# =========================================================
# ЗАГРУЗКА ПЛАГИНОВ
# =========================================================

load_plugins(commands)


# =========================================================
# ЗАПУСК
# =========================================================

title(t("startup_title", state.settings))

print(style("main", t("startup_line_1", state.settings)))
print(style("main", t("startup_line_2", state.settings)))
print()


# =========================================================
# ПОДКЛЮЧЕНИЕ К СЕРВЕРУ
# =========================================================

state.db = connect_db()

if state.db is not None:

    print(style("success", t("online_mode", state.settings)))
    print(style("success", t("database_connected", state.settings)))

    try:
        cleanup_expired_moderation()
    except Exception as exception:
        warning(t("moderation_cleanup_error", state.settings, error=exception))

else:

    print(style("warning", t("offline_mode", state.settings)))


# =========================================================
# ГЛАВНЫЙ ЦИКЛ
# =========================================================

try:

    while True:

        try:

            # =================================================
            # СТАТУС ПОЛЬЗОВАТЕЛЯ
            # =================================================

            if state.current_user is not None:
                set_user_status("interface")

            command = input("> ")

        except EOFError:

            set_user_offline()
            warning("\n" + t("input_finished", state.settings))
            break


        # =================================================
        # ПОДГОТОВКА КОМАНДЫ
        # =================================================

        command = command.strip()

        if not command:
            continue

        parts = command.split()
        command_name = parts[0]


        # =================================================
        # ALIAS
        # =================================================

        command_name = aliases.get(command_name, command_name)


        # =================================================
        # AI FALLBACK
        # =================================================

        if command_name not in commands:

            command_name, parts, handled = ai_fallback(
                command,
                command_name,
                parts,
                commands,
                show_changelog,
                reconnect
            )

            if handled:
                continue


        # =================================================
        # ВЫПОЛНЕНИЕ КОМАНДЫ
        # =================================================

        try:

            response = commands[command_name](*parts[1:])

            if response:
                if render_cli(response):
                    break

        except Exception as exception:

            render_cli(
                Response().error(
                    t("command_error", state.settings, error=exception)
                )
            )


# =========================================================
# CTRL + C
# =========================================================

except KeyboardInterrupt:

    set_user_offline()
    warning("\n\n" + t("ai_finished", state.settings))


# =========================================================
# ОСТАНОВКА
# =========================================================

set_user_offline()

print(style("warning", t("ai_stopped", state.settings)))
