#! /bin/bash

GENE_NAME=$1 	# gene name
SYS_NAME=$2		# systematic name
DBD_FAM=$3    	# dna binding domain family
ORI_FILE=$4		# original FIRE output without dbd family constrain (full path directory)
NEW_FILE=$5 	# new FIRE output with dbd family constrain (full path directory)
OUT_FILENAME=$6	# output motif filename
USE_YETFASCO=$7	# use YeTFaSCo as complement of ScerTF

TOMTOM_MIN_OVERLAP=5
TOMTOM_EVAL_THRESHOLD=10

OUT_DIRCT=$HOME/proj_motifinference/resources/yeast/validation/ChIP_data_comp_ori_vs_new/$OUT_FILENAME
SCERTF_PFM=$HOME/proj_motifinference/resources/scertf_meme/PFM.meme

mkdir -p $OUT_DIRCT
mkdir -p $OUT_DIRCT/$OUT_FILENAME'_ori'
mkdir -p $OUT_DIRCT/$OUT_FILENAME'_new'

DIR_SCRIPT=$HOME/proj_motifinference/script

# prase original file
if [ -s $ORI_FILE ] 
	then 
	# parse FIRE inference file
	read -r line_oriMotif < $ORI_FILE 
	arr_oriMotif=($line_oriMotif)
	seq_oriMotif=${arr_oriMotif[0]}
	scores_fire=$OUT_DIRCT/$OUT_FILENAME'_ori'/$OUT_FILENAME'_ori_FIRE.txt'
	touch $scores_fire
	echo -e "$seq_oriMotif\t ${arr_oriMotif[2]}\t ${arr_oriMotif[4]}\t ${arr_oriMotif[5]}" >> $scores_fire
	# create meme file of infered motif and compare motif using tomtom alignment
	python $DIR_SCRIPT/meme_conversion/fire2meme.py $seq_oriMotif -o $OUT_DIRCT/$OUT_FILENAME'_ori'/$OUT_FILENAME'.meme'
	cd $HOME/usr/meme/bin/
	./tomtom -no-ssc -oc $OUT_DIRCT/$OUT_FILENAME'_ori' -eps -verbosity 1 -min-overlap $TOMTOM_MIN_OVERLAP -dist pearson -evalue -thresh $TOMTOM_EVAL_THRESHOLD $OUT_DIRCT/$OUT_FILENAME'_ori'/$OUT_FILENAME'.meme' $SCERTF_PFM
	scores_tomtom=$OUT_DIRCT/$OUT_FILENAME'_ori'/tomtom.txt
	# run python code to parse FIRE and tomtom data
	python $DIR_SCRIPT/tomtom_comparison/parse_fire.py -f $scores_fire -o $OUT_DIRCT/$OUT_FILENAME'_ori/scores_fire.txt'
	python $DIR_SCRIPT/tomtom_comparison/parse_tomtom.py -t $scores_tomtom -m $GENE_NAME -o $OUT_DIRCT/$OUT_FILENAME'_ori/scores_tomtom.txt'
fi

# parse new file
if [ -s $NEW_FILE ] 
	then 
	# parse FIRE inference file
	read -r line_newMotif < $NEW_FILE 
	arr_newMotif=($line_newMotif)
	seq_newMotif=${arr_newMotif[0]}
	scores_fire=$OUT_DIRCT/$OUT_FILENAME'_new'/$OUT_FILENAME'_new_FIRE.txt'
	touch $scores_fire
	echo -e "$seq_newMotif\t ${arr_newMotif[2]}\t ${arr_newMotif[4]}\t ${arr_newMotif[5]}" >> $scores_fire
	# create meme file of infered motif and compare motif using tomtom alignment
	python $DIR_SCRIPT/meme_conversion/fire2meme.py $seq_newMotif -o $OUT_DIRCT/$OUT_FILENAME'_new'/$OUT_FILENAME'.meme'
	cd $HOME/usr/meme/bin/
	./tomtom -no-ssc -oc $OUT_DIRCT/$OUT_FILENAME'_new' -eps -verbosity 1 -min-overlap $TOMTOM_MIN_OVERLAP -dist pearson -evalue -thresh $TOMTOM_EVAL_THRESHOLD $OUT_DIRCT/$OUT_FILENAME'_new'/$OUT_FILENAME'.meme' $SCERTF_PFM
	scores_tomtom=$OUT_DIRCT/$OUT_FILENAME'_new'/tomtom.txt
	# run python code to parse FIRE and tomtom data
	python $DIR_SCRIPT/tomtom_comparison/parse_fire.py -f $scores_fire -o $OUT_DIRCT/$OUT_FILENAME'_new/scores_fire.txt'
	python $DIR_SCRIPT/tomtom_comparison/parse_tomtom.py -t $scores_tomtom -m $GENE_NAME -o $OUT_DIRCT/$OUT_FILENAME'_new/scores_tomtom.txt'
