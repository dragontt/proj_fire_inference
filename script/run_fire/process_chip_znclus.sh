#! /bin/bash
# bash process_chip_znclus.sh 0 YPL248C 11 6

# original = 0, contrained/new = 1, constrain_with_1_wildcard = 2
kmer_type=$1
file_name=$2
gap_size=$3
kmer_size=$4

cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta

# normal dbd family constrain
if [ $kmer_type -eq "0" ]; # original kmers with gap
then 
	file=$dir_data/ChIP_data_znclus_fam/original_kmers/$file_name
	echo "__@__PROCESSING ORIGINAL FILE: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$gap_size --k=$kmer_size --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	mv $file'_FIRE' $file'_FIRE_g'$gap_size'_k'$kmer_size

elif [ $kmer_type -eq "1" ]; # constrained/new kmers with gap
then 
	kmer_file=$dir_data/new_kmers/kmers_znclus_fam/'new_'$kmer_size'mers_dna.txt'
	file=$dir_data/ChIP_data_znclus_fam/new_kmers/$file_name
	echo "__@__PROCESSING FILE WITH CONTRAINT: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$gap_size --kmerfile=$kmer_file --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	mv $file'_FIRE' $file'_FIRE_g'$gap_size'_k'$kmer_size

elif [ $kmer_type -eq "2" ]; # constrained/new kmers with gap, allowing 1 wildcard position
then 
	kmer_file=$dir_data/new_kmers/kmers_znclus_fam/'new_'$kmer_size'mers_dna_wildcard.txt'
	file=$dir_data/ChIP_data_znclus_fam/new_kmers/$file_name
	echo "__@__PROCESSING FILE WITH CONTRAINT: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$gap_size --kmerfile=$kmer_file --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	mv $file'_FIRE' $file'_FIRE_g'$gap_size'_k'$kmer_size'_wildcard'
fi