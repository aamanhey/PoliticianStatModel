#General Imports
import json
from requests import get
from bs4 import BeautifulSoup

def get_links():
    response = get('https://en.wikipedia.org/wiki/List_of_United_States_Senate_elections_(1914%E2%80%93present)')
    # print(response.text[:500])

    #'html.parser' is python's built-in parser
    soup=BeautifulSoup(response.text, 'html.parser')

    #Election Titles/Dates
    elections = []
    for date in soup.find_all('span', {"class": "mw-headline"}):
       elections.append(date.get('id'))
    # print(elections)

    #Links of elections
    divs = soup.find_all('div a', {"role": "note"})
    links = []
    for link in soup.find_all('a', {"role": "note"}):
       links.append(link.get('href'))
    # print(links)

    #Links of elections
    links = []
    for div in soup.find_all('div',{'class':'hatnote'}):
      link = div.find('a',href=True)
      link = link.get('href')
      links.append(link)
    # print(links)
    return links

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class