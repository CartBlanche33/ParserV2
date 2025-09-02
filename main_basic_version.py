import json
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

from point_by_point_analyzer_4 import analyze_set_closure_detailed
from time_and_tour_name_6 import get_tournament_info_bs4
from zero_stage_prepare_info_1 import extract_set_scores
from claim_stats_2 import get_and_format_winner_stats
from utils_000 import get_safe_stats
from sets_analyze_logic_5 import handle_three_set_match, handle_two_set_match, handle_one_one_set_match

driver = webdriver.Chrome()
match_id = "0dfLuzkS"
driver.get(f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary/match-summary")
time.sleep(1)
match_score, set_scores, set_1_winner, set_2_winner, player1, player2 = extract_set_scores(driver)
time.sleep(1)

all_match_data = {}
match_results = None

if match_score in ["2-0", "0-2"]:
    match_results = handle_two_set_match(driver, match_id, player1, player2, set_1_winner)

elif match_score in ["2-1", "1-2"]:
    match_results = handle_three_set_match(driver, match_id, player1, player2, set_1_winner, set_2_winner)

elif match_score in ["1-1"]:
    match_results = handle_one_one_set_match(driver, match_id, player1, player2, set_1_winner)

else:
    print("Неизвестный формат счёта:", match_score)


if match_results:
    html = driver.page_source
    tour_name_and_time = get_tournament_info_bs4(html)
    match_prev_information = {
    "Match_Score": match_score,
    "SET-SCORES": set_scores,
    "Player1": player1,
    "Player2": player2,
    "SET1-Winner": set_1_winner,
    "SET2-Winner": set_2_winner,
    "Name&Time": tour_name_and_time
    }
    all_match_data[match_id] = match_prev_information
    all_match_data["Match-Statistics"] = match_results
    print(all_match_data)


driver.quit()
