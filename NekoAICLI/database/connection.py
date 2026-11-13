import mysql.connector

from core import state
from core.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)
from core.localization import t
from core.ui import style
from core.response import Response


def connect_db():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=5
        )

        return connection

    except mysql.connector.Error as exception:

        error_code = getattr(exception, "errno", None)

        if error_code in (2003, 2005, 2006, 2013):
            print(t("database_server_unavailable", state.settings))
        elif error_code == 1045:
            print(t("database_auth_error", state.settings))
        elif error_code == 1044:
            print(t("database_access_denied", state.settings))
        elif error_code == 1049:
            print(t("database_not_found", state.settings))
        else:
            print(t("database_error", state.settings, error=exception))

        return None


def reconnect(*args):

    r = Response()

    if args:
        return r.warning(t("reconnect_usage", state.settings))

    if state.db is not None:
        try:
            if state.db.is_connected():
                state.db.close()
        except Exception:
            pass

    state.db = None

    r.text(t("reconnect_connecting", state.settings), "main")

    try:

        state.db = connect_db()

        if state.db is not None and state.db.is_connected():
            r.success(t("reconnect_success", state.settings))
        else:
            r.error(t("reconnect_failed", state.settings))

    except Exception:

        state.db = None
        r.error(t("reconnect_failed", state.settings))

    return r
