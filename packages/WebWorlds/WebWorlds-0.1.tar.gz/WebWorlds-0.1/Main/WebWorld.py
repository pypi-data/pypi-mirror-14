'''
Created on Jan 12, 2016

@author: Callum McCulloch
@project: Web Worlds Project
@class: Web World Class

The set of all possible web diagrams that can be obtained from a web diagram. 
This is called a the Web World of the Diagram.
'''
from WebDiagram import WebDiagram
from CompareDiagrams import compare_diagrams
import itertools
import copy

class WebWorld:
    
    def __init__ (self,web_diagram):
        #This is the Basis Web Diagram the Web World is formed around
        self.ORIGINAL_WEB_DIAGRAM = web_diagram
        self.PERMUTATION_PEG_DICTIONARY = self.form_height_list_permutations()
        self.WEB_WORLD = self.form_web_world()
    '''
        Function to return the original Web Diagram the Web World is formed from.
    '''
    def get_original_diagram(self):
        return self.ORIGINAL_WEB_DIAGRAM
    '''
        Function to return a list of the Web Diagram Objects that form the Web World of
        the original Web World Diagram
    '''
    def get_web_world(self):
        return self.WEB_WORLD
    '''
        Function to form and return a list of all the web diagrams in the web world 
        as a list of vertext lists. 
    '''
    def get_web_world_list(self):
        web_world_list = []
        for web_diagram in self.WEB_WORLD:
            web_world_list.append(web_diagram.get_web_diagram())
        return web_world_list
    '''
        Function to form the Web World of the original diagram. 
    '''
    def form_web_world(self): 
        '''
            Helper function for the form_web_world function to remove duplicate Web diagrams 
            from the Web_World formed from the set of permutations.
        '''      
        def remove_duplicates(web_world):
            #copies the web_world list to a new list to return at the end
            unique_web_world = copy.copy(web_world)
            #loops through the unique web world list
            for focused_diagram in unique_web_world:
                #removes the focused diagram to ensure its not compared against itself.
                web_world.remove(focused_diagram)
                for diagram in web_world:
                    #if the compare_diagrams function returns an empty list 
                    if(compare_diagrams(focused_diagram, diagram) == []):
                        #then remove the diagram from the unique_web_world list 
                        unique_web_world.remove(diagram)
                #put the focused_diagram back into the web_world list
                web_world.append(focused_diagram)
            #returns a unique web world with no duplicate web diagrams
            return unique_web_world    
        #create an empty list container for all the web diagrams in the web world 
        web_world = []
        #get the original web diagram in the form of a list of vertices 
        diagram = self.get_original_diagram().get_web_diagram()
        #add the original diagram to the web world as this is also a member
        web_world.append(self.get_original_diagram())
        #get the peg list of the original web diagram 
        peg_list = self.ORIGINAL_WEB_DIAGRAM.get_peg_set()
        #get the permutation peg list 
        permutations = self.PERMUTATION_PEG_DICTIONARY
        #set up an iterative variable i
        i = 0
        #using a while loop and "i" to form the new diagram from the list of permutations
        while i < len(permutations):
            #pop a permutation of the original from the permutation list
            permutation = permutations.pop(0)
            #form a new web diagram in the form of a list of vertices using the
            #form_web_diagram() function of the web world class 
            new_diagram = list(self.form_web_diagram(permutation, diagram, peg_list))
            #create a new WebDiagram object from the new_diagram list
            diagram_permutation = WebDiagram(new_diagram)
            #add the WebDiagram object to the web_world list 
            web_world.append(diagram_permutation)
        #remove duplicate web worlds using the remove_duplicates function 
        web_world = remove_duplicates(web_world)
        #return the web_world with all unique entries in the list 
        return web_world
    
    '''
        Takes a permutation of the peg heights, the original diagram and the list of pegs and returns 
        the new diagram formed from the given permutation.
    '''
    def form_web_diagram(self, permutation, diagram, peg_list):
        new_diagram = []
        i = 0 
        #make a list for the permutation inputed
        permutation_list = list(permutation) 
        #make a copy of the diagram inputed
        original_diagram = copy.copy(diagram)
        #while the diagram has edges left in it
        while i < len(original_diagram):
            #remove the first edge
            edge = original_diagram.pop(0)
            #get the permutation for that edge by looking it up on the permutation list
            peg_1_permutation = permutation_list[peg_list[edge[0]-1]-1]
            #do the same for the 2nd peg
            peg_2_permutation = permutation_list[peg_list[edge[1]-1]-1]
            #make a new edge on the 2 pegs using an element from the permutation list
            new_diagram.append([edge[0], edge[1], peg_1_permutation[0], peg_2_permutation[0]]) 
            #remove the permutation elements from the permutation lists   
            replacement_1  = list(permutation_list[edge[0]-1])
            replacement_2 = list(permutation_list[edge[1]-1])
            replacement_1.pop(0)
            replacement_2.pop(0)
            permutation_list[edge[0]-1] = replacement_1
            permutation_list[edge[1]-1] = replacement_2
        #return the created diagram  
        return(new_diagram)
    
    '''
        Creates a list of all the permutations of every list taken from the 
        get_peg_height_permutations() function.
    '''
    def form_height_list_permutations(self):
        permutation_dictionary = dict({})
        peg_heights = self.ORIGINAL_WEB_DIAGRAM.get_peg_heights_list()
        for key in peg_heights:
            permutation_dictionary[key] = self.get_peg_height_permutations(peg_heights.get(key))
        return list(itertools.product(*list(permutation_dictionary.values())))
    
    '''
        Returns a list from [1,2..peg_height]. 
    '''
    def get_peg_height_permutations(self, peg_height):
        i = 1 
        permutation_list = []
        while i <= peg_height:
            permutation_list.append(i)
            i += 1
        permutation_set = list(itertools.permutations(permutation_list))
        for permutation in permutation_set:
            permutation_set[permutation_set.index(permutation)] = list(permutation)
        return permutation_set
        
        
        
            
            