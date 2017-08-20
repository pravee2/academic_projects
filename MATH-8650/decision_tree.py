'''
Name: Varun Praveen, Ravi Prakash Kandury
Email: pravee2,rkandur@g.clemson.edu
Course: MATH 8650
Assignment: Final Project

This code was developed as part of the project for MATH 8650 at Clemson University. The project implements a Random Forest 
Classifier which was later used to predict approval of credit card applications based on previously annotated data.

Usage: python decision_tree.py
Note: The python version used in the development of this project was Python 2.7

The file reads in a csv/txt file of data for training and test. The division of training and test datasets is outside the scope
of this code.
The paths to these files may be defined in the main function by defining the following variables.

data_path: path to folder containing train data
test_path: path to folder containing test data
filename: training data file
testfilename: test data file
'''

# importing headers
import math
from dataimport import fileio
import os
import time
from random import shuffle
from PIL import Image, ImageDraw
import unittest


def data_split(arr,feature_index,feature_val):
    '''
    This function splits a dataset into positive examples based on feature_index and 
    Value of feature_val
    
    input: 
    arr: data to be split
    feature_index: column index of the feature
    feature val: ground truth value value of the feature to be compared
    
    Return: 
    subset_1: subset of data points containing features of feature val
    subset_2: complement set
    '''
    
    if type(feature_val)==int or type(feature_val)==float:
        subset_1 = [data_row for data_row in arr if data_row[feature_index] >= feature_val]
        subset_2 = [data_row for data_row in arr if not data_row[feature_index] >= feature_val]
    else:
        subset_1 = [data_row for data_row in arr if data_row[feature_index] == feature_val]
        subset_2 = [data_row for data_row in arr if not data_row[feature_index] == feature_val]
    return subset_1, subset_2

def label_counts(arr):
    '''
    This function gives the number of elements for a given class in a data array.
    The class labels are assumed to be the last column of the dataset
    The functions scans through the last column to see the number of unique elements and
    creates a dictionary entry for that class label / updates the count for the class label
    input: array
    output:
        dictionary:
        key = class_labels
        value = associated count
    '''
    label_count = {}
    for data_points in arr:
        if data_points[len(data_points)-1] not in label_count:
            label_count[data_points[len(data_points)-1]]=0
        label_count[data_points[len(data_points)-1]]+=1
    return label_count
        

def entropy(arr):
    '''
    This function calculates entropy of the dataset arr pre/post splits
    input:
    arr: dataset array
    return:
    entropy
    '''
    label_count = label_counts(arr)
    entropy = 0
    p = 0.0
    for label in label_count.keys():
        p = float(label_count[label])/float(len(arr))
        entropy -= p*math.log(p,2)
    return entropy


def data_extract(data,numsplits):
    '''This function creates random splits of the data into smaller subsets.
    Input:
        data: data list to be split
        numsplits: number of splits to be divided

    Output:
        data_append: list of sub-lists of data
    '''
    data_out = []
    arraysize = len(data)
    index = [i for i in range(0,arraysize)]
    shuffle(index)
    num_points_persplit = int(math.ceil(float(arraysize)/float(numsplits)))

    for i in range(numsplits):
        dataappend = []
        lower = i*num_points_persplit
        upper = min(lower+num_points_persplit,arraysize)
        for j in range(lower,upper):
            dataappend.append(data[index[j]])
        data_out.append(dataappend)

    return data_out




