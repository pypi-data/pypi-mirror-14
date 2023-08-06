'''
Created on Jan 12, 2016

@author: Callum McCulloch
@project: WebWorldsProject
@class: WebWorldCalculations


''' 
from WebDiagram import WebDiagram 
from WebWorld import WebWorld
from WebGraph import WebGraph
from WebGraphDrawer import WebGraphDrawer
from CompareDiagrams import compare_diagrams
from sage.all import OrderedSetPartitions, PowerSeriesRing, TestSuite, ZZ, stirling_number2, factorial
import numpy
from fractions import Fraction
from datetime import datetime
import os 

class WebWorldCalculations:
    
    def __init__(self, diagram_data, save, save_name):
        
        #start the timer for calculations
        start = datetime.now() 
        
        #form the three main objects of the systems
        self.ORIGINAL_WEB_DIAGRAM = WebDiagram(diagram_data)
        self.WEB_GRAPH = WebGraph(self.ORIGINAL_WEB_DIAGRAM)
        self.WEB_WORLD = WebWorld(self.ORIGINAL_WEB_DIAGRAM)
        
        
        self.WEB_GRAPH_IMAGE = WebGraphDrawer(self.WEB_GRAPH)
        self.WEB_WORLD_LIST = self.WEB_WORLD.get_web_world_list()
        self.NUM_OF_EDGES = len(self.ORIGINAL_WEB_DIAGRAM.get_web_diagram())
        
        #use the Sage packages Ordered Set Partitions function
        self.ORDERED_SET_PARTITION = OrderedSetPartitions(self.NUM_OF_EDGES).list()
        
        #set the length of the matrix to the number of Web Diagrams in the Web World
        self.MATRIX_LENGTH = len(self.WEB_WORLD_LIST)
        
        #initialise the two matrices with zeros in every entry
        self.WEB_COLOURING_MATRIX = numpy.zeros((self.MATRIX_LENGTH, self.MATRIX_LENGTH),dtype = object)
        self.WEB_MIXING_MATRIX = numpy.zeros((self.MATRIX_LENGTH, self.MATRIX_LENGTH),dtype = object)      
        
        #initialise the web colouring row sums array
        self.WEB_COLOURING_ROW_SUMS = numpy.zeros((self.MATRIX_LENGTH,1), dtype = object)
        
        #begin calculations of the Web Colouring and Web Mixing Matrices
        self.form_matrices()
        #form the row sums for the Web Mixing Matrices 
        #NOTE: the Web Colouring Matrix row sums are calculated while the matrices are formed
        self.form_web_mixing_row_sums_matrix()
        
        #set booleans for the row sums of each matrix
        self.COLOURING_ROW_SUMS_CHECKER = True
        #calculate the expected result of the Web Colouring Matrix row sums
        self.CORRECT_WEB_COLOURING_MATRIX_ROW_SUM = self.correct_web_colouring_row_sum()
        self.MIXING_ROW_SUMS_CHECKER = True
        self.WEB_MIXING_ROW_SUMS = numpy.zeros((self.MATRIX_LENGTH,1), dtype = object)
        self.WEB_MIXING_MATRIX_TRACE = self.form_web_mixing_matrix_trace()
        self.WEB_COLOURING_MATRIX_TRACE = self.form_web_colouring_matrix_trace()
        end = datetime.now() 
        #calculate the total time to completion and store
        self.TIME_TO_CALCULATE = end - start
        
        #if the users has requested the results to be saved then the results are printed to file
        if(save == True):
            self.print_data_to_file(save_name)
    
    '''
        Return the Web World Object
    ''' 
    def get_web_world(self):
        return self.WEB_WORLD
    '''
        Return the Web Graph Object
    '''
    def get_web_graph(self):
        return self.WEB_GRAPH
    
    
    
    
            
    '''
        Returns the length of one side of the Web Colouring and Web Mixing Matrices
    '''
    def get_length_of_matrix(self):
        return self.MATRIX_LENGTH
    '''
        Returns the Web Colouring Matrix of the Web World
    '''
    def get_web_colouring_matrix(self):
        return self.WEB_COLOURING_MATRIX
    '''
        Returns the list of row sums for the Web Colouring Matrix
    '''
    def get_web_colouring_row_sums(self):
        return self.WEB_COLOURING_ROW_SUMS
    '''
        Returns the Web Colouring Matrix Trace
    '''
    def get_web_colouring_matrix_trace(self):
        return self.WEB_COLOURING_MATRIX_TRACE
    '''
        Returns the expected list of row sums for the Web Colouring Matrix
    '''
    def get_correct_web_colouring_row_sum(self):
        return self.CORRECT_WEB_COLOURING_MATRIX_ROW_SUM
    
    
    
    
    '''
        Returns the Web Mixing Matrix of the Web World
    '''
    def get_web_mixing_matrix(self):
        return self.WEB_MIXING_MATRIX
    '''
        Returns the list of row sums for the Web Mixing Matrix
    '''
    def get_web_mixing_row_sums(self):
        return self.WEB_MIXING_ROW_SUMS
    '''
        Returns the Web Colouring Matrix Trace
    '''
    def get_web_mixing_matrix_trace(self):
        return self.WEB_MIXING_MATRIX_TRACE
    '''
        Returns the expected list of row sums for the Web Mixing Matrix
    '''
    def get_mixing_matrix_row_sums_checker(self):
        return self.MIXING_ROW_SUMS_CHECKER
    
    
    
    
    '''
        Return the Web Graph Visual Representation
    '''
    def get_web_graph_image(self):
        return self.WEB_GRAPH_IMAGE
    '''
        Return the time to complete all calculations
    '''
    def get_time_to_calculate(self):
        return self.TIME_TO_CALCULATE
    
    
    
    
    
    '''
        Function that forms the Web Colouring Matrix of the specified Web World 
    '''   
    def form_matrices(self):
        def form_diagram_from_colouring(colouring_list, web_diagram):
            #for every colouring in the the colouring_list
                coloured_diagram_list = []
                added_height = 0
                append = coloured_diagram_list.append           
                for colour in colouring_list:
                    listed_colour = list(colour)
                    #for every index in0 the specified colouring
                    for index in listed_colour: 
                        #add the edge that is at the index specified in the original web diagram 
                        #to the new colouring list order 
                        extra_height_edge = [web_diagram[index-1][0], web_diagram[index-1][1], web_diagram[index-1][2] + added_height
                                                   , web_diagram[index-1][3] + added_height]
                        append(extra_height_edge)
                    added_height += 20
                #create a new web diagram object using list of ordered coloured edges 
                reconstructed_web_diagram = WebDiagram(coloured_diagram_list)               
                #loops through the Web World
                array_size = len(colouring_list)
                power_series_array = [0]*(array_size+1)
                power_series_array[len(power_series_array)-1] = 1            
                for diagram in self.WEB_WORLD.get_web_world(): 
                    #using the compare_diagrams function, checks to see which web diagram 
                    #in the web world has been formed using during the colouring-based reconstruction
                    if(compare_diagrams(diagram, reconstructed_web_diagram) == []):
                        #set the column for the matrix entry, this is the index of the 
                        #matching web diagram in the original web world
                        column = self.WEB_WORLD_LIST.index(diagram.get_web_diagram())
                        #set the row for the matrix entry, this will be the index of the 
                        #web_diagram being reconstructed by a colouring 
                        row = self.WEB_WORLD_LIST.index(web_diagram)
                        #Add on the created power series to the already formed power series 
                        #in the specified slot in the matrix
                        polynomial = self.WEB_COLOURING_MATRIX[row, column] + R(power_series_array)
                        #set the slot in the matrix as the calculated power series 
                        self.WEB_COLOURING_MATRIX[row, column] = polynomial 
                        mixing_entry = self.WEB_MIXING_MATRIX[row, column] + self.calculate_mixing_entry(R(power_series_array)) 
                        self.WEB_MIXING_MATRIX[row, column] = mixing_entry
                        colouring_row_sum = self.WEB_COLOURING_ROW_SUMS[row] + R(power_series_array)
                        self.WEB_COLOURING_ROW_SUMS[row] = colouring_row_sum 
                        break 
        
        #Using the PowerSeriesRing packages from SAGE to form 
        #a power series 
        R = PowerSeriesRing(ZZ, 'x')
        TestSuite(R).run()
        #loop through each diagram in the web world 
        for web_diagram in self.WEB_WORLD_LIST:
            [form_diagram_from_colouring(colouring_list, web_diagram) for colouring_list in self.ORDERED_SET_PARTITION]
    
    '''
        Form each row sum of the Web Mixing Matrix and check for errors
        Note: All row sums should equal 0
    '''
    def form_web_mixing_row_sums_matrix(self):
        self.WEB_MIXING_ROW_SUMS = self.WEB_MIXING_MATRIX.sum(axis = 1)
        for row in self.WEB_MIXING_ROW_SUMS:
            if row != 0:
                #change the global checker if not equal 0
                self.MIXING_ROW_SUMS_CHECKER = False
    
    '''
        Function to calculate each Web Mixing Matrix entry. This function is used within the 
        form_matrices() function. It implements the algorithm for forming the Web Mixing Matric 
        described in the project report.
    '''
    def calculate_mixing_entry(self, equation):
        entry = float(0.0)
        #use the exponents() and coefficients() functions in the SageMath packages 
        #to dismantle a polynomial
        exponents = equation.exponents()
        coefficients = equation.coefficients()
        #create a list of tuples to 
        tuples = zip(exponents, coefficients)
        for tuple in tuples:
            solution_part = 0
            #if the number is even, negate it
            if tuple[0] % 2 == 0:
                solution_part = -(tuple[1])/tuple[0]
            #else it is positive
            else:
                solution_part = tuple[1]/tuple[0]
            entry += solution_part
            #set the result as a fraction
            result = Fraction(entry).limit_denominator(1000)  
        return result
    '''
        Function to calculate and return the main trace of
        the Web Mixing Matrix
    '''
    def form_web_mixing_matrix_trace(self):
        trace = self.WEB_MIXING_MATRIX.trace(offset = 0)
        return trace    
    '''
        Function to calculate and return the main trace of
        the Web Colouring Matrix
    '''
    def form_web_colouring_matrix_trace(self):
        trace = self.WEB_COLOURING_MATRIX.trace(offset = 0)
        return trace
    
    '''
        Function to calculate the expected the correct row colouring 
        sum using the algorithm outlined in the project report
    '''
    def correct_web_colouring_row_sum(self):
        result = 0
        #Use SageMaths function to create a polynomial calculator
        R = PowerSeriesRing(ZZ, 'x')
        TestSuite(R).run()   
        i = 0
        m = self.NUM_OF_EDGES
        n = 1
        while i < self.get_length_of_matrix():
            integer_value = (stirling_number2(m, n, algorithm = None) * factorial(n))
            array_size = i + 2
            power_series_array = [0]*(array_size)
            power_series_array[len(power_series_array)-1] = integer_value 
            result += R(power_series_array)
            i += 1
            n += 1
        
        for row in self.get_web_colouring_row_sums():
            if(row[0] != result):
                self.COLOURING_ROW_SUMS_CHECKER = False
        return result
    
    '''
        Function that prints the data to a text file 
    '''
    def print_data_to_file(self, save_name):
        file_name = os.getcwd() +"/" + str(save_name) + ".txt"
        f = open(file_name, 'w')
        f.write("=============================================")
        f.write("\nWEB WORLD i.e. W(D1)")
        f.write("\n")
        i = 1
        for web_diagram in self.WEB_WORLD_LIST:
            f.write("\nD" + str(i) + ": " + str(web_diagram))
            i += 1
        f.write("\n")
        f.write("\n")
        row_num = 0
        f.write("=============================================")
        f.write("\nWEB COLOURING AND MIXING MATRICES")
        f.write("\n")
        f.write("Note: Position in Matrix: [Row,Column] \n      Web Colouring Matrix Entry: WC \n      Web Mixing Matrix Entry: WM")
        f.write("\n")
        for row in self.get_web_colouring_matrix():
            col = 0
            for column in row:
                f.write("\n[D" + str(row_num + 1) + ", D" + str(col + 1) + "] - (WC = " + str(column) + ") (WM = " + str(self.WEB_MIXING_MATRIX[row_num][col]) + ")")
                col += 1
            f.write("\n")
            row_num += 1
        f.write("\n=============================================")
        f.write("\nWEB COLOURING MATRIX TRACE: " + str(self.get_web_colouring_matrix_trace()))
        f.write("\n")
        f.write("\nALL WEB COLOURING ROW SUMS EQUAL " + str(self.get_correct_web_colouring_row_sum()) + ": " + str(self.COLOURING_ROW_SUMS_CHECKER))
        f.write("\n")
        f.write("\n=============================================")
        f.write("\nWEB MIXING MATRIX TRACE: " +  str(self.get_web_mixing_matrix_trace()))
        f.write("\n")
        f.write("\nALL WEB MIXING ROW SUMS EQUAL 0: " + str(self.get_mixing_matrix_row_sums_checker()))
        f.write("\n")
        f.write("\n=============================================")
        f.write("\nProgram Running Time (Hour:Minutes:Seconds:Milliseconds)")
        f.write("\n" + str(self.get_time_to_calculate()))
        f.write("\n=============================================\n")
        f.close()
        
        image_file_name = os.getcwd() + "/" +str(save_name) + ".png"
        self.WEB_GRAPH_IMAGE.get_drawing().savefig(image_file_name)
        self.WEB_GRAPH_IMAGE.get_drawing().gcf().clear()
        
        
        
        
                    
    