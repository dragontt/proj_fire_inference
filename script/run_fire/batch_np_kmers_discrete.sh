#! /bin/bash
# bash batch_np_kmers_discrete.sh gata 50

dbd_fam=$1 # dna binding domain family
type_bin=$2 # 1: equal-sized binning, 2: equal-score-interval binning
num_bin=$3 # number of bins

cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "FIREDIR is set."

dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta

# process original 7mers
for file in $dir_data/NP_data_${dbd_fam}_fam/original_7mers_bin${type_bin}_${num_bin}/*;
do 
	echo "__@__PROCESSING FILE: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done

# process original 8mers
for file in $dir_data/NP_data_${dbd_fam}_fam/original_8mers_bin${type_bin}_${num_bin}/*;
do 
	echo "__@__PROCESSING FILE: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --k=8 --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
done

# process new kmers k=7,8
for i in {7..8}
do
	new_kmers='new_'$i'mers'
	for file in $dir_data/NP_data_${dbd_fam}_fam/${new_kmers}_bin${type_bin}_${num_bin}/*;
	do
		echo "__@__PROCESSING FILE: $file"
		kmer_file=$dir_data/new_kmers/kmers_${dbd_fam}_fam/$new_kmers'_dna'.txt
		perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --kmerfile=$kmer_file --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	done
done


