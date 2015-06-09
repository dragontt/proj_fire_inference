#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in basic helix-loop-helix family, allowing 1 wildcard position.")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def filterkmers(kmer, k_str, new_kmer_list):
    k_str = k_str.split("NN")
    for i in range(len(kmer)-6):
        if kmer[i:i+2] == k_str[0]:
            if kmer[i+4] == k_str[1][0] or kmer[i+5] == k_str[1][1]:
                new_kmer_list.append(kmer)
        if kmer[i+4:i+6] == k_str[1]:
            if kmer[i] == k_str[0][0] or kmer[i+1] == k_str[0][1]:
                new_kmer_list.append(kmer)
    return new_kmer_list

def main(argv):
    parsed = parse_args(argv)

    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    for kmer in kmersList:
        kmer = kmer.split('\n')[0]
        # contain CANNTG subseq, the E-box; its reverse complement as itself
        k_str = 'CANNTG'
        newKmersList = filterkmers(kmer, k_str, newKmersList)
    newKmersList = sorted(set(newKmersList))

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
