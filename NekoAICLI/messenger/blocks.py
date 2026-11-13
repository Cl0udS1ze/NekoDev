from core import state
from core.localization import t
from core.response import Response

from database.queries import (
    is_blocked as database_is_blocked,
    is_blocked_between as database_is_blocked_between,
    create_block,
    delete_block,
    get_user_by_username,
)


def is_blocked(user_uuid, other_uuid):
    return database_is_blocked(user_uuid, other_uuid)


def is_blocked_between(user_uuid, other_uuid):
    return database_is_blocked_between(user_uuid, other_uuid)


def block(*args):

    if state.current_user is None:
        return Response().error(
            t("chat_account_required", state.settings)
        )

    if state.db is None or not state.db.is_connected():
        return Response().error(
            t("block_database_required", state.settings)
        )

    if len(args) != 1:
        return Response().warning(
            t("block_usage", state.settings)
        )

    username = args[0]
    user = get_user_by_username(username)

    if user is None:
        return Response().error(
            t("block_user_not_found", state.settings)
        )

    if user["uuid"] == state.current_user["uuid"]:
        return Response().error(
            t("block_self", state.settings)
        )

    if is_blocked(state.current_user["uuid"], user["uuid"]):
        return Response().warning(
            t("block_already", state.settings)
        )

    if not create_block(state.current_user["uuid"], user["uuid"]):
        return Response().error(
            t("database_error", state.settings)
        )

    return Response().success(
        t("block_success", state.settings, username=user["username"])
    )


def unblock(*args):

    if state.current_user is None:
        return Response().error(
            t("chat_account_required", state.settings)
        )

    if state.db is None or not state.db.is_connected():
        return Response().error(
            t("block_database_required", state.settings)
        )

    if len(args) != 1:
        return Response().warning(
            t("unblock_usage", state.settings)
        )

    username = args[0]
    user = get_user_by_username(username)

    if user is None:
        return Response().error(
            t("block_user_not_found", state.settings)
        )

    if not delete_block(state.current_user["uuid"], user["uuid"]):
        return Response().warning(
            t("block_not_found", state.settings)
        )

    return Response().success(
        t("unblock_success", state.settings, username=user["username"])
    )
