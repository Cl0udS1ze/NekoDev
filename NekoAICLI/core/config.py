
# =========================================================
# CONFIG
# =========================================================

import os
from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

# Load environment variables from .env
load_dotenv()


# =========================================================
# DATABASE
# =========================================================

DB_HOST = os.getenv("NEKO_DB_HOST", "")
DB_PORT = int(os.getenv("NEKO_DB_PORT", "3306"))
DB_USER = os.getenv("NEKO_DB_USER", "")
DB_PASSWORD = os.getenv("NEKO_DB_PASSWORD", "")
DB_NAME = os.getenv("NEKO_DB_NAME", "")


# =========================================================
# DIRECTORIES
# =========================================================

DATA_DIR = "data"

PLUGINS_DIR = "plugins"


os.makedirs(
    DATA_DIR,
    exist_ok=True
)

os.makedirs(
    PLUGINS_DIR,
    exist_ok=True
)


# =========================================================
# LOCAL FILES
# =========================================================

NOTES_FILE = os.path.join(
    DATA_DIR,
    "notes.json"
)

TASKS_FILE = os.path.join(
    DATA_DIR,
    "tasks.json"
)

SETTINGS_FILE = os.path.join(
    DATA_DIR,
    "settings.json"
)


# =========================================================
# DEFAULT SETTINGS
# =========================================================

default_settings = {

    "username": "User",

    "language": "ru",

    "theme": "default",

}

AI_CONFIDENCE_THRESHOLD = 0.6

ai_intent_commands = {
    "greeting": "hi",
    "time": "time",
    "date": "date",
    "note_get": "notes",
    "task_get": "tasks",
    "info": "info",
    "profile": "profile",
    "settings": "settings",
    "changelog": "changelog",
    "reconnect": "reconnect",
}
