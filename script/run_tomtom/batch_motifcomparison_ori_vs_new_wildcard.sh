#! /bin/bash

process_motif_comparison(){
	local MOTIFS0=(${!1})
	local MOTIFS1=(${!2})
	local DIRCT=$3
	local DBDFAM=$4
	for (( i=0; i<${#MOTIFS0[@]}; i++ ))
	do
		DIRCTORI0=$DIRCT'/original_7mers/'${MOTIFS1[i]}'_FIRE/DNA/'${MOTIFS1[i]}'.summary'
		DIRCTNEW0=$DIRCT'/new_7mers/'${MOTIFS1[i]}'_FIRE/DNA/'${MOTIFS1[i]}'.summary'
		bash motifcomparison_ori_vs_new.sh ${MOTIFS0[i]} $DBDFAM $DIRCTORI0 $DIRCTNEW0 ${MOTIFS1[i]}'_k7'
		DIRCTORI1=$DIRCT'/original_7mers/'${MOTIFS1[i]}'_FIRE/DNA/'${MOTIFS1[i]}'.summary'
		DIRCTNEW1=$DIRCT'/new_7mers_wildcard/'${MOTIFS1[i]}'_FIRE/DNA/'${MOTIFS1[i]}'.summary'
		bash motifcomparison_ori_vs_new.sh ${MOTIFS0[i]} $DBDFAM $DIRCTORI1 $DIRCTNEW1 ${MOTIFS1[i]}'_k7_w'
		DIRCTORI2=$DIRCT'/original_8mers/'${MOTIFS1[i]}'_FIRE/DNA/'${MOTIFS1[i]}'.summary'
		DIRCTNEW2=$DIRCT'/new_8mers/'${MOTIFS1[i]}'_FIRE/DNA/'${MOTIFS1[i]}'.summary'
		bash motifcomparison_ori_vs_new.sh ${MOTIFS0[i]} $DBDFAM $DIRCTORI2 $DIRCTNEW2 ${MOTIFS1[i]}'_k8'
	done
}

DIR_DATA=$HOME/proj_motifinference/resources/yeast

# gata family
GATA_MOTIFS0=( SRD1 GLN3 GAT1 GAT4 GZF3 ASH1 DAL80 GAT3 ECM23 )
GATA_MOTIFS1=( YCR018C YER040W YFL021W YIR013C YJL110C YKL185W YKR034W YLR013W YPL021W ) 
GATA_DIRCT=$DIR_DATA/ChIP_data_gata_fam
GATA_DBDFAM=gata
process_motif_comparison GATA_MOTIFS0[@] GATA_MOTIFS1[@] $GATA_DIRCT $GATA_DBDFAM 

# hlh family
HLH_MOTIFS0=( RTG3 INO2 PHO4 CBF1 RTG1 HMS1 TYE7 )
HLH_MOTIFS1=( YBL103C YDR123C YFR034C YJR060W YOL067C YOR032C YOR344C )
HLH_DIRCT=$DIR_DATA/ChIP_data_hlh_fam
HLH_DBDFAM=hlh
process_motif_comparison HLH_MOTIFS0[@] HLH_MOTIFS1[@] $HLH_DIRCT $HLH_DBDFAM

# homeobox family
HB_MOTIFS0=( HMLALPHA2 MATALPHA2 HMRA2 N/A PHO2 YHP1 TOS8 YOX1 )
HB_MOTIFS1=( YCL067C YCR039C YCR096C YCR097W YDL106C YDR451C YGL096W YML027W )
HB_DIRCT=$DIR_DATA/ChIP_data_homeobox_fam
HB_DBDFAM=homeobox
process_motif_comparison HB_MOTIFS0[@] HB_MOTIFS1[@] $HB_DIRCT $HB_DBDFAM

# hsf family
HSF_MOTIFS0=( HSF1 MGA1 SKN7 HMS2 SFL1 )
HSF_MOTIFS1=( YGL073W YGR249W YHR206W YJR147W YOR140W )
HSF_DIRCT=$DIR_DATA/ChIP_data_hsf_fam
HSF_DBDFAM=hsf
process_motif_comparison HSF_MOTIFS0[@] HSF_MOTIFS1[@] $HSF_DIRCT $HSF_DBDFAM

# znclus family with gapsize > 0
ZNCLUS_MOTIFS0=( OAF1 PUT3 PPR1 ECM22 HAP1 LEU3 PIP2 GAL4 )
ZNCLUS_MOTIFS1=( YAL051W YKL015W YLR014C YLR228C YLR256W YLR451W YOR363C YPL248C )  
ZNCLUS_DIRCT=$DIR_DATA/ChIP_data_znclus_fam/
ZNCLUS_DBDFAM=znclus
for (( i=0; i<${#ZNCLUS_MOTIFS0[@]}; i++ ))
do
	ZNCLUS_DIRCTORI0=$ZNCLUS_DIRCT'/original_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	ZNCLUS_DIRCTNEW0=$ZNCLUS_DIRCT'/new_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	bash motifcomparison_ori_vs_new.sh ${ZNCLUS_MOTIFS0[i]} $ZNCLUS_DBDFAM $ZNCLUS_DIRCTORI0 $ZNCLUS_DIRCTNEW0 ${ZNCLUS_MOTIFS1[i]}'_k6'
	ZNCLUS_DIRCTORI1=$ZNCLUS_DIRCT'/original_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	ZNCLUS_DIRCTNEW1=$ZNCLUS_DIRCT'/new_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6_wildcard/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	bash motifcomparison_ori_vs_new.sh ${ZNCLUS_MOTIFS0[i]} $ZNCLUS_DBDFAM $ZNCLUS_DIRCTORI1 $ZNCLUS_DIRCTNEW1 ${ZNCLUS_MOTIFS1[i]}'_k6_w'
	ZNCLUS_DIRCTORI2=$ZNCLUS_DIRCT'/original_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k8/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	ZNCLUS_DIRCTNEW2=$ZNCLUS_DIRCT'/new_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k8/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	bash motifcomparison_ori_vs_new.sh ${ZNCLUS_MOTIFS0[i]} $ZNCLUS_DBDFAM $ZNCLUS_DIRCTORI2 $ZNCLUS_DIRCTNEW2 ${ZNCLUS_MOTIFS1[i]}'_k8'
done
# znclus family with gapsize = 0
ZNCLUS_MOTIFS0=(  PDR3 PDR1 )
ZNCLUS_MOTIFS1=( YBL005W YGL013C )  
ZNCLUS_DIRCT=$DIR_DATA/ChIP_data_znclus_fam/
ZNCLUS_DBDFAM=znclus
for (( i=0; i<${#ZNCLUS_MOTIFS0[@]}; i++ ))
do
	ZNCLUS_DIRCTORI0=$ZNCLUS_DIRCT'/original_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	ZNCLUS_DIRCTNEW0=$ZNCLUS_DIRCT'/new_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	bash motifcomparison_ori_vs_new.sh ${ZNCLUS_MOTIFS0[i]} $ZNCLUS_DBDFAM $ZNCLUS_DIRCTORI0 $ZNCLUS_DIRCTNEW0 ${ZNCLUS_MOTIFS1[i]}'_k6'
	ZNCLUS_DIRCTORI1=$ZNCLUS_DIRCT'/original_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	ZNCLUS_DIRCTNEW1=$ZNCLUS_DIRCT'/new_kmers/'${ZNCLUS_MOTIFS1[i]}'_FIRE_*_k6_wildcard/DNA/'${ZNCLUS_MOTIFS1[i]}'.summary'
	bash motifcomparison_ori_vs_new.sh ${ZNCLUS_MOTIFS0[i]} $ZNCLUS_DBDFAM $ZNCLUS_DIRCTORI1 $ZNCLUS_DIRCTNEW1 ${ZNCLUS_MOTIFS1[i]}'_k6_w'
done

# # bzip family
# BZIP_MOTIFS0=( YAP6 CAD1 GCN4 ACA1 HAC1 YAP3 CST6 MET28 YAP5 YAP1 SKO1 YAP7 CIN5 )
# BZIP_MOTIFS1=( YDR259C YDR423C YEL009C YER045C YFL031W YHL009C YIL036W YIR017C YIR018W YML007W YNL167C YOL028C YOR028C )
# BZIP_DIRCT=$DIR_DATA/ChIP_data_bzip_fam
# BZIP_DBDFAM=bzip
# process_motif_comparison BZIP_MOTIFS0[@] BZIP_MOTIFS1[@] $BZIP_DIRCT $BZIP_DBDFAM

# summarize all sign reports
SUM_REPORT_DIRT=$DIR_DATA/validation/ChIP_data_comp_ori_vs_new/sum_sign_report.txt
touch $SUM_REPORT_DIRT
REPORT_DIRT=$DIR_DATA/validation/ChIP_data_comp_ori_vs_new/*/*_sign_report.txt
for file in $REPORT_DIRT
do
	if [ -s $file ]
		then
		read line < $file
		echo "$line" >> $SUM_REPORT_DIRT
	fi
done

# stats sum sign report
RANK_REPORT_DIR=$DIR_DATA/validation/ChIP_data_comp_ori_vs_new/stats_sign_report.txt
python $HOME/proj_motifinference/script/tomtom_comparison/stats_sign_reports_wildcard.py $SUM_REPORT_DIRT -o $RANK_REPORT_DIR



