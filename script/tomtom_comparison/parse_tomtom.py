#!/usr/bin/python

import sys
import os
import argparse
import os.path

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Parse TOMTOM scores")
    parser.add_argument('-t', '--tomtom_data', dest='tomtom_data', help='input TOMTOM output')
    parser.add_argument('-m', '--gene_name', dest='gene_name', help='gene name')
    parser.add_argument('-o', '--output_file', dest='output_file', type=str, default='scores_tomtom')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    if os.path.isfile(parsed.tomtom_data):
        # parse tomtom scores
        matched = False
        pValList = []
        eValList = []
        qValList = []
        tomtomLines = open(parsed.tomtom_data,"r").readlines()
        for line in tomtomLines:
            if not line.startswith("#"):
                lineSplit = line.split()
                if parsed.gene_name.lower() == lineSplit[1].strip().lower():
                    pValList.append(float(lineSplit[3]))
                    eValList.append(float(lineSplit[4]))
                    qValList.append(float(lineSplit[5]))
                    matched = True

        # write scores to output file
        if matched:
            eValMin = min(enumerate(eValList),key=lambda x: x[1])
            minIndex = eValMin[0]
            eVal = eValMin[1]
            pVal = pValList[minIndex]
            qVal = qValList[minIndex]
            writer = open(parsed.output_file, "w")
            writer.write("%s\t %s\t %s" % (pVal, eVal, qVal))
            writer.close()

if __name__ == "__main__":
    main(sys.argv)
