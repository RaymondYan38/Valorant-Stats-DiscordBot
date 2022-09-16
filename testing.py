from ast import main
from tkinter import END
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


# INSTEAD GO INTO A DIFFERENT PAGE THAT HOLDS THE DATA LIKE /Weapons at the end of the URL maybe

def createURL(user_input):
    TRACKER_GG_URL = "https://tracker.gg/valorant/profile/riot/"
    id_start = user_input.find("#") + 1
    user_name_end = user_input.find("#") - 1
    if " " in user_input:
        search_word = ""
        user_input_list = user_input.split(" ")
        print(user_input_list)
        print(f"Length: {len(user_input_list)}")
        for word_index in range(len(user_input_list)):
            print(word_index)
            print(user_input_list[word_index])
            if (len(user_input_list) - 1) == word_index:
                word_id_start = user_input_list[word_index].find("#")
                search_word += user_input_list[word_index][:word_id_start] + "%23" + user_input[id_start:]
            else:
                search_word += user_input_list[word_index] + "%20"
        END_URL = TRACKER_GG_URL + search_word + "/overview"
    else:
        END_URL = TRACKER_GG_URL + user_input[:user_name_end + 1] + "%23" + user_input[id_start:] + "/overview"
    return END_URL

def getDriver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def get_accuracy(driver, END_URL):
    driver.get(END_URL)
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "decagon-avatar")))
    ACCURACY_CLASS = "accuracy__stats"
    accuracy = driver.find_elements(By.CLASS_NAME, ACCURACY_CLASS)
    return accuracy

# def get_weapons(driver, END_URL):
#     driver.get(END_URL[:-8] + "weapons")
#     WEAPONS_CLASS = "trn-table trn-table--alternating"
#     elem = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "trn-tabs__item trn-tabs__item--active")))
#     weapons = driver.find_elements(By.CLASS_NAME, WEAPONS_CLASS)
#     return weapons

def get_weapons(driver, END_URL):
    driver.get(END_URL)
    WEAPONS_CLASS = "top-weapons__weapons"
    elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, WEAPONS_CLASS)))
    weapons = driver.find_elements(By.CLASS_NAME, WEAPONS_CLASS)
    return weapons

# def get_stats(driver, END_URL):
#     driver.get(END_URL)
#     elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "decagon-avatar")))
#     ACCURACY_CLASS = "accuracy__stats"
#     accuracy = driver.find_elements(By.CLASS_NAME, ACCURACY_CLASS)
#     TOP_WEAPONS_CLASS = "top-weapons area-top-weapons"
#     top_weapons = driver.find_elements(By.CLASS_NAME, TOP_WEAPONS_CLASS)
#     TOP_MAPS_CLASS = "top-maps area-top-maps"
#     top_maps = driver.find_elements(By.CLASS_NAME, TOP_MAPS_CLASS)
#     MAIN_STATS_CLASS = "segment-stats area-main-stats card bordered header-bordered responsive"
#     main_stats = driver.find_elements(By.CLASS_NAME, MAIN_STATS_CLASS)
#     return accuracy, top_weapons, top_maps, main_stats
#     return accuracy, top_maps, main_stats

def parse_accuracy(accuracy):
    accuracy_lst = []
    accuracy_stats_tag = accuracy[0].find_elements(By.CLASS_NAME, "stat__value")
    for stat_value in accuracy_stats_tag:
        accuracy_stat = stat_value.text
        accuracy_lst.append(accuracy_stat)
    return_str = f"Head Shot %: {accuracy_lst[0]}\nTotal Head Shots: {accuracy_lst[1]}\nBody Shot %: {accuracy_lst[2]}\nTotal Body Shots: {accuracy_lst[3]}\nLeg Shot %: {accuracy_lst[4]}\nTotal Leg Shots: {accuracy_lst[5]}"
    return return_str

def parse_top_weapons(top_weapons):
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

if __name__ == "__main__":
    END_URL = createURL(input("Enter Val Tag: "))
    driver = getDriver()
    weapons = get_weapons(driver, END_URL)
    weapons_lst = parse_top_weapons(weapons)
    print(weapons_lst)


    # url = title_tag.get_attribute("href")
    # thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
    # thumbnail_url = thumbnail_tag.get_attribute('src')
    # channel_div = video.find_element(By.CLASS_NAME, "ytd-channel-name")
    # channel_name = channel_div.text
    # description = video.find_element(By.ID, 'description-text').text
    # return {
    #     'title': title,
    #     'url': url,
    #     'thumbnail_url': thumbnail_url,
    #     'channel': channel_name,
    #     'description': description
    # }




    
    