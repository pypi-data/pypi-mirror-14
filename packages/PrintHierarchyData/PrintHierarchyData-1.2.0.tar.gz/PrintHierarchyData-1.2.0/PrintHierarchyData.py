"""This python script contain a method PrintData to print the hierarchy data structures
from the list of nth level"""

"""PrintData can be used to print data of a list which contains complex data"""
"""lstData is a argument for the method and its of type list"""
"""level is a argument to find the level"""
def PrintData(lstData,level=0):
    for data in lstData:
        if(isinstance(data,list)):
            PrintData(data,level + 1)
        else:
            for lvl in range(level):
                print "\t",
            print(data)
