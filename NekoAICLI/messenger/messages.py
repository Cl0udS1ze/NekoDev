from core import state
from core.localization import t
from core.response import Response

from database.queries import (
    get_global_messages as database_get_global_messages,
    create_global_message,
    get_private_messages,
    create_private_message,
    get_unread_messages as database_get_unread_messages,
    has_unread_messages as database_has_unread_messages,
    mark_messages_read as database_mark_messages_read,
    get_user_by_username,
    get_username_by_uuid,
    get_active_moderation,
)

from messenger.blocks import is_blocked_between


def is_user_muted(user_uuid):
    return get_active_moderation(user_uuid, "mute") is not None


def get_global_messages():
    if state.current_user is None:
        return []
    return database_get_global_messages()


def send_global_message(message):
    if state.current_user is None:
        return False
    if state.db is None or not state.db.is_connected():
        return False
    if is_user_muted(state.current_user["uuid"]):
        return False
    return create_global_message(state.current_user["uuid"], message)


def get_messages(receiver_uuid):
    if state.current_user is None:
        return []
    return get_private_messages(state.current_user["uuid"], receiver_uuid)


def send_message(receiver_username, message):
    if state.current_user is None:
        return False
    if state.db is None or not state.db.is_connected():
        return False
    if is_user_muted(state.current_user["uuid"]):
        return False
    receiver = get_user_by_username(receiver_username)
    if receiver is None:
        return False
    if receiver["uuid"] == state.current_user["uuid"]:
        return False
    if is_blocked_between(state.current_user["uuid"], receiver["uuid"]):
        return False
    return create_private_message(
        state.current_user["uuid"], receiver["uuid"], message
    )


def get_unread_messages():
    if state.current_user is None:
        return []
    return database_get_unread_messages(state.current_user["uuid"])


def has_unread_messages():
    if state.current_user is None:
        return False
    return database_has_unread_messages(state.current_user["uuid"])


def mark_messages_read():
    if state.current_user is None:
        return False
    return database_mark_messages_read(state.current_user["uuid"])


def newmessages(*args):

    if state.current_user is None:
        return Response().error(
            t("chat_account_required", state.settings)
        )

    if state.db is None or not state.db.is_connected():
        return Response().error(
            t("chat_database_required", state.settings)
        )

    messages = get_unread_messages()

    if not messages:
        return Response().text(
            t("newmessages_empty", state.settings), "main"
        )

    r = Response()
    r.title(t("newmessages_title", state.settings))

    for message_id, sender_uuid, receiver_uuid, message, created_at in messages:
        username = get_username_by_uuid(sender_uuid)
        if username is None:
            username = t("unknown_user", state.settings)
        message_time = created_at.strftime("%H:%M")
        r.text(f"[{message_time}] {username}: {message}", "main")

    if mark_messages_read():
        r.success(t("newmessages_marked", state.settings))

    return r
