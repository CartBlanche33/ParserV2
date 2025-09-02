import json
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import Dict, Any, List

# Импорты ваших функций для парсинга
from point_by_point_analyzer_4 import analyze_set_closure_detailed
from time_and_tour_name_6 import get_tournament_info_bs4
from zero_stage_prepare_info_1 import extract_set_scores
from claim_stats_2 import get_and_format_winner_stats
from utils_000 import get_safe_stats
from sets_analyze_logic_5 import handle_three_set_match, handle_two_set_match, handle_one_one_set_match


# --- Функции для работы с JSON ---
def load_data(file_path: str) -> Dict[str, Any]:
    """Загружает данные из JSON-файла."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_data(data: Dict[str, Any], file_path: str):
    """Сохраняет данные в JSON-файл."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# --- Основная функция для обработки матча ---
def process_single_match(driver, match_id: str) -> Dict[str, Any] | None:
    """Обрабатывает один матч и возвращает словарь с данными."""
    print(f"Обработка матча {match_id}...")
    driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/match-summary")
    time.sleep(1)

    try:
        match_score, set_scores, set_1_winner, set_2_winner, player1, player2 = extract_set_scores(driver)
        time.sleep(1)

        match_results = None
        if match_score in ["2-0", "0-2"]:
            match_results = handle_two_set_match(driver, match_id, player1, player2, set_1_winner)
        elif match_score in ["2-1", "1-2"]:
            match_results = handle_three_set_match(driver, match_id, player1, player2, set_1_winner, set_2_winner)
        elif match_score in ["1-1"]:
            match_results = handle_one_one_set_match(driver, match_id, player1, player2, set_1_winner)
        else:
            print(f"Неизвестный формат счёта для матча {match_id}:", match_score)
            return None

        if match_results:
            html = driver.page_source
            tour_name_and_time = get_tournament_info_bs4(html)

            return {
                "Match_ID": match_id,
                "Match_Score": match_score,
                "SET-SCORES": set_scores,
                "Player1": player1,
                "Player2": player2,
                "SET1-Winner": set_1_winner,
                "SET2-Winner": set_2_winner,
                "Name&Time": tour_name_and_time,
                "Match-Statistics": match_results
            }
        return None

    except Exception as e:
        print(f"Ошибка при обработке матча {match_id}: {e}")
        return None


# --- Основная функция, которая управляет всем процессом ---
def main():
    json_file_path = "tournaments_with_matches.json"
    target_key = "hard2024"  # <-- Укажите здесь нужный вам ключ
    output_filename = f"{target_key}.json"

    # 1. Загрузка исходных данных со всеми матчами
    source_data = load_data(json_file_path)
    if not source_data.get(target_key):
        print(f"Не найдено данных по ключу '{target_key}'. Завершение.")
        sys.exit()

    # 2. Загружаем уже обработанные данные, если они есть
    processed_data_output = load_data(output_filename)
    if processed_data_output:
        print(f"Найдены уже обработанные данные в файле {output_filename}. Возобновляем парсинг.")
        # Создаем множество (set) для быстрого поиска уже обработанных ID
        processed_ids = {
            match.get("Match_ID")
            for tournament in processed_data_output.get(target_key, [])
            for match in tournament.get("matches", [])
        }
    else:
        print(f"Файл {output_filename} не найден. Начинаем парсинг с нуля.")
        processed_data_output = {target_key: []}
        processed_ids = set()

    # 3. Начинаем парсинг
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Включаем headless-режим

    # Передаем опции в драйвер
    driver = webdriver.Chrome(options=chrome_options)

    try:
        source_tournaments = source_data.get(target_key, [])
        for source_tour in source_tournaments:
            tour_title = source_tour.get("title")
            print(f"\n--- Обработка турнира: {tour_title} ---")

            # Проверяем, существует ли уже этот турнир в файле с результатами
            target_tour_list = processed_data_output.get(target_key, [])
            target_tour = next((t for t in target_tour_list if t.get("title") == tour_title), None)

            if not target_tour:
                # Если турнира нет, создаем его начальную структуру
                target_tour = {
                    "title": tour_title,
                    "link": source_tour.get("link"),
                    "year": source_tour.get("year"),
                    "matches": []
                }
                processed_data_output[target_key].append(target_tour)

            output_matches_list = target_tour["matches"]
            source_matches_list = source_tour.get("matches", [])

            for match in source_matches_list:
                match_id = match.get("match_id")
                if not match_id:
                    continue

                if match_id in processed_ids:
                    print(f"Матч {match_id} уже обработан. Пропускаем.")
                    continue

                match_data = process_single_match(driver, match_id)
                if match_data:
                    output_matches_list.append(match_data)
                    # Сохраняем после каждого матча
                    save_data(processed_data_output, output_filename)
                    print(f"Данные для матча {match_id} успешно сохранены в файл: {output_filename}")

    finally:
        driver.quit()

    print("\nПарсинг завершён.")


if __name__ == "__main__":
    main()