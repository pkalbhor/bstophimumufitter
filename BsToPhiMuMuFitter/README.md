# BsToPhiMuMuFitter

## Overview of the design

* [`seqCollection.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/seqCollection.py)
* [`StdProcess.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/StdProcess.py)
* [`anaSetup.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/anaSetup.py)

# How to run?

## Standard fitting procedure

Select a pre-defined sequence in [`seqCollection.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/seqCollection.py), and then just

```sh
python seqCollection.py --binKey bin# --seqKey sequence_to_execute
```
Create RooWorkspace objects:
```bash
python seqCollection.py -b all -s buildPdfs
```
Load data
```
python seqCollection.py -b all -s loadMC {Also: -s loadMCGEN, -s loadMCk}
```
Fit efficiency plots:
```bash
python seqCollection.py -b all -s fitEff
```
Fit reco level plots:
```
python seqCollection.py -b all -s fitSig2D
```
Fit GEN level Plots:
```bash
python seqCollection.py -b all -s fitSigMCGEN
```
Create the plots:
```bash
python seqCollection.py -b all -s createplots --list effi
```
Create GEN-RECO comparison plots for signal MCs:
```bash
python seqCollection.py -s createplots --list angular2D_summary_RECO2GEN
```

## Fitter Validation

* [`script/batchTask_simpleToyValidation.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/batchTask_sigMCValidation.py)
Run validation script for low statistics sub-samples:
```bash
python script/batchTask_sigMCValidation.py -b all -t 10 run 0
python script/batchTask_sigMCValidation.py -b all postproc
```
Submit HTCondor job for large set of sub-samples:
```bash
python script/batchTask_sigMCValidation.py -b all -t 2000 submit -q workday -n 1 -s
```

* [`script/batchTask_simpleToyValidation.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/batchTask_simpleToyValidation.py)

## Statistical error

Due to low statistics, Feldman-Cousins method is suggested to estimate statistical uncertainties.
Two scripts are prepared for this procedure.
* Step1 - fitting to profiled toys with [`script/batchTask_profiledFeldmanCousins.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/batchTask_profiledFeldmanCousins.py)

* Step2 - harvest fit results and calculate error with [`script/postporcess_profiledFeldmanCousins.py`](https://github.com/pkalbhor/BsToPhiMuMuFitter/blob/master/BsToPhiMuMuFitter/script/postporcess_profiledFeldmanCousins.py)

## Systematics error

