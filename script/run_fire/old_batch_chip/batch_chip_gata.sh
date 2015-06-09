#! /bin/bash
# bash batch_chip_kmers.sh gata

dbd_fam=$1

cd ~/Documents/FIRE/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_data=/Users/KANG/Documents/GeneData/yeast
fasta_data=${dir_data}/s_cerevisiae.promoters.fasta

for i in {6..8}
	do
	new_kmers='new_'$i'mers'
	for file in ${dir_data}/ChIP_data_${dbd_fam}_fam/${new_kmers}/*;
	  do 
		echo "\nPROCESSING FILE: ${file}\n";
		perl fire.pl --expfiles=${file} --exptype=discrete --fastafile_dna=${fasta_data} --kmerfile=${dir_data}/kmers_${dbd_fam}_fam/${new_kmers}'_dna'.txt --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	done
done

