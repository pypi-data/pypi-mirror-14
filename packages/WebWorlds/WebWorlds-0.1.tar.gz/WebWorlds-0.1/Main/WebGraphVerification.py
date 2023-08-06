'''
Created on 26 Mar 2016

@author: callum
'''

from WebGraph import WebGraph
from WebDiagram import WebDiagram
import sys
import matplotlib.pyplot
from datetime import datetime
from WebGraphDrawer import WebGraphDrawer
import glob, os

web_diagram_edges = [[1,2,1,1],[1,7,2,2],[2,4,2,3],[3,4,1,1],[3,6,2,4],[4,6,2,3],[4,6,4,2],[5,6,1,1],[5,7,2,1]]
web_diagram = WebDiagram(web_diagram_edges)
web_graph = WebGraph(web_diagram)
web_graph_drawer = WebGraphDrawer(web_graph)
image_file_name = "/home/callum/WebWorldProject/WebWorldsFinal/SavedFiles/WebGraphVerification.png"
web_graph_drawer.draw_graph().savefig(image_file_name)