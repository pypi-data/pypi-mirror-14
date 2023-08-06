'''
Created on Feb 16, 2016

@author: Callum McCulloch
@project: WebWorldsProject

        Helper function to compare two Web Diagrams. Returns an empty list if the Web Diagrams 
        are identical.
'''
import copy
from WebDiagram import WebDiagram


def compare_diagrams(diagram_1, diagram_2):
    #make a copy of the first diagram
    return_diagram = copy.copy(diagram_1.get_web_diagram())
    #nested for loop to compare every edge of both diagrams against each other to see if they are identical. 
    for edge_1 in diagram_1.get_web_diagram():
        for edge_2 in diagram_2.get_web_diagram():
            #Two logical conditions to check if two edges are the same
            if((edge_1[0] == edge_2[0])
                and (edge_1[1] == edge_2[1])
                    and (edge_1[2] == edge_2[2])
                        and (edge_1[3] == edge_2[3])):
                return_diagram.remove(edge_1)
                #break if a same edges are the same
                break
    #returns an empty list if the two diagrams compared are identical
    return return_diagram