# Decision tree class definition
class decision_tree(object):
    def __init__(self, feature_index=-1,feature_value=None,class_label=None, true=None, false = None):
        self.feature_value = feature_value
        self.class_label = class_label
        self.feature_index = feature_index
        self.true = None
        self.false = None 
        
    def build_tree(self, data):
        '''
        Recursively builds a decision tree for categorical data
        input:
            current tree node object
            data array
        return"
            decision tree: linked list of nodes.'''
        current_entropy = entropy(data)
        feature_count = len(data[0])-1

        ig_global = 0.0
        ig_feature_valpair = None
        ig_setpair = None
        # choosing best feature and its value to split dataset
        for index in range(0, feature_count):
            # creating a set of unique values for a given feature in the dataset
            vals = set()
            for row in data:
                vals.add(row[index])
            # iterating through the unique set of features and calculating information gain
            for values in vals:
                (subset_1, subset_2) = data_split(data, index, values)
                pos = float(len(subset_1))/float(len(data))
                neg = float(len(subset_2))/float(len(data))
                gain = current_entropy - pos*entropy(subset_1) - (neg)*entropy(subset_2)
                # updating feature index, values and data splits for the best information gain
                if gain>ig_global and len(subset_1)>0 and len(subset_2)>0:
                    ig_global = gain
                    ig_feature_valpair = (index, values)
                    ig_setpair = (subset_1,subset_2)
        # ig >0 for impure sets: hence move on to subsets of data
        if ig_global>0.0:
            self.feature_index=ig_feature_valpair[0]
            self.feature_value=ig_feature_valpair[1]
            if not self.true:
                self.true = decision_tree()
                self.true.build_tree(ig_setpair[0])
            if not self.false:
                self.false = decision_tree()
                self.false.build_tree(ig_setpair[1])
        # decision leaf reached and decision label assigned to this leaf    
        else:
            self.class_label = label_counts(data)
            
    def classifytree(self, data_point):
        '''
        Recusively classifies a data point using the decision tree built.
        input: 
            self: head tree node object
            data_point: data point to be classified
        return:
            class label at current leaf node
        '''
        #base case: check if at head node / not
        if self.class_label != None:
            return self.class_label
        feature_interest = data_point[self.feature_index]
        next = None
        # traverse down node
        if type(feature_interest) == int or type(feature_interest)==float:
            if feature_interest >= self.feature_value:
                next = self.true
            else:
                next = self.false
        if type(feature_interest) == str:
            if feature_interest == self.feature_value:
                next = self.true
            else:
                next = self.false
        # recursively classify
        return next.classifytree(data_point)

    def width(self):
        '''
        This function recursively computes the width of the decision tree
        Input: 
            tree head node
        Output: 
            width
        '''
        if self.true==None and self.false == None:
            return 1
        return self.true.width()+self.false.width()

    def depth(self):
        '''
        This function recursively computes the depth of the decision tree
        Input: 
            tree head node
        Output: 
            depth
        '''
        if self.true == None and self.false == None:
            return 0
        return max(self.true.depth(),self.false.depth())+1

    def drawtree(self,jpeg="tree.jpg"):
        '''
        This function draws a decision tree by recursively drawing nodes of 
        the decision tree
        Input: 
            tree head node
        Output: 
            tree
        '''
        w=self.width()*100
        h=self.depth()*100+240
        img=Image.new('RGB',(w,h),(255,255,255))
        draw=ImageDraw.Draw(img)
        self.drawnode(draw,w/2,20)
        #img.show(title="treeNode")
        img.save(jpeg)


    def drawnode(self,draw,x,y):
        '''
        This function draws a single node given an x and y coordinates
        Input:
            current node
        Output:
            draw node
        '''
        if self.class_label==None:
            w1=self.true.width()*50
            w2=self.false.width()*50
            left=x-(w1+w2)/2
            right=x+(w1+w2)/2
            #draw.text((x-20,y-10),str(self.feature_index)+':'+str(self.feature_value),(0,0,0))
            draw.text((x-20,y-10),'{}:{}'.format(self.feature_index,self.feature_value),(0,0,0))
            draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
            draw.line((x,y,right-w2/2,y+100),fill=(0,255,0))
            self.false.drawnode(draw,left+w1/2,y+100)
            self.true.drawnode(draw,right-w2/2,y+100)
        else:
            txt='\n'.join(['%s:%d'%v for v in self.class_label.items()])
            draw.text((x-20,y),txt,(0,0,255))

	


class RandomForest(object):
    def __init__(self, numtree=10):
        self.numtree = numtree      # number of trees to be created
        self.treeheads = []         # list of head nodes corresponding to each tree

    def build_forest(self, data):
        '''
        This function builds a random forest of decision trees
        The data is split into smaller subsets and decision trees are created out 
        of those subsets.
        Input:
            Random forest object
            data: data on which the forest has to be built
        Output:
            List of tree heads, for self.numtree of trees
            '''
        split_data = data_extract(data, self.numtree)

        for i in range(self.numtree):
            treeNode = decision_tree()
            treeNode.build_tree(split_data[i])
            treeNode.drawtree(jpeg=("tree_{0}.png".format(i)))
            self.treeheads.append(treeNode)
            print "Built tree",i,
            print "Width: ", treeNode.width(),
            print "Depth: ", treeNode.depth()


    def classifyforest(self, data_point):
        '''
        A function to classify a single data point using a random forest.
        The data point is passed to every tree and the mode result is taken
        Input:
            Random forest object
            data_point: data point to be classified
        Output:
            class label
        ''' 
        # recursively classify using each tree
        '''
        classList = []
        for i in range(self.numtree):
            classLabel = self.treeheads[i].classifytree(data_point).keys()
            classList.append(classLabel)

        #creating list of labels
        labels = {}
        for i in range(self.numtree):
            if classList[i][0] not in labels.keys():
		labels[classList[i][0]]=0
            labels[classList[i][0]]+=1
        '''
        labels = {}
        for i in range(self.numtree):
            classLabel = self.treeheads[i].classifytree(data_point).keys()
            # for debugging
            # print 'tree Out of :' , i, classLabel
            if classLabel[0] not in labels.keys():
                labels[classLabel[0]] = 0
            labels[classLabel[0]] += 1
        # assigning correct class output
        maxval=max(labels.values())
        for key,values in labels.iteritems():
            if values==maxval:
                result=key
        return result

            
