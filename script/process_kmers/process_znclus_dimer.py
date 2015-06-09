#!/usr/bin/python

import sys
import os
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in zn cluster family, preferred 6 or 8-mers")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str, default='./kmers_znclus')
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
        # zninc cluster core sequence: CGG, CCG (dimer)
        # contain CGG, CCG subseq
        if kmer[0:3] == 'CGG' and kmer[len(kmer)-3:len(kmer)] == 'CCG':
            newKmersList.append(kmer)
        # contain CCG, CGG subseq
        elif kmer[0:3] == 'CCG' and kmer[len(kmer)-3:len(kmer)] == 'CGG':
            newKmersList.append(kmer)
        # contain CGG, CGG subseq
        elif kmer[0:3] == 'CGG' and kmer[len(kmer)-3:len(kmer)] == 'CGG':
            newKmersList.append(kmer)
        # contain reverse complement of CGG, CGG subseq
        elif kmer[0:3] == 'CCG' and kmer[len(kmer)-3:len(kmer)] == 'CCG':
            newKmersList.append(kmer)

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
