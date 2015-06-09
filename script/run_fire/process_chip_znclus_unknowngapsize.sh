#! /bin/bash
# bash process_chip_znclus_unknowngapsize.sh YPL248C 6

timer_start=$SECONDS

file_name=$1
kmer_size=$2 # k= 6 or 8(consider 2 inner bps)
max_robust=$3 # optional robustness input (default 10)

# gap size
min_gapsize=0
max_gapsize=20
if [ $kmer_size -eq 6 ]; then shift_gapsize=0;
elif [ $kmer_size -eq 8 ]; then shift_gapsize=2; fi
real_max_gapsize=$(($max_gapsize-$shift_gapsize))

# robustness 
min_robust=6
if [ -z $max_robust ]; then max_robust=10;
else min_robust=$((max_robust/10*6)); fi

# designate directories
dir_data=$HOME/proj_motifinference/resources/yeast
fasta_data=$dir_data/s_cerevisiae.promoters.fasta
kmer_file=$dir_data/new_kmers/kmers_znclus_fam/'new_'$kmer_size'mers_dna.txt'
file=$dir_data/ChIP_data_znclus_fam/new_unknowngapsize/$file_name

# set fire directory
cd $HOME/usr/FIRE-1.1a/
export FIREDIR=`pwd`
echo "__@__FIREDIR IS SET."

# create tmp directory and files
if [ $max_robust -ne 10 ]; then dir_out=$file'_FIRE_tmp_k'$kmer_size'_rb'$max_robust;
else dir_out=$file'_FIRE_tmp_k'$kmer_size; fi
mkdir -p $dir_out
sum_list=$dir_out'/summary_list.txt'
touch $sum_list

for gapsize in $(seq $min_gapsize $real_max_gapsize)	
do
	real_gapsize=$(($gapsize+$shift_gapsize))
	dir_tmp=$dir_out/'gap_size_'$real_gapsize
	mkdir -p $dir_tmp
	file_tmp=$dir_tmp/$file_name
	cp $file $file_tmp
	
	# process FIRE
	echo "__@__PROCESSING FILE WITH CONTRAINT KMERS AT GAP SIZE OF $real_gapsize: $file_tmp"
	perl fire.pl --expfiles=$file_tmp --exptype=discrete --fastafile_dna=$fasta_data --gap=$gapsize --kmerfile=$kmer_file --jn=$max_robust --jn_t=$min_robust --seqlen_dna=600 --nodups=1 --dorna=0 --dodnarna=0
	
	# write gap size, mi, z-score, robustness (if applicable, otherwise 'NA') to tmp score file
	sum_file=$file_tmp'_FIRE/DNA/'$file_name'.summary'
	if [ -s $sum_file ]
	then
		while read summary_line
		do
			echo -e "$real_gapsize\t $summary_line" >> $sum_list
		done < $sum_file
	fi
done

timer_duration=$(( SECONDS - timer_start ))
echo "__@__TIME ECLAPSED: $timer_duration sec"
