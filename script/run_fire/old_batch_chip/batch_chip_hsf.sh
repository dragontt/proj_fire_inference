#! /bin/bash

cd ~/Documents/FIRE/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

# for file in ~/Documents/GeneData/yeast/ChIP_data_hsf_fam/new_6mers/*;
# do 
# 	echo "\nPROCESSING FILE: ${file}\n";
# 	perl fire.pl --expfiles=${file} --exptype=discrete --fastafile_dna=/Users/KANG/Documents/GeneData/yeast/s_cerevisiae.promoters.fasta --k=6 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
# done

# for file in ~/Documents/GeneData/yeast/ChIP_data_hsf_fam/new_7mers/*;
# do 
# 	echo "\nPROCESSING FILE: ${file}\n";
# 	perl fire.pl --expfiles=${file} --exptype=discrete --fastafile_dna=/Users/KANG/Documents/GeneData/yeast/s_cerevisiae.promoters.fasta --k=7 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
# done

# for file in ~/Documents/GeneData/yeast/ChIP_data_hsf_fam/new_8mers/*;
# do 
# 	echo "\nPROCESSING FILE: ${file}\n";
# 	perl fire.pl --expfiles=${file} --exptype=discrete --fastafile_dna=/Users/KANG/Documents/GeneData/yeast/s_cerevisiae.promoters.fasta --k=8 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
# done

for file in ~/Documents/GeneData/yeast/ChIP_data_hsf_fam/original_7mers/*;
do 
	echo "\nPROCESSING FILE: ${file}\n";
	perl fire.pl --expfiles=${file} --exptype=discrete --fastafile_dna=/Users/KANG/Documents/GeneData/yeast/s_cerevisiae.promoters.fasta --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done