#!/bin/bash

for fichier in `ls clustered_data`
{
	path="clustered_data/${fichier}"
	if [ ! -f "streamcharts/$(cut -d'.' -f1 <<<"$fichier")_1_chart.html" ]; then
		echo $fichier;
		python3 createGraph.py $path;
	fi

	newname="motioncharts/$(cut -d'.' -f1 <<<"$fichier").html"
	if [ ! -f $newname ]; then
		echo "Création motionchart";
		python3 createMotionchart.py $path;
		mv temp.html $newname;
	fi
}
python3 correct_motioncharts.py