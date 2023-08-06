'''
Created on Jan 14, 2016

@author: Callum McCulloch
@project: Web Worlds Project
@class: WebGraphDrawer

Class used to represent the Web Graph of a Web World as a visual graph using MatPlotLib

'''

import networkx as nx 
from matplotlib import pyplot  as plt 

class WebGraphDrawer:
    
    def __init__ (self,WebGraph):
        self.WEB_GRAPH = WebGraph
        self.EDGE_LIST = self.WEB_GRAPH.EDGE_LIST
        self.WEIGHTED_EDGE_LIST = self.WEB_GRAPH.get_weighted_graph_edges()
        self.DIAGRAM = self.draw_graph()
    
    def get_drawing(self):
        return self.DIAGRAM

    def draw_graph(self):
    
        # extract nodes from graph
        nodes = self.WEB_GRAPH.get_node_list() 

        # create networkx graph
        G=nx.Graph() 

        # add nodes
        for node in nodes:
            G.add_node(node)

        # add edgesfrom Data import Five
        for edge in self.WEB_GRAPH.WEIGTED_GRAPH_EDGES:
            G.add_edge(edge[0], edge[1], weight = edge[2])
        # draw graph
        pos = nx.shell_layout(G)
        nx.draw(G, pos, with_labels = True)
        edge_labels = dict([((u,v,),d['weight'])
             for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

        # return graph
        return plt