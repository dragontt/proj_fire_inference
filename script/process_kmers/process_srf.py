#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in SRF family")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    # srf core sequence: CC([AT]x6)GG
    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    for kmer in kmersList:
        kmer = kmer.split("\n")[0]
        if kmer[0] == "C" or kmer[0] == "G":
            counter = 0
            for i in range(1,7):
                if kmer[i] == "A" or kmer[i] == "T":
                    counter += 1
            if counter == 6:
                newKmersList.append(kmer)
        if kmer[6] == "C" or kmer[6] == "G":
            counter = 0
            for i in range(6):
                if kmer[i] == "A" or kmer[i] == "T":
                    counter += 1
            if counter == 6:
                newKmersList.append(kmer)
    newKmersList = sorted(set(newKmersList))

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
