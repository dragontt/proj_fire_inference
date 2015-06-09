#!/usr/bin/python
# CHIP_DATA_DIR=$HOME/proj_motifinference/resources/yeast/ChIP_data
# CHIP_OUT_DIR=$HOME/proj_motifinference/resources/yeast/ChIP_data_<dbd fam>_fam/tf_<dbd fam>
# python parse_chip.py $CHIP_DATA_DIR/ryeastract_tnet.adj.dz -o $CHIP_OUT_DIR'_parsed/' -f $CHIP_OUT_DIR -r $CHIP_DATA_DIR/regulator_list.txt -t $CHIP_DATA_DIR/target_list.txt 

import sys
import os
import argparse
import linecache

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Get chip scores based on specified tf's dbd family")
    parser.add_argument('chip_data', metavar='chip_data', help='chip data')
    parser.add_argument('-o', '--output_directory', dest='output_directory', type=str, default='./output/')
    parser.add_argument('-f', '--tf_dbd_family', dest='tf_dbd_family', type=str, default=None, help="specified tf's dbd family ")
    parser.add_argument('-r', '--chip_regulator', dest='regulators', type=str, default=None, help='chip regulator list')
    parser.add_argument('-t', '--chip_target', dest='targets', type=str, default=None, help='chip target list')
    parsed = parser.parse_args(argv[1:])
    return parsed

def errprint(st):
    sys.stderr.write(st + "\n")

def main(argv):
    parsed = parse_args(argv)
    assert parsed.tf_dbd_family != None, "need to specify tf's bdb family"
    assert parsed.regulators != None, 'need to specify chip regulator list'
    assert parsed.targets != None, 'need to specify chip target list'

    if not parsed.output_directory.endswith('/'):
        parsed.output_directory += '/'
    if not os.path.exists(parsed.output_directory):
        os.makedirs(parsed.output_directory)

    lines_tf = open(parsed.tf_dbd_family,"r").readlines()
    lines_reg = open(parsed.regulators,"r").readlines()

    for tf in lines_tf:
        tar_pos = list()
        tar_neg = list()
        for idx, reg in enumerate(lines_reg, start=1):
            if tf.strip().lower() == reg.strip().lower():
                row_score = linecache.getline(parsed.chip_data,idx)
                break
        for idx, score in enumerate(row_score.split(), start=1):
            tar_pos.append(linecache.getline(parsed.targets,idx).replace("\n", "")) if score == "1" else tar_neg.append(linecache.getline(parsed.targets,idx).replace("\n", ""))

        file_name = os.path.join(parsed.output_directory,tf.strip())
        output_text = "target\tscore"
        for item in tar_pos:
            output_text += "\n" + item + "\t" + "1"
        for item in tar_neg: 
            output_text += "\n" + item + "\t" + "0"
        writer = open(file_name, 'w')
        writer.write(output_text)
        writer.close()

        print "parsing tf %s ... Done" % tf.strip()

if __name__ == "__main__":
    main(sys.argv)
