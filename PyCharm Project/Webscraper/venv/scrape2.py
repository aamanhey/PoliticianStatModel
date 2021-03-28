import requests
import json
from bs4 import BeautifulSoup
import html

class Senator:
    def __init__(self, name, elect_hist):
        self.name = name
        self.elect_hist = elect_hist

    def pretty_print(self):
        print(self.name)
        print(self.elect_hist)

class StateElection:
    def __init__(self, state, incumbent, result, candidates):
        self.state = state
        self.incumbent = incumbent
        self.result = result
        self.candidates = candidates

    def pretty_print(self):
        print("State Election:")
        print("  ",self.state)
        print("  ",self.incumbent.name)
        print("    ", "Prev Elects:", self.incumbent.elect_hist)
        print("  ",self.candidates)

class ElectionYear:
    def __init__(self, year, elections):
        self.year = year
        self.elections = elections

    def pretty_print(self):
        print(self.year)
        for each in self.elections:
            each.pretty_print()

def get_header(response):
    html_file = BeautifulSoup(response.text, "html.parser")
    heading = html_file.findAll('h1', {"class":"firstHeading"})
    return heading[0].text.strip()

def get_state_election_json(table_row):
    state_name = table_row.find('th')
    election_info = table_row.findAll('td')

    # get info on the incumbent senator
    election_history = election_info[2].findAll('a')  # election history in html
    # senator = Senator(election_info[0].text.strip(), [])
    incumbent = {"name": election_info[0].text.strip(), "elect_hist": []}

    for each in election_history:
        incumbent['elect_hist'].append(each.text)

    # the result of the election (blurb)
    election_result = election_info[3]

    # get the candidates that ran in this election
    candidates = election_info[4].findAll('li')  # candidates
    candidates_list = []
    for each in candidates:
        candidates_list.append(each.text)

    election = {"state":state_name.text.strip(), "incumbent":incumbent, "result":election_result.text.strip(), "candidates":candidates_list}
    return election

def parse_json(response):
    html_file = BeautifulSoup(response.text, "html.parser")
    #wikiTables = html_file.find('div', {'id': 'bodyContent'}).find('div', {'id': 'mw-content-text'}).find('div', {'class': 'mw-parser-output'}).findAll('table', {'class': 'wikitable sortable'})
    wikiTables = html_file.findAll('table', {'class': 'wikitable sortable'})

    # find the table for the elections leading to the next congress and get the data from the columns
    regular_elections = wikiTables[3].findAll('tr')
    year_info = get_header(response)
    year = year_info[:4]
    election_year = {"year":year, "elections":[]}
    for i in range(2, len(regular_elections)):
        election_year['elections'].append(get_state_election_json(regular_elections[i]))

    json_dump = json.dumps(election_year, indent=2)
    print(json_dump)
    f = open(year+"data.json", "w")
    f.write(json_dump)
    f.close()


def get_state_election(table_row):
    state_name = table_row.find('th')
    election_info = table_row.findAll('td')

    # get info on the incumbent senator
    election_history = election_info[2].findAll('a')  # election history in html
    senator = Senator(election_info[0].text.strip(), [])
    for each in election_history:
        senator.elect_hist.append(each.text)

    # the result of the election (blurb)
    election_result = election_info[3]

    # get the candidates that ran in this election
    candidates = election_info[4].findAll('li')  # candidates
    candidates_list = []
    for each in candidates:
        candidates_list.append(each.text)

    election = StateElection(state_name.text.strip(), senator, election_result, candidates_list)
    return election

def parse(response):
    html_file = BeautifulSoup(response.text, "html.parser")
    #wikiTables = html_file.find('div', {'id': 'bodyContent'}).find('div', {'id': 'mw-content-text'}).find('div', {'class': 'mw-parser-output'}).findAll('table', {'class': 'wikitable sortable'})
    wikiTables = html_file.findAll('table', {'class': 'wikitable sortable'})

    # find the table for the elections leading to the next congress and get the data from the columns
    regular_elections = wikiTables[3].findAll('tr')
    year_info = get_header(response)
    election_year = ElectionYear(year_info, [])
    for i in range(2, len(regular_elections)):
        election_year.elections.append(get_state_election(regular_elections[i]))

    election_year.pretty_print()


def parse2(response):
    html_file = BeautifulSoup(response.text, "html.parser")


    bodyContent = html_file.findAll('div', {'id': 'bodyContent'})
    print(len(bodyContent))
    contentText = bodyContent[0].findAll('div', {'id': 'mw-content-text'})
    print(len(contentText))
    # print(contentText)
    parserOutput = contentText[0].findAll('div', {'class': 'mw-parser-output'})
    print(len(parserOutput))
    wikiTables = parserOutput[0].findAll('table', {'class': 'wikitable sortable'})
    # print(type(wikiTables))
    print(len(wikiTables))
    # print(wikiTables[3])
    states = wikiTables[3].findAll('tr')
    print(len(states))
    # print(states[2])
    state = states[2].find('th')
    print(state.text)
    state = states[2].findAll('td')
    print("senator ", state[0].text)  # Doug, Jones
    previous_elections = []
    # print(senator[2].text)
    election_hist = state[2].findAll('a')
    # print(election_hist)
    for i in range(len(election_hist)):
        previous_elections.append(election_hist[i].text)

    print(previous_elections)
    state[3] # election result
    candidates = state[4].findAll('li') # candidates
    # print(candidates)
    candidates_list = []
    for each in candidates:
        # print(each.text)
        candidates_list.append(each.text)
    print(candidates_list)




elections_links = ["https://en.wikipedia.org/wiki/2020_United_States_Senate_elections"]

for election_link in elections_links:
    response = requests.get(election_link)
    #print(response.text[:500])
    parse_json(response)