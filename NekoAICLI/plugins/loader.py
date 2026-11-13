# =========================================================
# IMPORTS
# =========================================================

import importlib

from core import state

from core.localization import t

from core.ui import error


# =========================================================
# PLUGIN LOADER
# =========================================================

def load_plugins(commands):
    """
    Загрузить все Python-плагины и зарегистрировать
    их команды.
    """

    for plugin in state.plugins:

        # -------------------------------------------------
        # Только Python-файлы.
        # -------------------------------------------------

        if not plugin.endswith(".py"):
            continue

        # -------------------------------------------------
        # Скрытые/служебные файлы пропускаем.
        # -------------------------------------------------

        if plugin.startswith("_"):
            continue

        name = plugin[:-3]

        plugin_name = (
            "plugins." + name
        )

        try:

            module = importlib.import_module(
                plugin_name
            )

            # -------------------------------------------------
            # Плагин должен иметь функцию register().
            # -------------------------------------------------

            if hasattr(
                module,
                "register"
            ):

                module.register(
                    commands
                )

                state.loaded_plugins.append(
                    module
                )

        except Exception as exception:

            error(
                t(
                    "plugin_load_error",
                    state.settings,
                    name=name,
                    error=exception
                )
            )