def check_strategy_conditions(
        stats: dict,
        exact_double_faults: int,
        min_serve_win_pct: int
) -> bool:

    df_str = stats.get("Double Faults", "999")
    serve_win_str = stats.get("1st Serve Points Won", "0%")

    # Преобразуем строки в числа для сравнения
    try:
        double_faults = int(df_str)
    except ValueError:
        double_faults = 999  # Не сможет пройти проверку на равенство 0

    try:
        # Извлекаем процент из строки '75%(3/4)'
        serve_win_pct = int(serve_win_str.split('%')[0])
    except (ValueError, IndexError):
        serve_win_pct = 0  # Не сможет пройти проверку >= 70

    # --- САМА ПРОВЕРКА УСЛОВИЙ ---
    # Условие 1: Точное соответствие по двойным ошибкам
    condition1 = (double_faults == exact_double_faults)

    # Условие 2: Процент подачи не меньше заданного
    condition2 = (serve_win_pct >= min_serve_win_pct)

    # Возвращаем True, только если ОБА условия истинны
    return condition1 and condition2