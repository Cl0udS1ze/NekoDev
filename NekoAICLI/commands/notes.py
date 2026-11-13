import json
import os

from core import state
from core.config import NOTES_FILE
from core.localization import t
from core.response import Response

from database.queries import (
    create_note,
    get_user_notes,
    delete_note
)


def load_notes():

    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    return {}


def save_notes():

    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(
            state.notes,
            file,
            ensure_ascii=False,
            indent=4
        )


def note_add(*args):

    r = Response()

    if len(args) < 2:
        return r.warning(t("remember_usage", state.settings))

    name = args[0]
    text = " ".join(args[1:])

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        if not create_note(
            state.current_user["uuid"],
            name,
            text
        ):
            return r.error(t("database_error", state.settings))

    else:

        if isinstance(state.notes, dict):
            old_notes = state.notes
            state.notes = []

            for old_name, old_text in old_notes.items():
                state.notes.append({
                    "id": len(state.notes) + 1,
                    "name": old_name,
                    "text": old_text
                })

        if state.notes:
            last_id = max(
                note["id"] for note in state.notes
            )
            new_id = last_id + 1
        else:
            new_id = 1

        state.notes.append({
            "id": new_id,
            "name": name,
            "text": text
        })

        save_notes()

    return r.success(
        t("note_saved", state.settings, name=name, text=text)
    )


def note_get(*args):

    r = Response()
    r.title(t("notes_title", state.settings))

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        user_notes = get_user_notes(
            state.current_user["uuid"]
        )

    else:

        if isinstance(state.notes, dict):
            user_notes = []
            for note_id, (name, text) in enumerate(
                state.notes.items(), 1
            ):
                user_notes.append((note_id, name, text))
        else:
            user_notes = []
            for note in state.notes:
                user_notes.append(
                    (note["id"], note["name"], note["text"])
                )

    if not user_notes:
        return r.warning(t("notes_empty", state.settings))

    for note_id, name, text in user_notes:
        r.text(f"│ {note_id}. {name}: {text}", "main")

    return r


def note_del(*args):

    r = Response()

    if len(args) != 1:
        return r.warning(t("forget_usage", state.settings))

    note_id = args[0].strip()

    if not note_id.isdigit():
        return r.error(t("note_not_found", state.settings))

    note_id = int(note_id)

    if (
        state.db is not None
        and state.db.is_connected()
        and state.current_user is not None
    ):

        if not delete_note(
            state.current_user["uuid"],
            note_id
        ):
            return r.error(t("note_not_found", state.settings))

    else:

        if isinstance(state.notes, dict):
            return r.error(t("note_not_found", state.settings))

        found = False

        for index, note in enumerate(state.notes):
            if note["id"] == note_id:
                del state.notes[index]
                found = True
                break

        if not found:
            return r.error(t("note_not_found", state.settings))

        save_notes()

    return r.success(
        t("note_deleted", state.settings, name=str(note_id))
    )
