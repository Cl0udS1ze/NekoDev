import requests

from core import state
from core.response import Response


SYSTEM_PROMPT = (
    "Ты — Neko AI, дружелюбный виртуальный помощник. "
    "Отвечай кратко и по делу. "
    "Если пользователь пишет на русском — отвечай на русском. "
    "Ты умеешь помогать с вопросами, давать советы, "
    "поддерживать беседу и шутить. "
    "Не придумывай факты. "
    "Если не знаешь ответ — так и скажи."
)

MAX_HISTORY = 10

DEFAULT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"


# =========================================================
# ПРОВЕРКА
# =========================================================

def is_configured():
    """Проверить, настроен ли Cloudflare Workers AI."""
    return (
        bool(state.settings.get("cloudflare_api_token"))
        and bool(state.settings.get("cloudflare_account_id"))
    )


# =========================================================
# ИСТОРИЯ ДИАЛОГА
# =========================================================

def get_history():
    """Получить историю диалога из state."""
    if not hasattr(state, "ai_history"):
        state.ai_history = []
    return state.ai_history


def clear_history():
    """Очистить историю диалога."""
    state.ai_history = []


# =========================================================
# ЗАПРОС К API
# =========================================================

def ask_cloudflare(prompt, history=None):
    """
    Отправить запрос в Cloudflare Workers AI.

    Возвращает текст ответа или None при ошибке.
    """
    api_token = state.settings.get("cloudflare_api_token", "")
    account_id = state.settings.get("cloudflare_account_id", "")
    model = state.settings.get("cloudflare_model", DEFAULT_MODEL)

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/v1/chat/completions"
    )

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if history:
        messages.extend(history)

    messages.append(
        {"role": "user", "content": prompt}
    )

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]

    print(f"[DEBUG] HTTP {response.status_code}: {response.text}")
    return None


def _update_history(history, prompt, answer):
    """Обновить историю диалога."""
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": answer})

    if len(history) > MAX_HISTORY * 2:
        del history[:len(history) - MAX_HISTORY * 2]


# =========================================================
# КОМАНДА: ask
# =========================================================

def ai_ask(*args):
    """
    ask <текст> — задать вопрос AI.
    Поддерживает контекст диалога (история последних сообщений).
    """

    r = Response()

    if not args:
        r.text("Использование: ask <текст>", "main")
        return r

    if not is_configured():
        r.error(
            "Cloudflare AI не настроен.\n"
            "Укажите API-токен и Account ID:\n"
            "  set cloudflare_api_token <токен>\n"
            "  set cloudflare_account_id <id>"
        )
        return r

    prompt = " ".join(args)
    history = get_history()

    try:
        answer = ask_cloudflare(prompt, history)

    except requests.exceptions.ConnectionError:
        return r.error("Нет подключения к интернету.")

    except requests.exceptions.Timeout:
        return r.error("Cloudflare AI не ответил за 30 секунд.")

    except Exception as exception:
        return r.error(f"Ошибка: {exception}")

    if answer is None:
        return r.error("Cloudflare AI вернул ошибку. Проверьте токен и Account ID.")

    _update_history(history, prompt, answer)

    r.text(answer, "main")
    return r


# =========================================================
# КОМАНДА: clearai
# =========================================================

def ai_clear(*args):
    """Очистить историю диалога с AI."""
    clear_history()
    return Response().success("История диалога очищена.")


# =========================================================
# КОМАНДА: ai status
# =========================================================

def ai_status(*args):
    """Показать статус Cloudflare AI."""

    r = Response()
    r.title("Cloudflare Workers AI")

    if is_configured():
        r.text("Статус: настроен", "main")
        model = state.settings.get("cloudflare_model", DEFAULT_MODEL)
        r.text(f"Модель: {model}", "main")
        history = get_history()
        r.text(f"Сообщений в истории: {len(history)}", "main")
    else:
        r.text("Статус: не настроен", "main")
        r.text("", "main")
        r.text("Для настройки:", "main")
        r.text("  set cloudflare_api_token <токен>", "main")
        r.text("  set cloudflare_account_id <id>", "main")
        r.text(f"  set cloudflare_model {DEFAULT_MODEL}", "main")
        r.text("", "main")
        r.text("Получить токен: dash.cloudflare.com", "main")
        r.text("  1. Workers & Pages → Workers AI", "main")
        r.text("  2. Create API token", "main")
        r.text("Account ID — в правой панели дашборда", "main")

    return r


# =========================================================
# FALLBACK ДЛЯ НЕРАСПОЗНАННЫХ КОМАНД
# =========================================================

def ai_fallback_chat(command):
    """
    Попробовать отправить нераспознанную команду
    в Cloudflare AI как сообщение чата.

    Возвращает Response с ответом или None.
    """
    if not is_configured():
        return None

    history = get_history()

    try:
        answer = ask_cloudflare(command, history)

    except Exception:
        return None

    if answer is None:
        return None

    _update_history(history, command, answer)

    r = Response()
    r.text(answer, "main")
    return r
