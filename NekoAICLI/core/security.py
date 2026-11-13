import hashlib
import secrets


def hash_pass(password):
    """Создать хеш пароля и случайную соль."""

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000
    )

    return (
        password_hash.hex(),
        salt.hex()
    )


def verify_pass(
    password,
    password_hash,
    password_salt
):
    """Проверить пароль."""

    try:

        salt = bytes.fromhex(
            password_salt
        )

    except (
        ValueError,
        TypeError
    ):

        return False

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000
    ).hex()

    return secrets.compare_digest(
        new_hash,
        password_hash
    )