#! /bin/bash
# bash batch_chip_kmers.sh gata

# dna binding domain family
dbd_fam=$1

cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta

# process original 7mers
for file in $dir_data/ChIP_data_${dbd_fam}_fam/original_7mers/*;
do 
	echo "__@__PROCESSING FILE: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done

# process original 8mers
for file in $dir_data/ChIP_data_${dbd_fam}_fam/original_8mers/*;
do 
	echo "__@__PROCESSING FILE: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --k=8 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done

# process new kmers k=6,7,8
for i in {7..8}
do
	new_kmers='new_'$i'mers'
	for file in $dir_data/ChIP_data_${dbd_fam}_fam/$new_kmers/*;
	do
		echo "__@__PROCESSING FILE: $file"
		kmer_file=$dir_data/new_kmers/kmers_${dbd_fam}_fam/$new_kmers'_dna'.txt
		perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --kmerfile=$kmer_file --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	done
done

# # process new kmers k=7 allowing 1 wildcard-position constrain
# new_kmers='new_7mers'
# for file in $dir_data/ChIP_data_${dbd_fam}_fam/$new_kmers'_wildcard'/*;
# do 
# 	echo "__@__PROCESSING FILE: $file"
# 	kmer_file_wildcard=$dir_data/new_kmers/kmers_$dbd_fam_fam/$new_kmers'_dna_wildcard'.txt
# 	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --kmerfile=$kmer_file_wildcard --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
# done


