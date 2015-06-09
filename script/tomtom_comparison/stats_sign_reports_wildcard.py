#!/usr/bin/python

import sys
import os
import argparse
import numpy

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Output stats of sign report summary")
    parser.add_argument('input_dir', metavar='input_dir', help='sum_sign_report file')
    parser.add_argument('-o', '--output_dir', dest='output_dir', type=str, default='./rank_sign_report.txt')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def counter(data, table, sign_type, fam_dict, sign_dict):
    for key_d, val_d in data.iteritems():
        if val_d['kmer'] == '6' or val_d['kmer'] == '7':
            col_num = fam_dict[val_d['fam']]*3
            row_num = sign_dict[val_d[sign_type]]
            table[col_num][row_num] += 1
        elif val_d['kmer'] == '6_w' or val_d['kmer'] == '7_w':
            col_num = fam_dict[val_d['fam']]*3 + 1
            row_num = sign_dict[val_d[sign_type]]
            table[col_num][row_num] += 1
        elif val_d['kmer'] == '8':
            col_num = fam_dict[val_d['fam']]*3 + 2
            row_num = sign_dict[val_d[sign_type]]
            table[col_num][row_num] += 1
    return table

def sumcols(table, num_families, num_signs):
    for i in range(num_families*3):
        for j in range(num_signs):
            if i%3 == 0:
                table[num_families*3][j] += table[i][j]
            elif i%3 == 1:
                table[num_families*3+1][j] += table[i][j]
            else:
                table[num_families*3+2][j] += table[i][j]
    return table

def percent(table_count):
    table_pct = numpy.zeros(shape=(len(table_count), len(table_count[0])))
    for i in range(len(table_count)):
        s = sum(table_count[i])
        table_pct[i] = [float(c)/s for c in table_count[i]]
    return table_pct

def writetable(writer, table, num_families, num_signs, fam_dict):
    writer.write("#+1\t 0\t -1\t N/A\t fam_kmer\n")
    for i in range(num_families*3):
        for j in range(num_signs):
            writer.write("%.3f\t" % (table[i][j]))
        for key, val in fam_dict.iteritems():
            if i/3 == val:
                if key == "znclus":
                    if i%3 == 0:
                        writer.write("%s_k6\n" % (key))  
                    elif i%3 == 1:
                        writer.write("%s_k6_w\n" % (key))
                    else:
                        writer.write("%s_k8\n" % (key))
                else:
                    if i%3 == 0:
                        writer.write("%s_k7\n" % (key))
                    elif i%3 == 1:
                        writer.write("%s_k7_w\n" % (key))
                    else:
                        writer.write("%s_k8\n" % (key))
    for item in table[num_families*3]: 
        writer.write("%.3f\t" % (item)) 
    writer.write("all_k6/7\n")
    for item in table[num_families*3+1]:
        writer.write("%.3f\t" % (item)) 
    writer.write("all_k6/7_w\n")
    for item in table[num_families*3+2]:
        writer.write("%.3f\t" % (item))
    writer.write("all_k8\n")

def main(argv):
    parsed = parse_args(argv)

    # create nested dict
    lines = open(parsed.input_dir, "r").readlines()
    data = {}
    for line in lines:
        linesplit = line.split()
        l_fire = linesplit[0]
        l_tomtom = linesplit[1]
        l_combined = linesplit[2]
        l_kmer = linesplit[3].split("_k")[1]
        l_fam = linesplit[4]
        data[linesplit[3]] = {'sign_fire': l_fire, 'sign_tomtom': l_tomtom, 'sign_combined': l_combined, 'kmer': l_kmer, 'fam': l_fam}

    # count table
    num_families = 5
    num_signs = 4
    fam_dict = {'gata': 0, 'hlh': 1, 'homeobox': 2, 'hsf': 3, 'znclus': 4}
    sign_dict = {'+1': 0, '0': 1, '-1': 2, 'N/A': 3}

    table_count_fire = numpy.zeros(shape=(num_families*3+3, num_signs))
    table_count_tomtom = numpy.zeros(shape=(num_families*3+3, num_signs))
    table_count_combined = numpy.zeros(shape=(num_families*3+3, num_signs))
    table_count_fire = counter(data, table_count_fire, 'sign_fire', fam_dict, sign_dict)
    table_count_tomtom = counter(data, table_count_tomtom, 'sign_tomtom', fam_dict, sign_dict)
    table_count_tomtom = counter(data, table_count_combined, 'sign_combined', fam_dict, sign_dict)
    table_count_fire = sumcols(table_count_fire, num_families, num_signs)
    table_count_tomtom = sumcols(table_count_tomtom, num_families, num_signs)
    table_count_combined = sumcols(table_count_combined, num_families, num_signs)

    table_pct_fire = percent(table_count_fire)
    table_pct_tomtom = percent(table_count_tomtom)
    table_pct_combined = percent(table_count_combined)

    # write ranked motifs to output file
    writer = open(parsed.output_dir, 'w')
    writer.write("#FIRE score comparison only\n")
    writetable(writer, table_pct_fire, num_families, num_signs, fam_dict)
    writer.write("\n#TOMTOM score comparison only\n")
    writetable(writer, table_pct_tomtom, num_families, num_signs, fam_dict)
    writer.write("\n#Combined score comparison\n")
    writetable(writer, table_pct_combined, num_families, num_signs, fam_dict)
    writer.close()

if __name__ == "__main__":
    main(sys.argv)
