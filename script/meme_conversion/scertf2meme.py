#!/usr/bin/python

import sys
import os
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Convert Scer TF motif data files to meme type database")
    parser.add_argument('scertf_dir', metavar='scertf_dir', help='Directory of Scer TF motif data files')
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

    for input_fn in os.listdir(parsed.scertf_dir):
        # get motif names
        if not input_fn.startswith("."):
            author_name, motif_name = os.path.splitext(input_fn)
            motif_name = motif_name.replace(".","")
        
            # parse scertf file
            lines = open("%s/%s" % (parsed.scertf_dir, input_fn),"r").readlines()
            arrnum = [None for _ in range(4)]
            lncnt = 0
            for line in lines:
                arrnum[lncnt] = [float(item) for item in line.split() if isfloat(item)]
                lncnt += 1

            # write motif to output file
            writer.write("\nMOTIF %s\n\n" % motif_name)
            writer.write("letter-probability matrix: alength= 4 w= %d nsites= 20 E= 0\n" % len(arrnum[0]))
            for i in range(0, len(arrnum[0])):
                for j in range(0, 4):
                    writer.write("%.3f\t" % arrnum[j][i])
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
