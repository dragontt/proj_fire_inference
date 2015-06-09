#!/usr/bin/python

import sys
import os
import argparse
import sets

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Constrain k-mers in Myb/SANT family")
    parser.add_argument('kmers', metavar='kmers', help='k-mers')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def filterseq(kmer, dbd_seq, new_kmer_list):
    for i in range(len(kmer)-len(dbd_seq)+1):
        if kmer[i:i+len(dbd_seq)] == dbd_seq:
            new_kmer_list.append(kmer)
        elif kmer[0:len(dbd_seq)-1] == dbd_seq[1::] or kmer[len(kmer)-len(dbd_seq)+1:len(kmer)] == dbd_seq[0:len(dbd_seq)-1]:
            new_kmer_list.append(kmer)
    return new_kmer_list

def main(argv):
    parsed = parse_args(argv)

    kmersList = open(parsed.kmers,"r").readlines()
    newKmersList = list()

    for kmer in kmersList:
        kmer = kmer.split('\n')[0]
        # myb core sequence: AAC[TG]G, G[GT]T[GA], CTCAGCG
        dbdSeqList = ['AACGG', 'AACTG', 'CAGTT', 'CCGTT', 'CTCAGCG', 'CGCTGAG', 
        'GTTG', 'CAAC', 'GTTA', 'TAAC', 'GGTG', 'CACC', 'GGTA', 'TACC']
        for dbdSeq in dbdSeqList:
            newKmersList = filterseq(kmer, dbdSeq, newKmersList)
    newKmersList = sorted(set(newKmersList))

    filename = parsed.output_directory
    writer = open(filename, 'w')
    for newKmer in newKmersList:
        writer.write("%s\n" % newKmer)        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
