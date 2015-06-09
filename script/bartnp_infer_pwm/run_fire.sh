#! /bin/bash

dir_binned_files=$1 	# directory of binned expression files
tf_list=$2 	 # a list of tf names

cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_expfiles=$HOME/proj_fire_inference/${dir_binned_files}
fasta_data=$HOME/proj_fire_inference/resources/yeast/s_cerevisiae.promoters.fasta

while read -a line
do
	tf=${line[0]}
	echo "__@__PROCESSING TF: $tf"
	perl fire.pl --expfiles=${dir_expfiles}/$tf --exptype=discrete --fastafile_dna=$fasta_data -k=7 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done < $HOME/proj_fire_inference/${tf_list}

# cd $HOME/proj_fire_inference/
# python script/bartnp_infer_pwm/parse_infer_summary.py -i resources/yeast_bart_holstege/holstegeBartNp_binned/ -o resources/yeast_bart_holstege/holstegeBartNp.txt
