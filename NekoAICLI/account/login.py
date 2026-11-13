from core import state
from core.localization import t
from core.response import Response
from core.security import verify_pass

from database.queries import (
    cleanup_expired_moderation,
    get_user_credentials,
    increment_user_runs,
    has_unread_messages,
    set_user_status,
)

from moderation.helpers import get_moderation_text


def login(*args):

    r = Response()

    if state.db is None or not state.db.is_connected():
        return r.error(t("database_required", state.settings))

    if state.current_user is not None:
        return r.warning(
            t(
                "already_logged_in",
                state.settings,
                username=state.current_user["username"]
            )
        )

    if len(args) != 2:
        return r.warning(t("login_usage", state.settings))

    username = args[0]
    password = args[1]

    cleanup_expired_moderation()

    user = get_user_credentials(username)

    if not user:
        return r.error(t("user_not_found", state.settings))

    user_uuid = user["uuid"]
    username = user["username"]
    password_hash = user["password_hash"]
    password_salt = user["password_salt"]
    is_admin = user["is_admin"]

    if not verify_pass(password, password_hash, password_salt):
        return r.error(t("wrong_password", state.settings))

    increment_user_runs(user_uuid)

    ban = get_moderation_text(user_uuid, "ban")

    if ban is not None:

        if ban["expires_at"] is None:
            return r.error(
                t("account_banned_forever", state.settings)
            )

        return r.error(
            t(
                "account_banned_until",
                state.settings,
                date=ban["expires_at"].strftime("%d.%m.%Y %H:%M")
            )
        )

    state.current_user = {
        "uuid": user_uuid,
        "username": username,
        "is_admin": bool(is_admin)
    }

    set_user_status("interface")

    r.success(
        t("login_success", state.settings, username=username)
    )

    if has_unread_messages(user_uuid):
        r.warning(
            t("newmessages_notification", state.settings)
        )

    return r
