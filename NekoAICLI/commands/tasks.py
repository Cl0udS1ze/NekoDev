import os
import json

from core import state
from core.config import TASKS_FILE
from core.localization import t
from core.response import Response

from database.queries import (
    create_task,
    get_user_tasks,
    complete_task,
    delete_task
)


def load_tasks():

    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return {}


def save_tasks():

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            state.tasks,
            file,
            ensure_ascii=False,
            indent=4
        )


def task_add(*args):

    r = Response()

    if not args:
        return r.warning(t("addtask_usage", state.settings))

    task = " ".join(args)

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        if not create_task(
            state.current_user["uuid"],
            task
        ):
            return r.error(t("database_error", state.settings))

    else:

        state.tasks[task] = False
        save_tasks()

    return r.success(
        t("task_added", state.settings, task=task)
    )


def show_tasks(*args):

    r = Response()
    r.title(t("tasks_title", state.settings))

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        user_tasks = get_user_tasks(
            state.current_user["uuid"]
        )

        if user_tasks is None:
            return r.error(t("database_error", state.settings))

    else:

        user_tasks = [
            (number, task, completed)
            for number, (task, completed) in enumerate(
                state.tasks.items(), 1
            )
        ]

    if not user_tasks:
        return r.warning(t("tasks_empty", state.settings))

    for number, task, completed in user_tasks:
        status = "✓" if completed else " "
        r.text(f"│ {number}. [{status}] {task}", "main")

    return r


def complete(*args):

    r = Response()

    if not args:
        return r.warning(t("complete_usage", state.settings))

    task = " ".join(args)

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        if not complete_task(
            state.current_user["uuid"],
            task
        ):
            return r.error(t("task_not_found", state.settings))

    else:

        if task not in state.tasks:
            return r.error(t("task_not_found", state.settings))

        state.tasks[task] = True
        save_tasks()

    return r.success(
        t("task_completed", state.settings, task=task)
    )


def del_task(*args):

    r = Response()

    if not args:
        return r.warning(t("deltask_usage", state.settings))

    task = " ".join(args)

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        if not delete_task(
            state.current_user["uuid"],
            task
        ):
            return r.error(t("task_not_found", state.settings))

    else:

        if task not in state.tasks:
            return r.error(t("task_not_found", state.settings))

        del state.tasks[task]
        save_tasks()

    return r.success(
        t("task_deleted", state.settings, task=task)
    )
