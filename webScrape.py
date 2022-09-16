"""Webscrapeing application for Tracker.gg

    webScrape.py uses selenium to webscrape on Tracker.gg based
    on user_input which is taken from valBot.py's user input. The 
    user input is created into a URL for this file to scrape and returns
    the resquested information back to valBot.py that then sends the 
    return string back to the user to get the information they requested.
"""

from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from typing import List

def createURL(user_input: str) -> str:
    """Created URL based on user_input(riot ids and tags for Valorant accounts linked to Tracker.gg)

    Args:
        user_input: RIOT_ID#TAG as a astring from discord bot command
    
    Returns:
        END_URL: A str that contains the URL to the requested user's Tracker.gg page
    """
    TRACKER_GG_URL = "https://tracker.gg/valorant/profile/riot/"
    id_start = user_input.find("#") + 1
    user_name_end = user_input.find("#") - 1
    if " " in user_input:
        search_word = ""
        user_input_list = user_input.split(" ")
        for word_index in range(len(user_input_list)):
            if (len(user_input_list) - 1) == word_index:
                word_id_start = user_input_list[word_index].find("#")
                search_word += user_input_list[word_index][:word_id_start] + "%23" + user_input[id_start:]
            else:
                search_word += user_input_list[word_index] + "%20"
        END_URL = TRACKER_GG_URL + search_word + "/overview"
    else:
        END_URL = TRACKER_GG_URL + user_input[:user_name_end + 1] + "%23" + user_input[id_start:] + "/overview"
    return END_URL

def getDriver() -> Driver:
    """Creates webdriver

    Returns:
        Chrome Driver for Selenium
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def get_accuracy(driver: Driver, END_URL: str) -> List:
    """Finds statistics about accuracy

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        accuracy: List that contains requested elements
    """
    driver.get(END_URL)
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "decagon-avatar")))
    ACCURACY_CLASS = "accuracy__stats"
    accuracy = driver.find_elements(By.CLASS_NAME, ACCURACY_CLASS)
    return accuracy

def get_weapons(driver: Driver, END_URL: str) -> List:
    """Finds statistics about weapons

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        weapons: List that contains requested elements
    """
    driver.get(END_URL)
    WEAPONS_CLASS = "top-weapons__weapons"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, WEAPONS_CLASS)))
    weapons = driver.find_elements(By.CLASS_NAME, WEAPONS_CLASS)
    return weapons


def get_maps(driver: Driver, END_URL: str) -> List:
    """Finds statistics about maps

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        maps: List that contains requested elements
    """
    driver.get(END_URL)
    MAPS_CLASS = "top-maps__maps"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, MAPS_CLASS)))
    maps = driver.find_elements(By.CLASS_NAME, MAPS_CLASS)
    return maps

def get_current_rank(driver: Driver, END_URL: str) -> List:
    """Finds statistics about current rank

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        current_rank: List that contains requested elements
    """
    driver.get(END_URL)
    CURRENT_RANK_CLASS = "rating-content"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, CURRENT_RANK_CLASS)))
    current_rank = driver.find_elements(By.CLASS_NAME, CURRENT_RANK_CLASS)
    return current_rank

def get_peak_rank(driver: Driver, END_URL: str) -> List:
    """Finds statistics about peak rank

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        peak_rank: List that contains requested elements
    """
    driver.get(END_URL)
    PEAK_RANK_CLASS = "rating-entry__rank-info"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, PEAK_RANK_CLASS)))
    peak_rank = driver.find_elements(By.CLASS_NAME, PEAK_RANK_CLASS)
    return peak_rank

def get_agents(driver: Driver, END_URL: str) -> List:
    """Finds statistics about agents

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        agents: List that contains requested elements
    """
    driver.get(END_URL)
    AGENT_CLASS = "st-content__category"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, AGENT_CLASS)))
    agents = driver.find_elements(By.CLASS_NAME, AGENT_CLASS)
    return agents

def get_overview(driver: Driver, END_URL: str) -> tuple:
    """Finds overall statistics of a player

    Args:
        driver: Selenium Chrome Driver
        END_URL: URL to user's requested Tracker.gg page
    
    Returns:
        overview_giant_stats: List that contains requested elemnts
        overview_stats: List that contains requested elemnts
        KAD: List that contains requested elemnts
    """
    driver.get(END_URL)
    OVERVIEW_GIANT_CLASS = "giant-stats"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, OVERVIEW_GIANT_CLASS)))
    overview_giant_stats = driver.find_elements(By.CLASS_NAME, OVERVIEW_GIANT_CLASS)
    OVERVIEW_CLASS = "main"
    overview_stats = driver.find_elements(By.CLASS_NAME, OVERVIEW_CLASS)
    KAD_CLASS = "trn-profile-highlighted-content__stats"
    KAD = driver.find_elements(By.CLASS_NAME, KAD_CLASS)
    return overview_giant_stats, overview_stats, KAD

def parse_accuracy(accuracy: List) -> str:
    """Parses statistics about accuracy

    Args:
        accuracy: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    accuracy_lst = []
    accuracy_stats_tag = accuracy[0].find_elements(By.CLASS_NAME, "stat__value")
    for stat_value in accuracy_stats_tag:
        accuracy_stat = stat_value.text
        accuracy_lst.append(accuracy_stat)
    return_str = f"Head Shot %: {accuracy_lst[0]}\nTotal Head Shots: {accuracy_lst[1]}\nBody Shot %: {accuracy_lst[2]}\nTotal Body Shots: {accuracy_lst[3]}\nLeg Shot %: {accuracy_lst[4]}\nTotal Leg Shots: {accuracy_lst[5]}"
    return return_str

