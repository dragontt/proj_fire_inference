#!/usr/bin/python

import sys
import os
import argparse
import csv

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in heat shock factor (HSF) family")
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
        # hsf core sequence: AGAA
        for i in range(0,len(kmer)-4):
            # contain AGAAN subseq
            if kmer[i:i+4] == 'AGAA':
                newKmersList.append(kmer)
            # contain partial kmers
            elif kmer[0:3] == 'GAA' or kmer[len(kmer)-3:len(kmer)] == 'AGA':
                newKmersList.append(kmer)
            # contain reverse complement TTCT subseq
            elif kmer[i:i+4] == 'TTCT':
                newKmersList.append(kmer)
            # contain partial kmers
            elif kmer[0:3] == 'TCT' or kmer[len(kmer)-3:len(kmer)] == 'TTC':
                newKmersList.append(kmer)

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
