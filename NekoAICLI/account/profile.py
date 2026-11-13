from core import state
from core.localization import t
from core.response import Response
from database.queries import get_db_profile


def show_profile(*args):

    if state.current_user is None:
        return Response().error(
            t("login_required", state.settings)
        )

    profile_data = get_db_profile(
        state.current_user["uuid"]
    )

    if profile_data is None:
        return Response().error(
            t("profile_unavailable", state.settings)
        )

    r = Response()

    r.title(t("profile_title", state.settings))

    r.text(f"👤 {profile_data['username']}", "main")
    r.text(f"🆔 {profile_data['uuid']}", "main")
    r.text(f"📅 {profile_data['created_at']}", "main")
    r.text(f"🚀 {profile_data['runs']}", "main")

    if profile_data["is_admin"]:
        r.text("👑 Admin", "main")

    return r
