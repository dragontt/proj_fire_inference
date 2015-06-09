#!/usr/bin/python

import sys
import os
import argparse
import csv

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in gata family")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    for kmer in kmersList:
        kmer = kmer.split('\n')[0]
        # gata core sequence: GAT[AC]
        # contain GAT[AC] subseq 
        for i in range(0,len(kmer)-3):
            if kmer[i:i+3] == 'GAT':
                if kmer[i+3] == 'A' or kmer[i+3] == 'C':
                    newKmersList.append(kmer)
        # contain reverse complement GAT[AC]
        kmerRev = kmer[::-1]
        for i in range(0,len(kmerRev)-3):
            if kmerRev[i:i+3] == 'CTA':
                if kmerRev[i+3] == 'T' or kmerRev[i+3] == 'G':
                    newKmersList.append(kmer)

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
