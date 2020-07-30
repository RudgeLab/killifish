!/usr/bin/bash


for f in $( ls *.py ); do
    echo Processing: $f
    python $HOME/cellmodeller/killifish/scripts/batch.py $f 0 0
done

