"""Валидация: границы (if-elif-else), классификация и статус режима."""
from well_valid import config
def input_bounded(prompt: str, name: str, lo: float, hi: float) -> float:
    """Циклический ввод числа в диапазоне [lo; hi] с проверкой границ."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if raw == "":
            print(f"[пропуск] Поле '{name}' обязательно.")
            continue
        try:
            value = float(raw)
        except ValueError:
            print(f"[ошибка] '{raw}' — не число.")
            continue
        if value < lo:
            print(f"[ошибка] {name} = {value:g} меньше {lo:g}.")
            continue
        elif value > hi:
            print(f"[ошибка] {name} = {value:g} больше {hi:g}.")
            continue
        else:
            return value
def classify_well(w_pct: float) -> str:
    """Классификация по обводнённости (if-elif-else)."""
    if w_pct < 5:
        return "нефтяная (маловодная)"
    elif w_pct < 30:
        return "условно-безводная"
    elif w_pct < 80:
        return "обводнённая"
    else:
        return "водяная (эксплуатация нерациональна)"
def check_mode(p_res: float, p_bhp: float):
    """Определяет статус режима по депрессии (if-elif-else)."""
    drawdown = p_res - p_bhp  # депрессия на пласт, МПа
    if abs(drawdown) <= 0.5:
        return "нулевая", drawdown
    elif drawdown < 0:
        return "фонтанирование", drawdown
    elif drawdown < 2.0:
        return "низкий", drawdown
    else:
        return "норма", drawdown
def print_action(status: str, drawdown: float, q_liq: float) -> None:
    """Маршрутизация действия по статусу через match-case."""
    match status:
        case "норма":
            j = q_liq / drawdown
            print(f"Коэффициент продуктивности J = {j:.3f} м³/(сут·МПа)")
        case "низкий":
            print("Депрессия мала — продуктивность оценена грубо.")
        case "фонтанирование":
            print("(!) Pзаб > Pпл: скважина фонтанирует, расчёт J некорректен.")
        case "нулевая":
            print("Депрессия нулевая — J не определён (деление на ноль!).")
        case _:
            print("Неизвестный статус.")