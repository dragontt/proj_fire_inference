#!/usr/bin/python

import sys
import os
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Convert motif infered from FIRE to MEME format")
    parser.add_argument('motif', metavar='motif', help='Motif infered from FIRE')
    parser.add_argument('-o', '--output_filename', dest='output_fn', type=str, default='motif_meme')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    # write header to output file
    writer = open(parsed.output_fn, "w")
    writer.write("MEME version 4.9.1\n\nALPHABET= ACGT\n\nstrands: + -\n\nBackground letter frequencies\nA 0.3 C 0.2 G 0.2 T 0.3\n")

    # parse string by character
    charList = [];
    charMotif = list(parsed.motif)
    i = 0
    while i < len(charMotif):
        if charMotif[i] == "[":
            childList = []
            i += 1
            while charMotif[i] != "]":
                childList.append(charMotif[i])
                i += 1
            charList.append(childList)
        else: 
            charList.append(charMotif[i])
        i += 1

    # make pfm, row order of ACGT
    pfm = [[float(0) for item in range(4)] for item in range(len(charList))]
    for i in range(len(charList)):
        if len(charList[i]) > 1:
            for item in charList[i]:
                pfm[i][0] = float(1)/len(charList[i]) if item == "A" else pfm[i][0]
                pfm[i][1] = float(1)/len(charList[i]) if item == "C" else pfm[i][1]
                pfm[i][2] = float(1)/len(charList[i]) if item == "G" else pfm[i][2]
                pfm[i][3] = float(1)/len(charList[i]) if item == "T" else pfm[i][3]
        else:
            if charList[i] == "N" or charList[i] == ".":
                for j in range(4):
                    pfm[i][j] = 0.25
            else:
                pfm[i][0] = 1 if charList[i] == "A" else pfm[i][0]
                pfm[i][1] = 1 if charList[i] == "C" else pfm[i][1]
                pfm[i][2] = 1 if charList[i] == "G" else pfm[i][2]
                pfm[i][3] = 1 if charList[i] == "T" else pfm[i][3]

    # write motif to output file
    writer.write("\nMOTIF %s\n\n" % parsed.motif)
    writer.write("letter-probability matrix: alength= 4 w= %d nsites= 20 E= 0\n" % len(charList))
    for i in range(len(charList)):
        for j in range(4):
            writer.write("%.3f\t" % pfm[i][j])
        writer.write("\n")
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
