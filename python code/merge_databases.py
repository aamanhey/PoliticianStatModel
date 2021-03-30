# gets the data from propublica and merges is with the webscraped data

import json
import matplotlib.pyplot as plt
from os import path

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "propublica","propublica_formatted.json"))

# propublica data
with open(filepath) as f:
  propublica = json.load(f)

filepath = path.abspath(path.join(basepath, "..", "data","wikidata.json"))

# webscraped wikipedia data
with open(filepath) as f:
  wikidata = json.load(f)

merged_data = []

for year in range(1990, 2015+1):
    index = int((year-1914)/2)
    elections = wikidata[index]['elections']
    propublica_senate = propublica[str(int((year-1788)/2))]
    for election in elections:
        senator = election['incumbent']['name']
        if(senator in propublica_senate):
            pp_info = propublica_senate[senator]
            election['incumbent']['pp_info'] = pp_info
    merged_data.append(wikidata[index])

with open('merged_data.json', 'w') as outfile:
    json.dump(merged_data, outfile, indent=2)
