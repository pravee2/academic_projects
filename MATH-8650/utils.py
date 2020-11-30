"""Utilities required to preprocess the data."""

import logging
import math
import random

logger = logging.getLogger(__name__)


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
    subset_1 = []
    subset_2 = []
    if isinstance(feature_val, (float, int)):
        for data_row in arr:
            if data_row[feature_index] == '?':
                subset_1.append(data_row)
            else:
                if data_row[feature_index] >= feature_val:
                    subset_1.append(data_row)
                else:
                    subset_2.append(data_row)
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
        if data_points[len(data_points) - 1] not in label_count:
            label_count[data_points[len(data_points) - 1]]=0
        label_count[data_points[len(data_points) - 1]] += 1
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
    entropy_val = 0
    p_val = 0.0
    for label in list(label_count.keys()):
        p_val = float(label_count[label]) / float(len(arr))
        entropy_val -= p_val * math.log(p_val, 2)
    return entropy_val


def data_extract(data, numsplits, seed=42):
    '''This function creates random splits of the data into smaller subsets.
    Input:
        data: data list to be split
        numsplits: number of splits to be divided

    Output:
        data_append: list of sub-lists of data
    '''
    data_out = []
    arraysize = len(data)
    index = [i for i in range(0, arraysize)]
    random.seed(seed)
    random.shuffle(index)
    num_points_persplit = int(math.ceil(float(arraysize)/float(numsplits)))

    for i in range(numsplits):
        dataappend = []
        lower = i*num_points_persplit
        upper = min(lower+num_points_persplit,arraysize)
        for j in range(lower,upper):
            dataappend.append(data[index[j]])
        data_out.append(dataappend)

    return data_out


def evaluate(test_points, forest, testdata):
    """Get classsification metrics."""
    # Testing random forest created on test data points
    tpcount = 0  # true positive
    tncount = 0  # true negative
    fpcount = 0  # false positive
    fncount = 0  # false negative
    for idx, data_point in enumerate(test_points):
        out = forest.classifyforest(data_point)
        if out == testdata[idx][len(testdata[idx])-1]:
            if out == '+':
                tpcount += 1
            else:
                tncount += 1
        else:
            if out == '+':
                fpcount += 1
            else:
                fncount += 1

    logger.debug('Displaying first 40 outputs:')
    for i in range(40):
        out = forest.classifyforest(test_points[i])
        logger.debug("Forest Output: {} Actual Output: {}".format(
            out,
            testdata[i][len(testdata[i]) - 1])
        )

    print("Performance Metrics of the Random Forest:")
    print('accuracy: {:0.4f}'.format(
        float(tpcount + tncount) / float(len(test_points))))
    print('recall: {:0.4f}'.format(float(tpcount) / float(tpcount + fncount)))
    print('precison: {:0.4f}'.format(
        float(tpcount) / float(tpcount + fpcount)))
