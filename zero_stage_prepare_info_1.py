from selenium.webdriver.common.by import By

def extract_set_scores(driver):


    try:
        # Игроки
        player1 = driver.find_element(By.CSS_SELECTOR, ".smh__participantName.smh__home a").text.strip()
        player2 = driver.find_element(By.CSS_SELECTOR, ".smh__participantName.smh__away a").text.strip()

        # Счёт по сетам (матчевый счёт)
        score1 = int(driver.find_element(By.CSS_SELECTOR, ".smh__part.smh__score.smh__home.smh__part--current").text.strip())
        score2 = int(driver.find_element(By.CSS_SELECTOR, ".smh__part.smh__score.smh__away.smh__part--current").text.strip())

        print(f"\n🎯 Match score (by sets): {player1} {score1} - {score2} {player2}")
        total_sets = score1 + score2
        match_score_str = f"{score1}-{score2}"

        print("\n📊 Set scores:")
        set_winners = []
        set_scores = []
        for set_num in range(1, total_sets + 1):
            # Домашний игрок
            p1_block = driver.find_element(By.CSS_SELECTOR, f".smh__part.smh__home.smh__part--{set_num}")
            p1_main = p1_block.get_attribute("innerText").strip().split("\n")[0]
            try:
                p1_sup = p1_block.find_element(By.TAG_NAME, "sup").text.strip()
                p1_score = f"{p1_main}({p1_sup})"
            except:
                p1_score = p1_main

            # Гостевой игрок
            p2_block = driver.find_element(By.CSS_SELECTOR, f".smh__part.smh__away.smh__part--{set_num}")
            p2_main = p2_block.get_attribute("innerText").strip().split("\n")[0]
            try:
                p2_sup = p2_block.find_element(By.TAG_NAME, "sup").text.strip()
                p2_score = f"{p2_main}({p2_sup})"
            except:
                p2_score = p2_main

            set_dict = {
                "set_num": set_num,
                "player1_score": p1_score,
                "player2_score": p2_score
            }
            set_scores.append(set_dict)

            # Определение победителя сета
            try:
                p1_main_int = int(p1_main)
                p2_main_int = int(p2_main)

                if p1_main_int > p2_main_int:
                    set_winner = player1
                elif p2_main_int > p1_main_int:
                    set_winner = player2
                else:
                    set_winner = "Ничья / ошибка"


            except:
                set_winner = "Ошибка определения"

            set_winners.append(set_winner)

            print(f"Set {set_num}: {player1} {p1_score} - {p2_score} {player2} ✅ Победитель: {set_winner}")

        # print(set_winners)
        print(set_scores)
        set_1_winner = set_winners[0]
        set_2_winner = set_winners[1]
        return match_score_str, set_scores, set_1_winner, set_2_winner, player1, player2
    except Exception as e:
        print("❌ Ошибка при извлечении данных о сэтах:", e)


