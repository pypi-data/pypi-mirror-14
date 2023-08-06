'''
Created on Jan 12, 2016

@author: Callum McCulloch
@project: Web Worlds Project 
@class: Web Graph

Class to represent the Web Graph of Web World

The web graph is the graph that results from `forgetting' the heights of all end points of edges
in a web diagram. Another way to say this is that this is the graph one sees by looking down onto
a web diagram, so that the pegs appear as points, and where each edge of G(W) is weighted by
the number of edges between the two pegs containing its end points in the original diagram.

'''
import copy

class WebGraph:
    
    '''
         Initialises the Web Diagram Object and defines a list of global variables for the Web Diagram Class
    '''
    def __init__ (self,WebDiagram):
        self.WEB_DIAGRAM = WebDiagram.get_web_diagram()
        if self.WEB_DIAGRAM != [[]]:
            self.NODE_LIST = WebDiagram.get_peg_set()
            self.WEIGTED_GRAPH_EDGES = self.form_graph_edges()
            self.EDGE_LIST = self.form_edge_list()
        else:
            self.NODE_LIST = []
            self.WEIGTED_GRAPH_EDGES = []
    
    '''
        Returns the list of nodes of the Web Graph.
    '''
    def get_node_list(self):
        if self.WEB_DIAGRAM != [[]]:
            return self.NODE_LIST
    
    '''
        Returns the Weighted Graph Edges in the form [[Node0,Node1,Weight].....] where Node0 and Node1 are two 
        nodes with a connection edge and Weight being the weight associated with that edge.
    '''
    def get_weighted_graph_edges(self):
        if self.WEB_DIAGRAM != [[]]:
            return self.WEIGTED_GRAPH_EDGES
    
    '''
        Function to form a list representation of the edges in the Web Graph in the form
        [[Node0,Node1,Weight]....] where "Node0" and "Node1" are two pegs with at least 1 connection 
        in its related web diagram and "Weight" is the number of edges between the two pegs in the
        associated Web Diagram. 
    '''
    def form_graph_edges(self):
        edges_between_pegs_list = []
        #for every edge in the original web diagram
        for edge in self.WEB_DIAGRAM:
            #append an initialised 3-tuple which consists of the two pegs
            #with a edge between them and a 0. 
            edges_between_pegs_list.append([edge[0],edge[1], 0])
        #for every one of these peg pairs in the edges_between_pegs_list
        for node_pair in edges_between_pegs_list:
            #create a copy of the original list 
            other_edge_list = []
            other_edge_list = copy.copy(edges_between_pegs_list)
            #remove the node_pair in focus to prevent it from being compared against itself
            other_edge_list.remove(node_pair)
            #for every other pair in the list 
            for other_node_pair in other_edge_list:
                #check that there isn't any duplicates in the edges_between_pegs_list 
                #if there is, remove them from the list
                if (node_pair[0] == other_node_pair[0] and node_pair[1] == other_node_pair[1]):
                    edges_between_pegs_list.remove(other_node_pair)
                if (node_pair[0] == other_node_pair[1] and node_pair[1] == other_node_pair[0]):
                    edges_between_pegs_list.remove(other_node_pair)
        weighted_edge_list = []
        #once all the duplicates have been removed
        for node_pair in edges_between_pegs_list:
            #use the get_edge_weight_function to calculate the weight of each edge in the list 
            weighted_edge_list.append(self.get_edge_weight(node_pair))   
        #return the completed list
        return weighted_edge_list
        
    '''
        Function to calculate the number of edges between a peg and return that weight
        in the form [Edge1, Edge2, Weight].
    '''
    def get_edge_weight(self, connection):
        for edge in self.WEB_DIAGRAM:
            if (edge[0] == connection[0]) and (edge[1] == connection[1]):
                connection = [connection[0],connection[1],connection[2]+1]
            if (edge[0] == connection[1]) and (edge[1] == connection[0]):
                connection = [connection[0],connection[1],connection[2]+1]
        return connection
    
    '''
        Function to get a list of edges in the Web Graph
    '''
    def form_edge_list(self):
        edge_list = []
        for edge in self.WEIGTED_GRAPH_EDGES:
            edge_list.append([edge[0],edge[1]])
        return edge_list