#!/usr/bin/python

import sys
import os
import argparse
import os.path

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Parse FIRE scores")
    parser.add_argument('-f', '--fire_data', dest='fire_data', help='input FIRE summary')
    parser.add_argument('-o', '--output_file', dest='output_file', type=str, default='scores_fire')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    if os.path.isfile(parsed.fire_data):
        # parse fire scores
        fireLine = open(parsed.fire_data,"r").readline()
        fireLine = fireLine.split("/")[0]

        # write scores to output file
        writer = open(parsed.output_file, "w")
        writer.write("%s\t" % fireLine)
        writer.close()

if __name__ == "__main__":
    main(sys.argv)
