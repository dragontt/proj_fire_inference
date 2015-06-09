#!/usr/bin/python

import sys
import os
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Convert YeTFaSCo motif data files to meme type database")
    parser.add_argument('yetfasco_dir', metavar='yetfasco_dir', help='Directory of YeTFsSco motif data files')
    parser.add_argument('-o', '--output_filename', dest='output_fn', type=str, default='motif_meme')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    # write header to output file
    writer = open(parsed.output_fn, "w")
    writer.write("MEME version 4.9.1\n\nALPHABET= ACGT\n\nstrands: + -\n\nBackground letter frequencies\nA 0.3 C 0.2 G 0.2 T 0.3\n")

    tfDict = {}
    for input_fn in os.listdir(parsed.yetfasco_dir):
        # get motif names
        if not input_fn.startswith("."):
            motif_name = os.path.basename(input_fn).split('_')[0]
        
            # parse yetfasco file, which has letter order ATGC
            lines = open("%s/%s" % (parsed.yetfasco_dir, input_fn),"r").readlines()
            arrnum = [None for _ in range(4)]
            lncnt = 0
            for line in lines:
                arrnum[lncnt] = [float(item) for item in line.split() if isfloat(item)]
                lncnt += 1

            # set key, val pair
            tfDict[motif_name] = arrnum

    # write motif to output file
    for tfName, tfPFM in tfDict.iteritems():
        writer.write("\nMOTIF %s\n\n" % tfName)
        writer.write("letter-probability matrix: alength= 4 w= %d nsites= 20 E= 0\n" % len(tfPFM[0]))
        # write pfm in letter order ACGT
        for i in range(0, len(tfPFM[0])):
            writer.write("%.3f\t" % tfPFM[0][i])
            writer.write("%.3f\t" % tfPFM[3][i])
            writer.write("%.3f\t" % tfPFM[2][i])
            writer.write("%.3f\t" % tfPFM[1][i])
            writer.write("\n")
    writer.close()

def isfloat(var):
    try: 
        float(var)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main(sys.argv)
