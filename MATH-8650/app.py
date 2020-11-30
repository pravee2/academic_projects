"""Classification using a random forest."""

import argparse
import logging
import os
import sys
import time
import unittest

from dataimport import fileio
from decision_tree import DecisionTree
from decision_tree import TestDecisionTree
from random_forest import RandomForest
from utils import evaluate

logger = logging.getLogger(__name__)

pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


def parse_command_line_args(cl_args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="Random Forest Classifier",
        description="Simple program to classify categorical data"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="output",
        help="Path to the outputs"
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default=None,
        required=True,
        help="Path to the input data"
    )
    parser.add_argument(
        "--test_path",
        type=str,
        default=None,
        required=True,
        help="Path to the test data"
    )
    parser.add_argument(
        "--num_trees",
        type=int,
        default=5,
        help="Number of trees in the Random Forests."
    )
    parser.add_argument(
        "--random_seed",
        type=int,
        default=42,
        help="Random seed for the shuffler etc."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Flag to set verbose logger."
    )
    parser.add_argument(
        "--run_tests",
        action="store_true",
        default=False,
        help="Flag to set run unit test."
    )
    return vars(parser.parse_args(cl_args))


def main(cl_args=sys.argv[1:]):
    """Main wrapper to run the classification app."""
    args = parse_command_line_args(cl_args=cl_args)
    datafile = os.path.realpath(args["data_path"])
    testfile = os.path.realpath(args["test_path"])
    output_root = os.path.realpath(args["output_path"])
    random_seed = args["random_seed"]
    info_level = "INFO"
    if args["verbose"]:
        info_level = "DEBUG"
    # Configure the logger.
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                        level=info_level)
    num_trees = args["num_trees"]
    if not os.path.exists(output_root):
        os.makedirs(output_root)

    # annotated training data
    data = fileio(datafile)
    # annotated test data
    testdata=fileio(testfile)

    # Invoking unit test for decision tree
    if args["run_tests"]:
        logger.info("Invoking test case for decision trees")
        suite = unittest.TestLoader().loadTestsFromTestCase(TestDecisionTree)
        unittest.TextTestRunner().run(suite)
        sys.exit()

    # Creating a set of test points from test data
    test_points=[]
    for line in testdata:
        test_points.append(line[0:len(line)-1])

    # Single decision tree for entire credit approval dataset
    tree_credit = DecisionTree()
    logger.info('Commencing single Decision Tree for credit approval data')
    start_time = time.time()
    tree_credit.build_tree(data)
    end_time = time.time()
    logger.info('time_lapsed: {:0.4f}'.format(end_time - start_time))
    tree_credit.drawtree(jpeg=os.path.join(output_root, 'singletree.png'))

    # Random forest of decision trees for the credit approval dataset
    logger.info('Commencing single Random Forest for credit approval data')
    forest = RandomForest(num_trees)
    start_time = time.time()
    forest.build_forest(data, output_path=output_root, seed=random_seed)
    end_time = time.time()
    logger.info('Time to build forest: {:0.4f}'.format(end_time - start_time))

    evaluate(test_points, forest, testdata)


if __name__ == "__main__":
    main()
