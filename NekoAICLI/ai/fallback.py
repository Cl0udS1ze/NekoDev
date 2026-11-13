from ai.engine import (
    predict,
    parse_calculator,
    is_math_expression,
    extract_ai_action,
    validate_ai_intent
)

from ai.chat import ai_fallback_chat

from core import state
from core.config import (
    AI_CONFIDENCE_THRESHOLD,
    ai_intent_commands
)
from core.localization import t
from core.response import Response, render_cli

from commands.notes import (
    note_add,
    note_get,
    note_del
)

from commands.tasks import (
    task_add,
    show_tasks,
    complete,
    del_task
)


# =====================================================
# CHAT FALLBACK HELPER
# =====================================================

def _try_chat_fallback(command):
    """
    Попробовать отправить команду в чат с AI.
    Если AI недоступен — показать 'Неизвестная команда'.
    Возвращает True (обработано) в любом случае.
    """
    response = ai_fallback_chat(command)

    if response is not None:
        render_cli(response)
    else:
        render_cli(
            Response().error(
                t("unknown_command", state.settings)
            )
        )

    return True


def ai_fallback(
    command,
    command_name,
    parts,
    commands,
    show_changelog,
    reconnect
):

    # =====================================================
    # МАТЕМАТИЧЕСКОЕ ВЫРАЖЕНИЕ
    # =====================================================

    if is_math_expression(command):
        command_name = "calc"
        parts = [command_name, command]
        return command_name, parts, False


    # =====================================================
    # STRUCTURAL FALLBACK
    # =====================================================

    normalized_command = command.lower().strip()
    structural_handled = False

    # --- задача <текст> ---

    if normalized_command.startswith("задача "):
        task_text = command[len("задача "):].strip()
        if task_text:
            command_name = "addtask"
            parts = [command_name, task_text]
            structural_handled = True

    # --- удали задачу / удалить задачу ---

    elif normalized_command.startswith("удали задачу "):
        task_text = command[len("удали задачу "):].strip()
        if task_text:
            command_name = "deltask"
            parts = [command_name, task_text]
            structural_handled = True

    elif normalized_command.startswith("удалить задачу "):
        task_text = command[len("удалить задачу "):].strip()
        if task_text:
            command_name = "deltask"
            parts = [command_name, task_text]
            structural_handled = True

    # --- выполни задачу / выполнить задачу ---

    elif normalized_command.startswith("выполни задачу "):
        task_name = command[len("выполни задачу "):].strip()
        if task_name:
            command_name = "complete"
            parts = [command_name, task_name]
            structural_handled = True

    elif normalized_command.startswith("выполнить задачу "):
        task_name = command[len("выполнить задачу "):].strip()
        if task_name:
            command_name = "complete"
            parts = [command_name, task_name]
            structural_handled = True

    # --- ... выполнено / готово / сделано ---

    elif (
        normalized_command.endswith(" выполнено")
        or normalized_command.endswith(" готово")
        or normalized_command.endswith(" сделано")
    ):
        if normalized_command.endswith(" выполнено"):
            suffix = " выполнено"
        elif normalized_command.endswith(" готово"):
            suffix = " готово"
        else:
            suffix = " сделано"

        task_text = command[:-len(suffix)].strip()
        if task_text:
            command_name = "complete"
            parts = [command_name, task_text]
            structural_handled = True

    # --- выполнено <текст> ---

    elif normalized_command.startswith("выполнено "):
        task_text = command[len("выполнено "):].strip()
        if task_text:
            command_name = "complete"
            parts = [command_name, task_text]
            structural_handled = True

    # --- удали заметку / удалить заметку / забудь заметку ---

    elif normalized_command.startswith("удали заметку "):
        note_name = command[len("удали заметку "):].strip()
        if note_name:
            command_name = "forget"
            parts = [command_name, note_name]
            structural_handled = True

    elif normalized_command.startswith("удалить заметку "):
        note_name = command[len("удалить заметку "):].strip()
        if note_name:
            command_name = "forget"
            parts = [command_name, note_name]
            structural_handled = True

    elif normalized_command.startswith("забудь заметку "):
        note_name = command[len("забудь заметку "):].strip()
        if note_name:
            command_name = "forget"
            parts = [command_name, note_name]
            structural_handled = True

    elif normalized_command.startswith("забудь мою заметку "):
        note_name = command[len("забудь мою заметку "):].strip()
        if note_name:
            command_name = "forget"
            parts = [command_name, note_name]
            structural_handled = True

    # --- надо / нужно / мне нужно / хочу сделать / необходимо ---

    elif normalized_command.startswith("надо "):
        task_text = command[len("надо "):].strip()
        if task_text:
            command_name = "addtask"
            parts = [command_name, task_text]
            structural_handled = True

    elif normalized_command.startswith("нужно "):
        task_text = command[len("нужно "):].strip()
        if task_text:
            command_name = "addtask"
            parts = [command_name, task_text]
            structural_handled = True

    elif normalized_command.startswith("мне нужно "):
        task_text = command[len("мне нужно "):].strip()
        if task_text:
            command_name = "addtask"
            parts = [command_name, task_text]
            structural_handled = True

    elif normalized_command.startswith("хочу сделать "):
        task_text = command[len("хочу сделать "):].strip()
        if task_text:
            command_name = "addtask"
            parts = [command_name, task_text]
            structural_handled = True

    elif normalized_command.startswith("необходимо "):
        task_text = command[len("необходимо "):].strip()
        if task_text:
            command_name = "addtask"
            parts = [command_name, task_text]
            structural_handled = True

    # =====================================================
    # NOTE GET PRIORITY
    # =====================================================

    note_get_phrases = [
        "что я сохранял",
        "что я записывал",
        "что у меня сохранено",
        "что у меня записано",
        "что я сохранял раньше",
        "что я записывал раньше",
        "что я сохранял в заметках",
        "что я записывал в заметки"
    ]

    if normalized_command in note_get_phrases:
        command_name = "notes"
        parts = [command_name]
        structural_handled = True

    # =====================================================
    # TASK GET PRIORITY
    # =====================================================

    task_get_phrases = [
        "что осталось сделать",
        "что мне осталось сделать",
        "что осталось по задачам",
        "что у меня осталось по задачам",
        "какие задачи остались",
        "какие дела у меня остались"
    ]

    if normalized_command in task_get_phrases:
        render_cli(show_tasks())
        return command_name, parts, True

    # =====================================================
    # CHANGELOG / RECONNECT (детерминированные)
    # =====================================================

    changelog_phrases = [
        "что нового?",
        "что нового",
        "какие были обновления",
        "какие нововведения"
    ]

    if normalized_command in changelog_phrases:
        render_cli(show_changelog())
        return command_name, parts, True

    reconnect_phrases = [
        "соединение сломалось, восстанови",
        "попробуй переподключится"
    ]

    if normalized_command in reconnect_phrases:
        render_cli(reconnect())
        return command_name, parts, True

    # =====================================================
    # AI CLASSIFIER
    # =====================================================

    if not structural_handled:

        ai_result = predict(command)
        intent = ai_result["intent"]
        confidence = ai_result["confidence"]

        # --- UNKNOWN ---

        if intent == "unknown":
            return command_name, parts, _try_chat_fallback(command)

        # --- CONFIDENCE ---

        if confidence < AI_CONFIDENCE_THRESHOLD:
            return command_name, parts, _try_chat_fallback(command)

        # --- AI GUARD ---

        if not validate_ai_intent(command, intent):
            return command_name, parts, _try_chat_fallback(command)

        # --- REMEMBER ---

        if intent == "remember":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            render_cli(note_add("AI", action["text"]))
            return command_name, parts, True

        # --- ADD TASK ---

        if intent == "addtask":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            render_cli(task_add(action["task"]))
            return command_name, parts, True

        # --- NOTE GET ---

        if intent == "note_get":
            render_cli(note_get())
            return command_name, parts, True

        # --- NOTE DELETE ---

        if intent == "note_del":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            render_cli(note_del(action["name"]))
            return command_name, parts, True

        # --- TASK GET ---

        if intent == "task_get":
            render_cli(show_tasks())
            return command_name, parts, True

        # --- TASK COMPLETE ---

        if intent == "task_complete":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            render_cli(complete(action["task"]))
            return command_name, parts, True

        # --- TASK DELETE ---

        if intent == "task_del":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            render_cli(del_task(action["task"]))
            return command_name, parts, True

        # --- SETTINGS ---

        if intent == "settings":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            render_cli(
                commands["set"](
                    action["setting"],
                    action["value"]
                )
            )
            return command_name, parts, True

        # --- CALCULATOR ---

        if intent == "calculator":
            expression = parse_calculator(command)
            if expression is None:
                return command_name, parts, _try_chat_fallback(command)

            command_name = "calc"
            parts = [command_name, expression]

        # --- INFO ---

        elif intent == "info":
            action = extract_ai_action(command, intent)
            if action is None:
                return command_name, parts, _try_chat_fallback(command)

            command_name = "info"
            if action["full"]:
                parts = [command_name, "full"]
            else:
                parts = [command_name]

        # --- CHANGELOG ---

        elif intent == "changelog":
            render_cli(show_changelog())
            return command_name, parts, True

        # --- RECONNECT ---

        elif intent == "reconnect":
            render_cli(reconnect())
            return command_name, parts, True

        # --- ОСТАЛЬНЫЕ AI-КОМАНДЫ ---

        elif intent in ai_intent_commands:
            command_name = ai_intent_commands[intent]
            if command_name not in commands:
                return command_name, parts, _try_chat_fallback(command)
            parts = [command_name]

        # --- НЕИЗВЕСТНЫЙ INTENT ---

        else:
            return command_name, parts, _try_chat_fallback(command)

    return command_name, parts, False
