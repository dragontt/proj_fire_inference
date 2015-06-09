#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in gata family, allowing 1 wildcard position.")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def filterkmers(kmer, k_str, new_kmer_list):
    for i in range(len(kmer)-len(k_str)+1):
        for j in range(len(k_str)):
            if kmer[i:i+j] == k_str[0:j] and kmer[i+j+1:i+len(k_str)] == k_str[j+1:len(k_str)]:
                new_kmer_list.append(kmer)
    return new_kmer_list

def main(argv):
    parsed = parse_args(argv)

    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    # contain GAT[AC] and its reverse complement including 1 wildcard 
    k_gata0 = 'GATA'
    k_gata1 = 'GATC'
    k_gata2 = 'CTAT'
    k_gata3 = 'CTAG'
    for kmer in kmersList:
        kmer = kmer.split('\n')[0]
        newKmersList = filterkmers(kmer, k_gata0, newKmersList)
        newKmersList = filterkmers(kmer, k_gata1, newKmersList)
        kmerRev = kmer[::-1]
        newKmersList = filterkmers(kmer, k_gata2, newKmersList)
        newKmersList = filterkmers(kmer, k_gata3, newKmersList)
    newKmersList = sorted(set(newKmersList))
    
    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
