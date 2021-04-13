import csv
import people
import elections
import json

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

    jsonstr = json.dumps(incumbent_stats, indent=2)
    print(jsonstr)
