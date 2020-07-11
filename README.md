# BsToPhiMuMuFitter

This fitter package is designed for ![](http://latex.codecogs.com/svg.latex?B_{s}^{0}\rightarrow{\Phi^{0}\mu\mu}) angular analysis with CMS Run2016/17/18 data.

The core of the fitting procedure, i.e. parts not for this particular analysis, are collected in `v2Fitter` directory. It may be re-used for future works. On the other hand, the customized ones are placed in `BsToPhiMuMuFitter` directory. Please check the `README.md` in each directory for further information

# Setup

The package depends on python2.7 and pyROOT.

On lxplus, run: (Every time you start Fitter session)

```bash
source setup_ROOTEnv.sh
```

For the first time, you may need to install following pre-requisites with

```bash
pip install --user enum34
```

# Instructions 
Clean junk files:
```bash
TotalClean
```
Create RooWorkspace objects:
```bash
python seqCollection.py -b all -s buildPdfs
```
Create efficiency plots and fit efficiency + RECO level Plots:
```bash
python seqCollection.py -b all -s fitall
```
Fit GEN level Plots:
```bash
python seqCollection.py -b all -s fitSigMCGEN
```
Create the plots:
```bash
python seqCollection.py -b all -s createplots --list effi
```
Transfer fitter result for futher calculation:
```bash
cp Plots/*.db input/selected
```
Create GEN-RECO comparison plots for signal MCs:
```bash
python seqCollection.py -s createplots
```
Run validation script for low statistics sub-samples:
```bash
python script/batchTask_sigMCValidation.py -b all -t 10 run 0
python script/batchTask_sigMCValidation.py -b all postproc
```
Submit HTCondor job for large set of sub-samples:
```bash
python script/batchTask_sigMCValidation.py -b all -t 2000 submit -q workday -n 1 -s
```
