# =========================================================
# UPDATER
# =========================================================

import os
import sys
import json
import shutil
import zipfile
import tempfile
import urllib.request

from core import state
from core.config import DATA_DIR
from core.ui import style, warning, success, error, title
from core.localization import t


# =========================================================
# КОНФИГУРАЦИЯ
# =========================================================

# URL для проверки обновлений.
# Можно указать GitHub Releases API или прямой JSON.
# Формат JSON:
# {
#     "version": "prealpha-1.2",
#     "url": "https://...download/archive.zip",
#     "changelog": "Что нового..."
# }

UPDATE_CHECK_URL = "https://api.github.com/repos/Cl0udS1ze/Neko-AI/releases/latest"

# Текущая версия проекта.
VERSION = "prealpha-1.1"


# =========================================================
# ПРОВЕРКА ОБНОВЛЕНИЙ
# =========================================================

def _fetch_latest_version():
    """Получить информацию о последней версии. Вернуть dict или None."""

    if not UPDATE_CHECK_URL:
        return None

    try:
        with urllib.request.urlopen(
            UPDATE_CHECK_URL,
            timeout=10
        ) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except Exception:
        return None


def _version_is_newer(latest, current):
    """Сравнить версии. True, если latest новее current."""

    def parse(v):
        # prealpha-1.2 → (1, 2)
        parts = v.replace("prealpha-", "").replace("alpha-", "").replace("beta-", "")
        nums = []
        for part in parts.split("."):
            try:
                nums.append(int(part))
            except ValueError:
                nums.append(0)
        return tuple(nums)

    return parse(latest) > parse(current)


def _ask_permission(message):
    """Спросить у пользователя разрешение. Вернуть True/False."""

    try:
        answer = input(message).strip().lower()
        return answer in ("y", "yes", "д", "да", "")
    except (EOFError, KeyboardInterrupt):
        return False


def _download_file(url, dest_path):
    """Скачать файл. Вернуть True при успехе."""

    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(response, f)
        return True
    except Exception:
        return False


def _backup_project():
    """Создать резервную копию текущих файлов."""

    backup_dir = os.path.join(DATA_DIR, "backup")

    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)

    os.makedirs(backup_dir)

    # Копируем все .py файлы и папки кроме data и backup
    skip = {"data", "__pycache__", ".git"}

    for item in os.listdir("."):

        if item in skip:
            continue

        src = os.path.join(".", item)
        dst = os.path.join(backup_dir, item)

        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        elif item.endswith(".py"):
            shutil.copy2(src, dst)

    return backup_dir


def _apply_update(zip_path):
    """Распаковать обновление поверх текущих файлов."""

    with tempfile.TemporaryDirectory() as tmp_dir:

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_dir)

        # Ищем корневую папку с кодом (где есть .py файлы)
        source_dir = tmp_dir

        entries = os.listdir(tmp_dir)

        if len(entries) == 1:
            only = os.path.join(tmp_dir, entries[0])
            if os.path.isdir(only):
                source_dir = only

        skip = {"data", "__pycache__", ".git"}

        for item in os.listdir(source_dir):

            if item in skip:
                continue

            src = os.path.join(source_dir, item)
            dst = os.path.join(".", item)

            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)


# =========================================================
# ОСНОВНАЯ ФУНКЦИЯ
# =========================================================

def check_updates():

    if not UPDATE_CHECK_URL:
        return

    try:
        import urllib.request
        import json

        request = urllib.request.Request(
            UPDATE_CHECK_URL,
            headers={"Accept": "application/vnd.github+json"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())

        latest_version = data.get("tag_name", "")
        changelog = data.get("body", "")
        download_url = data.get("zipball_url", "")

        if not latest_version or not download_url:
            return

        if not _version_is_newer(latest_version, VERSION):
            return

        print()
        title("UPDATE AVAILABLE")

        print(style("main", f"Current: {VERSION}"))
        print(style("success", f"Latest:  {latest_version}"))

        if changelog:
            print()
            print(style("main", "Changelog:"))
            for line in changelog.split("\n"):
                if line.strip():
                    print(style("main", f"  {line}"))

        print()
        answer = input("Download and install? [Y/n] ").strip().lower()

        if answer not in ("", "y", "yes", "д", "да"):
            return

        backup_dir = _backup_project()

        zip_path = os.path.join(backup_dir, "update.zip")

        if not _download_file(download_url, zip_path):
            error(
                t("update_download_failed", state.settings)
            )
            return

        _apply_update(zip_path)

        os.remove(zip_path)

        success(
            t("update_success", state.settings)
        )

        print(
            style(
                "main",
                t("update_restart", state.settings)
            )
        )

    except Exception as exception:
        warning(
            t(
                "update_check_failed",
                state.settings,
                error=exception
            )
        )

