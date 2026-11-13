from core import state
from core.localization import t
from core.response import Response


def show_plugins(*args):

    r = Response()

    r.title(t("plugins_title", state.settings))

    if not state.loaded_plugins:
        return r.warning(t("plugins_empty", state.settings))

    for number, plugin in enumerate(state.loaded_plugins, 1):

        plugin_name = getattr(
            plugin, "PLUGIN_NAME",
            t("plugin_unknown", state.settings)
        )

        plugin_version = getattr(
            plugin, "PLUGIN_VERSION",
            t("plugin_unknown", state.settings)
        )

        plugin_author = getattr(
            plugin, "PLUGIN_AUTHOR",
            t("plugin_unknown", state.settings)
        )

        r.text(
            f"│ {number}. {plugin_name}\n"
            f"│ {t('plugin_version', state.settings, version=plugin_version)}\n"
            f"│ {t('plugin_author', state.settings, author=plugin_author)}\n"
            f"│",
            "main"
        )

    r.success(
        t("plugins_loaded", state.settings, amount=len(state.loaded_plugins))
    )

    return r
