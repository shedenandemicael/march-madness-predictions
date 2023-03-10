import numpy as np
from scipy.stats import norm

NUM_TEAMS = 363

def main():
    data = np.loadtxt("data.csv", delimiter=",", dtype=str)

    # removes non-tournament teams
    data = tournament_teams(data)

    team1 = generate_dist(data[0])
    team2 = generate_dist(data[6])

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

if __name__ == "__main__":
    main()