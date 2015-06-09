#! /bin/bash

cd ~/Documents/FIRE/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

for file in ~/Documents/GeneData/yeast/processed_hits_hsf_fam/original/*;
do 
	echo "\nPROCESSING FILE: ${file}\n";
	perl fire.pl --expfiles=${file} --exptype=continuous --fastafile_dna=/Users/KANG/Documents/GeneData/yeast/s_cerevisiae.promoters.fasta --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done

