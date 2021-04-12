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

if __name__ == '__main__':
    all_election_years = get_data()
    # color value (0=no women, 1=woman won, 2=woman lost, 3=both women
    all_years = {}
    model = {"no_women" : 0,
            "woman_won" : 0,
            "woman_lost" : 0,
            "both_women" : 0
             }

    for election_year in all_election_years:
        if(election_year != None):
            year = election_year.year
            current_data = {"no_women" : 0,
                    "woman_won" : 0,
                    "woman_lost" : 0,
                    "both_women" : 0
                     }
            for election in election_year.elections:
                incumbent = election.incumbent
                candidates = election.candidates
                c1 = candidates[0]
                c2 = candidates[1]

                if(incumbent == None and c2.person.name == "Unopposed"):
                    # no incumbent and only one candidate
                    if(c1.person.gender):
                        current_data["both_women"] += 1
                    else:
                        current_data["no_women"] += 1
                elif(incumbent == None and c2.person.name != "Unopposed"):
                    # no incumbent and two candidates
                    if(c1.person.gender and c2.person.gender):
                        current_data["both_women"] += 1
                    elif(c1.person.gender and c2.person.gender == 0):
                        current_data["woman_won"] += 1
                    elif(c1.person.gender == 0 and c2.person.gender):
                        current_data["woman_lost"] += 1
                    else:
                        current_data["no_women"] += 1
                elif(incumbent != None and c2.person.name == "Unopposed"):
                    # incumbent and one one candidate
                    if(c1.person.gender):
                        current_data["both_women"] += 1
                    else:
                        current_data["no_women"] += 1
                elif(incumbent != None and c2.person.name != "Unopposed"):
                    # incumbent and two candidates
                    if(c1.person.gender and c2.person.gender):
                        current_data["both_women"] += 1
                    elif(c1.person.gender and c2.person.gender == 0):
                        current_data["woman_won"] += 1
                    elif(c1.person.gender == 0 and c2.person.gender):
                        current_data["woman_lost"] += 1
                    else:
                        current_data["no_women"] += 1

                # putting all of them into both women!
            all_years[year] = current_data
            current_data = model
    jsonstr = json.dumps(all_years, indent=2)
    print(jsonstr)
