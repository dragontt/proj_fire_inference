#!/usr/bin/python

import sys
import os
import argparse
import operator

def parse_args(argv):
    parser = argparse.ArgumentParser(description=
        "Discretize continuous NetProphet scores into specific number of equal-value-range bins, along with a bin of all zeros.")
    parser.add_argument('tf_np_score', metavar='tf_np_score', help='the continuous np tf-target scores')
    parser.add_argument('-n', '--num_bin', dest='num_bin', type=int, default=50, help='Number of bins')
    parser.add_argument('-o', '--output_file', dest='output_file', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    # parse scores and put (target: score) in dictionary
    dict_target = {}
    num_targets = 0
    lines = open(parsed.tf_np_score).readlines()
    for i, line in enumerate(lines):
        if i > 0 and line.strip():
            line_split = line.split();
            dict_target[line_split[0]] = float(line_split[1])
            num_targets += 1
    # sort dictionary based on score
    dict_target_sorted = sorted(dict_target.iteritems(), key=operator.itemgetter(1))
    dict_target_sorted.reverse()

    # get score intervals
    max_score = dict_target_sorted[0][1]
    min_score = dict_target_sorted[len(dict_target_sorted)-1][1]
    interval_score = (max_score-min_score)/(parsed.num_bin-1)
    
    list_target_sorted = []
    # do binning on non-zero scores
    i = 0
    j = 0
    while i < len(dict_target_sorted):
        if round(dict_target_sorted[i][1],15) >= round((max_score-interval_score*(j+1)),15):
            if dict_target_sorted[i][1] != 0:
                list_target_sorted.append((dict_target_sorted[i][0], j, dict_target_sorted[i][1]))
            i += 1
        else:   j += 1
    # do binning on zero scores
    for i in range(len(dict_target_sorted)):
        if dict_target_sorted[i][1] == 0:
            list_target_sorted.append((dict_target_sorted[i][0], parsed.num_bin-1, dict_target_sorted[i][1]))

    # write discrete tf-target scores to output file
    writer = open(parsed.output_file, "w")
    writer.write("target\tscore\n")
    for i in range(num_targets):
        writer.write("%s\t%d\n" % (list_target_sorted[i][0], list_target_sorted[i][1]))
        # writer.write("%s\t%d\t%.15f\n" % (list_target_sorted[i][0], list_target_sorted[i][1], list_target_sorted[i][2]))
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
