#!/usr/bin/python

import sys
import os
import argparse
import operator

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Sort a collection of FIRE motifs by mi, zscore, robust combined")
    parser.add_argument('firesum', metavar='firesum', help='fire summary')
    parser.add_argument('-o', '--output_fn', dest='output_fn', type=str, default='optimal_score')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)

    maxRobust = 10 # robustness 

    miDict = {} # multual info
    zsDict = {} # z score
    rbDict = {} # robustness
    gapDict = {} # gap size
    rankDict = {} # rank
    # parse line and put 3 scores into dictionary
    sumLines = open(parsed.firesum,"r").readlines()
    for line in sumLines:
        if line.strip():
            lineSplit = line.split()
            motif = lineSplit[1]
            miDict[motif] = float(lineSplit[3])
            zsDict[motif] = float(lineSplit[5])
            rbDict[motif] = int(lineSplit[6].split("/")[0])
            gapDict[motif] = lineSplit[0]
            rankDict[motif] = 0

    # sort dictionary by value
    miDictSorted = sorted(miDict.iteritems(), key=operator.itemgetter(1))
    zsDictSorted = sorted(zsDict.iteritems(), key=operator.itemgetter(1))
    rbDictSorted = sorted(rbDict.iteritems(), key=operator.itemgetter(1))

    # rank sorted dict
    for i in range(len(miDict)):
        rankDict[miDictSorted[i][0]] += i
        rankDict[zsDictSorted[i][0]] += i
        rankDict[rbDictSorted[i][0]] += 1-float(rbDictSorted[i][1])/maxRobust
    rankDictSorted = sorted(rankDict.iteritems(), key=operator.itemgetter(1))
    rankDictSorted.reverse()
    # calculate rank number, specially tie ranks
    rankVal = range(len(rankDictSorted))
    it = 0
    tmpRankValList = []
    tieRankFlag = False
    while it < len(rankDictSorted)-2:
        tmpRankValList.append(rankVal[it])
        while rankDictSorted[it][1] == rankDictSorted[it+1][1]:
            it += 1
            tieRankFlag = True
            tmpRankValList.append(rankVal[it])
        if tieRankFlag:
            tieRankVal = float(sum(tmpRankValList))/len(tmpRankValList)
            for num in tmpRankValList:
                rankVal[int(num)] = tieRankVal 
            tieRankFlag = False
        else:
            it += 1 
        tmpRankValList = []

    # write ranked motifs to output file
    writer = open(parsed.output_fn, 'w')
    writer.write("#rank\t motif\t\t\t mi\t z_score\t robust\t gap_size\n")
    for i in range(len(rankDictSorted)):
        motif = rankDictSorted[i][0]
        writer.write("%.1f\t %s\t %.4f\t %.3f\t %d/%d\t %s\n" % (rankVal[i], motif, miDict[motif], zsDict[motif], rbDict[motif], maxRobust, gapDict[motif]))
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
