import uuid

from core import state
from core.localization import t
from core.response import Response
from database.queries import username_exists, create_user
from core.security import hash_pass


def register(*args):

    r = Response()

    if state.db is None or not state.db.is_connected():
        return r.error(t("database_required", state.settings))

    if len(args) != 2:
        return r.warning(t("register_usage", state.settings))

    username = args[0]
    password = args[1]

    if username_exists(username):
        return r.error(t("user_exists", state.settings))

    user_uuid = str(uuid.uuid4())

    password_hash, password_salt = hash_pass(password)

    if not create_user(
        user_uuid,
        username,
        password_hash,
        password_salt
    ):
        return r.error(t("database_error", state.settings))

    return r.success(
        t("register_success", state.settings, username=username)
    )
