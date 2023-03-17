import numpy as np
import random
from scipy.stats import norm
from teams import first_round, first_round_id

NUM_TEAMS = 363

def main():
    data = np.loadtxt("data.csv", delimiter=",", dtype=str)

    # removes non-tournament teams
    data = tournament_teams(data)

    print(highest_likelihood(first_round, data))
    print(highest_ranked(first_round, data))
    print(random_likelihood(first_round, data))

def tournament_teams(data):
    """ 
    Removes teams from the data set that
    do not have a seed in the tournament 
    """
    # removes field names
    data = np.delete(data, 0, 0)

    for team in reversed(range(NUM_TEAMS)):
        if data[team][3] == "":
            data = np.delete(data, team, 0)
    return data

def generate_dist(team):
    """ 
    Returns a list with parameters to a 
    normal distribution (mean and variance) 
    """
    mean = float(team[1])
    
    # converts consistency into variance
    consistency = float(team[2])
    var = 1.0 / consistency

    return [mean, var]

def A_beats_B(team1, team2):
    """ 
    Given the parameters to each team's 
    normal distribution, the function returns 
    the probability that the first team beats 
    the secondn (assuming game results are 
    independent of matchups). This is 
    P(B < A) = P(B - A < 0). 
    """
    # find statistics of the joint normal 
    joint_mean = team2[0] - team1[0]
    joint_var = team2[1] + team2[1]

    # determine z-score
    z = -joint_mean / joint_var

    # generate probability
    return norm.cdf(z)

def simulate_game_highest_likelihood(next_round, i, game1_prob, game2_prob):
    """
    Simulates a game in the tournament bracket
    where the team with the highest probability
    of winning wins.
    """
    next_game = []
    if game1_prob >= 0.5:
        next_game.append(first_round_id[i][0])
    else:
        game1_prob = 1 - game1_prob
        next_game.append(first_round_id[i][1])
    
    if game2_prob >= 0.5:
        next_game.append(first_round_id[i + 1][0])
    else:
        game2_prob = 1 - game2_prob
        next_game.append(first_round_id[i + 1][1])
    # set up next round
    next_round.append(next_game)
    return game1_prob / 0.5 * game2_prob / 0.5

def simulate_round_highest_likelihood(cur_round, next_round, bracket_likelihood, data):
    """
    The function generates a round and returns the
    likelihood that the better team wins in each match
    wins.
    """
    for i in range(0, len(cur_round), 2):
        # generate probabilites
        game1_prob = A_beats_B(generate_dist(data[first_round_id[i][0]]), generate_dist(data[first_round_id[i][1]]))
        game2_prob = A_beats_B(generate_dist(data[first_round_id[i + 1][0]]), generate_dist(data[first_round_id[i + 1][1]]))

        # set up next round
        simulate_game_highest_likelihood(next_round, i, game1_prob, game2_prob)

        # calculate current likelihood
        bracket_likelihood *= simulate_game_highest_likelihood(next_round, i, game1_prob, game2_prob)
    return bracket_likelihood

def highest_likelihood(first_round, data):
    """
    Given a tournament bracket, the function
    determines the likelihood of the most
    probable bracket.
    """
    second_round = []
    sweet_sixteen = []
    elite_eight = []
    final_four = []
    championship = []
    winner = []

    bracket_likelihood = 1

    # simulate first round
    bracket_likelihood = simulate_round_highest_likelihood(first_round, second_round, bracket_likelihood, data)
    # simulate second round
    bracket_likelihood = simulate_round_highest_likelihood(second_round, sweet_sixteen, bracket_likelihood, data)
    # simulate sweet sixteen
    bracket_likelihood = simulate_round_highest_likelihood(sweet_sixteen, elite_eight, bracket_likelihood, data)
    # simulate elite eight
    bracket_likelihood = simulate_round_highest_likelihood(elite_eight, final_four, bracket_likelihood, data)
    # simulate final four
    bracket_likelihood = simulate_round_highest_likelihood(final_four, championship, bracket_likelihood, data)
    # simulate championchip
    bracket_likelihood = simulate_round_highest_likelihood(championship, winner, bracket_likelihood, data)
    
    return bracket_likelihood

