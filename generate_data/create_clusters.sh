#!/bin/bash

corpora=("data/sackler_corpus.json" "data/pma_corpus.json" "data/ocr_corpus.json" "data/marie-claire_corpus.json");
for corpus in "${corpora[@]}"
{
	for i in {1..3}
	{
		if [ ! -f "clustered_data/$(cut -d'_' -f1 <<<"$(cut -d'/' -f2 <<<"$corpus")")_${i}.json" ]; then
			echo $corpus $i;
			python3 create_clustered_data.py $corpus $i;
		fi
	}
}



