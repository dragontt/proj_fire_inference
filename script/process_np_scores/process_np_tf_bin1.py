#!/usr/bin/python

import sys
import os
import argparse
import operator

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Discretize continuous NetProphet scores into specific number of equal-sized bins.")
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

    # do binning on the sorted list
    item_per_bin = (num_targets+parsed.num_bin)/parsed.num_bin
    list_target_sorted = []
    for i in range(parsed.num_bin-1):
        for j in range(item_per_bin):
            list_target_sorted.append((dict_target_sorted[i*item_per_bin+j][0], i))
    for j in range((parsed.num_bin-1)*item_per_bin, num_targets):
        list_target_sorted.append((dict_target_sorted[j][0], parsed.num_bin-1))

    # write discrete tf-target scores to output file
    writer = open(parsed.output_file, "w")
    writer.write("target\tscore\n")
    for i in range(num_targets):
        writer.write("%s\t%d\n" % (list_target_sorted[i][0], list_target_sorted[i][1]))
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
