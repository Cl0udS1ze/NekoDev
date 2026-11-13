# =========================================================
# DATABASE QUERIES
# =========================================================

from core import state


# =========================================================
# USERS
# =========================================================

def get_user_by_username(username):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT uuid, username
            FROM neko_users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return None

        return {
            "uuid": user[0],
            "username": user[1]
        }

    finally:

        cursor.close()


def get_username_by_uuid(user_uuid):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT username
            FROM neko_users
            WHERE uuid = %s
            """,
            (user_uuid,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        return user[0]

    finally:

        cursor.close()
        
# =========================================================
# DATABASE QUERIES
# =========================================================

import mysql.connector

from core import state


# =========================================================
# USERS
# =========================================================

def get_user_by_username(username):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT uuid, username
            FROM neko_users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            return None

        return {
            "uuid": user[0],
            "username": user[1]
        }

    finally:

        cursor.close()


def get_username_by_uuid(user_uuid):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT username
            FROM neko_users
            WHERE uuid = %s
            """,
            (user_uuid,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        return user[0]

    finally:

        cursor.close()


# =========================================================
# SESSIONS
# =========================================================

def set_user_status(
    status,
    chat_with_uuid=None
):

    if state.current_user is None:
        return False

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_sessions
            (
                user_uuid,
                status,
                chat_with_uuid,
                last_seen
            )
            VALUES (%s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
                status = VALUES(status),
                chat_with_uuid = VALUES(chat_with_uuid),
                last_seen = NOW()
            """,
            (
                state.current_user["uuid"],
                status,
                chat_with_uuid
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def set_user_offline():

    if state.current_user is None:
        return False

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            UPDATE neko_sessions
            SET
                status = 'offline',
                chat_with_uuid = NULL,
                last_seen = NOW()
            WHERE user_uuid = %s
            """,
            (
                state.current_user["uuid"],
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# ACCOUNT
# =========================================================

def username_exists(username):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM neko_users
            WHERE username = %s
            """,
            (username,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()


def create_user(
    user_uuid,
    username,
    password_hash,
    password_salt
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_users
            """
        )

        user_count = cursor.fetchone()[0]

        is_admin = (
            1
            if user_count == 0
            else 0
        )

        cursor.execute(
            """
            INSERT INTO neko_users
            (
                uuid,
                username,
                password_hash,
                password_salt,
                is_admin
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_uuid,
                username,
                password_hash,
                password_salt,
                is_admin
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# AUTHENTICATION
# =========================================================

def get_user_credentials(username):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                uuid,
                username,
                password_hash,
                password_salt,
                is_admin
            FROM neko_users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if user is None:
            return None

        return {
            "uuid": user[0],
            "username": user[1],
            "password_hash": user[2],
            "password_salt": user[3],
            "is_admin": bool(user[4])
        }

    finally:

        cursor.close()
        
# =========================================================
# USER RUNS
# =========================================================

def increment_user_runs(user_uuid):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            UPDATE neko_users
            SET runs = runs + 1
            WHERE uuid = %s
            """,
            (user_uuid,)
        )

        state.db.commit()

        return cursor.rowcount > 0

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# MODERATION
# =========================================================

def get_active_moderation(
    user_uuid,
    moderation_type
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                type,
                reason,
                expires_at,
                created_at
            FROM neko_moderation
            WHERE user_uuid = %s
            AND type = %s
            AND (
                expires_at IS NULL
                OR expires_at > NOW()
            )
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                user_uuid,
                moderation_type
            )
        )

        return cursor.fetchone()

    finally:

        cursor.close()
        
def cleanup_expired_moderation():

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM neko_moderation
            WHERE expires_at IS NOT NULL
            AND expires_at <= NOW()
            """
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# NOTES
# =========================================================

def create_note(
    user_uuid,
    name,
    text
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_notes
            (user_uuid, name, text)
            VALUES (%s, %s, %s)
            """,
            (
                user_uuid,
                name,
                text
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# GET NOTES
# =========================================================

def get_user_notes(user_uuid):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT id, name, text
            FROM neko_notes
            WHERE user_uuid = %s
            ORDER BY id
            """,
            (
                user_uuid,
            )
        )

        return cursor.fetchall()

    finally:

        cursor.close()
        
# =========================================================
# DELETE NOTE
# =========================================================

def delete_note(
    user_uuid,
    note_id
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM neko_notes
            WHERE id = %s
            AND user_uuid = %s
            """,
            (
                note_id,
                user_uuid
            )
        )

        if cursor.rowcount == 0:
            return False

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# TASKS
# =========================================================

def create_task(
    user_uuid,
    task
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_tasks
            (user_uuid, task, completed)
            VALUES (%s, %s, %s)
            """,
            (
                user_uuid,
                task,
                0
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def get_user_tasks(user_uuid):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT id, task, completed
            FROM neko_tasks
            WHERE user_uuid = %s
            ORDER BY id
            """,
            (
                user_uuid,
            )
        )

        return cursor.fetchall()

    finally:

        cursor.close()


def complete_task(
    user_uuid,
    task
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            UPDATE neko_tasks
            SET completed = 1
            WHERE user_uuid = %s
            AND task = %s
            """,
            (
                user_uuid,
                task
            )
        )

        if cursor.rowcount == 0:
            return False

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def delete_task(
    user_uuid,
    task
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM neko_tasks
            WHERE user_uuid = %s
            AND task = %s
            """,
            (
                user_uuid,
                task
            )
        )

        if cursor.rowcount == 0:
            return False

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# MESSAGES
# =========================================================

def get_global_messages():

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return []

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                sender_uuid,
                message,
                created_at
            FROM neko_messages
            WHERE receiver_uuid IS NULL
            ORDER BY created_at DESC, id DESC
            LIMIT 30
            """
        )

        messages = cursor.fetchall()

        messages.reverse()

        return messages

    finally:

        cursor.close()


def create_global_message(
    sender_uuid,
    message
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_messages
            (
                sender_uuid,
                receiver_uuid,
                message
            )
            VALUES (%s, NULL, %s)
            """,
            (
                sender_uuid,
                message
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def get_private_messages(
    user_uuid,
    receiver_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return []

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                sender_uuid,
                message,
                created_at
            FROM neko_messages
            WHERE
                (
                    sender_uuid = %s
                    AND receiver_uuid = %s
                )
                OR
                (
                    sender_uuid = %s
                    AND receiver_uuid = %s
                )
            ORDER BY created_at DESC, id DESC
            LIMIT 30
            """,
            (
                user_uuid,
                receiver_uuid,
                receiver_uuid,
                user_uuid
            )
        )

        messages = cursor.fetchall()

        messages.reverse()

        return messages

    finally:

        cursor.close()


def create_private_message(
    sender_uuid,
    receiver_uuid,
    message
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_messages
            (
                sender_uuid,
                receiver_uuid,
                message
            )
            VALUES (%s, %s, %s)
            """,
            (
                sender_uuid,
                receiver_uuid,
                message
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


# =========================================================
# BLOCKS
# =========================================================

def is_blocked(
    user_uuid,
    other_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM neko_blocks
            WHERE blocker_uuid = %s
            AND blocked_uuid = %s
            """,
            (
                user_uuid,
                other_uuid
            )
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()


def is_blocked_between(
    user_uuid,
    other_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM neko_blocks
            WHERE
                (
                    blocker_uuid = %s
                    AND blocked_uuid = %s
                )
                OR
                (
                    blocker_uuid = %s
                    AND blocked_uuid = %s
                )
            LIMIT 1
            """,
            (
                user_uuid,
                other_uuid,
                other_uuid,
                user_uuid
            )
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()


def create_block(
    blocker_uuid,
    blocked_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_blocks
            (
                blocker_uuid,
                blocked_uuid
            )
            VALUES (%s, %s)
            """,
            (
                blocker_uuid,
                blocked_uuid
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def delete_block(
    blocker_uuid,
    blocked_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM neko_blocks
            WHERE blocker_uuid = %s
            AND blocked_uuid = %s
            """,
            (
                blocker_uuid,
                blocked_uuid
            )
        )

        deleted = cursor.rowcount

        if deleted == 0:
            return False

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


# =========================================================
# UNREAD MESSAGES
# =========================================================

def get_unread_messages(
    user_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return []

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                sender_uuid,
                receiver_uuid,
                message,
                created_at
            FROM neko_messages
            WHERE receiver_uuid = %s
            AND is_read = 0
            ORDER BY created_at ASC, id ASC
            """,
            (
                user_uuid,
            )
        )

        return cursor.fetchall()

    finally:

        cursor.close()


def has_unread_messages(
    user_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_messages
            WHERE receiver_uuid = %s
            AND is_read = 0
            """,
            (
                user_uuid,
            )
        )

        count = cursor.fetchone()[0]

        return count > 0

    finally:

        cursor.close()


def mark_messages_read(
    user_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            UPDATE neko_messages
            SET is_read = 1
            WHERE receiver_uuid = %s
            AND is_read = 0
            """,
            (
                user_uuid,
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()
        
# =========================================================
# PROFILE
# =========================================================

def get_db_profile(user_uuid):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                uuid,
                username,
                is_admin,
                runs,
                created_at
            FROM neko_users
            WHERE uuid = %s
            """,
            (
                user_uuid,
            )
        )

        return cursor.fetchone()

    finally:

        cursor.close()
        
# =========================================================
# ADMIN
# =========================================================

def get_admin_users():

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                u.id,
                u.uuid,
                u.username,
                u.is_admin,
                u.created_at,
                s.status,
                s.chat_with_uuid,
                s.last_seen
            FROM neko_users u
            LEFT JOIN neko_sessions s
                ON u.uuid = s.user_uuid
            ORDER BY u.id ASC
            """
        )

        return cursor.fetchall()

    finally:

        cursor.close()


def get_admin_user(username):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            SELECT
                u.id,
                u.uuid,
                u.username,
                u.is_admin,
                u.created_at,
                s.status,
                s.chat_with_uuid,
                s.last_seen
            FROM neko_users u
            LEFT JOIN neko_sessions s
                ON u.uuid = s.user_uuid
            WHERE u.username = %s
            """,
            (
                username,
            )
        )

        return cursor.fetchone()

    finally:

        cursor.close()


def create_moderation(
    user_uuid,
    moderation_type,
    reason,
    expires_at
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO neko_moderation
            (
                user_uuid,
                type,
                reason,
                expires_at
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                user_uuid,
                moderation_type,
                reason,
                expires_at
            )
        )

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def delete_moderation(
    user_uuid,
    moderation_type
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return 0

    cursor = state.db.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM neko_moderation
            WHERE user_uuid = %s
            AND type = %s
            """,
            (
                user_uuid,
                moderation_type
            )
        )

        deleted = cursor.rowcount

        state.db.commit()

        return deleted

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return 0

    finally:

        cursor.close()


def delete_user(
    user_uuid
):

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return False

    cursor = state.db.cursor()

    try:

        # =================================================
        # MESSAGES
        # =================================================

        cursor.execute(
            """
            DELETE FROM neko_messages
            WHERE sender_uuid = %s
            OR receiver_uuid = %s
            """,
            (
                user_uuid,
                user_uuid
            )
        )

        # =================================================
        # USER
        # =================================================

        cursor.execute(
            """
            DELETE FROM neko_users
            WHERE uuid = %s
            """,
            (
                user_uuid,
            )
        )

        if cursor.rowcount == 0:

            state.db.rollback()

            return False

        state.db.commit()

        return True

    except mysql.connector.Error:

        try:
            state.db.rollback()
        except Exception:
            pass

        return False

    finally:

        cursor.close()


def get_admin_statistics():

    if (
        state.db is None
        or not state.db.is_connected()
    ):
        return None

    cursor = state.db.cursor()

    try:

        statistics = {}

        # =================================================
        # USERS
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_users
            """
        )

        statistics["users_count"] = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_users
            WHERE is_admin = 1
            """
        )

        statistics["admins_count"] = (
            cursor.fetchone()[0]
        )

        # =================================================
        # ONLINE
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_sessions
            WHERE status != 'offline'
            """
        )

        statistics["online_count"] = (
            cursor.fetchone()[0]
        )

        # =================================================
        # MODERATION
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_moderation
            WHERE type = 'ban'
            AND (
                expires_at IS NULL
                OR expires_at > NOW()
            )
            """
        )

        statistics["banned_count"] = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_moderation
            WHERE type = 'mute'
            AND (
                expires_at IS NULL
                OR expires_at > NOW()
            )
            """
        )

        statistics["muted_count"] = (
            cursor.fetchone()[0]
        )

        # =================================================
        # MESSAGES
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_messages
            """
        )

        statistics["messages_count"] = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_messages
            WHERE DATE(created_at) = CURDATE()
            """
        )

        statistics["messages_today"] = (
            cursor.fetchone()[0]
        )

        # =================================================
        # NOTES
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_notes
            """
        )

        statistics["notes_count"] = (
            cursor.fetchone()[0]
        )

        # =================================================
        # TASKS
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_tasks
            """
        )

        statistics["tasks_count"] = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_tasks
            WHERE completed = 1
            """
        )

        statistics["completed_tasks"] = (
            cursor.fetchone()[0]
        )

        # =================================================
        # ACTIVITY
        # =================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_users
            WHERE DATE(created_at) = CURDATE()
            """
        )

        statistics["new_users_today"] = (
            cursor.fetchone()[0]
        )

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM neko_users
            WHERE created_at >=
                DATE_SUB(NOW(), INTERVAL 7 DAY)
            """
        )

        statistics["new_users_week"] = (
            cursor.fetchone()[0]
        )

        return statistics

    finally:

        cursor.close()