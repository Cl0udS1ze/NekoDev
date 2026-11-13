from core import state

translations = {

    "ru": {

        # -------------------------
        # Система
        # -------------------------

        "unknown_command": "Неизвестная команда.",
        "exit": "До встречи! Жду тебя снова!",
        "console_cleared": "Консоль очищена.",
        "input_finished": "Ввод завершён.",
        "ai_finished": "Neko AI завершён.",
        "ai_stopped": "Neko AI остановлен.",

        "error":
            "Ошибка: {error}",

        "command_error":
            "Произошла ошибка при выполнении команды: {error}",

        "online_mode":
            "Вы в онлайн режиме.",

        "offline_mode":
            "Neko работает в офлайн режиме.",

        "database_connected":
            "Успешно подключено!",

        "database_error":
            "Не удалось подключиться к серверу.",

        # -------------------------
        # Reconnect
        # -------------------------

        "reconnect_usage":
            "Использование: reconnect",

        "reconnect_connecting":
            "Переподключение к серверу...",

        "reconnect_success":
            "Подключение к серверу восстановлено.",

        "reconnect_failed":
            "Не удалось подключиться к серверу.",

        # -------------------------
        # Настройки
        # -------------------------

        "settings_title":
            "НАСТРОЙКИ",

        "setting_changed":
            "Изменено: {setting} → {value}",

        "setting_must_exist":
            "Такого параметра не существует.",

        "set_usage":
            "Использование: set <параметр> <значение>",

        "language_invalid":
            "Доступные языки: ru, en.",

        "theme_invalid":
            "Доступные темы: default, dark, terminal.",

        # -------------------------
        # Заметки
        # -------------------------

        "notes_title":
            "ЗАМЕТКИ",

        "notes_empty":
            "Заметок пока нет.",

        "note_saved":
            "Записано: {name} = {text}",

        "note_deleted":
            "Удалено: {name}",

        "note_not_found":
            "Такой заметки нет.",

        "remember_usage":
            "Использование: remember <название> <содержание>",

        "forget_usage":
            "Использование: forget <название>",

        # -------------------------
        # Задачи
        # -------------------------

        "tasks_title":
            "ЗАДАЧИ",

        "tasks_empty":
            "Задач пока нет.",

        "addtask_usage":
            "Использование: addtask <задача>",

        "task_added":
            "Задача добавлена: {task}",

        "complete_usage":
            "Использование: complete <задача>",

        "task_not_found":
            "Такой задачи нет.",

        "task_completed":
            "Задача выполнена: {task}",

        "deltask_usage":
            "Использование: deltask <задача>",

        "task_deleted":
            "Задача удалена: {task}",

        # -------------------------
        # Аккаунт
        # -------------------------

        "register_title":
            "РЕГИСТРАЦИЯ",

        "login_title":
            "АВТОРИЗАЦИЯ",

        "register_usage":
            "Использование: register <имя_пользователя> <пароль>",

        "login_usage":
            "Использование: login <имя_пользователя> <пароль>",

        "account_required":
            "Для этой функции необходимо войти в аккаунт.",

        "database_required":
            "Для этой функции необходимо соединение с сервером.",

        "user_exists":
            "Такой пользователь уже существует.",

        "user_not_found":
            "Пользователь не найден.",

        "wrong_password":
            "Неверный пароль.",

        "register_success":
            "Пользователь {username} успешно зарегистрирован!",

        "login_success":
            "Вы успешно вошли как {username}!",

        "logout_success":
            "Вы успешно вышли из аккаунта {username}!",

        "not_logged_in":
            "Вы не авторизованы.",

        "already_logged_in":
            "Вы уже вошли как {username}.",

        # -------------------------
        # Ban / Mute
        # -------------------------

        "account_banned":
            "Ваш аккаунт заблокирован.",

        "account_banned_until":
            "Ваш аккаунт заблокирован до {date}.",

        "account_banned_forever":
            "Ваш аккаунт заблокирован навсегда.",

        # -------------------------
        # Мессенджер
        # -------------------------

        "global_chat_title":
            "Глобальный чат",

        "newmessages_title":
            "Новые сообщения",

        "newmessages_empty":
            "Новых сообщений нет.",

        "newmessages_marked":
            "Сообщения отмечены как прочитанные.",

        "newmessages_notification":
            "🔔 У вас есть новые сообщения! Используйте newmessages для просмотра.",

        "unknown_user":
            "Неизвестный пользователь",

        "chat_usage":
            "Использование: chat <имя_пользователя>",

        "chat_account_required":
            "Для использования мессенджера необходимо войти в аккаунт.",

        "chat_database_required":
            "Для использования мессенджера необходимо подключение к серверу.",

        "chat_user_not_found":
            "Пользователь не найден.",

        "chat_self":
            "Нельзя открыть чат с самим собой.",

        "chat_title":
            "Чат с {username}",

        "chat_exit":
            "│ Введите exit, чтобы выйти из чата.",

        "chat_empty":
            "Сообщений пока нет.",

        "message_you":
            "Вы",

        "message_send_error":
            "Не удалось отправить сообщение.",

        "message_muted":
            "Вы не можете отправлять сообщения: ваш аккаунт замьючен.",

        # -------------------------
        # Блокировки
        # -------------------------

        "block_usage":
            "Использование: block <имя_пользователя>",

        "unblock_usage":
            "Использование: unblock <имя_пользователя>",

        "block_user_not_found":
            "Пользователь не найден.",

        "block_self":
            "Нельзя заблокировать самого себя.",

        "block_already":
            "Пользователь уже заблокирован.",

        "block_success":
            "Пользователь {username} заблокирован.",

        "block_not_found":
            "Этот пользователь не заблокирован.",

        "unblock_success":
            "Блокировка пользователя {username} снята.",

        "block_database_required":
            "Для управления блокировками необходимо подключение к серверу.",

        "message_blocked":
            "Нельзя отправить сообщение этому пользователю.",

        # -------------------------
        # Roll
        # -------------------------

        "roll_usage":
            "Использование: roll <минимум> <максимум>",

        "min_greater_max":
            "Минимум не может быть больше максимума.",

        "roll_result":
            "🎲 Выпало: {result}",

        # -------------------------
        # Choice
        # -------------------------

        "choice_usage":
            "Использование: choice <вариант 1> <вариант 2> ...",

        "choice_result":
            "🎯 Выбор: {result}",

        # -------------------------
        # Count
        # -------------------------

        "count_usage":
            "Использование: count <слово 1> <слово 2> ...",

        "count_result":
            "Количество: {amount}",

        # -------------------------
        # Echo
        # -------------------------

        "echo_usage":
            "Использование: echo <текст>",

        "echo_result":
            "Эхо: {text}",

        # -------------------------
        # Say
        # -------------------------

        "say_usage":
            "Использование: say <текст>",

        # -------------------------
        # Repeat
        # -------------------------

        "repeat_usage":
            "Использование: repeat <количество> <текст>",

        "repeat_positive":
            "Количество должно быть положительным.",

        "repeat_max":
            "Максимальное количество повторов: 1000.",

        # -------------------------
        # Время
        # -------------------------

        "date":
            "Дата: {date}",

        "time":
            "Время: {time}",

        # -------------------------
        # Калькулятор
        # -------------------------

        "calculator_title":
            "КАЛЬКУЛЯТОР",

        "calculator_choose_mode":
            "Выберите режим: ",

        "calculator_mode_1":
            "1 — обычный калькулятор",

        "calculator_mode_2":
            "2 — возведение в степень",

        "calculator_mode_3":
            "3 — периметр прямоугольника",

        "calculator_mode_4":
            "4 — объём прямоугольного параллелепипеда",

        "calculator_first_number":
            "Введите первое число: ",

        "calculator_second_number":
            "Введите второе число: ",

        "calculator_number":
            "Введите число: ",

        "calculator_power":
            "Введите степень: ",

        "calculator_first_side":
            "Введите длину первой стороны: ",

        "calculator_second_side":
            "Введите длину второй стороны: ",

        "calculator_length":
            "Введите длину: ",

        "calculator_width":
            "Введите ширину: ",

        "calculator_height":
            "Введите высоту: ",

        "calculator_operation":
            "Действие: ",

        "calculator_unknown_operation":
            "Неизвестное действие.",

        "calculator_no_mode":
            "Такого режима нет.",

        "calculator_result":
            "Результат: {result}",

        "calculator_perimeter":
            "Периметр: {result}",

        "calculator_volume":
            "Объём: {result}",

        "power_too_large":
            "Степень слишком большая. Максимум: 1000.",

        "division_by_zero":
            "Ошибка: деление на ноль.",

        # -------------------------
        # Commands
        # -------------------------

        "commands_title":
            "СПИСОК КОМАНД",

        # -------------------------
        # Profile
        # -------------------------

        "profile_title":
            "ПРОФИЛЬ",

        "profile_username":
            "Имя пользователя: {username}",

        "profile_created":
            "Дата создания: {date}",

        "profile_launches":
            "Запусков Neko AI: {launches}",

        # -------------------------
        # Plugins
        # -------------------------

        "plugins_title":
            "ПЛАГИНЫ",

        "plugins_empty":
            "Нет загруженных плагинов.",

        "plugin_unknown":
            "Не указано",

        "plugin_version":
            "Версия: {version}",

        "plugin_author":
            "Автор: {author}",

        "plugins_loaded":
            "Загружено плагинов: {amount}",

        "plugin_load_error":
            "Ошибка загрузки плагина {name}: {error}",

        # -------------------------
        # Changelog
        # -------------------------

        "changelog_title":
            "ИЗМЕНЕНИЯ",

        "changelog_new":
            "НОВОЕ",

        "changelog_01":
    "Добавлен Neko AI с классификацией пользовательских запросов",

        "changelog_02":
    "Добавлена интеграция AI с существующими командами",

        "changelog_03":
    "Добавлена обработка параметров AI-команд",

        "changelog_04":
    "Добавлена AI-поддержка заметок и задач",

        "changelog_05":
    "Добавлена AI-поддержка профиля",

        "changelog_06":
    "Добавлена AI-поддержка информации о проекте",

        "changelog_07":
    "Добавлена AI-поддержка настроек",

        "changelog_08":
    "Добавлена проверка AI-интентов",

        "changelog_09":
    "Улучшена обработка пользовательских запросов",

        "changelog_10":
    "Добавлено обучение и сохранение AI-модели",

        "changelog_11":
    "Расширена поддержка RU/EN в AI",

        "changelog_12":
    "AI интегрирован в существующую архитектуру Neko",

        "changelog_13":
    "Улучшена обработка ошибок AI",

        "changelog_14":
    "Добавлена AI-поддержка изменения языка и темы",

        # -------------------------
        # Информация
        # -------------------------

        "info_project":
            "О ПРОЕКТЕ",

        "info_name":
            "Название: Neko AI",

        "info_version":
            "Версия: Pre-alpha 1",

        "info_developer":
            "Разработчик: Rip_Neko",

        "info_features":
            "ВОЗМОЖНОСТИ",

        "info_commands":
            "Командный интерфейс",

        "info_math":
            "Математические операции",

        "info_text":
            "Работа с текстом",

        "info_repeat":
            "Повторение текста",

        "info_count":
            "Подсчёт элементов",

        "info_echo":
            "Эхо-команда",

        "info_notes":
            "Система заметок",

        "info_tasks":
            "Система задач",

        "info_settings":
            "Настройки",

        "info_profile":
            "Профиль",

        "info_plugins":
            "Система плагинов",

        "info_localization":
            "Локализация RU/EN",

        "info_themes":
            "Система тем",

        "info_accounts":
            "Система аккаунтов",

        "info_messenger":
            "Личный мессенджер",

        "info_ai":
            "AI-функции",

        "info_tech":
            "ТЕХНОЛОГИИ",

        "info_language":
            "Язык: Python",

        "info_interface":
            "Интерфейс: CLI",

        "info_database":
            "База данных: MariaDB",

        "info_stage":
            "Стадия: Pre-alpha 1",

        "info_plan":
            "ПЛАНЫ",

        "info_done":
            "[DONE]",

        "info_todo":
            "[ ]",

        "info_future_math":
            "Новые математические функции",

        "info_files":
            "Работа с файлами",

        "info_voice":
            "Голосовой интерфейс",

        "info_global_chat":
            "Глобальный чат",

        "info_block":
            "Блокировка пользователей",

        "info_developer_section":
            "О РАЗРАБОТЧИКЕ",

        "info_interests":
            "Интересы: программирование, разработка игр",

        "info_thanks":
            "БЛАГОДАРНОСТИ",

        "info_thanks_chatgpt":
            "ChatGPT — за генерацию идей и помощь в обучении программированию.",

        "info_thanks_openai":
            "OpenAI — за создание ChatGPT.",

        "info_thanks_python":
            "Python — за избавление от необходимости писать собственный язык.",

        "info_thanks_friends":
            "Друзьям — за моральную поддержку.",

        "info_full_usage":
            "Введите \"info full\", чтобы узнать подробнее.",

        # -------------------------
        # Greeting
        # -------------------------

        "greeting":
            "Привет! Это Neko AI — твой персональный помощник.",

        "joke":
            "Я тебе не клоун, чтобы анекдоты рассказывать!",

        # -------------------------
        # Startup
        # -------------------------

        "startup_title":
            "NEKO AI",

        "startup_line_1":
            "Введите команду или 'exit' для выхода.",

        "startup_line_2":
            "Введите 'cmds' для просмотра списка команд.",

        # -------------------------
        # Database
        # -------------------------

        "database_server_unavailable":
            "Не удалось подключиться к серверу БД. Проверь интернет.",

        "database_auth_error":
            "БД отклонила авторизацию. Проверь данные подключения.",

        "database_access_denied":
            "Нет доступа к указанной базе данных.",

        "database_not_found":
            "Указанная база данных не найдена.",

        "database_error":
            "Ошибка подключения к БД: {error}",

        # -------------------------
        # Descriptions
        # -------------------------

        "desc_clear":
            "Очистить консоль",

        "desc_settings":
            "Показать настройки",

        "desc_changelog":
            "Показать изменения",

        "desc_set":
            "Изменить настройку",

        "desc_profile":
            "Показать профиль",

        "desc_addtask":
            "Добавить задачу",

        "desc_tasks":
            "Показать задачи",

        "desc_complete":
            "Выполнить задачу",

        "desc_deltask":
            "Удалить задачу",

        "desc_plugins":
            "Показать плагины",

        "desc_hi":
            "Поздороваться",

        "desc_info":
            "Показать информацию",

        "desc_joke":
            "Рассказать анекдот",

        "desc_cmds":
            "Показать список команд",

        "desc_say":
            "Вывести текст",

        "desc_echo":
            "Повторить введённый текст",

        "desc_count":
            "Посчитать количество элементов",

        "desc_repeat":
            "Повторить текст",

        "desc_calc":
            "Открыть калькулятор",

        "desc_roll":
            "Сгенерировать случайное число",

        "desc_time":
            "Показать время",

        "desc_date":
            "Показать дату",

        "desc_choice":
            "Выбрать случайный вариант",

        "desc_remember":
            "Сохранить заметку",

        "desc_notes":
            "Показать заметки",

        "desc_forget":
            "Удалить заметку",

        "desc_register":
            "Создать аккаунт",

        "desc_login":
            "Войти в аккаунт",

        "desc_logout":
            "Выйти из аккаунта",

        "desc_chat":
            "Открыть глобальный или личный чат",

        "desc_newmessages":
            "Показать новые сообщения",

        "desc_block":
            "Заблокировать пользователя",

        "desc_unblock":
            "Разблокировать пользователя",

        "desc_reconnect":
            "Переподключиться к серверу",

        "desc_admin":
            "Открыть панель администратора",

        "desc_exit":
            "Выйти из Neko AI",

        # -------------------------
        # Categories
        # -------------------------

        "category_core":
            "🧠 ОСНОВНЫЕ",

        "category_notes":
            "📝 ЗАМЕТКИ",

        "category_tasks":
            "📋 ЗАДАЧИ",

        "category_settings":
            "⚙️ НАСТРОЙКИ",

        "category_math":
            "🧮 МАТЕМАТИКА",

        "category_text":
            "💬 ТЕКСТ",

        "category_time":
            "🕐 ВРЕМЯ",

        "category_plugins":
            "🔌 ПЛАГИНЫ",

        "category_account":
            "👤 АККАУНТ",

        "category_messenger":
            "💬 МЕССЕНДЖЕР",

        "category_system":
            "📦 СИСТЕМА",

        "category_admin":
            "👑 АДМИНИСТРАТОР",

        
        # -------------------------
        # Requirements
        # -------------------------

        "requirements_missing":
            "Не хватает библиотек: {count}. Сейчас установлю.",

        "requirements_installing":
            "Устанавливаю {package}...",

        "requirements_installed":
            "✓ {package} установлен.",

        "requirements_failed":
            "✗ Не удалось установить {package}.",

        # -------------------------
        # Updater
        # -------------------------

        "update_latest":
            "Установлена последняя версия.",

        "update_available":
            "ДОСТУПНО ОБНОВЛЕНИЕ",

        "update_versions":
            "Текущая: {current} → Новая: {latest}",

        "update_changelog":
            "Что нового: {changelog}",

        "update_no_url":
            "Ссылка для скачивания не найдена. Обновите вручную.",

        "update_permission":
            "Обновить сейчас? [Y/n]: ",

        "update_skipped":
            "Обновление пропущено.",

        "update_downloading":
            "Скачиваю обновление...",

        "update_download_error":
            "Не удалось скачать обновление.",

        "update_backup":
            "Создаю резервную копию...",

        "update_backup_error":
            "Не удалось создать резервную копию. Продолжаю без неё.",

        "update_apply_error":
            "Ошибка при установке обновления: {error}",

        "update_success":
            "✓ Обновление установлено!",

        "update_restart":
            "Перезапустить сейчас? [Y/n]: ",

    },


    # =====================================================
    # ENGLISH
    # =====================================================

    "en": {

        # -------------------------
        # System
        # -------------------------

        "unknown_command":
            "Unknown command.",

        "exit":
            "See you! I'll be waiting for you!",

        "console_cleared":
            "Console cleared.",

        "input_finished":
            "Input finished.",

        "ai_finished":
            "Neko AI terminated.",

        "ai_stopped":
            "Neko AI stopped.",

        "error":
            "Error: {error}",

        "command_error":
            "An error occurred while executing the command: {error}",

        "online_mode":
            "You are in online mode.",

        "offline_mode":
            "Neko is running in offline mode.",

        "database_connected":
            "Successfully connected!",

        "database_error":
            "Failed to connect to the server.",

        # -------------------------
        # Reconnect
        # -------------------------

        "reconnect_usage":
            "Usage: reconnect",

        "reconnect_connecting":
            "Reconnecting to the server...",

        "reconnect_success":
            "Connection to the server has been restored.",

        "reconnect_failed":
            "Failed to connect to the server.",

        # -------------------------
        # Settings
        # -------------------------

        "settings_title":
            "SETTINGS",

        "setting_changed":
            "Changed: {setting} → {value}",

        "setting_must_exist":
            "This parameter does not exist.",

        "set_usage":
            "Usage: set <parameter> <value>",

        "language_invalid":
            "Available languages: ru, en.",

        "theme_invalid":
            "Available themes: default, dark, terminal.",

        # -------------------------
        # Notes
        # -------------------------

        "notes_title":
            "NOTES",

        "notes_empty":
            "There are no notes yet.",

        "note_saved":
            "Saved: {name} = {text}",

        "note_deleted":
            "Deleted: {name}",

        "note_not_found":
            "That note does not exist.",

        "remember_usage":
            "Usage: remember <name> <content>",

        "forget_usage":
            "Usage: forget <name>",

        # -------------------------
        # Tasks
        # -------------------------

        "tasks_title":
            "TASKS",

        "tasks_empty":
            "There are no tasks yet.",

        "addtask_usage":
            "Usage: addtask <task>",

        "task_added":
            "Task added: {task}",

        "complete_usage":
            "Usage: complete <task>",

        "task_not_found":
            "That task does not exist.",

        "task_completed":
            "Task completed: {task}",

        "deltask_usage":
            "Usage: deltask <task>",

        "task_deleted":
            "Task deleted: {task}",

        # -------------------------
        # Account
        # -------------------------

        "register_title":
            "REGISTRATION",

        "login_title":
            "LOGIN",

        "register_usage":
            "Usage: register <username> <password>",

        "login_usage":
            "Usage: login <username> <password>",

        "account_required":
            "You need to log in to use this feature.",

        "database_required":
            "A server connection is required for this feature.",

        "user_exists":
            "This username is already taken.",

        "user_not_found":
            "User not found.",

        "wrong_password":
            "Incorrect password.",

        "register_success":
            "User {username} successfully registered!",

        "login_success":
            "Successfully logged in as {username}!",

        "logout_success":
            "Successfully logged out of {username}!",

        "not_logged_in":
            "You are not logged in.",

        "already_logged_in":
            "You are already logged in as {username}.",

        # -------------------------
        # Ban / Mute
        # -------------------------

        "account_banned":
            "Your account is banned.",

        "account_banned_until":
            "Your account is banned until {date}.",

        "account_banned_forever":
            "Your account is permanently banned.",

        # -------------------------
        # Messenger
        # -------------------------

        "global_chat_title":
            "Global Chat",

        "newmessages_title":
            "New Messages",

        "newmessages_empty":
            "There are no new messages.",

        "newmessages_marked":
            "Messages marked as read.",

        "newmessages_notification":
            "🔔 You have new messages! Use newmessages to view them.",

        "unknown_user":
            "Unknown user",

        "chat_usage":
            "Usage: chat <username>",

        "chat_account_required":
            "You need to log in to use the messenger.",

        "chat_database_required":
            "A server connection is required to use the messenger.",

        "chat_user_not_found":
            "User not found.",

        "chat_self":
            "You cannot open a chat with yourself.",

        "chat_title":
            "Chat with {username}",

        "chat_exit":
            "│ Enter exit to leave the chat.",

        "chat_empty":
            "There are no messages yet.",

        "message_you":
            "You",

        "message_send_error":
            "Failed to send message.",

        "message_muted":
            "You cannot send messages because your account is muted.",

        # -------------------------
        # Blocks
        # -------------------------

        "block_usage":
            "Usage: block <username>",

        "unblock_usage":
            "Usage: unblock <username>",

        "block_user_not_found":
            "User not found.",

        "block_self":
            "You cannot block yourself.",

        "block_already":
            "This user is already blocked.",

        "block_success":
            "User {username} has been blocked.",

        "block_not_found":
            "This user is not blocked.",

        "unblock_success":
            "Block from {username} has been removed.",

        "block_database_required":
            "A server connection is required to manage blocks.",

        "message_blocked":
            "You cannot send a message to this user.",

        # -------------------------
        # Roll
        # -------------------------

        "roll_usage":
            "Usage: roll <minimum> <maximum>",

        "min_greater_max":
            "Minimum cannot be greater than maximum.",

        "roll_result":
            "🎲 Rolled: {result}",

        # -------------------------
        # Choice
        # -------------------------

        "choice_usage":
            "Usage: choice <option 1> <option 2> ...",

        "choice_result":
            "🎯 Choice: {result}",

        # -------------------------
        # Count
        # -------------------------

        "count_usage":
            "Usage: count <word 1> <word 2> ...",

        "count_result":
            "Count: {amount}",

        # -------------------------
        # Echo
        # -------------------------

        "echo_usage":
            "Usage: echo <text>",

        "echo_result":
            "Echo: {text}",

        # -------------------------
        # Say
        # -------------------------

        "say_usage":
            "Usage: say <text>",

        # -------------------------
        # Repeat
        # -------------------------

        "repeat_usage":
            "Usage: repeat <amount> <text>",

        "repeat_positive":
            "Amount must be positive.",

        "repeat_max":
            "Maximum number of repetitions: 1000.",

        # -------------------------
        # Time
        # -------------------------

        "date":
            "Date: {date}",

        "time":
            "Time: {time}",

        # -------------------------
        # Calculator
        # -------------------------

        "calculator_title":
            "CALCULATOR",

        "calculator_choose_mode":
            "Choose a mode: ",

        "calculator_mode_1":
            "1 — basic calculator",

        "calculator_mode_2":
            "2 — exponentiation",

        "calculator_mode_3":
            "3 — rectangle perimeter",

        "calculator_mode_4":
            "4 — rectangular cuboid volume",

        "calculator_first_number":
            "Enter the first number: ",

        "calculator_second_number":
            "Enter the second number: ",

        "calculator_number":
            "Enter a number: ",

        "calculator_power":
            "Enter the exponent: ",

        "calculator_first_side":
            "Enter the first side length: ",

        "calculator_second_side":
            "Enter the second side length: ",

        "calculator_length":
            "Enter the length: ",

        "calculator_width":
            "Enter the width: ",

        "calculator_height":
            "Enter the height: ",

        "calculator_operation":
            "Operation: ",

        "calculator_unknown_operation":
            "Unknown operation.",

        "calculator_no_mode":
            "There is no such mode.",

        "calculator_result":
            "Result: {result}",

        "calculator_perimeter":
            "Perimeter: {result}",

        "calculator_volume":
            "Volume: {result}",

        "power_too_large":
            "Exponent is too large. Maximum: 1000.",

        "division_by_zero":
            "Error: division by zero.",

        # -------------------------
        # Commands
        # -------------------------

        "commands_title":
            "COMMAND LIST",

        # -------------------------
        # Profile
        # -------------------------

        "profile_title":
            "PROFILE",

        "profile_username":
            "Username: {username}",

        "profile_created":
            "Created: {date}",

        "profile_launches":
            "Neko AI launches: {launches}",

        # -------------------------
        # Plugins
        # -------------------------

        "plugins_title":
            "PLUGINS",

        "plugins_empty":
            "No plugins loaded.",

        "plugin_unknown":
            "Not specified",

        "plugin_version":
            "Version: {version}",

        "plugin_author":
            "Author: {author}",

        "plugins_loaded":
            "Loaded plugins: {amount}",

        "plugin_load_error":
            "Error loading plugin {name}: {error}",

        # -------------------------
        # Changelog
        # -------------------------

        "changelog_title":
            "CHANGELOG",

        "changelog_new":
            "NEW",

        "changelog_01":
    "Added Neko AI with user query classification",

        "changelog_02":
    "Added AI integration with existing commands",

        "changelog_03":
    "Added AI command parameter processing",

        "changelog_04":
    "Added AI support for notes and tasks",

        "changelog_05":
    "Added AI support for the user profile",

        "changelog_06":
    "Added AI support for project information",

        "changelog_07":
    "Added AI support for settings",

        "changelog_08":
    "Added AI intent validation",

        "changelog_09":
    "Improved handling of user requests",

        "changelog_10":
    "Added AI model training and saving",

        "changelog_11":
    "Expanded RU/EN support in AI",

        "changelog_12":
    "Integrated AI into the existing Neko architecture",

        "changelog_13":
    "Improved AI error handling",

        "changelog_14":
    "Added AI support for changing language and theme",

        # -------------------------
        # Info
        # -------------------------

        "info_project":
            "ABOUT THE PROJECT",

        "info_name":
            "Name: Neko AI",

        "info_version":
            "Version: Pre-alpha 1",

        "info_developer":
            "Developer: Rip_Neko",

        "info_features":
            "FEATURES",

        "info_commands":
            "Command interface",

        "info_math":
            "Mathematical operations",

        "info_text":
            "Text processing",

        "info_repeat":
            "Text repetition",

        "info_count":
            "Element counting",

        "info_echo":
            "Echo command",

        "info_notes":
            "Notes system",

        "info_tasks":
            "Task system",

        "info_settings":
            "Settings",

        "info_profile":
            "Profile",

        "info_plugins":
            "Plugin system",

        "info_localization":
            "RU/EN localization",

        "info_themes":
            "Theme system",

        "info_accounts":
            "Account system",

        "info_messenger":
            "Private messenger",

        "info_ai":
            "AI features",

        "info_tech":
            "TECHNOLOGIES",

        "info_language":
            "Language: Python",

        "info_interface":
            "Interface: CLI",

        "info_database":
            "Database: MariaDB",

        "info_stage":
            "Stage: Pre-alpha 1",

        "info_plan":
            "PLANS",

        "info_done":
            "[DONE]",

        "info_todo":
            "[ ]",

        "info_future_math":
            "New mathematical functions",

        "info_files":
            "File handling",

        "info_voice":
            "Voice interface",

        "info_global_chat":
            "Global chat",

        "info_block":
            "User blocking",

        "info_developer_section":
            "ABOUT THE DEVELOPER",

        "info_interests":
            "Interests: programming, game development",

        "info_thanks":
            "THANKS",

        "info_thanks_chatgpt":
            "ChatGPT — for generating ideas and helping me learn programming.",

        "info_thanks_openai":
            "OpenAI — for creating ChatGPT.",

        "info_thanks_python":
            "Python — for saving me from having to write my own language.",

        "info_thanks_friends":
            "Friends — for moral support.",

        "info_full_usage":
            "Enter \"info full\" to learn more.",

        # -------------------------
        # Greeting
        # -------------------------

        "greeting":
            "Hello! This is Neko AI — your personal assistant.",

        "joke":
            "I'm not a clown, you know, I don't tell jokes!",

        # -------------------------
        # Startup
        # -------------------------

        "startup_title":
            "NEKO AI",

        "startup_line_1":
            "Enter a command or 'exit' to quit.",

        "startup_line_2":
            "Enter 'cmds' to see the command list.",

        # -------------------------
        # Database
        # -------------------------

        "database_server_unavailable":
            "Could not connect to the database server. Check your internet connection or server availability.",

        "database_auth_error":
            "The database rejected authentication. Check the connection credentials.",

        "database_access_denied":
            "Access to the specified database was denied.",

        "database_not_found":
            "The specified database was not found.",

        "database_error":
            "Database connection error: {error}",

        # -------------------------
        # Descriptions
        # -------------------------

        "desc_clear":
            "Clear the console",

        "desc_settings":
            "Show settings",

        "desc_changelog":
            "Show changelog",

        "desc_set":
            "Change a setting",

        "desc_profile":
            "Show profile",

        "desc_addtask":
            "Add a task",

        "desc_tasks":
            "Show tasks",

        "desc_complete":
            "Complete a task",

        "desc_deltask":
            "Delete a task",

        "desc_plugins":
            "Show plugins",

        "desc_hi":
            "Say hello",

        "desc_info":
            "Show information",

        "desc_joke":
            "Tell a joke",

        "desc_cmds":
            "Show command list",

        "desc_say":
            "Print text",

        "desc_echo":
            "Repeat entered text",

        "desc_count":
            "Count elements",

        "desc_repeat":
            "Repeat text",

        "desc_calc":
            "Open calculator",

        "desc_roll":
            "Generate a random number",

        "desc_time":
            "Show time",

        "desc_date":
            "Show date",

        "desc_choice":
            "Choose a random option",

        "desc_remember":
            "Save a note",

        "desc_notes":
            "Show notes",

        "desc_forget":
            "Delete a note",

        "desc_register":
            "Create an account",

        "desc_login":
            "Log in",

        "desc_logout":
            "Log out",

        "desc_chat":
            "Open a global or private chat",

        "desc_newmessages":
            "Show new messages",

        "desc_block":
            "Block a user",

        "desc_unblock":
            "Unblock a user",

        "desc_reconnect":
            "Reconnect to the server",

        "desc_admin":
            "Open administrator panel",

        "desc_exit":
            "Exit Neko AI",

        # -------------------------
        # Categories
        # -------------------------

        "category_core":
            "🧠 CORE",

        "category_notes":
            "📝 NOTES",

        "category_tasks":
            "📋 TASKS",

        "category_settings":
            "⚙️ SETTINGS",

        "category_math":
            "🧮 MATH",

        "category_text":
            "💬 TEXT",

        "category_time":
            "🕐 TIME",

        "category_plugins":
            "🔌 PLUGINS",

        "category_account":
            "👤 ACCOUNT",

        "category_messenger":
            "💬 MESSENGER",

        "category_system":
            "📦 SYSTEM",

        "category_admin":
            "👑 ADMINISTRATOR",

        
        "requirements_missing":
            "Missing libraries: {count}. Installing now.",

        "requirements_installing":
            "Installing {package}...",

        "requirements_installed":
            "✓ {package} installed.",

        "requirements_failed":
            "✗ Failed to install {package}.",

        "update_latest":
            "Latest version is installed.",

        "update_available":
            "UPDATE AVAILABLE",

        "update_versions":
            "Current: {current} → New: {latest}",

        "update_changelog":
            "What's new: {changelog}",

        "update_no_url":
            "Download URL not found. Please update manually.",

        "update_permission":
            "Update now? [Y/n]: ",

        "update_skipped":
            "Update skipped.",

        "update_downloading":
            "Downloading update...",

        "update_download_error":
            "Failed to download update.",

        "update_backup":
            "Creating backup...",

        "update_backup_error":
            "Failed to create backup. Continuing without it.",

        "update_apply_error":
            "Error applying update: {error}",

        "update_success":
            "✓ Update installed!",

        "update_restart":
            "Restart now? [Y/n]: ",

    }
}

def t(key, settings, **kwargs):

    language = settings.get(
        "language",
        "ru"
    )

    if language not in translations:
        language = "ru"

    text = translations[language].get(
        key,
        key
    )

    if not kwargs:
        return text

    # Безопасная подстановка: если переменной нет в kwargs,
    # оставляем как есть, вместо KeyError.
    for name, value in kwargs.items():
        text = text.replace(
            "{" + name + "}",
            str(value)
        )

    return text



def command_description(command, settings):

    return t(
        f"desc_{command}",
        settings
    )
