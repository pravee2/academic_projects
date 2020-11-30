"""Random Forest for categorical data."""

import os

from decision_tree import DecisionTree
from utils import data_extract


class RandomForest:
    """Implementation of a random forest."""

    def __init__(self, numtree=10):
        """Initialize a random forest."""
        self.numtree = numtree      # number of trees to be created
        self.treeheads = []         # list of head nodes corresponding to each tree

    def build_forest(self, data_array, output_path="output", seed=42):
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
        split_data = data_extract(data_array, self.numtree, seed=seed)

        for i in range(self.numtree):
            tree_node = DecisionTree()
            tree_node.build_tree(split_data[i])
            tree_node.drawtree(
                jpeg=os.path.join(output_path, "tree_{0}.png".format(i))
            )
            self.treeheads.append(tree_node)
            print("Built tree", i, end=' ')
            print("Width: ", tree_node.width(), end=' ')
            print("Depth: ", tree_node.depth())

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
        labels = {}
        for i in range(self.numtree):
            class_label = list(
                self.treeheads[i].classifytree(data_point).keys())
            # for debugging
            # print('tree Out of :{}, {}'.format(i, class_label))
            if class_label[0] not in list(labels.keys()):
                labels[class_label[0]] = 0
            labels[class_label[0]] += 1
        # assigning correct class output
        maxval = max(labels.values())
        for key, values in labels.items():
            if values == maxval:
                result = key
        return result
