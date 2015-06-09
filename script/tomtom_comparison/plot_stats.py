#!/usr/bin/python
# python plot_stats.py ~/Documents/GeneData/yeast/ChIP_data_comp_archive/ChIP_data_comp_ori_vs_new_v2/stats_sign_report.txt 

import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Plot stats signs report.")
    parser.add_argument('report_file', metavar='report_file', help='stats_sign_report file')
    parser.add_argument('-f', '--all_fam_dir', dest='all_fam_dir', type=str)
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def appendkmer(fam, columns):
    if fam == "znclus":
        columns.append(fam + '_k6')
    else: 
        columns.append(fam + '_k7')
    columns.append(fam + '_k8')
    return columns

def main(argv):
    parsed = parse_args(argv)

    # parse data
    lines = open(parsed.report_file, 'r')
    parsing = False
    data = []
    for line in lines:
        if line.startswith('#Combined score comparison'):
            parsing = True
            startnum = line
        if parsing and not line.startswith('#'):
            tmprow = []
            for item in line.split('\t'):
                if item.startswith('0') or item.startswith('1'):
                    tmprow.append(float(item))
            data.append(tmprow)

    # handle data
    data = np.rot90(np.rot90(np.rot90(data)))
    lines = open(parsed.all_fam_dir, "r").readlines()
    columns = []
    for line in lines:
        columns = appendkmer(line.split('\n')[0], columns)
    columns = tuple(columns) + ('ALL_k6/7', 'ALL_k8')
    values = np.arange(0, 101, 10)
    value_increment = 100

    colors = plt.cm.BuPu(np.linspace(0, 4, len(columns)))
    n_rows = len(data)
    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4
    y_offset = np.array([0.0] * len(columns))
    label_arr = ['+1', '0', '-1', 'N/A']

    # plot data
    for row in range(n_rows):
        tmpdata = data[row]*100
        tmpdata = tmpdata[::-1]
        plt.bar(index, tmpdata, bar_width, bottom=y_offset, color=colors[row], label=label_arr[row])
        y_offset = y_offset + tmpdata

    locs, labels = plt.xticks(index, columns)
    plt.setp(labels, rotation=45)
    plt.ylabel("Percentage (%)")
    plt.yticks(values, ['%d' % val for val in values])
    plt.ylim([0, 100])
    plt.title('Combined FIRE scores and TOMTOM alignment data')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main(sys.argv)
