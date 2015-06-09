#!/usr/bin/python

import sys
import os
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Determine dbd families of each tf")
    parser.add_argument('seq_fasta', metavar='seq_fasta', help='sequence data in fasta')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str, default='./tf_dbd_families/')
    parser.add_argument('-t', '--targets', dest='targets', type=str, default=None, help='tf database')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)
    assert parsed.targets != None, 'need to specify the tf database'

    if not parsed.output_directory.endswith('/'):
        parsed.output_directory += '/'
    if not os.path.exists(parsed.output_directory):
        os.makedirs(parsed.output_directory)

    lines_seq = open(parsed.seq_fasta,"r").readlines()
    lines_fam = open(parsed.targets,"r").readlines()

    for line_seq in lines_seq:
        if line_seq.strip().startswith(">"):
            tfSeq = line_seq[1:].strip()
            families = list()
            matchCount = 0

            for line_fam in lines_fam:
                if not line_fam.strip().startswith("#"):
                    tfFam = line_fam.split(None, 2)[1].strip()
                    if tfSeq.lower() == tfFam.lower():
                        families.append(line_fam.rsplit(None, 1)[-1])
                        matchCount += 1

            if matchCount > 0:
                families.sort()
                filename = os.path.join(parsed.output_directory,tfSeq)
                writer = open(filename, 'w')
                for item in families:
                    writer.write("%s\n" % item)        
                writer.close()

if __name__ == "__main__":
    main(sys.argv)
