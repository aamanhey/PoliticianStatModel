# visualizes the webscraper data
import networkx as nx
import matplotlib.pyplot as plt
from os import path
import json

# Defining a graph class
class GraphVisualization:

    def __init__(self):
        # the set of edges
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G, with_labels=False)
        plt.show()

def graph():
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data","wikidata.json"))

    # webscraped wikipedia data
    with open(filepath) as f:
      wikidata = json.load(f)

    senate = GraphVisualization()

    for each in wikidata:
        if(int(each['year']) in range(1990, 2015+1) and int(each['year']) != 2004):
            elections = each['elections']
            for state in elections:
                incumbent_info = state['incumbent']
                if(incumbent_info != None):
                    print(each['year'])
                    if(incumbent_info['name'] == 'Ohio'):
                        quit()
                    senator = incumbent_info['name']
                    election_history = incumbent_info['elect_hist']
                    for year in election_history:
                        senate.addEdge(senator, year[:4])
    senate.visualize()

def scatter():
    with open('wiki_stats.json') as f:
        data = json.load(f)
    # creates a scatter plot of the data
    x_vals = []
    y_vals = []
    z_vals = []

    for each in data:
        # print(each)
        if(each != 'total'):
            # get the proportion of women to men in the senate in the current year
            year = 1788 + 2*(int(each))
            congress = data[each]
            incumbent_wins = congress['incumbent_wins']
            elections = congress['elections']
            candidates = congress['candidates']
            p = incumbent_wins / elections
            x_vals.append(year)
            y_vals.append(p)
            z_vals.append(candidates)
    # create the scatter plot using matplotlib
    fig = plt.figure()
    s = plt.scatter(x_vals, y_vals)
    fig.suptitle('Proportion of Incumbent Wins to Total Elections in the Senate\nfrom the 101st to the 113th Congresses')
    plt.show()

    fig = plt.figure()
    s = plt.scatter(x_vals, z_vals)
    fig.suptitle('Number of Candidates Running for Senate Position\nfrom the 101st to the 113th Congresses')
    plt.show()


def hist_race():
    with open('racial_stats.json') as f:
        data = json.load(f)
    # gets the total number of racial groups in senate
    total = len(data['African Americans']) + len(data['Asian Americans']) + len(data['Hispanic Americans']) + len(data['Native American Indians'])
    new_data = {'African\nAmericans':len(data['African Americans']),'Asian\nAmericans':len(data['Asian Americans']), 'Hispanic\nAmericans':len(data['Hispanic Americans']), 'Native American\nIndians':len(data['Native American Indians'])}
    new_data['total'] = total
    groups = list(new_data.keys())
    values = list(new_data.values())

    # create the histogram using matplotlib
    fig, axs = plt.subplots()
    axs.bar(groups, values)
    fig.suptitle('Total Racial Makeup of the Senate')
    plt.show()

hist_race()
