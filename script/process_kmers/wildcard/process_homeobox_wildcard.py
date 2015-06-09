#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in homeobox family, allowing 1 wildcard position.")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def filterkmers(kmer, k_str, new_kmer_list):
    for i in range(len(kmer)-len(k_str)):
        for j in range(len(k_str)):
            if kmer[i:i+j] == k_str[0:j] and kmer[i+j+1:i+len(k_str)] == k_str[j+1:len(k_str)]:
                new_kmer_list.append(kmer)
    return new_kmer_list

def main(argv):
    parsed = parse_args(argv)

    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    # contain ATTA and its reverse complement TAAT 
    k_homeobox0 = 'ATTA'
    k_homeobox1 = 'TAAT'
    for kmer in kmersList:
        kmer = kmer.split('\n')[0]
        newKmersList = filterkmers(kmer, k_homeobox0, newKmersList)
        newKmersList = filterkmers(kmer, k_homeobox1, newKmersList) 
    newKmersList = sorted(set(newKmersList))
    
    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
