'''
Created on Jan 12, 2016

@author: Callum McCulloch
@project: Web Worlds Project 
@module: main.py

The main module in the system used to intialise the system

'''
from WebWorldCalculations import WebWorldCalculations
import sys
import matplotlib.pyplot
from datetime import datetime
from WebGraphDrawer import WebGraphDrawer
import glob, os

One = [[1,2,1,3],[1,2,2,1],[2,3,2,1]]
Two = [[1,2,1,1],[2,3,2,2],[3,4,1,1]]
Three = [[1,2,1,1],[1,2,2,3],[1,2,3,4],[2,1,5,4]]
Four = [[1,2,1,1],[1,2,2,2],[1,2,3,3],[1,2,4,4],[2,3,5,1]]

def run_calculations(diagram_data):     
        while(True):
            save_to_file = raw_input("Save results to File? (y/n) \n")
            if(str(save_to_file) == "y"):
                save  = True
                break
            if(str(save_to_file) == "n"):
                save = False
                break
            else:
                print "Please input either y/n \n"
    
        if(save == True):
            while(True):
                got_save_name = False
                overwrite = False
                new_name = False
                no = False
                save_name = raw_input("Please enter a file name for save results \n")
                if(save_name != " " ):
                    os.chdir(os.getcwd())
                    for file_name in glob.glob("*.txt"):
                        if (str(file_name) == str(save_name) +".txt"):
                            while(overwrite == False):
                                over_write = raw_input(str(file_name) + " already exists. Overwrite? (y/n) \n")
                                if(str(over_write) == "y"):
                                    os.remove(os.getcwd() + "/"+ save_name + ".png")
                                    got_save_name = True
                                    overwrite = True
                                if(str(over_write) == "n"):
                                    overwrite = True
                                    no = True
                                else:
                                    print "Please input either y/n \n"
                    if(got_save_name == False and no == False):
                        new_name = True
                if(got_save_name == True or new_name == True):
                    break
        elif(save == False):
            save_name = "NA"    
        
        print "Calculating..."
        results = WebWorldCalculations(diagram_data, save, save_name)
        
        print "============================================="
        print "WEB WORLD i.e. W(D1)"
        i = 1
        for web_diagram in results.WEB_WORLD_LIST:
            print "\nD" + str(i) + ": " + str(web_diagram)
            i += 1
        row_num = 0
        print "\n============================================="
        print "WEB COLOURING AND MIXING MATRICES"
        print "Note: Position in Matrix: [Row,Column] \n      Web Colouring Matrix Entry: WC \n      Web Mixing Matrix Entry: WM"
        for row in results.get_web_colouring_matrix():
            col = 0
            for column in row:
                print "\n[D" + str(row_num + 1) + ", D" + str(col + 1) + "] - (WC = " + str(column) + ") (WM = " + str(results.WEB_MIXING_MATRIX[row_num][col]) + ")"
                col += 1
            print "\n"
            row_num += 1
        print "============================================="
        print "WEB COLOURING MATRIX TRACE: " + str(results.get_web_colouring_matrix_trace())
        print "\nALL WEB COLOURING ROW SUMS EQUAL " + str(results.get_correct_web_colouring_row_sum()) + ": " + str(results.COLOURING_ROW_SUMS_CHECKER)
        print "\n============================================="
        print "WEB MIXING MATRIX TRACE: " +  str(results.get_web_mixing_matrix_trace())
        print "\nALL WEB MIXING ROW SUMS EQUAL 0: " + str(results.get_mixing_matrix_row_sums_checker())
        print "\n============================================="
        print "Program Running Time (Hour:Minutes:Seconds:Milliseconds)"
        print results.get_time_to_calculate()
        if(save_name != "NA"):
            print "\nResults Saved to: "+ os.getcwd() + "/" + save_name +".txt"
            print "=============================================\n"
        else:
            print "=============================================\n"

while True:
    print "============================================="
    user_input = input("Example Input: [[1,2,1,3],[1,2,2,1],[2,3,2,1]] \n"
            + "Pre-made Diagrams: \n1: [[1,2,1,3],[1,2,2,1],[2,3,2,1]]"
             +" \n2: [[1,2,1,1],[2,3,2,2],[3,4,1,1]] \n3: [[1,2,1,1],[1,2,2,3],[1,2,3,4],[2,1,5,4]]"
                + " \n4: [[1,2,1,1],[1,2,2,2],[1,2,3,3],[1,2,4,4],[2,3,5,1]]\n"
                    + "\n5: For text files of diagram results \n"
                     +  "=============================================\n")
    
    if(user_input == 0):
        sys.exit()
    elif (user_input == 1):
        run_calculations(One)
    elif (user_input == 2):
        run_calculations(Two)
    elif (user_input == 3):
        run_calculations(Three)
    elif (user_input == 4):
        run_calculations(Four)
    elif(user_input == 5):
        print "============================================="
        print "SAVED RESULTS \n"
        os.chdir(str(os.getcwd()))
        for file_name in glob.glob("*.txt"):
            print str(file_name) + ""
        print "\n"
        while True:
            got_file = False
            while got_file == False:
                user_input = raw_input("Type file name to open or b to return to main menu\n")
                for file_name in glob.glob("*.txt"):
                    if (str(file_name) == user_input):
                        file  = open (user_input)
                        file_contents = file.read()
                        print file_contents
                        file.close()
                        got_file = True
                        break
                if(str(user_input) == "b" ):
                    got_file = True
                elif(got_file == False):   
                    print "Error: File Doesn't Exist \n"
                    for file_name in glob.glob("*.txt"):
                        print str(file_name)
                    print "\n"
            break
                     
    else:
        run_calculations(user_input)  
    
    
    

    

