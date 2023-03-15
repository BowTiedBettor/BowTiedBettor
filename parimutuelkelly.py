import matplotlib.pyplot as plt

# kelly with a prior [in most cases estimated] turnover
# where your bet affects the odds [parimutuel betting]

def expected_growth(odds, probability, turnover, wager, rtp = 0.85, bankroll = 10000000):
    """
    ...
    """
    new_odds = (turnover + wager) * rtp / (turnover * rtp / odds + wager)
    fraction_bet = wager/bankroll
    eg = (1+fraction_bet*(new_odds-1))**probability * (1-fraction_bet)**(1-probability)
    return eg

odds = 5.02
probability = 0.23
turnover = 200000

"""
RUN
"""

wager = [i*100 for i in range(200)]
growths = [expected_growth(odds, probability, turnover, bet) for bet in wager]

plt.plot(wager, growths)
plt.show()

# kelly is just the preimage of the maximum along the graph