# unit test case code to test Decision Tree
class TestDecisionTree(unittest.TestCase):
    def test_construct(self):
        ''' 
        This functon tests the constructor to initialise the decision tree root node
        '''
        print "Testing constructor for decision tree"
        tree = decision_tree()
        self.assertEqual(tree.feature_index , -1)
        self.assertEqual(tree.feature_value , None)
        self.assertEqual(tree.class_label, None)
        self.assertEqual(tree.true, None)
        self.assertEqual(tree.false, None)

    def test_buildTree(self):
        ''' 
        This function tests the build_tree member function of the decision tree class
        '''
        print "Testing build tree of decision tree"
        my_data=[['slashdot','USA','yes',18,'None'],
             ['google','France','yes',23,'Premium'],
             ['digg','USA','yes',24,'Basic'],
             ['kiwitobes','France','yes',23,'Basic'],
             ['google','UK','no',21,'Premium'],
             ['(direct)','New Zealand','no',12,'None'],
             ['(direct)','UK','no',21,'Basic'],
             ['google','USA','no',24,'Premium'],
             ['slashdot','France','yes',19,'None'],
             ['digg','USA','no',18,'None'],
             ['google','UK','no',18,'None'],
             ['kiwitobes','UK','no',19,'None'],
             ['digg','New Zealand','yes',12,'Basic'],
             ['slashdot','UK','no',21,'None'],
             ['google','UK','yes',18,'Basic'],
             ['kiwitobes','France','yes',19,'Basic']]

        tree = decision_tree()
        tree.build_tree(my_data)
        tree.drawtree(jpeg='checktree.png')
        # checking root node of the tree
        self.assertEqual(tree.feature_value, 'google')
        self.assertEqual(tree.feature_index, 0)
        self.assertEqual(tree.class_label, None)

        # checking false branch of the root node
        self.assertEqual(tree.false.feature_value, 'slashdot')

    def test_classify(self):
        '''
        This function tests the classify function of the decision tree class
        for data points in the training set
        '''
        print "Testing classify of decision tree"
        my_data=[['slashdot','USA','yes',18,'None'],
             ['google','France','yes',23,'Premium'],
             ['digg','USA','yes',24,'Basic'],
             ['kiwitobes','France','yes',23,'Basic'],
             ['google','UK','no',21,'Premium'],
             ['(direct)','New Zealand','no',12,'None'],
             ['(direct)','UK','no',21,'Basic'],
             ['google','USA','no',24,'Premium'],
             ['slashdot','France','yes',19,'None'],
             ['digg','USA','no',18,'None'],
             ['google','UK','no',18,'None'],
             ['kiwitobes','UK','no',19,'None'],
             ['digg','New Zealand','yes',12,'Basic'],
             ['slashdot','UK','no',21,'None'],
             ['google','UK','yes',18,'Basic'],
             ['kiwitobes','France','yes',19,'Basic']]

        tree = decision_tree()
        tree.build_tree(my_data)
        self.assertEqual(tree.classifytree(['(direct)','USA','yes',5]).keys(),['Basic'])
        self.assertEqual(tree.classifytree(['(direct)','USA','no',23]).keys(),['Basic'])
        self.assertEqual(tree.classifytree(['slashdot','USA','yes',18]).keys(), ['None'])


if __name__ == "__main__":

    data_path = 'data'
    test_path = 'data'
    filename = 'data_credit_approval.txt'
    testfilename='test_credit_approval.txt'
    datafile = os.path.join(data_path,filename)    
    testfile=os.path.join(test_path,testfilename)

    # annotated training data
    data = fileio(datafile)
    # annotated test data
    testdata=fileio(testfile)

    # Invoking unit test for decision tree
    print "Invoking test case for decision trees"
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecisionTree)
    unittest.TextTestRunner().run(suite) 

    # Creating a set of test points from test data
    test_points=[]
    for i in range(len(testdata)):
        test_points.append(testdata[i][0:len(testdata[i])-1])

    # Single decision tree for entire credit approval dataset
    tree_credit = decision_tree()
    print 'Commencing single Decision Tree for credit approval data'
    start_time = time.time()
    tree_credit.build_tree(data)
    end_time = time.time()
    print 'time_lapsed', end_time - start_time
    tree_credit.drawtree(jpeg='singletree.png')

    # Random forest of decision trees for the credit approval dataset
    print 'Commencing single Random Forest for credit approval data'
    forest=RandomForest(10)
    start_time = time.time()
    forest.build_forest(data)
    end_time = time.time()
    print 'Time to build forest: ', end_time - start_time

    # Testing random forest created on test data points
    # print test_points
    tpcount = 0 #true positive 
    tncount = 0 #true negative
    fpcount = 0 #false positive
    fncount = 0 #false negative
    for i in range(0,len(test_points)):   
        out=forest.classifyforest(test_points[i])
        if out == testdata[i][len(testdata[i])-1]:
            if out == '+':
                tpcount += 1
            else:
                tncount += 1
        else:
            if out == '+':
                fpcount += 1
            else:
                fncount += 1

    print 'Displaying first 40 outputs:'
    for i in range(40):
        out=forest.classifyforest(test_points[i]) 
        print "Forest Output",out,"Actual Output",testdata[i][len(testdata[i])-1] 

    print "Performance Metrics of the Random Forest:"
    print 'accuracy:', float(tpcount+tncount)/float(len(test_points))
    print 'recall:', float(tpcount)/float(tpcount+fncount)
    print 'precison:', float(tpcount)/float(tpcount+fpcount)
    
  


    
