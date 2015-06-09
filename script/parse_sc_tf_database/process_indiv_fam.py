#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Filter all TFs in individual dbd family.")
    parser.add_argument('sc_tf_ass', metavar='sc_tf_ass', help='sgd database')
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, default=None)
    parser.add_argument('-f', '--fam_name', dest='fam_name', type=str, default=None)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)
    assert parsed.fam_name != None, 'Need to specify individual dbd family'

    tf_list = []
    lines = open(parsed.sc_tf_ass, "r").readlines()
    for line in lines:
        if not line.startswith("#"):
            line_split = line.split()
            if line_split[3].strip() == parsed.fam_name:
                tf_list.append(line_split[1])
    tf_list = sorted(set(tf_list))

    writer = open(parsed.out_dir, "w")
    for item in tf_list:
        writer.write("%s\n" % item)
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
