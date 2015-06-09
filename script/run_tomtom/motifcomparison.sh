#! /bin/bash
# bash motifcomparison.sh [AG][AC]GATA[AC]G[ACG] YER040W

MOTIF=$1 # infered motif string
FN=$2    # tf name

dir_data=$HOME/proj_motifinference/yeast/tmp_tomtom_validation
mkdir -p ${dir_data}/'tomtom_'${FN}

# create meme file of infered motif
motif_fn=$FN'.meme'
python $HOME/proj_motifinference/script/meme_conversion/fire2meme.py ${MOTIF} -o ${dir_data}/'tomtom_'${FN}/${motif_fn}

# compare motif using tomtom
cd $HOME/usr/meme/bin/
dir_pfm=$HOME/proj_motifinference/resources/scertf_meme/PFM.meme
./tomtom -no-ssc -oc ${dir_data}/'tomtom_'${FN} -eps -verbosity 1 -min-overlap 5 -dist pearson -evalue -thresh 10 ${dir_data}/'tomtom_'${FN}/${motif_fn} $dir_pfm