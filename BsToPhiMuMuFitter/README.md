# BsToPhiMuMuFitter

## Overview of the design

* [`seqCollection.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/seqCollection.py)
* [`StdProcess.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/StdProcess.py)
* [`anaSetup.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/anaSetup.py)

# How to run?
Explore availabe options using
```bash
python seqCollection.py --help
```
## Standard fitting procedure

Select a pre-defined sequence in [`seqCollection.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/seqCollection.py), and then just

```sh
python seqCollection.py --binKey bin# --seqKey sequence_to_execute
```
Create RooWorkspace objects:
```bash
python seqCollection.py -b all -s buildPdfs -y 2016
```
Load data
```
python seqCollection.py -b all -s loadMC -y 2016 {Also: -s loadMCGEN, -s loadMCk}
```
Fit efficiency plots:
```bash
python seqCollection.py -b all -s fitEff -y 2016
```
Fit reco level plots:
```
python seqCollection.py -b all -s fitSig3D -y 2016
```
Fit GEN level Plots:
```bash
python seqCollection.py -b all -s fitSigMCGEN -y 2016
```
Create the plots:
```bash
python seqCollection.py -b all -s createplots -y 2016 --list effi
```
Create GEN-RECO comparison plots for signal MCs:
```bash
python seqCollection.py -s createplots --list summary_RECO2GEN -y 2016
```

## Fitter Validation

* [`script/batchTask_simpleToyValidation.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/batchTask_sigMCValidation.py)
Run validation script for low statistics sub-samples:
```bash
./seqCollection.py -b bin1A -s sigMCValidation -y 2016 -t 100 run 0
./seqCollection.py -s sigMCValidation -y 2016 postproc --forall
```
Submit HTCondor job for large set of sub-samples:
```bash
./seqCollection.py -b bin1A -s sigMCValidation -t 1000 --SimFit submit -n 3 -s
```
`--SimFit` for simultaneous fit

## Statistical error

Due to low statistics, Feldman-Cousins method is suggested to estimate statistical uncertainties.
Two scripts are prepared for this procedure.
* Step1 - fitting to profiled toys with [`script/batchTask_profiledFeldmanCousins.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/batchTask_profiledFeldmanCousins.py)

* Step2 - harvest fit results and calculate error with [`script/postporcess_profiledFeldmanCousins.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/postporcess_profiledFeldmanCousins.py)

## Systematics error

## Collecting Results
* Table of status of fits
```bash
./seqCollection.py -s StatusTable -y 2018 MakeTables --TSeq sigAFitter sig3DFitter
```
`--TSeq` option is used to fetch results of different fit sequences. Example options are `sig3DFitter`, `bkgCombAFitter`, `finalFitter_WithKStar`, ...

* Table of Efficiency values
```bash
./seqCollection.py -s EffiTable -y 2016
```

* Table of Peaking Background Fractions
```bash
./seqCollection.py -s PeakFracTable -y 2016
```

