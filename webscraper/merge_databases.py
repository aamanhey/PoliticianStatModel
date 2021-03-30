# gets the data from propublica and merges is with the webscraped wiki data

import json
import matplotlib.pyplot as plt
from os import path

# set the filepath to get files outside current directory
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "propublica","propublica_formatted.json"))

# propublica data
with open(filepath) as f:
  propublica = json.load(f)

#redefine filepath for wiki data
filepath = path.abspath(path.join(basepath, "..", "data","wikidata.json"))

# webscraped wikipedia data
with open(filepath) as f:
  wikidata = json.load(f)

merged_data = []

'''
Iterates through the wiki data and adds the correponding propublica data to
each of the incumbents as a new dictionary.
'''
for year in range(1990, 2015+1):
    index = int((year-1914)/2) # turn the year into a usable index,
    elections = wikidata[index]['elections'] # regular elections for senate in a given year
    propublica_senate = propublica[str(int((year-1788)/2))] # the corresponding senate for that year
    for election in elections:
        # get the current incumbent candidate and the corresponding propublica data if it exists
        senator = election['incumbent']['name']
        if(senator in propublica_senate):
            pp_info = propublica_senate[senator]
            election['incumbent']['pp_info'] = pp_info
    # take the new data and add it to the merged data dictionary
    merged_data.append(wikidata[index])

# exports the merged_data dictionary to a file as a JSON string
with open('merged_data.json', 'w') as outfile:
    json.dump(merged_data, outfile, indent=2)
