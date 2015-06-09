#! /bin/bash
# bash batch_np_kmers_discrete_others.sh 1 50

type_bin=$1 # 1: equal-sized binning, 2: equal-score-interval binning
num_bin=$2 # number of bins

cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta

num_kmers=8
for (( i=0; i<${#num_kmers}; i++ ))
do
	for file in $dir_data/NP_data_others/${num_kmers[i]}mers_bin${type_bin}_${num_bin}/*;
	do 
		echo "__@__PROCESSING FILE: $file"
		perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data -k=${num_kmers[i]} --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	done
done
