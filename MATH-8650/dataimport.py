'''
Name: Varun Praveen, Ravi Prakash Kandury
Email: pravee2,rkandur@g.clemson.edu

This code was written as part of the final project for MATH 8650
at Clemson University. The program contains functions to
handle/pre-process data for the Random Forest Application

fileio():
    This function reads a text file/ csv file and converts
    the dataset into a list of feature vector. Each feature
    vector is also considered as list of features. Thus,
    the function outputs a list of lists.

isfloat(x):
    This function checks if variable x is a float or
    not and returns either True / False
'''


import csv


def isfloat(value):
    """Check if a value is float or not."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def fileio(filepath):
    """Read the data file and parse the tables."""
    aepdata = []
    with open(filepath, 'r') as aepfile:
        reader = csv.reader(aepfile, delimiter=',')
        for row in reader:
            curr = []
            for elem in row:
                if isfloat(elem):
                    curr.append(float(elem))
                else:
                    curr.append(elem)
            aepdata.append(curr)
    return aepdata
