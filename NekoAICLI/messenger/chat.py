from datetime import datetime

from core import state
from core.localization import t
from core.ui import style, error, title
from core.response import Response

from database.queries import (
    get_user_by_username,
    get_username_by_uuid,
    set_user_status
)

from messenger.messages import (
    get_global_messages,
    send_global_message,
    get_messages,
    send_message,
    is_user_muted
)

from messenger.blocks import is_blocked_between


def chat(*args):

    if state.current_user is None:
        return Response().error(
            t("chat_account_required", state.settings)
        )

    if state.db is None or not state.db.is_connected():
        return Response().error(
            t("chat_database_required", state.settings)
        )

    if len(args) == 0:
        return _global_chat()

    if len(args) != 1:
        return Response().warning(
            t("chat_usage", state.settings)
        )

    return _private_chat(args[0])


def _global_chat():

    set_user_status("chat")

    try:
        title(t("global_chat_title", state.settings))
        print(style("main", t("chat_exit", state.settings)))

        messages = get_global_messages()

        if not messages:
            print(style("main", t("chat_empty", state.settings)))
        else:
            for sender_uuid, message, created_at in messages:
                username = get_username_by_uuid(sender_uuid)
                if username is None:
                    username = t("unknown_user", state.settings)
                message_time = created_at.strftime("%H:%M")
                if sender_uuid == state.current_user["uuid"]:
                    username = t("message_you", state.settings)
                print(style("main", f"[{message_time}] {username}: {message}"))

        print()

        while True:

            try:
                message = input("> ")
            except EOFError:
                return None

            if message.lower() == "exit":
                return None

            if not message.strip():
                continue

            if is_user_muted(state.current_user["uuid"]):
                error(t("message_muted", state.settings))
                continue

            if send_global_message(message):
                current_time = datetime.now().strftime("%H:%M")
                print(style("main", f"[{current_time}] {t('message_you', state.settings)}: {message}"))
            else:
                error(t("message_send_error", state.settings))

    finally:
        set_user_status("interface")


def _private_chat(username):

    receiver = get_user_by_username(username)

    if receiver is None:
        return Response().error(
            t("chat_user_not_found", state.settings)
        )

    if receiver["uuid"] == state.current_user["uuid"]:
        return Response().error(
            t("chat_self", state.settings)
        )

    set_user_status("chat", receiver["uuid"])

    try:
        title(t("chat_title", state.settings, username=receiver["username"]))
        print(style("main", t("chat_exit", state.settings)))

        messages = get_messages(receiver["uuid"])

        if not messages:
            print(style("main", t("chat_empty", state.settings)))
        else:
            for sender_uuid, message, created_at in messages:
                message_time = created_at.strftime("%H:%M")
                if sender_uuid == state.current_user["uuid"]:
                    username_to_show = t("message_you", state.settings)
                else:
                    username_to_show = receiver["username"]
                print(style("main", f"[{message_time}] {username_to_show}: {message}"))

        print()

        while True:

            try:
                message = input("> ")
            except EOFError:
                return None

            if message.lower() == "exit":
                return None

            if not message.strip():
                continue

            if is_user_muted(state.current_user["uuid"]):
                error(t("message_muted", state.settings))
                continue

            if is_blocked_between(state.current_user["uuid"], receiver["uuid"]):
                error(t("message_blocked", state.settings))
                continue

            if send_message(receiver["username"], message):
                current_time = datetime.now().strftime("%H:%M")
                print(style("main", f"[{current_time}] {t('message_you', state.settings)}: {message}"))
            else:
                error(t("message_send_error", state.settings))

    finally:
        set_user_status("interface")
