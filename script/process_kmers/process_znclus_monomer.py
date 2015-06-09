#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain 6-bp monomers in znclus family")
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
        kmer = kmer.split("\n")[0]
        # zninc cluster core sequence: CGG, CCG (monomer)
        for i in range(0,len(kmer)-3):
            if (kmer[i:i+3] == "CGG" or kmer[i:i+3] == "GCC" or kmer[i:i+3] == "CCG" or kmer[i:i+3] == "GGC"):
                newKmersList.append(kmer)
    newKmersList = sorted(set(newKmersList))

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
