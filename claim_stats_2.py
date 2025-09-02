from bs4 import BeautifulSoup
import re
from check_strategy_3 import check_strategy_conditions


def parse_stat_value(stat_str: str) -> dict:
    """Универсальный парсер для строки статистики."""
    parsed_data = {}
    if '%' in stat_str:
        try:
            parsed_data['percentage'] = int(stat_str.split('%')[0].strip())
        except ValueError:
            pass
    match = re.search(r'\((\d+)/(\d+)\)', stat_str)
    if match:
        try:
            won, total = int(match.group(1)), int(match.group(2))
            parsed_data.update({'won': won, 'total': total, 'ratio': f"{won}/{total}"})
        except ValueError:
            pass
    if not parsed_data:
        try:
            parsed_data['value'] = int(stat_str)
        except ValueError:
            if stat_str:
                parsed_data['raw'] = stat_str
    return parsed_data


def get_and_format_winner_stats(html: str, player1: str, player2: str, winner: str) -> dict or bool:
    """
    Собирает статистику обеих сторон, проверяет только победителя.
    Если победитель проходит проверку — возвращает всю статистику (home + away).
    Иначе — False.
    """
    soup = BeautifulSoup(html, "html.parser")
    # Определение стороны победителя
    if winner == player1:
        winner_side = "home"
    elif winner == player2:
        winner_side = "away"
    else:
        print(f"[!] Победитель {winner} не соответствует игрокам.")
        return False

    # Сбор всей статистики
    full_stats = {}
    stat_blocks = soup.select("div.wcl-category_Ydwqh")

    # print("Нашли блоков:", len(stat_blocks))
    for block in stat_blocks:
        # print(block)
        stat_name_el = block.select_one("div.wcl-category_6sT1J strong")
        home_value_el = block.select_one(".wcl-homeValue_3Q-7P")
        away_value_el = block.select_one(".wcl-awayValue_Y-QR1")

        if not (stat_name_el and home_value_el and away_value_el):
            continue

        stat_name = stat_name_el.text.strip()
        home_val = home_value_el.text.strip()
        away_val = away_value_el.text.strip()

        full_stats[stat_name] = {
            "home": home_val,
            "away": away_val
        }

    # Проверка условий по победителю
    raw_winner_stats = {
        stat: values.get(winner_side) for stat, values in full_stats.items()
    }

    if not raw_winner_stats:
        print("[!] Статистика победителя пуста.")
        return False

    conditions = {
        "exact_double_faults": 0,
        "min_serve_win_pct": 70
    }

    if not check_strategy_conditions(raw_winner_stats, **conditions):
        return False

    # print(full_stats)
    # Форматируем всю статистику (оба игрока)
    formatted_stats = {}
    for stat_name, values in full_stats.items():
        formatted_stats[stat_name] = {
            "home": parse_stat_value(values["home"]),
            "away": parse_stat_value(values["away"])
        }
    # print(formatted_stats)
    return formatted_stats, winner
