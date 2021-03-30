# counts the number of representatives that are Male and Female
import json
from os import path
from urllib.request import urlopen

# calls the GenderAPI to approximate the gender based on a person's name for senators that did not have
# a gender available in propublica
def approx_gender(name):
    myKey = "cuBFBDdkJGrCWETndE"
    #split up the name split=tim%20johnson to first and last and replace space with %20
    url = "https://gender-api.com/get?key=" + myKey + "&country=US"
    # includes first and last names if available
    if (len(name) == 2):
        url = url + "&split=" + name[0] + "%20" + name[1]
    # includes first name if available
    elif (len(name) == 1):
        url = url + "&name=" + name[0]
    # does not make query if no name available
    else:
        return {"gender":None, "accuracy":100}
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    info = json.loads(decoded)
    return {"gender":info["gender"], "accuracy":info['accuracy']}

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "data","wikidata.json"))

# webscraped wikipedia data
with open(filepath) as f:
  wikidata = json.load(f)

# counters for all the years considered
tot_incumbent_wins = 0
tot_candidates = 0
tot_elections = 0

stats = {}

# iterate through each of the congresses in the propublica dataset and count the number of men and women
# data = []
# data.append(wikidata[int((1990-1914)/2)])
for each in wikidata:
    congress_num = str(int((int(each['year'])-1788)/2)) # convert year into the congress number
    if(int(each['year']) in range(1990, 2015+1) and int(each['year']) != 2004):
        elections = each['elections']
        num_incumbent_wins = 0
        num_candidates = 0
        num_elections = 0
        for state in elections:
            if(state['incumbent'] != None and state['incumbent']['name'] in state['candidates'][0]):
                num_candidates += len(state['candidates']) - 1
                tot_candidates += len(state['candidates']) - 1

                num_incumbent_wins += 1
                tot_incumbent_wins += 1
            else:
                num_candidates += len(state['candidates'])
                tot_candidates += len(state['candidates'])
            num_elections += 1
            tot_elections += 1
        stats[congress_num] = {'incumbent_wins':num_incumbent_wins, 'candidates':num_candidates, 'elections':num_elections}
# add the total value of the counters to a seperate field in the overall dictionary
stats['total'] = {'incumbent_wins':tot_incumbent_wins, 'candidates':tot_candidates, 'elections':tot_elections}

# exports the stats dictionary to a file as a JSON string
with open('wiki_stats.json', 'w') as outfile:
    json.dump(stats, outfile, indent=2)
