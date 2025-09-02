from typing import Tuple, Optional, Dict, Any
from claim_stats_2 import get_and_format_winner_stats

def get_safe_stats(set_num, html: str, player1: str, player2: str, winner: str) -> Tuple[
    Optional[Dict[str, Any]], Optional[str]]:
    """
    Безопасно вызывает get_and_format_winner_stats и распаковывает результат.
    Возвращает кортеж (данные, имя_игрока) или (None, None).
    """
    result = get_and_format_winner_stats(html, player1, player2, winner)
    stats_dict = {}
    key = f"set_{set_num}_stats"
    if result:
        # ПРАВИЛЬНЫЙ ПОРЯДОК: (имя, данные)
        formatted_stats, winner_name = result
        stats_dict[key] = formatted_stats
        print(stats_dict)
        return stats_dict, winner_name
    else:
        # Если result - False, выводим сообщение и возвращаем None для обоих значений
        print(f"Игрок {winner} не соответствует критериям.")
        return None, None


def save_serve_attempts(results_dict: Dict[str, Any], key: str, serving_history: Dict[str, Any]):
    results_dict[key] = serving_history
    # print(f"{results_dict}- Сохранил попытки")
    return results_dict