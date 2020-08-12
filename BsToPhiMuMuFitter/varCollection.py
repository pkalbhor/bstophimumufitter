#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Description     : Shared object definition.

from ROOT import RooRealVar
from ROOT import RooArgSet
from BsToPhiMuMuFitter.anaSetup import bMassRegions

Bmass = RooRealVar("Bmass","m_{#phi#mu#mu} [GeV]", 4.5, 6.0)
for regName, regCfg in bMassRegions.items():
    # Remark: Only regions defined while running pdfCollection could be used in ROOT.RooFit(regionName)
    regName=Bmass.setRange(regName, regCfg['range'][0], regCfg['range'][1])
CosThetaK   = RooRealVar("CosThetaK", "cos#theta_{K}", -1., 1.)
CosThetaL   = RooRealVar("CosThetaL", "cos#theta_{l}", -1., 1.)
Mumumass    = RooRealVar("Mumumass", "m_{#mu#mu} [GeV]", 0., 10.)
Mumumasserr = RooRealVar("Mumumasserr", "Error of m_{#mu#mu} [GeV]", 0., 10.)
Phimass     = RooRealVar("Phimass", "m_{K^{+} K^{-}} [GeV]", 0.5, 1.5)
Q2          = RooRealVar("Q2", "q^{2} [GeV^{2}]", 0.0, 20.)
Triggers    = RooRealVar("Triggers", "", 0, 10)
JpsiTriggers = RooRealVar("JpsiTriggers", "", 0, 1)
PsiPTriggers = RooRealVar("PsiPTriggers", "", 0, 1)
LMNTTriggers = RooRealVar("LMNTTriggers", "", 0, 1)
Bdt         = RooRealVar("Bdt", "", -0.5, 1.)
Mupeta      = RooRealVar("Mupeta", "#mu_{+}(#eta)", -10, 10)
Mumeta      = RooRealVar("Mumeta", "#mu_{-}(#eta)", -10, 10)
Muppt       = RooRealVar("Muppt", "#mu_{+}(pt)", 0, 2000)
Mumpt       = RooRealVar("Mumpt", "#mu_{-}(pt)", 0, 2000)
Kppt        = RooRealVar("Kppt", "#K_{+}(pt)", 0, 2000)
Kmpt        = RooRealVar("Kmpt", "#K_{-}(pt)", 0, 2000)
Kpeta       = RooRealVar("Kpeta", "#K_{+}(#eta)", -10, 10)
Kmeta       = RooRealVar("Kmeta", "#K_{-}(#eta)", -10, 10)
mtrkqual    = RooRealVar("mtrkqual", "#K_{-}(TrackQual)", 0, 1)
ptrkqual    = RooRealVar("ptrkqual", "#K_{+}(TrackQual)", 0, 1)
dr0         = RooRealVar("dr0", "#Delta_{0}(R)", 0, 100)
dr1         = RooRealVar("dr1", "#Delta_{1}(R)", 0, 100)
Kptrkdcasigbs = RooRealVar("Kptrkdcasigbs", "#K_{+}(dca)", 0, 500)
Kmtrkdcasigbs = RooRealVar("Kmtrkdcasigbs", "#K_{-}(dca)", 0, 500)

#Not used
genMupEta      = RooRealVar("genMupEta", "#mu_{+}^{gen}(#eta)", -10, 10)
genMumEta      = RooRealVar("genMumEta", "#mu_{-}^{gen}(#eta)", -10, 10)
genMupPt       = RooRealVar("genMupPt", "#mu_{+}^{gen}(pt)", 0, 2000)
genMumPt       = RooRealVar("genMumPt", "#mu_{-}^{gen}(pt)", 0, 2000)
genKpPt        = RooRealVar("genKpPt", "#K_{+}^{gen}(pt)", 0, 2000)
genKmPt        = RooRealVar("genKmPt", "#K_{-}^{gen}(pt)", 0, 2000)
genKpEta       = RooRealVar("genKpEta", "#K_{+}^{gen}(#eta)", -10, 10)
genKmEta       = RooRealVar("genKmEta", "#K_{-}^{gen}(#eta)", -10, 10)

#For K*0mumu DataSet
LMNTTriggersdr0 = RooRealVar("LMNTTriggersdr0", "LMNTTriggersdr0", 0, 1e8)
LMNTTriggersdr1 = RooRealVar("LMNTTriggersdr1", "LMNTTriggersdr1", 0, 1e8)
JpsiTriggersdr0 = RooRealVar("JpsiTriggersdr0", "JpsiTriggersdr0", 0, 1e8)
JpsiTriggersdr1 = RooRealVar("JpsiTriggersdr1", "JpsiTriggersdr1", 0, 1e8)
PsiPTriggersdr0 = RooRealVar("PsiPTriggersdr0", "PsiPTriggersdr0", 0, 1e8)
PsiPTriggersdr1 = RooRealVar("PsiPTriggersdr1", "PsiPTriggersdr1", 0, 1e8)

TriggerBase = RooArgSet(JpsiTriggers, PsiPTriggers, LMNTTriggers, mtrkqual, ptrkqual, dr0, dr1)
VarSet = RooArgSet(Bmass, CosThetaK, CosThetaL, Mumumass, Mumumasserr, Phimass, Bdt)
dataArgs = RooArgSet(VarSet, TriggerBase, "RooArgSet for Data and MC")

#For producing K*0mumu DataSet
TriggerBaseKstar = RooArgSet(JpsiTriggers, PsiPTriggers, LMNTTriggers, mtrkqual, ptrkqual)
DRVars           = RooArgSet(LMNTTriggersdr0, LMNTTriggersdr1, JpsiTriggersdr0, JpsiTriggersdr1, PsiPTriggersdr0, PsiPTriggersdr1)
TrigBaseDR      = RooArgSet(TriggerBaseKstar, DRVars, "RooArgSet, trigger, dr, trackQual")
dataArgsKStar   = RooArgSet(VarSet, TrigBaseDR, "RooArgSet for bd->K*0mumu MC")

genCosThetaK = RooRealVar("genCosThetaK", "cos#theta_{K}", -1., 1.)
genCosThetaL = RooRealVar("genCosThetaL", "cos#theta_{l}", -1., 1.)
genQ2        = RooRealVar("genQ2", "q^{2} [GeV^{2}]", 0.1, 20.)
dataArgsGEN = RooArgSet(
    genQ2,
    genCosThetaK,
    genCosThetaL)
