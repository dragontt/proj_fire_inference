#! /bin/bash
# bash batch_chip_znclus_monomer.sh (optional max_robustness)

timer_start=$SECONDS

max_robust=$1 # optional robustness input (default 10)

# robustness 
min_robust=6
if [ -z $max_robust ]; then max_robust=10;
else min_robust=$((max_robust/10*6)); fi

# designate directories
dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta
kmer_file=$dir_data/new_kmers/kmers_znclus_fam/'new_6mers_monomer_dna.txt'

# set fire directory
cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "__@__FIREDIR IS SET."

# run fire on monomer constrained 6mers and copy directories over
for file in $dir_data/ChIP_data_znclus_fam/new_monomer/*;
do 
	echo "__@__PROCESSING FILE: $file"
	perl fire.pl --expfiles=$file --exptype=discrete --fastafile_dna=$fasta_data --kmerfile=$kmer_file --jn=$max_robust --jn_t=$min_robust --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	if [ $max_robust -ne 10 ]; then dir_out=$file'_FIRE_tmp_k6_rb'$max_robust;
	else dir_out=$file'_FIRE_tmp_k6'; fi
	mv $file'_FIRE' $dir_out
done

timer_duration=$(( SECONDS - timer_start ))
echo "__@__TIME ECLAPSED: $timer_duration sec"

