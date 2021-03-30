import csv
import json

with open('racial.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0
    group_ctr = 0
    all = {}
    group = []
    group_names = ['African Americans', 'Asian Americans', 'Hispanic Americans', 'Native American Indians']
    for row in csv_reader:
        if(row[0] == "//"):
            all[group_names[group_ctr]] = group
            group = []
            group_ctr += 1
        else:
            senator = {"lastname":row[0],
                "firstname":row[1],
                "party-state":row[2],
                "term":[]
                }
            term = row[3].strip().split("(")
            print(term)
            senator['term'].append(term[0].strip())
            if(group_ctr == 3):
                senator['tribe'] = term[1].strip(")")
            group.append(senator)

    with open('racial_stats.json', 'w') as outfile:
        json.dump(all, outfile, indent=2)
