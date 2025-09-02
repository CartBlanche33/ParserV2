import time
import sys
from selenium import webdriver

# Remember to import your other functions from their respective files
from utils_000 import get_safe_stats,save_serve_attempts
from point_by_point_analyzer_4 import analyze_set_closure_detailed


def handle_one_one_set_match(driver, match_id, player1, player2, set_1_winner):
    print("--- Обработка матча в два сета ---")
    driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/match-statistics/1")
    time.sleep(1)
    html = driver.page_source

    # Используем новую функцию
    first_set_stat_claim, first_set_player_pass = get_safe_stats(1,html, player1, player2, set_1_winner)

    serve_attempts_results = {}

    if first_set_stat_claim:
        driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/point-by-point/1")
        time.sleep(1)
        html = driver.page_source
        serving_history = analyze_set_closure_detailed(html, player1, player2, first_set_player_pass, None)
        time.sleep(1)
        key = "set2_attempts"
        serve_attempts_results["Stats"] = first_set_stat_claim
        save_serve_attempts(serve_attempts_results, key, serving_history)

    return serve_attempts_results

def handle_two_set_match(driver, match_id, player1, player2, set_1_winner):
    print("--- Обработка матча в два сета ---")
    driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/match-statistics/1")
    time.sleep(1)
    html = driver.page_source

    # Используем новую функцию
    first_set_stat_claim, first_set_player_pass = get_safe_stats(1, html, player1, player2, set_1_winner)

    serve_attempts_results = {}

    if first_set_stat_claim:
        driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/point-by-point/1")
        time.sleep(1)
        html = driver.page_source
        serving_history = analyze_set_closure_detailed(html, player1, player2, first_set_player_pass, None)
        time.sleep(1)
        key = "set2_attempts"
        serve_attempts_results["Stats"] = first_set_stat_claim
        save_serve_attempts(serve_attempts_results, key, serving_history)

    return serve_attempts_results


def handle_three_set_match(driver, match_id, player1, player2, set_1_winner, set_2_winner):
    print("--- Обработка матча в три сета ---")

    # 1. Собираем статистику обоих игроков
    driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/match-statistics/1")
    time.sleep(1)
    html_set1 = driver.page_source
    first_set_stat_claim, first_set_player_pass = get_safe_stats(1, html_set1, player1, player2, set_1_winner)
    print("Статистика 1-го сета:")

    time.sleep(1)

    driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/match-statistics/2")
    time.sleep(1)
    html_set2 = driver.page_source
    second_set_stat_claim, second_set_player_pass = get_safe_stats(2, html_set2, player1, player2, set_2_winner)
    print("Статистика 2-го сета:")

    serve_attempts_results = {}

    # 2. Проверяем, была ли возможность закрытия в первом сете
    if first_set_stat_claim:
        driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/point-by-point/1")
        time.sleep(1)
        html_points_set1 = driver.page_source
        serving_history = analyze_set_closure_detailed(html_points_set1, player1, player2, first_set_player_pass, None)
        if serving_history:
            print("Найдена возможность закрытия сета в первом сете. Программа завершена.")
            key = "set2_attempts"
            serve_attempts_results["Stats"] = first_set_stat_claim
            save_serve_attempts(serve_attempts_results, key, serving_history)
            return serve_attempts_results

    # 3. Если в первом сете не было возможности, проверяем остальные логики

    # Логика 1: У первого игрока есть данные, у второго - нет
    if first_set_stat_claim and not second_set_stat_claim:
        driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/point-by-point/2")
        time.sleep(1)
        html_points_set2 = driver.page_source
        serving_history = analyze_set_closure_detailed(html_points_set2, player1, player2, first_set_player_pass, None)
        print("Анализ по первому игроку:")
        key = "set3_attempts"
        serve_attempts_results["Stats"] = first_set_stat_claim
        save_serve_attempts(serve_attempts_results, key, serving_history)

    # Логика 2: У второго игрока есть данные, у первого - нет
    elif second_set_stat_claim and not first_set_stat_claim:
        driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/point-by-point/2")
        time.sleep(1)
        html_points_set2 = driver.page_source
        serving_history = analyze_set_closure_detailed(html_points_set2, player1, player2, second_set_player_pass, None)
        print("Анализ по второму игроку:")
        key = "set3_attempts"
        serve_attempts_results["Stats"] = second_set_stat_claim
        save_serve_attempts(serve_attempts_results, key, serving_history)

    # Логика 3: У обоих игроков есть данные
    elif first_set_stat_claim and second_set_stat_claim:
        driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/point-by-point/2")
        time.sleep(1)
        html_points_set2 = driver.page_source
        serving_history = analyze_set_closure_detailed(html_points_set2, player1, player2, first_set_player_pass,
                                                       second_set_player_pass)
        print("Анализ по обоим игрокам:")
        key = "set3_attempts"
        serve_attempts_results["Stats"] = first_set_stat_claim, second_set_stat_claim
        save_serve_attempts(serve_attempts_results, key, serving_history)

    else:
        print("Третий сэт закончился тайбрейком , и без возможностей на закрытие / Игроки не соответствуют")

    return serve_attempts_results

