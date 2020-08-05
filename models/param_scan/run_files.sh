!/usr/bin/bash


for f in $( ls *.py ); do
    echo Processing: $f
    for i in {1..10}; do
	echo Iteration: $i
    	python $HOME/Code/killifish/scripts/batch.py $f 0 0
    done
done