def simulate_round_highest_ranked(cur_round, next_round, bracket_likelihood, data):
    """
    The function generates a round and returns the
    likelihood that the higher ranked team wins in 
    each match wins.
    """
    for i in range(0, len(cur_round), 2):
        # determine higher ranked team
        higher_ranked1 = first_round_id[i][0]  # makes arbitrary choice of first team if tied
        lower_ranked1 = first_round_id[i][1]
        higher_ranked2 = first_round_id[i + 1][0]
        lower_ranked2 = first_round_id[i + 1][1]
        if data[higher_ranked1][3] > data[lower_ranked1][3]:
            lower_ranked1 = first_round_id[i][0]
            higher_ranked1 = first_round_id[i][1]
        if data[higher_ranked2][3] > data[lower_ranked2][3]:
            lower_ranked2 = first_round_id[i + 1][0]
            higher_ranked2 = first_round_id[i + 1][1]

        # generate probabilites
        game1_prob = A_beats_B(generate_dist(data[higher_ranked1]), generate_dist(data[lower_ranked1]))
        game2_prob = A_beats_B(generate_dist(data[higher_ranked2]), generate_dist(data[lower_ranked2]))

        # set up next round
        next_game = [higher_ranked1, higher_ranked2]
        print(next_game)
        next_round.append(next_game)

        # calculate current likelihood
        bracket_likelihood *= game1_prob / 0.5 * game2_prob / 0.5

    return bracket_likelihood

def highest_ranked(first_round, data):
    """
    Given a tournament bracket, the function
    determines the likelihood of a bracket 
    with no upsets.
    """
    second_round = []
    sweet_sixteen = []
    elite_eight = []
    final_four = []
    championship = []
    winner = []

    bracket_likelihood = 1

    # simulate first round
    bracket_likelihood = simulate_round_highest_ranked(first_round, second_round, bracket_likelihood, data)
    # simulate second round
    bracket_likelihood = simulate_round_highest_ranked(second_round, sweet_sixteen, bracket_likelihood, data)
    # simulate sweet sixteen
    bracket_likelihood = simulate_round_highest_ranked(sweet_sixteen, elite_eight, bracket_likelihood, data)
    # simulate elite eight
    bracket_likelihood = simulate_round_highest_ranked(elite_eight, final_four, bracket_likelihood, data)
    # simulate final four
    bracket_likelihood = simulate_round_highest_ranked(final_four, championship, bracket_likelihood, data)
    # simulate championchip
    bracket_likelihood = simulate_round_highest_ranked(championship, winner, bracket_likelihood, data)
    
    return bracket_likelihood

def simulate_round_random_likelihood(cur_round, next_round, bracket_likelihood, data):
    """
    The function generates a round and returns the
    likelihood a random team wins. 
    """
    for i in range(0, len(cur_round), 2):
        # randomly selct winners
        winner1 = first_round_id[i][0]  # makes arbitrary choice of first team if tied
        loser1 = first_round_id[i][1]
        winner2 = first_round_id[i + 1][0]
        loser2 = first_round_id[i + 1][1]

        if random.random() >= 0.5:
            loser1 = winner1
            winner1 = first_round_id[i][1]
            loser2 = winner2
            winner2 = first_round_id[i + 1][1]

        # generate probabilites
        game1_prob = A_beats_B(generate_dist(data[winner1]), generate_dist(data[loser1]))
        game2_prob = A_beats_B(generate_dist(data[loser1]), generate_dist(data[loser2]))

        # set up next round
        next_game = [winner1, winner2]
        next_round.append(next_game)

        # calculate current likelihood
        bracket_likelihood *= game1_prob / 0.5 * game2_prob / 0.5
    return bracket_likelihood

def random_likelihood(first_round, data):
    """
    Given a tournament bracket, the function
    determines the likelihood of a random
    bracket.
    """
    second_round = []
    sweet_sixteen = []
    elite_eight = []
    final_four = []
    championship = []
    winner = []

    bracket_likelihood = 1

    # simulate first round
    bracket_likelihood = simulate_round_random_likelihood(first_round, second_round, bracket_likelihood, data)
    # simulate second round
    bracket_likelihood = simulate_round_random_likelihood(second_round, sweet_sixteen, bracket_likelihood, data)
    # simulate sweet sixteen
    bracket_likelihood = simulate_round_random_likelihood(sweet_sixteen, elite_eight, bracket_likelihood, data)
    # simulate elite eight
    bracket_likelihood = simulate_round_random_likelihood(elite_eight, final_four, bracket_likelihood, data)
    # simulate final four
    bracket_likelihood = simulate_round_random_likelihood(final_four, championship, bracket_likelihood, data)
    # simulate championchip
    bracket_likelihood = simulate_round_random_likelihood(championship, winner, bracket_likelihood, data)
    
    return bracket_likelihood


if __name__ == "__main__":
    main()