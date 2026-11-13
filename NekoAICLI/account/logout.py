from core import state
from core.localization import t
from core.response import Response
from database.queries import set_user_offline


def logout(*args):

    if state.current_user is None:
        return Response().warning(
            t("not_logged_in", state.settings)
        )

    username = state.current_user["username"]

    set_user_offline()

    state.current_user = None

    return Response().success(
        t("logout_success", state.settings, username=username)
    )