def parse_top_weapons(top_weapons: List) -> str:
    """Parses statistics about weapons

    Args:
        top_weapons: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    weapons_lst = []
    weapons_tag = top_weapons[0].find_elements(By.CLASS_NAME, "weapon__name")
    for weapon in weapons_tag:
        weapons_stat = weapon.text
        weapons_lst.append(weapons_stat)
    hit_lst = []
    hit_tag = top_weapons[0].find_elements(By.CLASS_NAME, "value")
    for hits in hit_tag:
        hits_stat = hits.text
        hit_lst.append(hits_stat)
    accuracy_lst = []
    accuracy_stats_tag = top_weapons[0].find_elements(By.CLASS_NAME, "stat")
    for stat_value in accuracy_stats_tag:
        accuracy_stat = stat_value.text
        accuracy_lst.append(accuracy_stat)
    return_str = f"Top 3 weapons in terms of kills:\n1) {weapons_lst[0]}\n    -Kills: {hit_lst[0]}\n    -Head Shot %: {accuracy_lst[0]}\n    -Body Shot %: {accuracy_lst[1]}\n    -Leg Shot %: {accuracy_lst[2]}\n2) {weapons_lst[1]}\n    -Kills: {hit_lst[1]}\n    -Head Shot %: {accuracy_lst[3]}\n    -Body Shot %: {accuracy_lst[4]}\n    -Leg Shot %: {accuracy_lst[5]}\n3) {weapons_lst[2]}\n    -Kills: {hit_lst[2]}\n    -Head Shot %: {accuracy_lst[6]}\n    -Body Shot %: {accuracy_lst[7]}\n    -Leg Shot %: {accuracy_lst[8]}"
    return return_str

def parse_maps(maps: List) -> str:
    """Parses statistics about maps

    Args:
        maps: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    maps_lst = []
    maps_tag = maps[0].find_elements(By.CLASS_NAME, "name")
    for map in maps_tag:
        map = map.text
        maps_lst.append(map)
    map_win_percentage_lst = []
    map_win_percentage = maps[0].find_elements(By.CLASS_NAME, "value")
    for win_percentage in map_win_percentage:
        win_percentage = win_percentage.text
        map_win_percentage_lst.append(win_percentage)
    map_win_record_lst = []
    map_win_record_tag = maps[0].find_elements(By.CLASS_NAME, "label")
    for map_win_record in map_win_record_tag:
        map_win_record = map_win_record.text
        map_win_record_lst.append(map_win_record)
    if len(maps_lst) == 1:
        return_str = f"Top 3 Maps in terms of Win %:\n1) {maps_lst[0]}\n    -Win %: {map_win_percentage_lst[0]}\n    -Record: {map_win_record_lst[0]}"
    elif len(maps_lst) == 2:
        return_str = f"Top 3 Maps in terms of Win %:\n1) {maps_lst[0]}\n    -Win %: {map_win_percentage_lst[0]}\n    -Record: {map_win_record_lst[0]}\n2) {maps_lst[1]}\n    -Win %: {map_win_percentage_lst[1]}\n    -Record: {map_win_record_lst[1]}"
    elif len(maps_lst) >=3:
        return_str = f"Top 3 Maps in terms of Win %:\n1) {maps_lst[0]}\n    -Win %: {map_win_percentage_lst[0]}\n    -Record: {map_win_record_lst[0]}\n2) {maps_lst[1]}\n    -Win %: {map_win_percentage_lst[1]}\n    -Record: {map_win_record_lst[1]}\n3) {maps_lst[2]}\n    -Win %: {map_win_percentage_lst[2]}\n    -Record: {map_win_record_lst[2]}"
    return return_str

def parse_current_rank(current_rank: List) -> str:
    """Parses statistics about current rank

    Args:
        current_rank: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    current_rank_tag = current_rank[0].find_element(By.CLASS_NAME, "value")
    current_rank = current_rank_tag.text
    return_str = f"Current Rank: {current_rank}"
    return return_str

def parse_peak_rank(peak_rank: List) -> str:
    """Parses statistics about peak rank

    Args:
        peak_rank: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    peak_rank_time_tag = peak_rank[1].find_element(By.CLASS_NAME, "subtext")
    peak_rank_time = peak_rank_time_tag.text
    peak_rank_tag = peak_rank[1].find_element(By.CLASS_NAME, "value")
    peak_rank = peak_rank_tag.text
    return_str = f"Peak Rank: {peak_rank}\n    -{peak_rank_time}"
    return return_str

