'''
Created on Jan 12, 2016

@author: Callum McCulloch
@project: Web Worlds Project
@class: Web Diagram 

'''
from Relabel import relabel
class WebDiagram:
    
    '''
         Initialises the Web Diagram Object and defines a list of global variables for the Web Diagram Class
    '''
    def __init__ (self,EDGE_LIST):
        self.PEG_SET = self.form_peg_set(EDGE_LIST)
        #when initialised the Web Diagram is relabelled using the relabel function 
        self.WEB_DIAGRAM = relabel(EDGE_LIST, self.PEG_SET)
        self.PEG_HEIGHTS_LIST = self.form_peg_heights_dictionary()
        self.PEG_PAIRS_SET = self.form_peg_pairs_set()
        self.NUM_OF_EDGES_ON_EACH_PEG = self.form_num_of_edges_on_pegs_list()
        
    '''
        Returns the Web Diagram in the form of a list of 4-tuples representing the
        edges between the pegs of the diagram.
    '''
    def get_web_diagram(self):
        return self.WEB_DIAGRAM
        
    '''
        Returns a list representing the set of pegs in the Web Diagram.
    '''
    def get_peg_set(self):
        return self.PEG_SET
        
    '''
        Return a list of tuples that represent pairs of pegs that has at least one edge between them
        between them.
    '''
    def get_peg_pairs_set(self):
        return self.PEG_PAIRS_SET
    
    '''
        Returns a dictionary with the pegs in the Web Diagram as the keys and the number of edges
        on each peg as the values for each key.
    '''
    def get_num_of_edges_on_pegs(self):
        return self.NUM_OF_VERTICES_ON_EACH_PEG
    '''
        Returns a dictionary with the pegs in the Web Diagram as the keys and the maximum height 
        of each peg as the value for the keys.
    '''
    def get_peg_heights_list(self):
        return self.PEG_HEIGHTS_LIST
    
    '''
        Function to set the PEG_SET attribute of the Web diagram class. Used when relabelling 
        web diagrams to ensure the sub web diagram has the "empty" pegs from its parent 
        web diagram.
    '''
    def set_peg_set(self, newPegSet):
            self.PEG_SET = newPegSet
    '''
        Function forms and sets the PegsHeightList for the Diagram.
    '''
    def form_peg_heights_dictionary(self):
        peg_heights = dict ({})
        for peg in self.PEG_SET:
            peg_heights[peg] = 0
        for peg in self.PEG_SET:
            highest = 0
            for edge in self.WEB_DIAGRAM:
                if edge[0] == peg and edge[2] > highest:
                    highest = edge[2]
                if edge[1] == peg and edge[3] > highest:
                    highest = edge[3]
            peg_heights[peg] = highest            
        return peg_heights

    '''
        Function forms and sets the PegSet Variable for the Web Diagram.
    '''
    def form_peg_set(self,edge_list):
        peg_list = []
        for edge in edge_list:
            if edge[0] not in peg_list : 
                peg_list.append(edge[0])
            if edge[1] not in peg_list:
                peg_list.append(edge[1])
        return sorted(peg_list)
    
    '''
        Function forms and sets the PegPairsSet Variable for the Web Diagram.
    '''
    def form_peg_pairs_set(self):
        pair_list = []
        for edge in self.WEB_DIAGRAM:
            peg_pair_1 = [edge[0],edge[1]]
            peg_pair_2 = [edge[1],edge[0]]
            if peg_pair_1 not in pair_list and peg_pair_2 not in pair_list:
                pair_list.insert(len(pair_list), [edge[0],edge[1]])
        return pair_list

    '''
        Function forms and sets the list of the number of edges associated with each 
        peg in the Web Diagram.
    '''    
    def form_num_of_edges_on_pegs_list(self):
        edges_on_each_peg = dict({})
        for peg in self.PEG_SET:
            edges_on_each_peg[peg] = 0
        for peg in self.PEG_SET:
            for edges in self.WEB_DIAGRAM:
                if edges[0] == peg or edges[1] == peg:
                    edges_on_each_peg[peg] = edges_on_each_peg[peg] + 1
        return edges_on_each_peg
        
    '''
        Function to add 2 web diagrams together.
        NOTE: Unused function, though useful for further development of system in the future.
        
    def add_diagram(self, D2):
        combined_peg_set = self.get_peg_set() + D2.get_peg_set()
        combined_peg_set = list(set(combined_peg_set))
        peg_height_set = {key: 0 for key in combined_peg_set}
        updatedD2 = []
        append = updatedD2.append
        for edge in D2.get_web_diagram():
            append([edge[0], edge[1], edge[2] + peg_height_set[edge[0]], edge[3] + peg_height_set[edge[1]]])
        added_diagrams_list = self.get_web_diagram()
        append = added_diagrams_list.append
        for edge in updatedD2:
            append(edge)
        added_web_diagram = WebDiagram(added_diagrams_list)
        return added_web_diagram
    '''  
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        