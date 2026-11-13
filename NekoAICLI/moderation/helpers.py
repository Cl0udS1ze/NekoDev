from database.queries import get_active_moderation


def get_moderation_text(
    user_uuid,
    moderation_type
):

    moderation = get_active_moderation(
        user_uuid,
        moderation_type
    )

    if moderation is None:
        return None

    expires_at = moderation[3]

    if expires_at is None:

        return {
            "reason": moderation[2],
            "expires_at": None
        }

    return {
        "reason": moderation[2],
        "expires_at": expires_at
    }
    
# =========================================================
# ПРОВЕРКА БАНА
# =========================================================

def is_user_banned(user_uuid):

    return (
        get_active_moderation(
            user_uuid,
            "ban"
        )
        is not None
    )