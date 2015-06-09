#! /bin/bash
# process discrete (binned) netprophet scores

file_name=$1
gap_size=$2
bin_type=$3
bin_num=$4

cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta

# original kmers
file=$dir_data/NP_data_znclus_fam/original_kmers_bin${bin_type}_${bin_num}/$file_name
echo "__@__PROCESSING ORIGINAL FILE: $file"
perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$gap_size --k=6 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
mv $file'_FIRE' $file'_FIRE_g'$gap_size'_k6'

if [ $gap_size != "0" ] && [ $gap_size != "1" ]
	then
	echo "__@__PROCESSING ORIGINAL FILE: $file"
	tmp_gap_size=$(( gap_size - 2 ))
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$tmp_gap_size --k=8 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	mv $file'_FIRE' $file'_FIRE_g'$tmp_gap_size'_k8'
fi

# new kmers
kmer_file=$dir_data/new_kmers/kmers_znclus_fam/'new_6mers_dna.txt'
file=$dir_data/NP_data_znclus_fam/new_kmers_bin${bin_type}_${bin_num}/$file_name
echo "__@__PROCESSING NEW FILE: $file"
perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$gap_size --kmerfile=$kmer_file --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
mv $file'_FIRE' $file'_FIRE_g'$gap_size'_k6'

if [ $gap_size != "0" ] && [ $gap_size != "1" ]
	then
	kmer_file=$dir_data/new_kmers/kmers_znclus_fam/'new_8mers_dna.txt'
	echo "__@__PROCESSING NEW FILE: $file"
	tmp_gap_size=$(( gap_size - 2 ))
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --gap=$tmp_gap_size --kmerfile=$kmer_file --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	mv $file'_FIRE' $file'_FIRE_g'$tmp_gap_size'_k8'
fi