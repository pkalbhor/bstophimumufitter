#!/bin/bash

for arg in 'bin1A' 'bin1B' 'bin1C' 'bin3' 'bin5A' 'bin5B' 'bin0' 'summaryLowQ2'
do
    echo -e "\n>>>>>>> File: plotCollection.py, Where?: Entering Bin $arg <<<<<<<\n"
    python plotCollection.py $arg
done
