import sys
import subprocess

from core.ui import style, success, warning

REQUIRED_PACKAGES = {
    "mysql-connector-python": "mysql.connector",
    "scikit-learn": "sklearn",
}


def ensure_requirements():

    missing = []

    for pip_name, import_name in REQUIRED_PACKAGES.items():

        try:
            __import__(import_name)

        except ImportError:
            missing.append(pip_name)

    if not missing:
        return

    warning(
        "Не хватает библиотек: " + ", ".join(missing)
    )

    answer = input("Установить? [Y/n] ").strip().lower()

    if answer not in ("", "y", "yes", "д", "да"):
        warning("Продолжаю без установки. Возможны ошибки.")
        return

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + missing
        )
        success("Библиотеки установлены.")

    except Exception as e:
        warning(f"Не удалось установить: {e}")
