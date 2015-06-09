#! /bin/bash

znclus_list=( YBL066C YBR033W YBR150C YBR239C YBR240C YBR297W YCR106W YDL170W YDR034C YDR207C YDR213W YDR303C YDR421W YDR520C YER184C YFL052W YGR288W YHR056C YHR178W YIL130W YIR023W YJL089W YJL103C YJL206C YKL038W YKL222C YKR064W YLL054C YLR098C YLR266C YLR278C YML099C YMR019W YMR168C YMR280C YNR063W YOL089C YOR162C YOR172W YOR337W YOR380W YPL133C YPR196W )

for (( i=0; i<${#znclus_list[@]}; i++ ))
do
	# gapped dimmer-constrained k-mers (k = 6 or 8) with unknown gap size
	bash process_chip_znclus_unknowngapsize.sh ${znclus_list[i]} 6
done
