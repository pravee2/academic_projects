'''
Name: Varun Praveen, Ravi Prakash Kandury
Email: pravee2,rkandur@g.clemson.edu

This code was written as part of the final project for MATH 8650 at Clemson University. The program contains functions to handle/pre-process data for the Random Forest Application

fileio(): 
	This function reads a text file/ csv file and converts the dataset into a list of feature vector. Each feature vector is also considered as list of features. Thus, the function outputs a list of lists.

isfloat(x):
	This function checks if variable x is a float or not and returns either True / False
'''




import numpy as np
import matplotlib.pyplot as plt
import csv
import os



def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False
	
def fileio(filepath):
	aepdata = []
	with open(filepath, 'rb') as aepfile:
		reader = csv.reader(aepfile, delimiter=',')
		for row in reader:
			curr = []
			for i in range(len(row)):
				if isfloat(row[i]):
					curr.append(float(row[i]))
				else:
					curr.append(row[i])
			aepdata.append(curr)
	aepfile.closed
	return aepdata


