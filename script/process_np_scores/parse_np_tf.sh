#! /bin/bash
# bash parse_np_tf.sh gata 1 50
 
dbd_fam=$1 # dna binding domain family
type_bin=$2 # 1: equal-sized binning, 2: equal-score-interval binning
num_bin=$3 # number of bins

dir_data=$HOME/proj_motifinference/resources/yeast
# mkdir $dir_data/NP_data_${dbd_fam}_fam/tf_${dbd_fam}_parsed
mkdir -p $dir_data/NP_data_${dbd_fam}_fam/tf_${dbd_fam}_bin${type_bin}_${num_bin}

while read tf; do 
	# cp $dir_data/NP_data/$tf $dir_data/NP_data_${dbd_fam}_fam/tf_${dbd_fam}_parsed/$tf
	dir_input=$dir_data/NP_data_${dbd_fam}_fam/tf_${dbd_fam}_parsed/$tf
	dir_output=$dir_data/NP_data_${dbd_fam}_fam/tf_${dbd_fam}_bin${type_bin}_${num_bin}/$tf
	if [ $type_bin == "1" ]	# bin1: equal-sized binning
		then
		python $HOME/proj_motifinference/script/process_np_scores/process_np_tf_bin1.py $dir_input -n $num_bin -o $dir_output
	elif [ $type_bin == "2" ]	# bin2: equal-score-interval binning
		then
		python $HOME/proj_motifinference/script/process_np_scores/process_np_tf_bin2.py $dir_input -n $num_bin -o $dir_output
	fi
done < $dir_data/NP_data_${dbd_fam}_fam/tf_${dbd_fam}
