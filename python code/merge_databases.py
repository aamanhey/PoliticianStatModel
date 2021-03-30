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

# start with 2000 - 2015
senators = {}
# str(int((year-1788)/2))
for year in range(2000, 2015+1):
    congress_num = str(int((year-1788)/2))
    senate = propublica[congress_num]
# unfinished
