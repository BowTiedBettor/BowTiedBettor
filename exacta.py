from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

# Necessary input variables
track = "eskilstuna"
race = 9
date = "2022-07-20"
max_wait = 2

def win_probability(
    odds_list: list,
    track_take: float = 0.15
) -> float:
    """
    Computes the win probability for a horse given the exacta odds for all combinations with the horse as the winner

    :param: odds_list: List containing the odds for all relevant exacta combinations
    :param: track_take: Track take, usually 0.15

    :return: Win probability
    :rtype: float
    """
    unadj_prob = 0
    for odds in odds_list:
        if odds == 0:
            pass
        else:
            unadj_prob += 1 / odds
    win_prob = unadj_prob * (1 - track_take)
    return win_prob

# Initiates the selenium session
path = "/Applications/chromedriver"
driver = webdriver.Chrome(path)

driver.get(f"https://www.atg.se/spel/{date}/komb/{track}/lopp{race}")

# Preparations
odds_lists = []
horses_left = True
i = 1

# Scrapes the exacta matrix -> list of lists for each row in the online web matrix
while horses_left == True:
    # While there are horses left in the field not yet scraped, the try block will execute without errors
    # As soon as there is a request for horse n+1 with a field of n horses the try block returns an exception, forcing the while loop to close
    try:
        odds_list = []
        row = WebDriverWait(driver, max_wait).until(EC.presence_of_element_located(
            (By.XPATH, f"//*[@id='main']/div[3]/div[2]/div/div/div/div/div/div/div[7]/table/tbody/tr[{i}]")))
        odds_row = WebDriverWait(row, max_wait).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "css-7g5myv-combomatrix-styles--padding")))
        for odds in odds_row:
            # Loops through all combinations with horse i as the winner. If the "second" horse is the horse itself/is scratched
            # it appends a zero to the odds_list, else it appends the exacta odds
            if odds_row.index(odds) + 1 == i:
                odds_list.append(float(0))
            else:
                try:
                    odds_list.append(
                        float(odds.text.replace(",", ".").replace(" ", "")))
                except:
                    odds_list.append(float(0))
        odds_lists.append(odds_list)
        i += 1
    except:
        horses_left = False

# Exits chromedriver
driver.quit()

# Prepares the probability matrix
prob_lists = []
for odds_list in odds_lists:
    # Loops through and uses every exacta odds to compute the ~ implied probability
    # for horse B coming in at second position given horse A winning the race
    prob_list = []
    win_prob = win_probability(odds_list)
    for odds in odds_list:
        if odds == 0:
            necessary_prob = 1
            prob_list.append(necessary_prob)
        else:
            prob_exacta = 1 / odds
            necessary_prob = prob_exacta / win_prob
            prob_list.append(necessary_prob)
    prob_lists.append(prob_list)

odds_matrix = np.array([i for i in odds_lists])
prob_matrix = np.array([i for i in prob_lists])
