from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Optional, Any


def get_points_for_row(row):
    point_scores = []
    points_block = row.find_next_sibling("div", class_="matchHistoryRow__fifteens")
    if points_block:
        points = points_block.select("div.matchHistoryRow__fifteen")
        for point in points:
            point_scores.append(point.get_text(strip=True).replace(',', ''))
    return point_scores


# !!! ИЗМЕНЕННАЯ ВЕРСИЯ ФУНКЦИИ !!!
def analyze_set_closure_detailed(html: str, player1: str, player2: str, set1_winner: Optional[str],
                                 set2_winner: Optional[str]) -> Dict[str, List[Dict[str, Any]]]:
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("div.matchHistoryRow")

    # Создаем список игроков, которых нужно анализировать
    players_to_analyze = []
    if set1_winner and set1_winner != player1 and set1_winner != player2:
        raise ValueError(f"Победитель '{set1_winner}' не совпадает с именами игроков.")
    if set2_winner and set2_winner != player1 and set2_winner != player2:
        raise ValueError(f"Победитель '{set2_winner}' не совпадает с именами игроков.")

    if set1_winner:
        players_to_analyze.append(set1_winner)
    if set2_winner:
        # Проверяем, чтобы не дублировать, если победитель один и тот же
        if set2_winner != set1_winner:
            players_to_analyze.append(set2_winner)

    if not players_to_analyze:
        print("[!] Нет игроков для анализа.")
        return False

    results: Dict[str, Any] = {}

    # Теперь итерируемся по каждому игроку, которого нужно проанализировать
    for winner in players_to_analyze:
        if winner == player1:
            winner_side, winner_score_idx = "home", 0
        elif winner == player2:
            winner_side, winner_score_idx = "away", 1

        player_attempts_key = f"{winner}_closing_attempts"
        results[player_attempts_key] = []

        prev_score: Optional[Tuple[int, int]] = None
        opponent_score_idx = 1 - winner_score_idx
        attempt_id = 0

        # Проходим по всем строкам HTML для текущего игрока
        for row in rows:
            try:
                spans = row.select(".matchHistoryRow__scoreBox span")
                if len(spans) < 2:
                    continue
                current_score = (int(spans[0].text), int(spans[1].text))
            except (ValueError, IndexError):
                continue

            if current_score == (6, 6):
                break

            server_side = None
            if row.select_one(".matchHistoryRow__servis.matchHistoryRow__home div[title='Serving player']"):
                server_side = "home"
            elif row.select_one(".matchHistoryRow__servis.matchHistoryRow__away div[title='Serving player']"):
                server_side = "away"

            if prev_score and server_side == winner_side:
                is_serving_on_set_point = prev_score[winner_score_idx] >= 5 and \
                                          prev_score[winner_score_idx] > prev_score[opponent_score_idx]

                if is_serving_on_set_point:
                    attempt_id += 1
                    attempt_details: Dict[str, Any] = {}
                    attempt_details["id"] = attempt_id

                    prev_score_str = f"{prev_score[0]}-{prev_score[1]}"
                    current_score_str = f"{current_score[0]}-{current_score[1]}"
                    current_points = get_points_for_row(row)

                    attempt_details["score"] = f"{prev_score_str} -> {current_score_str}"
                    points_str = ", ".join(current_points) if current_points else "Нет данных по очкам"
                    attempt_details["points"] = points_str
                    attempt_details["player_name"] = winner

                    realization_2nd_point = False
                    prev_point_p1_score = 0
                    prev_point_p2_score = 0
                    if len(current_points) >= 2:
                        for i, point_score_str in enumerate(current_points):
                            try:
                                p1_point, p2_point = point_score_str.split(":")
                                p1_point_val = int(p1_point.replace('BP', '').strip())
                                p2_point_val = int(p2_point.replace('BP', '').strip())

                                if i == 1:
                                    if winner_score_idx == 0:
                                        if p1_point_val > prev_point_p1_score:
                                            realization_2nd_point = True
                                    elif winner_score_idx == 1:
                                        if p2_point_val > prev_point_p2_score:
                                            realization_2nd_point = True

                                prev_point_p1_score = p1_point_val
                                prev_point_p2_score = p2_point_val
                            except (ValueError, IndexError):
                                continue

                    attempt_details["realization_2nd_point"] = realization_2nd_point

                    if current_score[winner_score_idx] > prev_score[winner_score_idx]:
                        attempt_details["outcome"] = "closed_on_serve"
                    elif current_score[0] == current_score[1]:
                        attempt_details["outcome"] = "failed_to_close_on_serve"
                    else:
                        attempt_details["outcome"] = "not_a_closing_game"

                    results[player_attempts_key].append(attempt_details)
            prev_score = current_score

    # Проверка, были ли найдены попытки для какого-либо игрока
    total_attempts_found = any(results[key] for key in results)

    if not total_attempts_found:
        return False
    else:
        print(results)
        return results