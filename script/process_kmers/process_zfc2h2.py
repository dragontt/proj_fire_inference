#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in C2H2 zinc finger family")
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

    # c2h2 zinc finger core sequence: [CG] rich (>= 4bp) and contains 2 consecutive subseq (>= 1pair)
    for kmer in kmersList:
        kmer_split = kmer.split('\n')[0]
        count_cgrich = 0
        count_cons = 0
        for i in range(len(kmer_split)-1):
            if kmer_split[i] == "C" or kmer_split[i] == "G": 
                count_cgrich += 1
            if kmer_split[i:i+2] == "CC" or kmer_split[i:i+2] == "GG":
                count_cons += 1
        if kmer_split[len(kmer_split)-1] == "C" or kmer_split[len(kmer_split)-1] == "G": 
            count_cgrich += 1
        if count_cgrich >= 4 and count_cons >= 1:
            newKmersList.append(kmer_split)
    newKmersList = sorted(set(newKmersList))

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
