'''
Name: Varun Praveen, Ravi Prakash Kandury
Email: pravee2,rkandur@g.clemson.edu
Course: MATH 8650
Assignment: Final Project

This code was developed as part of the project for MATH 
8650 at Clemson University. The project implements a Random
Forest Classifier which was later used to predict approval
of credit card applications based on previously annotated data.

Usage: python decision_tree.py
Note: The python version used in the development of this project
was Python 2.7

The file reads in a csv/txt file of data for training and
test. The division of training and test datasets is outside
the scope of this code.

The paths to these files may be defined in the main function by
defining the following variables.

data_path: path to folder containing train data
test_path: path to folder containing test data
filename: training data file
testfilename: test data file
'''

# importing headers
import logging
import unittest

from PIL import Image, ImageDraw
from utils import data_split, entropy, label_counts

logger = logging.getLogger(__name__)


# Decision tree class definition
class DecisionTree:
    """Implementation of a decision tree."""

    def __init__(
        self,
        feature_index=-1,
        feature_value=None,
        class_label=None,
        true=None,
        false = None):
        self.feature_value = feature_value
        self.class_label = class_label
        self.feature_index = feature_index
        self.true = true
        self.false = false

    def build_tree(self, data_array):
        '''
        Recursively builds a decision tree for categorical data_array
        input:
            current tree node object
            data_array array
        return"
            decision tree: linked list of nodes.
        '''
        current_entropy = entropy(data_array)
        feature_count = len(data_array[0])-1

        ig_global = 0.0
        ig_feature_valpair = None
        ig_setpair = None
        # choosing best feature and its value to split data_arrayset
        for index in range(0, feature_count):
            # creating a set of unique values for a given feature in the data_arrayset
            vals = set()
            for row in data_array:
                vals.add(row[index])
            # iterating through the unique set of features and calculating information gain
            for values in vals:
                (subset_1, subset_2) = data_split(
                    data_array, index, values)
                pos = float(len(subset_1))/float(len(data_array))
                neg = float(len(subset_2))/float(len(data_array))
                gain = current_entropy - pos * \
                    entropy(subset_1) - (neg)*entropy(subset_2)
                # updating feature index, values and data_array splits for the best information gain
                if gain > ig_global and len(subset_1) > 0 and len(subset_2) > 0:
                    ig_global = gain
                    ig_feature_valpair = (index, values)
                    ig_setpair = (subset_1, subset_2)
        # ig >0 for impure sets: hence move on to subsets of data_array
        if ig_global > 0.0:
            self.feature_index = ig_feature_valpair[0]
            self.feature_value = ig_feature_valpair[1]
            if not self.true:
                self.true = DecisionTree()
                self.true.build_tree(ig_setpair[0])
            if not self.false:
                self.false = DecisionTree()
                self.false.build_tree(ig_setpair[1])
        # decision leaf reached and decision label assigned to this leaf
        else:
            self.class_label = label_counts(data_array)

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
        if self.class_label is not None:
            return self.class_label
        feature_interest = data_point[self.feature_index]
        next_node = None
        # traverse down node
        if isinstance(feature_interest, (int, float)):
            if feature_interest == '?' or self.feature_value == "?":
                next_node = self.true
            elif feature_interest >= self.feature_value:
                # logger.debugself.feature_value)
                next_node = self.true
            else:
                next_node = self.false
        if isinstance(feature_interest, str):
            if feature_interest == self.feature_value:
                next_node = self.true
            else:
                next_node = self.false
        # recursively classify
        return next_node.classifytree(data_point)

    def width(self):
        '''
        This function recursively computes the width of the decision tree
        Input: 
            tree head node
        Output: 
            width
        '''
        if self.true is None and self.false is None:
            return 1
        return self.true.width() + self.false.width()

    def depth(self):
        '''
        This function recursively computes the depth of the decision tree
        Input: 
            tree head node
        Output: 
            depth
        '''
        if self.true is None and self.false is None:
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
        w = self.width()*100
        h = self.depth()*100+240
        img = Image.new('RGB',(w,h),(255,255,255))
        draw = ImageDraw.Draw(img)
        self.drawnode(draw, w/2, 20)
        #img.show(title="tree_node")
        img.save(jpeg)

    def drawnode(self, draw, coord_x, coord_y):
        '''
        This function draws a single node given an coord_x and coord_y coordinates

        Input:
            draw: draw object.
            coord_x: x coordinate to draw
            coord_y: y coordinate to draw

        Output:
            draw node
        '''
        if self.class_label is None:
            w_1 = self.true.width() * 50
            w_2 = self.false.width() * 50
            left = coord_x - (w_1 + w_2) / 2
            right = coord_x + (w_1 + w_2) / 2
            #draw.text((x-20,y-10),str(self.feature_index)+':'+str(self.feature_value),(0,0,0))
            draw.text(
                (coord_x - 20, coord_y - 10),
                '{}:{}'.format(
                    self.feature_index,
                    self.feature_value
                ),
                (0, 0, 0)
            )
            draw.line((coord_x, coord_y, left + w_1/2,
                       coord_y + 100), fill=(255, 0, 0))
            draw.line((coord_x, coord_y, right - w_2/2,
                       coord_y + 100), fill=(0, 255, 0))
            self.false.drawnode(draw, left + w_1 / 2, coord_y + 100)
            self.true.drawnode(draw, right - w_2 / 2, coord_y + 100)
        else:
            txt = '\n'.join(
                ['%s:%d' % v for v in list(self.class_label.items())])
            draw.text((coord_x - 20, coord_y), txt, (0, 0, 255))


# unit test case code to test Decision Tree
class TestDecisionTree(unittest.TestCase):
    """Unit test for Testing the decision tree build."""

    def test_construct(self):
        '''
        This functon tests the constructor to initialise the decision tree root node
        '''
        logger.debug("Testing constructor for decision tree")
        tree = DecisionTree()
        self.assertEqual(tree.feature_index , -1)
        self.assertEqual(tree.feature_value , None)
        self.assertEqual(tree.class_label, None)
        self.assertEqual(tree.true, None)
        self.assertEqual(tree.false, None)

    def test_build_tree(self):
        '''
        This function tests the build_tree member function of the decision tree class
        '''
        logger.debug("Testing build tree of decision tree")
        my_data=[
            ['slashdot','USA','yes',18,'None'],
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
            ['kiwitobes','France','yes',19,'Basic']
        ]

        tree = DecisionTree()
        tree.build_tree(my_data)
        if logging.getLevelName(logger.getEffectiveLevel()) == "DEBUG":
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
        logger.debug("Testing classify of decision tree")
        my_data=[
            ['slashdot','USA','yes',18,'None'],
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
            ['kiwitobes','France','yes',19,'Basic']
        ]

        tree = DecisionTree()
        tree.build_tree(my_data)
        self.assertEqual(list(tree.classifytree(['(direct)','USA','yes',5]).keys()),['Basic'])
        self.assertEqual(list(tree.classifytree(['(direct)','USA','no',23]).keys()),['Basic'])
        self.assertEqual(list(tree.classifytree(['slashdot','USA','yes',18]).keys()), ['None'])
