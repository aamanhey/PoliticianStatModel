# visualizes the webscraper data
# First networkx library is imported
# along with matplotlib
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
# creates a blob
