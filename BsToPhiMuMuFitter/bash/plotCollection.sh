#!/bin/bash

for arg in 'belowJpsiA' 'belowJpsiB' 'belowJpsiC' 'betweenPeaks' 'abovePsi2sA' 'abovePsi2sB' #'summary' 'summaryLowQ2'
do
    echo -e "\n>>>>>>> File: plotCollection.py, Where?: Entering Bin $arg <<<<<<<\n"
    python plotCollection.py $arg
done
