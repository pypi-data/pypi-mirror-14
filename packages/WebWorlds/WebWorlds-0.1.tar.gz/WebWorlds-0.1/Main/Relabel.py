'''
Created on Feb 15, 2016

@author: Callum McCulloch
@project: Web Worlds Project
'''
'''
    Function to relabel every edge height on every peg
    so that the heights on every peg are of the structure 
    [1,2,....,X] for some X and for all pegs in the diagram. 
    The resulting web diagram is described as a sub web diagram of
    the original web diagram.
'''
def relabel(web_diagram_list, peg_set):
    '''
        Small helper function that returns the the sort key from an edge
        of a diagram. Used to determine the order of heights on a peg.
    '''
    def get_sort_key(edge, peg):      
        sort_key = 0 
        if(peg == edge[0]):
            sort_key = edge[2]
        if(peg == edge[1]):
            sort_key = edge[3]         
        return sort_key
    '''
        Helper function to reorder the list of edges on each peg so that they are ordered
        from lowest to highest.
    '''
    def reorder(peg):
        edges_containing_peg = []   
        #for every edge in the Web Diagram 
        for edge in web_diagram_list:
            #if the peg is an end point of the edge
            if (edge[0] == peg) or (edge[1] == peg):
                #add it to the list
                edges_containing_peg.append(edge) 
        #if the list isn't empty
        if (len(edges_containing_peg) != 0):
            i = 0
            ordered_list = []
            #sets the lowest edge to be the first in the  list
            lowest = edges_containing_peg[0]
            #while the list isn't empty
            while len(edges_containing_peg) > 0:
                #use the function above to determine which peg is being looked at
                if get_sort_key(edges_containing_peg[i],peg) < get_sort_key(lowest, peg):
                    #if the edges peg is lower set it to the lowest
                    lowest = edges_containing_peg[i]
                i += 1
                #if the end of the list is reached
                if i == len(edges_containing_peg):
                    #add the lowest to the ordered list
                    ordered_list.append(lowest)
                    edges_containing_peg.remove(lowest)
                    if edges_containing_peg:
                        lowest = edges_containing_peg[0]
                    i = 0
        return ordered_list
    #Form a list of all the edges in the sub web diagram
    relabelled_web_diagram_edges = web_diagram_list
    #Loops through the peg set and for each peg 
    for peg in peg_set:
        #reorder the list of edges associated with it using the already defined reorder function.
        reordered_list = reorder(peg)
        #For every edge in the reorderedList
        for edge in reordered_list:
            #Check which is the peg is being altered and then create a re-labelled edge
            #based on the old edge position in the reordered list defined earlier.
            if edge[0] == peg:
                relabelled_edge = [edge[0], edge[1], reordered_list.index(edge)+1, edge[3]]
            if edge[1] == peg:
                relabelled_edge = [edge[0], edge[1],edge[2],reordered_list.index(edge)+1]
            for old_edge in relabelled_web_diagram_edges:
                #Find the old edge in the re-labelled diagram and replace it with the new 
                #re-labelled edge defined earlier.
                if old_edge == edge:
                    relabelled_web_diagram_edges[relabelled_web_diagram_edges.index(old_edge)] = relabelled_edge  
    #return the finished re-labelled web diagram
    return relabelled_web_diagram_edges
        