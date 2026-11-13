from core.ui import style, title, success, warning, error


class Response:

    def __init__(self):
        self.messages = []

    def title(self, text):
        self.messages.append(("title", text))
        return self

    def text(self, text, style_name="main"):
        self.messages.append((style_name, text))
        return self

    def success(self, text):
        self.messages.append(("success", text))
        return self

    def warning(self, text):
        self.messages.append(("warning", text))
        return self

    def error(self, text):
        self.messages.append(("error", text))
        return self

    def clear(self):
        self.messages.append(("clear", None))
        return self

    def exit(self):
        self.messages.append(("exit", None))
        return self


def render_cli(response):
    """Вывести Response в консоль. Вернуть True если нужно выйти."""

    if not response or not response.messages:
        return False

    should_exit = False

    for style_name, text in response.messages:

        if style_name == "clear":
            import os
            os.system("clear")
            continue

        if style_name == "exit":
            should_exit = True
            continue

        if style_name == "title":
            title(text)
        else:
            print(style(style_name, text))

    return should_exit
