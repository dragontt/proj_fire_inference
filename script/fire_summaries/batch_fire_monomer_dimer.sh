#! /bin/bash

motifs=( YAL051W YBL005W YGL013C YKL015W YLR014C YLR256W YLR228C YLR451W YOR363C YPL248C YBL066C YBR033W YBR150C YBR239C YBR240C YBR297W YCR106W YDL170W YDR034C YDR207C YDR213W YDR303C YDR421W YDR520C YER184C YFL052W YGR288W YHR056C YHR178W YIL130W YIR023W YJL089W YJL103C YJL206C YKL038W YKL222C YKR064W YLL054C YLR098C YLR266C YLR278C YML099C YMR019W YMR168C YMR280C YNR063W YOL089C YOR162C YOR172W YOR337W YOR380W YPL133C YPR196W ) 
dir_dim=$HOME/proj_motifinference/resources/yeast/ChIP_data_znclus_fam/new_unknowngapsize
dir_mono=$HOME/proj_motifinference/resources/yeast/ChIP_data_znclus_fam/new_monomer

# robustness 10
for (( i=0; i<${#motifs[@]}; i++ ))
do 
	input_dim=$dir_dim/${motifs[i]}'_FIRE_tmp_k6/summary_list.txt'
	input_mono=$dir_mono/${motifs[i]}'_FIRE_tmp_k6/DNA/'${motifs[i]}'.summary'
	output=$HOME/proj_motifinference/resources/yeast/ChIP_data_znclus_fam/new_combined_monomer_dimer/${motifs[i]}'summary_monomer_dimer_rank.txt'
	python combine_znclus_monomer_dimer.py -m $input_mono -d $input_dim -o $output
done

# # robustness 20
# for (( i=0; i<${#motifs[@]}; i++ ))
# do 
# 	input=$dir/${motifs[i]}'_FIRE_tmp_k6_rb20/summary_list.txt'
# 	output=$dir/${motifs[i]}'_FIRE_tmp_k6_rb20/summary_list_ranked.txt'
# 	python process_fire_summaries.py $input -o $output
# done