fi

# run tomtom alignment using YeTFaSCo motif if can't be aligned with ScerTF
if [ "$USE_YETFASCO" == "1" ]
	then
	if [ -s $ORI_FILE ] && [ -s $NEW_FILE ] && ! [ -s $OUT_DIRCT/$OUT_FILENAME'_ori/scores_tomtom.txt' ] && ! [ -s $OUT_DIRCT/$OUT_FILENAME'_new/scores_tomtom.txt' ]
		then
		# echo $SYS_NAME
		YETFASCO_PFM=$HOME/proj_motifinference/resources/yetfasco_meme/PFM.meme
		cd $HOME/usr/meme/bin
		# original file
		./tomtom -no-ssc -oc $OUT_DIRCT/$OUT_FILENAME'_ori' -eps -verbosity 1 -min-overlap $TOMTOM_MIN_OVERLAP -dist pearson -evalue -thresh $TOMTOM_EVAL_THRESHOLD $OUT_DIRCT/$OUT_FILENAME'_ori'/$OUT_FILENAME'.meme' $YETFASCO_PFM
		python $DIR_SCRIPT/tomtom_comparison/parse_tomtom.py -t $OUT_DIRCT/$OUT_FILENAME'_ori'/tomtom.txt -m $SYS_NAME -o $OUT_DIRCT/$OUT_FILENAME'_ori/scores_tomtom.txt'
		# new file
		./tomtom -no-ssc -oc $OUT_DIRCT/$OUT_FILENAME'_new' -eps -verbosity 1 -min-overlap $TOMTOM_MIN_OVERLAP -dist pearson -evalue -thresh $TOMTOM_EVAL_THRESHOLD $OUT_DIRCT/$OUT_FILENAME'_new'/$OUT_FILENAME'.meme' $YETFASCO_PFM
		python $DIR_SCRIPT/tomtom_comparison/parse_tomtom.py -t $OUT_DIRCT/$OUT_FILENAME'_new'/tomtom.txt -m $SYS_NAME -o $OUT_DIRCT/$OUT_FILENAME'_new/scores_tomtom.txt'
	fi
fi		

# compare scores in orignal and new
touch $OUT_DIRCT/$OUT_FILENAME'_sign_report.txt'
scores_ori_fire=$OUT_DIRCT/$OUT_FILENAME'_ori/scores_fire.txt'
scores_new_fire=$OUT_DIRCT/$OUT_FILENAME'_new/scores_fire.txt'
scores_ori_tomtom=$OUT_DIRCT/$OUT_FILENAME'_ori/scores_tomtom.txt'
scores_new_tomtom=$OUT_DIRCT/$OUT_FILENAME'_new/scores_tomtom.txt'
python $DIR_SCRIPT/tomtom_comparison/compare_ori_new_scores.py -m $scores_ori_fire -n $scores_new_fire -p $scores_ori_tomtom -q $scores_new_tomtom -o $OUT_DIRCT/$OUT_FILENAME'_sign_report.txt' -t $OUT_FILENAME -b $DBD_FAM


