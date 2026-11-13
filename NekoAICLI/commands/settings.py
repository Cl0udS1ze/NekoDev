import os
import json

from core import state
from core.config import SETTINGS_FILE, default_settings
from core.localization import t
from core.response import Response
from core.theme import themes
from database.queries import set_user_status


def load_settings():

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return default_settings.copy()


def save_settings():

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            state.settings,
            file,
            ensure_ascii=False,
            indent=4
        )


def show_settings(*args):

    if state.current_user is not None:
        set_user_status("interface")

    r = Response()
    r.title(t("settings_title", state.settings))

    for name, value in state.settings.items():
        r.text(f"│ {name}: {value}", "main")

    return r


def set_setting(*args):

    r = Response()

    if len(args) < 2:
        return r.warning(t("set_usage", state.settings))

    setting = args[0].lower()
    value = args[1]

    allowed_settings = (
        "language",
        "theme",
        "cloudflare_api_token",
        "cloudflare_account_id",
    )

    if setting not in allowed_settings:
        return r.warning(t("setting_must_exist", state.settings))

    if setting == "language":
        value = value.lower()
        if value not in ("ru", "en"):
            return r.warning(t("language_invalid", state.settings))

    if setting == "theme":
        value = value.lower()
        if value not in themes:
            return r.warning(t("theme_invalid", state.settings))

    if setting == "yandexgpt_model":
        value = value.lower()
        if value not in ("yandexgpt", "yandexgpt-lite", "yandexgpt-5.1"):
            return r.warning(
                "Доступные модели: yandexgpt, yandexgpt-lite, yandexgpt-5.1"
            )

    state.settings[setting] = value
    save_settings()

    return r.success(
        t("setting_changed", state.settings, setting=setting, value=value)
    )
