"""This python script contain a method PrintData to print the hierarchy data structures
from the list of nth level"""

"""PrintData can be used to print data of a list which contains complex data"""
"""lstData is a argument for the method and its of type list"""
def PrintData(lstData):
    for data in lstData:
        if(isinstance(data,list)):
            PrintData(data)
        else:    
            print(data)
