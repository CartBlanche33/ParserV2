
import json
import os
from typing import Dict, Any

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


def process_tournaments(json_file_path: str, target_key: str):
    data = load_data(json_file_path)
    tournaments = data.get(target_key, [])

    if not tournaments:
        print(f"Не найдено данных по ключу '{target_key}'.")
        return

    processed_tournaments_data = {target_key: []}

    for tournament_info in tournaments:
        title = tournament_info.get("title")
        link = tournament_info.get("link")
        year = tournament_info.get("year")

        print(f"\n--- Обработка турнира: {title} ({year}) ---")

        matches = tournament_info.get("matches", [])

        # Добавляем отладочный вывод, чтобы видеть, что происходит
        print(f"Найдено {len(matches)} матчей.")

        if not matches:
            print("Нет матчей для обработки.")
            continue

        for match in matches:
            match_id = match.get("match_id")

            if match_id:
                print(f"Обработка match_id: {match_id}")
                # ... ваш код парсинга ...

        processed_tournaments_data[target_key].append(tournament_info)

    # ... остальная часть кода ...


# --- Запуск кода ---
process_tournaments("tournaments_with_matches.json", "hard2024")