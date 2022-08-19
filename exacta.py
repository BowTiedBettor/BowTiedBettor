import requests
import numpy as np

# Necessary input variables
race = 9
date = "2022-07-20"
track_code = 14

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

url = f"https://atg.se/services/racinginfo/v1/api/games/komb_{date}_{track_code}_{race}"

response = requests.get(url)
response_json = response.json()


odds_lists = []
for horseodds in response_json['pools']['komb']['comboOdds']:
    odds_list = []
    for odds in horseodds:
        odds_list.append(odds / 100)
    odds_lists.append(odds_list)

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
