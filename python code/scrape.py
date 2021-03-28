import requests
import json
from bs4 import BeautifulSoup
import html


def get_header(response):
    html_file = BeautifulSoup(response.text, "html.parser")
    heading = html_file.findAll('h1', {"class":"firstHeading"})
    return heading[0].text.strip()

def get_election(table_row):
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

def parse(response):
    # find the table for the elections leading to the next congress and
    html_file = BeautifulSoup(response.text, "html.parser")
    wikiTables = html_file.findAll('table', {'class': 'wikitable sortable'})

    # get the data from the rows of the wikitable
    regular_elections = wikiTables[3].findAll('tr')
    year_info = get_header(response)
    year = year_info[:4]
    election_year = {"year":year, "elections":[]}
    for i in range(2, len(regular_elections)):
        election_year['elections'].append(get_election(regular_elections[i]))

    # convert to JSON
    json_dump = json.dumps(election_year, indent=2)

    # write to external file
    f = open(year+"data.json", "w")
    f.write(json_dump)
    f.close()

def scrape(elections_links):
    for election_link in elections_links:
        response = requests.get(election_link)
        parse(response) # parses the response into JSON

if __name__ == '__main__':
    elections_links = ["https://en.wikipedia.org/wiki/2020_United_States_Senate_elections"]
    scrape(elections_links)