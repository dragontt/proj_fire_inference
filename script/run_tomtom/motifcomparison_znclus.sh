#! /bin/bash
# bash motifcomparison_znclus.sh [AG][AC]GATA[AC]G[ACG] YER040W

MOTIF=$1 # infered motif string
FN=$2    # tf name
USE_YETFASCO=$3	# use YeTFaSCo as complement of ScerTF

dir_data=$HOME/proj_motifinference/resources/yeast/validation/ChIP_data_znclus
dir_pfm_scertf=$HOME/proj_motifinference/resources/scertf_meme/PFM.meme
if [ $USE_YETFASCO == 1 ]
	then
	dir_pfm_yetfasco=$HOME/proj_motifinference/resources/yetfasco/PFM.meme/
fi
mkdir -p $dir_data/$FN

# create meme file of infered motif
motif_fn=$FN'.meme'
python $HOME/proj_motifinference/script/meme_conversion/fire2meme.py $MOTIF -o $dir_data/$FN/$motif_fn

# compare motif using tomtom
cd $HOME/usr/meme/bin/
cmp_out=$FN'_scertf'
./tomtom -no-ssc -oc $dir_data/$FN/$cmp_out -eps -verbosity 1 -min-overlap 5 -dist pearson -evalue -thresh 10 $dir_data/$FN/$motif_fn $dir_pfm_scertf
if [ $USE_YETFASCO == 1 ]
	then
	cmp_out2=$FN'_yetfasco'
fi