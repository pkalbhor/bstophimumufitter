#!/bin/bash

for arg in 'belowJpsiA' 'belowJpsiB' 'belowJpsiC' 'betweenPeaks' 'abovePsi2sA' 'abovePsi2sB'
do
    echo -e "\n>>>>>>> File: seqCollection.py, Where?: Entering Bin $arg <<<<<<<\n"
    python seqCollection.py -b $arg -s fitall
done
