from core import state
from core.localization import t
from core.response import Response


def show_info(*args):

    if args and args[0].lower() == "full":
        return show_full_info()

    return show_short_info()


def show_short_info():

    r = Response()

    r.title(t("info_project", state.settings))

    r.text(
        f"""│ {t("info_name", state.settings)}
│ {t("info_version", state.settings)}
│ {t("info_developer", state.settings)}
│
│ {t("info_features", state.settings)}
│ • {t("info_commands", state.settings)}
│ • {t("info_math", state.settings)}
│ • {t("info_text", state.settings)}
│ • {t("info_repeat", state.settings)}
│ • {t("info_count", state.settings)}
│ • {t("info_echo", state.settings)}
│ • {t("info_notes", state.settings)}
│ • {t("info_tasks", state.settings)}
│ • {t("info_settings", state.settings)}
│ • {t("info_profile", state.settings)}
│ • {t("info_plugins", state.settings)}
│ • {t("info_localization", state.settings)}
│ • {t("info_themes", state.settings)}
│ • {t("info_accounts", state.settings)}
│ • {t("info_messenger", state.settings)}
│ • {t("info_ai", state.settings)}
│
│ {t("info_tech", state.settings)}
│ {t("info_language", state.settings)}
│ {t("info_interface", state.settings)}
│ {t("info_database", state.settings)}
│ {t("info_stage", state.settings)}
│
│ {t("info_plan", state.settings)}
│ {t("info_done", state.settings)} {t("info_notes", state.settings)}
│ {t("info_done", state.settings)} {t("info_tasks", state.settings)}
│ {t("info_done", state.settings)} {t("info_settings", state.settings)}
│ {t("info_done", state.settings)} {t("info_profile", state.settings)}
│ {t("info_done", state.settings)} {t("info_plugins", state.settings)}
│ {t("info_done", state.settings)} {t("info_localization", state.settings)}
│ {t("info_done", state.settings)} {t("info_accounts", state.settings)}
│ {t("info_done", state.settings)} {t("info_messenger", state.settings)}
│ {t("info_done", state.settings)} {t("info_ai", state.settings)}
│ {t("info_done", state.settings)} {t("info_global_chat", state.settings)}
│ {t("info_done", state.settings)} {t("info_block", state.settings)}
│ {t("info_todo", state.settings)} {t("info_future_math", state.settings)}
│ {t("info_todo", state.settings)} {t("info_files", state.settings)}
│ {t("info_todo", state.settings)} {t("info_voice", state.settings)}
│
│ {t("info_full_usage", state.settings)}""",
        "main"
    )

    return r


def show_full_info():

    r = Response()

    r.text(
        f"""
=== {t("info_project", state.settings)} ===

{t("info_name", state.settings)}
{t("info_version", state.settings)}
{t("info_developer", state.settings)}

=== {t("info_features", state.settings)} ===

• {t("info_commands", state.settings)}
• {t("info_math", state.settings)}
• {t("info_text", state.settings)}
• {t("info_repeat", state.settings)}
• {t("info_count", state.settings)}
• {t("info_echo", state.settings)}
• {t("info_notes", state.settings)}
• {t("info_tasks", state.settings)}
• {t("info_settings", state.settings)}
• {t("info_profile", state.settings)}
• {t("info_plugins", state.settings)}
• {t("info_localization", state.settings)}
• {t("info_themes", state.settings)}
• {t("info_accounts", state.settings)}
• {t("info_messenger", state.settings)}
• {t("info_ai", state.settings)}

=== {t("info_tech", state.settings)} ===

{t("info_language", state.settings)}
{t("info_interface", state.settings)}
{t("info_database", state.settings)}
{t("info_stage", state.settings)}

=== {t("info_plan", state.settings)} ===

{t("info_done", state.settings)} {t("info_notes", state.settings)}
{t("info_done", state.settings)} {t("info_tasks", state.settings)}
{t("info_done", state.settings)} {t("info_settings", state.settings)}
{t("info_done", state.settings)} {t("info_profile", state.settings)}
{t("info_done", state.settings)} {t("info_plugins", state.settings)}
{t("info_done", state.settings)} {t("info_localization", state.settings)}
{t("info_done", state.settings)} {t("info_accounts", state.settings)}
{t("info_done", state.settings)} {t("info_messenger", state.settings)}
{t("info_done", state.settings)} {t("info_ai", state.settings)}
{t("info_done", state.settings)} {t("info_global_chat", state.settings)}
{t("info_done", state.settings)} {t("info_block", state.settings)}

{t("info_todo", state.settings)} {t("info_future_math", state.settings)}
{t("info_todo", state.settings)} {t("info_files", state.settings)}
{t("info_todo", state.settings)} {t("info_voice", state.settings)}

=== {t("info_developer_section", state.settings)} ===

{t("info_developer", state.settings)}
{t("info_interests", state.settings)}

=== {t("info_thanks", state.settings)} ===

{t("info_thanks_chatgpt", state.settings)}
{t("info_thanks_openai", state.settings)}
{t("info_thanks_python", state.settings)}
{t("info_thanks_friends", state.settings)}
""",
        "main"
    )

    return r
