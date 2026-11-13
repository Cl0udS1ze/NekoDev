from core import state
from core.localization import t
from core.response import Response
from database.queries import set_user_status


def calculator(*args):

    if state.current_user is not None:
        set_user_status("interface")

    r = Response()

    # calc без аргументов — справка
    if not args:
        r.title(t("calculator_title", state.settings))
        r.text(
            f"""│ {t("calculator_mode_1", state.settings)}
│ {t("calculator_mode_2", state.settings)}
│ {t("calculator_mode_3", state.settings)}
│ {t("calculator_mode_4", state.settings)}""",
            "main"
        )
        r.text(
            f"│ calc 2 + 2     → {t('calculator_mode_1', state.settings)}",
            "main"
        )
        r.text(
            f"│ calc power 2 3 → {t('calculator_mode_2', state.settings)}",
            "main"
        )
        r.text(
            f"│ calc perimeter 5 10 → {t('calculator_mode_3', state.settings)}",
            "main"
        )
        r.text(
            f"│ calc volume 3 4 5   → {t('calculator_mode_4', state.settings)}",
            "main"
        )
        return r

    # Подкоманды
    sub = args[0].lower()

    if sub == "power" and len(args) == 3:
        try:
            a = int(args[1])
            b = int(args[2])
            if abs(b) > 1000:
                return r.error(t("power_too_large", state.settings))
            return r.success(
                t("calculator_result", state.settings, result=a ** b)
            )
        except ValueError as exception:
            return r.error(t("error", state.settings, error=exception))

    if sub == "perimeter" and len(args) == 3:
        try:
            a = int(args[1])
            b = int(args[2])
            return r.success(
                t("calculator_perimeter", state.settings, result=2 * a + 2 * b)
            )
        except ValueError as exception:
            return r.error(t("error", state.settings, error=exception))

    if sub == "volume" and len(args) == 4:
        try:
            a = int(args[1])
            b = int(args[2])
            c = int(args[3])
            return r.success(
                t("calculator_volume", state.settings, result=a * b * c)
            )
        except ValueError as exception:
            return r.error(t("error", state.settings, error=exception))

    # Прямой расчёт: calc 2 + 2
    try:
        expr = " ".join(args)
        result = eval(expr)
        return r.success(
            t("calculator_result", state.settings, result=result)
        )
    except ZeroDivisionError:
        return r.error(t("division_by_zero", state.settings))
    except Exception as exception:
        return r.error(t("error", state.settings, error=exception))
