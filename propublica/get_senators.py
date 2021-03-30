# gets senators from propublica_congress_members.json
import json
import matplotlib.pyplot as plt

# open json file
with open('propublica.json') as f:
  data = json.load(f)

#print(json.dumps(data, indent=2))
all_senators = {}
for i in range(80, 117+1):
    senators = data[str(i)]['results'][0]['members']
    formatted_senators = {}
    for each in senators:
        sen = {"title": each['title'],
        "first_name": each['first_name'],
        "middle_name": each['middle_name'],
        "last_name": each['last_name'],
        "date_of_birth": each['date_of_birth'],
        "gender": each['gender'],
        "party": each['party'],
        "leadership_role": each['leadership_role'],
        "govtrack_id": each['govtrack_id'],
        "google_entity_id": each['google_entity_id'],
        "fec_candidate_id": each['fec_candidate_id'],
        "in_office": each['in_office'],
        "dw_nominate": each['dw_nominate'],
        "ideal_point": each['ideal_point'],
        "seniority": each['seniority'],
        "next_election": each['next_election'] if 'next_election' in each.keys() else None,
        "total_votes": each['total_votes'],
        "missed_votes": each['missed_votes'],
        "total_present": each['total_present'],
        "state": each['state'],
        "senate_class": each['senate_class'],
        "state_rank": each['state_rank'],
        "lis_id": each['lis_id'],
        "missed_votes_pct": each['missed_votes'],
        "votes_with_party_pct": each['votes_with_party_pct'] if 'votes_with_party_pct' in each.keys() else None,
        "votes_against_party_pct": each['votes_against_party_pct'] if 'votes_against_party_pct' in each.keys() else None
        }
        formatted_senators[each['first_name'] + " " + each['last_name']] = sen
        all_senators[i] = formatted_senators
    print(i, "parsed")

with open('propublica_formatted.json', 'w') as outfile:
    json.dump(all_senators, outfile, indent=2)
