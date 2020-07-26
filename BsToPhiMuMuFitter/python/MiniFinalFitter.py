# Description : Final fitter using minimum package modules
#
# Author      : Pritam Kalbhor (physics.pritam@gmail.com)
#
#-----------------------------------------------------------------------

import os, sys, pdb, shelve
import ROOT
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from BsToPhiMuMuFitter.varCollection import Bmass, CosThetaK, CosThetaL, Mumumass, Phimass
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

#----------------------------
# Create DataSet and PDFs
#----------------------------
dfile=ROOT.TFile.Open(modulePath+"/data/preload_dataReader_bin0.root")
data=dfile.Get('dataReader.Fit')

pfile=ROOT.TFile.Open(modulePath+"/input/wspace_bin0.root")
wspace = pfile.Get('wspace.bin0')
pdf = wspace.obj('f_final')

#----------------------------
# Assemble TMinuit Minimizer
#----------------------------




#----------------------------
# Plot Post-Fit Distributions
#----------------------------
pdb.set_trace()
odbfile = modulePath+"/Plots/fitResults_bin0.db"
args = pdf.getParameters(ROOT.RooArgSet(Bmass, CosThetaK, CosThetaL, Mumumass, Phimass))
FitDBPlayer.initFromDB(odbfile, args)
args = pdf.getParameters(ROOT.RooArgSet(Bmass, CosThetaK, CosThetaL))

nSigDB = args.find('nSig').getVal()
nSigErrorDB = args.find('nSig').getError()
nBkgCombDB = args.find('nBkgComb').getVal()
nBkgCombErrorDB = args.find('nBkgComb').getError()

#flDB = unboundFlToFl(args.find('unboundFl').getVal())
#afbDB = unboundAfbToAfb(args.find('unboundAfb').getVal(), flDB)

###
obs=pdf.getObservables(data)
obs.find('Bmass').setRange("sigRegion", 5.2, 5.6) 
Bmass.setRange("sigRegion")
sigFrac = pdf.createIntegral(obs, ROOT.RooFit.NormSet(obs), ROOT.RooFit.Range("sigRegion")).getVal()

frameB=Bmass.frame(5.2,5.6)
data.plotOn(frameB, ROOT.RooFit.CutRange("sigRegion"))
pdf.plotOn(frameB)#, ROOT.RooFit.Normalization(data.sumEntries(), ROOT.RooAbsReal.NumEvent), ROOT.RooFit.Range("sigRegion"))
frameB.Draw()
os.system('root -l')
