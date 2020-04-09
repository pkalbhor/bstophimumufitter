#!/bin/bash

#Number of Subsamples N: Put N=1 if to run on BIG Sample 
N=1 
for ((irun=0; irun<1; irun++))
do
for arg in 'belowJpsiA' 'belowJpsiB' 'belowJpsiC' 'betweenPeaks' 'abovePsi2sA' 'abovePsi2sB'
do
    echo -e "\n>>>>>>> File: seqCollection.py, Where?: Entering Bin $arg $irun <<<<<<<\n"
    python seqCollection.py $arg $irun
done
done
