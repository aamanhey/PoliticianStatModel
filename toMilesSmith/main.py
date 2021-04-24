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
    return all_election_years

def get_percentage_of_votes(current_data, election):
    data_point = {"x-val":None,
        "Percent of Vote": 0, "type":None}

    candidates = election.candidates
    c1 = candidates[0]
    c2 = candidates[1]

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

    # current_data[data_point["type"]]["x_vals"].append(data_point["x-val"])
    # current_data[data_point["type"]]["y_vals"].append(data_point["Percent of Vote"])

    return data_point

def election_stats(all_election_years):
    data = [{"x_vals":[], "y_vals":[]}, {"x_vals":[], "y_vals":[]}, {"x_vals":[], "y_vals":[]}, {"x_vals":[], "y_vals":[]}] # category: {x_vals[], y_vals[]}

    with open('formatted.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["year", "state", "candidate", "winner", "Percent of Vote", "type"])
        for election_year in all_election_years:
            if(election_year != None and election_year.year != "year"):
                year = election_year.year
                for election in election_year.elections:
                    # election.print()
                    data_point = get_percentage_of_votes(data, election)
                    data[data_point["type"]]["x_vals"].append(election.year)
                    data[data_point["type"]]["y_vals"].append(data_point["Percent of Vote"])
                    # skip over the second of the unopposed
                    for i in range(0, len(election.candidates)):
                        if(election.candidates[i].person.name != "Unopposed"):
                            writer.writerow([election.year, election.state, election.candidates[i].person.name, i == 0, data_point["Percent of Vote"], data_point["type"]])


    colormap = np.array(['#FFC20A', '#0C7BDC', '#E66100', '#5D3A9B'])
    # yellow = #FFC20A, blue = #0C7BDC, orange = #E66100, purple = #5D3A9B
    labelmap = np.array(["WW", "WM", "MW", "MM"])
    # WW, WM, MW, MM
    i = 3
    for each in data:
        print(labelmap[i], len(data[i]["y_vals"])) # PRINTS OUT COUNTS
        plt.scatter(data[i]["x_vals"], data[i]["y_vals"], color=colormap[i], label=labelmap[i])
        i -= 1
    # CREATE SCATTER PLOT
    plt.xlabel("Year")
    plt.ylabel("Percentage of Votes")
    plt.text(2, 0, "Tallies of Races: \n(AvB: A won against B) \nMvM 287 \nMvW 57 \nWvM 40 \nWvW 15")
    plt.legend()
    plt.title("Percentage of Vote with Time")
    plt.show()



if __name__ == '__main__':
    all_election_years = get_data()
    election_stats = election_stats(all_election_years)
