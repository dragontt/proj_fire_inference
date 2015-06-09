#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in zn cluster family, preferred 6 or 8-mers")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def filterkmers(kmer, k_str, new_kmer_list):
    if kmer[0:len(k_str[0])] == k_str[0]:
        for i in range(len(k_str[1])):
            if kmer[len(kmer)-len(k_str[1]):len(kmer)-len(k_str[1])+i] == k_str[1][0:i] and kmer[len(kmer)-len(k_str[1])+i+1:len(kmer)] == k_str[1][i+1:len(k_str[1])]:
                new_kmer_list.append(kmer)
    if kmer[len(kmer)-len(k_str[1]):len(kmer)] == k_str[1]:
        for i in range(len(k_str[0])):
            if kmer[0:i] == k_str[0:i] and kmer[i+1:len(k_str[0])] == k_str[0][i+1:len(k_str[0])]:
                new_kmer_list.append(kmer)
    return new_kmer_list

def main(argv):
    parsed = parse_args(argv)

    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    # contain CGG_CCG, CCG_CGG, CGG_CGG, CCG_CCG subseq
    k_znclus0 = ['CGG', 'CCG']
    k_znclus1 = ['CCG', 'CGG']
    k_znclus2 = ['CGG', 'CGG']
    k_znclus3 = ['CCG', 'CCG']
    for kmer in kmersList:
        kmer = kmer.split('\n')[0]
        newKmersList = filterkmers(kmer, k_znclus0, newKmersList)
        newKmersList = filterkmers(kmer, k_znclus1, newKmersList)
        newKmersList = filterkmers(kmer, k_znclus2, newKmersList)
        newKmersList = filterkmers(kmer, k_znclus3, newKmersList)
    newKmersList = sorted(set(newKmersList))

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
