#!/usr/bin/python

import sys
import os
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Used to parse the S. cerevisiae database to get unique binding domain families.")
    parser.add_argument('sc_tf', metavar='sc_tf', help='the .ass file of S. cerevisiae database')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str, default='./')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)
    # put familiy name and count in dict
    families = {}
    lines = open(parsed.sc_tf,"r").readlines()
    for line in lines:
        if not line.strip().startswith("#"):
            currentFam = line.rsplit(None, 1)[-1]
            if not currentFam in families.keys():
                families[currentFam] = 1
            else:
                families[currentFam] += 1
    # sort familiy dict
    families_sort = sorted(((count,family) for family,count in families.iteritems()), reverse=True)

    if not parsed.output_directory.endswith('/'):
        parsed.output_directory += '/'
    if not os.path.exists(parsed.output_directory):
        os.makedirs(parsed.output_directory)

    filename = os.path.join(parsed.output_directory,'family_list')
    writer = open(filename, 'w')
    for count,family in families_sort:
        writer.write("%s: %d\n" % (family,count))        
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