def parse_agents(agents: List) -> str:
    """Parses statistics about agents

    Args:
        agents: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    agents_tag = agents[0].find_elements(By.CLASS_NAME, "value")
    agents_lst = []
    for info in agents_tag:
        info = info.text
        agents_lst.append(info)
    if len(agents_lst) == 8:
        return_str = f"Top 3 Agents:\n1) {agents_lst[0]}\n    -Time Played: {agents_lst[1]}\n    -Matches: {agents_lst[2]}\n    -Win %: {agents_lst[3]}\n    -K/D: {agents_lst[4]}\n    -ADR: {agents_lst[5]}\n    -ACS: {agents_lst[6]}\n    -Head Shot%: {agents_lst[7]}"
    elif len(agents_lst) == 16:
        return_str = f"Top 3 Agents:\n1) {agents_lst[0]}\n    -Time Played: {agents_lst[1]}\n    -Matches: {agents_lst[2]}\n    -Win %: {agents_lst[3]}\n    -K/D: {agents_lst[4]}\n    -ADR: {agents_lst[5]}\n    -ACS: {agents_lst[6]}\n    -Head Shot%: {agents_lst[7]}\n2) {agents_lst[8]}\n    -Time Played: {agents_lst[9]}\n    -Matches: {agents_lst[10]}\n    -Win %: {agents_lst[11]}\n    -K/D: {agents_lst[12]}\n    -ADR: {agents_lst[13]}\n    -ACS: {agents_lst[14]}\n    -Head Shot%: {agents_lst[15]}"
    elif len(agents_lst) == 24:
        return_str = f"Top 3 Agents:\n1) {agents_lst[0]}\n    -Time Played: {agents_lst[1]}\n    -Matches: {agents_lst[2]}\n    -Win %: {agents_lst[3]}\n    -K/D: {agents_lst[4]}\n    -ADR: {agents_lst[5]}\n    -ACS: {agents_lst[6]}\n    -Head Shot%: {agents_lst[7]}\n2) {agents_lst[8]}\n    -Time Played: {agents_lst[9]}\n    -Matches: {agents_lst[10]}\n    -Win %: {agents_lst[11]}\n    -K/D: {agents_lst[12]}\n    -ADR: {agents_lst[13]}\n    -ACS: {agents_lst[14]}\n    -Head Shot%: {agents_lst[15]}\n3) {agents_lst[16]}\n    -Time Played: {agents_lst[17]}\n    -Matches: {agents_lst[18]}\n    -Win %: {agents_lst[19]}\n    -K/D: {agents_lst[20]}\n    -ADR: {agents_lst[21]}\n    -ACS: {agents_lst[22]}\n    -Head Shot%: {agents_lst[23]}"
    return return_str

def parse_overview(overview: tuple) -> str:
    """Parses overall statistics of a player

    Args:
        overview: A list that contains requested elements
    
    Returns:
        return_str: A string describing requested elements
    """
    overview_giant_tag = overview[0][0].find_elements(By.CLASS_NAME, "value")
    overview_rank_tag = overview[0][0].find_elements(By.CLASS_NAME, "rank")
    overview_giant_lst = []
    overview_rank_lst = []
    for info in overview_giant_tag:
        info = info.text
        overview_giant_lst.append(info)
    for info in overview_rank_tag:
        info = info.text
        overview_rank_lst.append(info)
    overview_tag = overview[1][0].find_elements(By.CLASS_NAME, "value")
    overview_lst = []
    for info in overview_tag:
        info = info.text
        overview_lst.append(info)
    KAD_tag = overview[2][0].find_elements(By.CLASS_NAME, "stat__value")
    KAD_lst = []
    for info in KAD_tag:
        info = info.text
        KAD_lst.append(info)
    KAD = KAD_lst[1]
    current_rank = KAD_lst[0]
    return_str = f"Overview:\nDamage/Round: {overview_giant_lst[0]}\n    -{overview_rank_lst[0]}\nK/D Ratio: {overview_giant_lst[1]}\n    -{overview_rank_lst[1]}\nHead Shot %: {overview_giant_lst[2]}\n    -{overview_rank_lst[2]}\nWin %: {overview_giant_lst[3]}\n    -{overview_rank_lst[3]}\nCurrent Rank: {current_rank}\nKAD: {KAD}\nMatches Won: {overview_lst[0]}\nKills: {overview_lst[1]}\nHeadshots: {overview_lst[2]}\nDeaths: {overview_lst[3]}\nAssists: {overview_lst[4]}\nScore/Round: {overview_lst[5]}\nKills/Round: {overview_lst[6]}\nFirst Bloods: {overview_lst[7]}\nAces: {overview_lst[8]}\nClutches: {overview_lst[9]}\nFlawless: {overview_lst[10]}\nMost Kills(Match): {overview_lst[11]}"
    return return_str
