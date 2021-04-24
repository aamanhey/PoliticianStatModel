import csv
import people
import elections
import json
import random
import matplotlib.pyplot as plt
import numpy as np

def get_data():
    all_election_years = []
    with open('cleaned_data.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        year = 0
        current = None
        for row in spamreader:
            # print(row)
            if(year != row[0]):
                all_election_years.append(current)
                current = elections.ElectionYear(row[0])
                year = row[0]
            current.add_election(row)
        # all_election_years[1].print()
        # all_election_years[2].print()
    return all_election_years

def get_woman_cand_stats(current_data, election):
    incumbent = election.incumbent
    candidates = election.candidates
    c1 = candidates[0]
    c2 = candidates[1]

    # print(incumbent == None, c1.person.gender, c2.person.gender)

    if(c1.person.gender == "1"):
        # winner female
        if(c2.person.gender == "1"):
            # winner female, loser female
            current_data["both_women"] += 1
        else:
            # winner female, loser male
            current_data["woman_won"] += 1
    else:
        # winner male
        if(c2.person.gender == "1"):
            # winner male, loser female
            current_data["woman_lost"] += 1
        else:
            # winner male, loser male
            current_data["no_women"] += 1
    return current_data

def competition_stats(all_election_years):
    '''
    returns the number of elections where the candidates are both women, one
    woman and they one, one woman and they lost, and had no women as a dictionary
    '''
    all_years = {}
    model = {"no_women" : 0, "woman_won" : 0,
        "woman_lost" : 0, "both_women" : 0}

    for election_year in all_election_years:
        if(election_year != None):
            year = election_year.year
            current_data = {"no_women" : 0, "woman_won" : 0,
                "woman_lost" : 0, "both_women" : 0}

            for election in election_year.elections:
                current_data = get_woman_cand_stats(current_data, election)
            all_years[year] = current_data
            current_data = model
    return all_years

def get_percentage_of_votes(current_data, election):
    data_point = {"x-val":None,
        "Percent of Vote": 0, "type":None}
    incumbent = election.incumbent
    candidates = election.candidates
    c1 = candidates[0]
    c2 = candidates[1]

    # print(incumbent == None, c1.person.gender, c2.person.gender)
    #data_point["x-val"] = float("".join(c1.funding.strip("$").split(",")))
    data_point["x-val"] = election.year

    data_point["Percent of Vote"] = float(c1.perc_votes.strip("%"))

    if(c1.person.gender == "1"):
        # winner female
        if(c2.person.gender == "1"):
            # winner female, loser female
            data_point["type"] = 0
        else:
            # winner female, loser male
            data_point["type"] = 1
    else:
        # winner male
        if(c2.person.gender == "1"):
            # winner male, loser female
            data_point["type"] = 2
        else:
            # winner male, loser male
            data_point["type"] = 3

    # current_data["x_vals"].append(data_point["x-val"])
    # current_data["y_vals"].append(data_point["Percent of Vote"])
    # current_data["categories"].append(data_point["type"])

    current_data[data_point["type"]]["x_vals"].append(data_point["x-val"])
    current_data[data_point["type"]]["y_vals"].append(data_point["Percent of Vote"])

    return current_data

def election_stats(all_election_years):
    #data = {"x_vals":[], "y_vals":[], "categories":[]}
    sub_data = {"x_vals":[], "y_vals":[]}
    data = [{"x_vals":[], "y_vals":[]}, {"x_vals":[], "y_vals":[]}, {"x_vals":[], "y_vals":[]}, {"x_vals":[], "y_vals":[]}] # category: {x_vals[], y_vals[]}

    for election_year in all_election_years:
        if(election_year != None and election_year.year != "year"):
            year = election_year.year
            for election in election_year.elections:
                election.print()
                data = get_percentage_of_votes(data, election)

    # colormap = np.array(['#f4b400', '#4285f4', '#db4437', '#bebdbe'])
    colormap = np.array(['#FFC20A', '#0C7BDC', '#E66100', '#5D3A9B'])
    # yellow = #f4b400, blue = #4285f4, red = #db4437, green = #0f9d58, grey = #bebdbe
    # yellow = #FFC20A, blue = #0C7BDC, orange = #E66100, purple = #5D3A9B
    labelmap = np.array(["WW", "WM", "MW", "MM"])
    # WW, WM, MW, MM
    # plt.scatter(data["x_vals"], data["y_vals"], s=100, c=colormap[data["categories"]])
    i = 3
    for each in data:
        print(labelmap[i], len(data[i]["y_vals"]))
        plt.scatter(data[i]["x_vals"], data[i]["y_vals"], color=colormap[i], label=labelmap[i])
        i -= 1
    plt.xlabel("Year")
    plt.ylabel("Percentage of Votes")
    plt.text(2, 0, "Tallies of Races: \n(AvB: A won against B) \nMvM 287 \nMvW 57 \nWvM 40 \nWvW 15")
    plt.legend()
    plt.title("Percentage of Vote with Time")
    plt.show()
    with open('stats.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)

    # return percentages

def format_num(num):
    num = num * 1000
    num = int(num)
    num = num / 1000
    return num

def get_proportion_of_women(elections):
    num_women = 0
    num_men = 0
    for election in elections:
        candidates = election.candidates
        c1 = candidates[0]
        c2 = candidates[1]
        if(c1.person.gender == "1"):
            num_women += 1
        else:
            num_men += 1
        if(c2.person.gender == "1"):
            num_women += 1
        else:
            num_men += 1
    return format_num(num_women/num_men)

def get_candidate_gender_makeup(all_election_years):
    percent_women = {}
    for election_year in all_election_years:
        if(election_year != None):
            year = election_year.year
            percent_women[year] = get_proportion_of_women(election_year.elections)
    return percent_women

def get_proportion_of_incumbent(elections):
    num_incumbent_winners = 0
    total = 0
    for election in elections:
        candidates = election.candidates
        c1 = candidates[0]
        if(c1.incumbent):
            num_incumbent_winners += 1
        total += 1
    return format_num(num_incumbent_winners/total)

def get_incumbent_winners(all_election_years):
    percent_incumbent = {}
    for election_year in all_election_years:
        if(election_year != None):
            year = election_year.year
            percent_incumbent[year] = get_proportion_of_incumbent(election_year.elections)
    return percent_incumbent


if __name__ == '__main__':
    all_election_years = get_data()
    # color value (0=no women, 1=woman won, 2=woman lost, 3=both women
    # comp_stats = competition_stats(all_election_years)
    # cand_stats = get_candidate_gender_makeup(all_election_years)
    incumbent_stats = get_incumbent_winners(all_election_years)
    # election_stats = election_stats(all_election_years)

    jsonstr = json.dumps(incumbent_stats, indent=2)
    print(jsonstr)
