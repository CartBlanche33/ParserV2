import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


def collect_tournament_matches():
    source_filename = "tournaments_by_surface_and_year.json"
    target_filename = "tournaments_with_matches.json"

    # Загружаем исходные турниры
    with open(source_filename, "r", encoding="utf-8") as f:
        surface_data = json.load(f)

    # Загружаем или создаём новый файл, в который будем сохранять матчи
    match_data = {}
    if os.path.exists(target_filename):
        with open(target_filename, "r", encoding="utf-8") as f:
            try:
                match_data = json.load(f)
            except json.JSONDecodeError:
                match_data = {}

    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    for surface_key, tournaments in surface_data.items():
        if surface_key not in match_data:
            match_data[surface_key] = []

        for tournament in tournaments:
            existing_links = {t["link"] for t in match_data[surface_key]}
            if tournament["link"] in existing_links:
                print(f"⏭️ Уже есть турнир: {tournament['link']}")
                continue

            print(f"🌐 Открываю: {tournament['link']}")
            driver.get(tournament["link"])
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            match_divs = soup.find_all("div", class_="event__match")

            matches = []
            for match_div in match_divs:
                match_id_raw = match_div.get("id", "")
                if match_id_raw.startswith("g_2_"):
                    match_id = match_id_raw.replace("g_2_", "")
                    match_link = f"https://www.flashscore.com/match/{match_id}/"
                    matches.append({
                        "match_id": match_id,
                        "link": match_link
                    })

            if matches:
                tournament["matches"] = matches
                match_data[surface_key].append(tournament)

                # Сохраняем после каждого турнира
                with open(target_filename, "w", encoding="utf-8") as f:
                    json.dump(match_data, f, ensure_ascii=False, indent=2)

                print(f"✅ Добавлены матчи: {len(matches)} шт. | {tournament['link']}")
            else:
                print(f"⚠️ Нет матчей для турнира: {tournament['link']} — не добавляю.")

    driver.quit()
    print("\n🏁 Завершено.")
