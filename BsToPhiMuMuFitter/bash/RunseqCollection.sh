#!/bin/bash

for arg in 'belowJpsiA' 'belowJpsiB' 'belowJpsiC' 'betweenPeaks' 'abovePsi2sA' 'abovePsi2sB' 'summary' 'summaryLowQ2'
do
    echo -e "\n>>>>>>> File: seqCollection.py, Where?: Entering Bin $arg <<<<<<<\n"
    python seqCollection.py $arg
done
