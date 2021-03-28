import requests
import json
from bs4 import BeautifulSoup
import html
import get_election_links


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

    if (state_name == None and election_result == None):
        election = {"state":state_name, "incumbent":incumbent, "result":election_result, "candidates":candidates_list}
    elif(state_name == None):
        election = {"state":state_name, "incumbent":incumbent, "result":election_result.text.strip(), "candidates":candidates_list}
    elif(election_result == None):
        election = {"state":state_name.text.strip(), "incumbent":incumbent, "result":election_result, "candidates":candidates_list}
    else:
        election = {"state":state_name.text.strip(), "incumbent":incumbent, "result":election_result.text.strip(), "candidates":candidates_list}
    return election

def parse(response):
    # find the table for the elections leading to the next congress and
    html_file = BeautifulSoup(response.text, "html.parser")
    # wikiTables = html_file.findAll('table', {'class': 'wikitable sortable'})
    headers = html_file.findAll('h3')
    wikiTables = []
    for each in headers:
        if("leading" in each.text.strip() or "next Congress" in each.text.strip()):
            wikiTables.append(each.find_next_siblings('table')[0])

    for each in wikiTables:
        col = each.find('th', {'colspan':'3'})
        if(col != None and col.text.strip() == 'Incumbent'):
            wikiTable = each;

    # get the data from the rows of the wikitable
    regular_elections = wikiTable.findAll('tr')
    year_info = get_header(response)
    year = year_info[:4]
    election_year = {"year":year, "elections":[]}
    for i in range(2, len(regular_elections)):
        election_year['elections'].append(get_election(regular_elections[i]))

    return election_year

def toJSON(elections):
    # convert to JSON
    json_dump = json.dumps(elections, indent=2)
    # write to external file
    f = open("completElectionData.json", "w")
    f.write(json_dump)
    f.close()

def scrape(elections_links, params):
    url_head = 'https://en.wikipedia.org'
    elections = []
    for election_link in elections_links:
        # print(url_head+election_link)
        year = election_link[6:10]
        if(int(year) in range(params['start'], params['end'])):
            print(year)
            response = requests.get(url_head+election_link)
            elections.append(parse(response)) # parses the response into JSON
    toJSON(elections)

if __name__ == '__main__':
    # elections_links = ["/wiki/2008_United_States_Senate_elections"]
    elections_links = get_election_links.get_links()
    scrape(elections_links, {'start':1914, 'end':2020})