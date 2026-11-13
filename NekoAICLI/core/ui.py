from core import state
from core.theme import themes, RESET


def style(kind, text):

    current_theme = state.settings.get(
        "theme",
        "default"
    )

    if current_theme not in themes:
        current_theme = "default"

    color = themes[current_theme].get(
        kind,
        themes[current_theme]["main"]
    )

    return f"{color}{text}{RESET}"


def success(text):

    print(
        style(
            "success",
            f"✓ {text}"
        )
    )


def warning(text):

    print(
        style(
            "warning",
            f"⚠ {text}"
        )
    )


def error(text):

    print(
        style(
            "error",
            f"✗ {text}"
        )
    )


def title(text):

    print(
        style(
            "title",
            f"\n╭─ {text} ─╮"
        )
    )

    print(
        style(
            "title",
            "╰" + "─" * (len(text) + 6) + "╯"
        )
    )