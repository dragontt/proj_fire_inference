#!/usr/bin/python

import sys
import os
import argparse
import os.path

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Compare scors in original and new motif inferences")
    parser.add_argument('-m', '--ori_fire', dest='ori_fire', help='original fire scores')
    parser.add_argument('-n', '--new_fire', dest='new_fire', help='new fire scores')
    parser.add_argument('-p', '--ori_tomtom', dest='ori_tomtom', help='original tomtom scores')
    parser.add_argument('-q', '--new_tomtom', dest='new_tomtom', help='new tomtom scores')
    parser.add_argument('-o', '--output_file', dest='output_file', type=str, default='sign_report')
    parser.add_argument('-t', '--motif_name', dest='motif_name', type=str)
    parser.add_argument('-b', '--dbd_fam', dest='dbd_fam', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def sign(val):
    if val > 0: 
        return ("+1", 1)
    elif val == 0: 
        return ("0", 0)
    elif val < 0: 
        return ("-1", -1)

def main(argv):
    parsed = parse_args(argv)

    # flag exisiting file
    flagOriFire = os.path.isfile(parsed.ori_fire)
    flagNewFire = os.path.isfile(parsed.new_fire)
    flagOriTomtom = os.path.isfile(parsed.ori_tomtom)
    flagNewTomtom = os.path.isfile(parsed.new_tomtom)
    
    # parse and compare scores
    if flagOriFire:
        line = open(parsed.ori_fire,"r").readline()
        lineOriFire = line.split()
    if flagNewFire:
        line = open(parsed.new_fire,"r").readline()
        lineNewFire = line.split()
    if flagOriTomtom:
        line = open(parsed.ori_tomtom,"r").readline()
        lineOriTomtom = line.split()
    if os.path.isfile(parsed.new_tomtom):
        line = open(parsed.new_tomtom,"r").readline()
        lineNewTomtom = line.split()

    # parse mi, z-score, robustness, preferring higher scores
    counterFire = [0, 0]
    counterTomtom = [0, 0]
    if flagOriFire and flagNewFire:
        for i in range(1,4):
            if float(lineOriFire[i]) > float(lineNewFire[i]):
                counterFire[0] += 1
            elif float(lineOriFire[i]) < float(lineNewFire[i]):
                counterFire[1] += 1
        signFire, intFire = sign(counterFire[1] - counterFire[0])
    # parse p-value, e-value, q-value, preferring lower scores
    if flagOriTomtom and flagNewTomtom:
        for i in range(3):
            if float(lineOriTomtom[i]) < float(lineNewTomtom[i]):
                counterTomtom[0] += 1
            elif float(lineOriTomtom[i]) > float(lineNewTomtom[i]):
                counterTomtom[1] += 1
        signTomtom, intTomtom = sign(counterTomtom[1] - counterTomtom[0])

    # write scores to output file
    writer = open(parsed.output_file, "w")
    if flagOriFire and flagNewFire:
        if flagOriTomtom and flagNewTomtom:
            signCombined, intCombined = sign(intFire+intTomtom)
            writer.write("%s\t %s\t %s\t" % (signFire, signTomtom, signCombined))
        elif not flagOriTomtom and flagNewTomtom:
            writer.write("%s\t +1\t +1\t" % signFire)
        elif flagOriTomtom and not flagNewTomtom:
            writer.write("%s\t -1\t -1\t" % signFire)
        else:
            writer.write("%s\t N/A\t N/A\t" % signFire)
    elif flagOriFire and not flagNewFire:
        if flagOriTomtom:
            writer.write("-1\t -1\t -1\t")
        else:
            writer.write("-1\t N/A\t N/A\t")
    elif not flagOriFire and flagNewFire:
        if flagNewTomtom:
            writer.write("+1\t +1\t +1\t")
        else:
            writer.write("+1\t N/A\t N/A\t")
    else:
        writer.write("N/A\t N/A\t N/A\t")
    writer.write("%s\t %s" % (parsed.motif_name, parsed.dbd_fam))
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
