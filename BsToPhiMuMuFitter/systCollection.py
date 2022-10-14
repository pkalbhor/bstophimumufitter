#!/usr/bin/env python
# vim: set sts=4 sw=4 fdm=indent fdn=3 et:

#!/usr/bin/env python
# vim: set sts=4 sw=4 fdm=indent fdl=0 fdn=2 et:

from __future__ import print_function, division

import os
import sys
import math
import types
import shelve
import functools
import itertools
import tempfile, datetime
from copy import copy, deepcopy
from collections import OrderedDict

import ROOT
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.varCollection as varCollection
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection
import BsToPhiMuMuFitter.plotCollection as plotCollection
from BsToPhiMuMuFitter.StdProcess import createNewProcess

from v2Fitter.Fitter.ObjProvider import ObjProvider
from v2Fitter.Fitter.FitterCore import FitterCore
from v2Fitter.Fitter.AbsToyStudier import AbsToyStudier
from v2Fitter.Fitter.DataReader import DataReader
from BsToPhiMuMuFitter.anaSetup import modulePath, q2bins, bMassRegions
from BsToPhiMuMuFitter.StdFitter import StdFitter, unboundFlToFl, unboundAfbToAfb
from BsToPhiMuMuFitter.EfficiencyFitter import EfficiencyFitter
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.Plotter import Plotter
from BsToPhiMuMuFitter.seqCollection import Instantiate
from BsToPhiMuMuFitter.python.datainput import GetInputFiles

# Simultaneous Fit: Limited MC size
# # Determinded by varying efficiency map with FitDBPlayer.fluctuateFromDB.
def func_randEffi_simultaneous(args):
    """ Typically less than 5% """
    p = createNewProcess("systProcess", "plots_simultaneous")
    p.cfg['args'] = deepcopy(args)
    p.cfg['sysargs'] = sys.argv
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['binKey'] = p.cfg['bins'][0]
    
    finalRandEffiFitter = fitCollection.SimFitter_Final_WithKStar
    setupFinalRandEffiFitter = finalRandEffiFitter.cfg
    setupFinalRandEffiFitter.update({
        'argAliasInDB': {'unboundAfb':'unboundAfb_randEffiSim', 'unboundFl':'unboundFl_randEffiSim'},
        'argAliasFromDB': {**fitCollection.ArgAliasGEN},
    })

    def preFitSteps_randEffi(self):
        self.args = self.minimizer.getParameters(self.dataWithCategories)
        for pdf, data, Year in zip(self.pdf, self.data, self.Years):
            args = pdf.getParameters(self.dataWithCategories)
            odbfile = os.path.join(self.process.cwd, "plots_{0}".format(Year), self.process.dbplayer.odbfile)
            if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(odbfile, args, aliasDict=self.cfg['argAliasFromDB'])

            # Fluctuate cross-term correction w/o considering the correlation
            effiArgs = ROOT.RooArgSet()
            FitterCore.ArgLooper(args, lambda iArg: effiArgs.add(iArg), targetArgs=[r"x\d{1,2}", r"^l\d+\w*", r"^k\d+\w*"])
            FitDBPlayer.fluctuateFromDB(odbfile, effiArgs, self.cfg['argAliasInDB'])

            self.ToggleConstVar(args, True)
            # Rename parameter names
            FitterCore.ArgLooper(args, lambda p: p.SetName(p.GetName()+"_{0}".format(Year)), targetArgs=self.cfg['argPattern'], inverseSel=True) 
        self.ToggleConstVar(self.minimizer.getParameters(self.dataWithCategories), False, self.cfg['argPattern'])

    finalRandEffiFitter._preFitSteps = types.MethodType(preFitSteps_randEffi, finalRandEffiFitter)

    os.makedirs(os.path.join(modulePath, p.work_dir, "randEffi"), exist_ok=True)
    foutName = "syst_randEffi_{0}.root".format(args.binKey)
    class effiStudier(AbsToyStudier):
        def _preSetsLoop(self):
            self.hist_afb = ROOT.TH1F("hist_afb", "", 300, -1., 1.)
            self.hist_afb.GetXaxis().SetTitle("A_{6}")
            self.hist_fl = ROOT.TH1F("hist_fl", "", 200, 0., 1.)
            self.hist_fl.GetXaxis().SetTitle("F_{L}")

        def _preRunFitSteps(self, setIndex):
            pass

        def _postRunFitSteps(self, setIndex):
            if self.fitter.fitter.fitResult['{}.StdFitter'.format(self.fitter.name)]['covQual'] == 3:
                unboundAfb = self.fitter.args.find('unboundAfb').getVal()
                unboundFl = self.fitter.args.find('unboundFl').getVal()
                fl = unboundFlToFl(unboundFl)
                afb = unboundAfbToAfb(unboundAfb, fl)
                # afb = self.process.sourcemanager.get('afb.{}'.format(args.Year))
                # fl = self.process.sourcemanager.get('fl.{}'.format(args.Year))
                self.hist_afb.Fill(afb)
                self.hist_fl.Fill(fl)

        def _postSetsLoop(self):
            os.chdir(os.path.join(modulePath, p.work_dir, "randEffi"))
            fout = ROOT.TFile(foutName, "RECREATE")
            fout.cd()
            self.hist_afb.Write()
            self.hist_fl.Write()
            fout.Close()

        def getSubDataEntries(self, setIndex, Type, Year=2016):
            return 1

        def getSubData(self, idx):
            while True:
                yield self.data[0]

    setupStudier = deepcopy(effiStudier.templateConfig())
    setupStudier.update({
        'name': "effiStudier",
        'data': ["dataReader.{}.Fit".format(args.Year)],
        'Type': [(0, 'nSig', 'Sim')],
        'fitter': finalRandEffiFitter,
        'nSetOfToys': 200,
        'Spread': 'Gaus',
    })
    studier = effiStudier(setupStudier)

    def runSimSequences():
        for Year in [2016, 2017, 2018]:
            p.cfg['args'].Year=Year
            GetInputFiles(p)
            sequence=Instantiate(p, ['dataReader', 'stdWspaceReader'])
            p.setSequence(sequence)
            p.beginSeq()
            p.runSeq()
        p.cfg['args'].Year=args.Year
    runSimSequences()

    p.setSequence([studier])
    try:
        p.beginSeq()
        if os.path.exists("{0}".format(foutName)):
            print("{0} exists, skip fitting procedure".format(foutName))
        else:
            p.runSeq()

        if not args.isBatchTask:
            ROOT.gStyle.SetOptStat("r")
            ROOT.gStyle.SetOptFit(11)

            fin = ROOT.TFile("{0}".format(foutName))

            hist_fl = fin.Get("hist_fl")
            hist_fl.UseCurrentStyle()
            gaus_fl = ROOT.TF1("gaus_fl", "gaus(0)", .3, .9)
            hist_fl.Fit(gaus_fl, "MR")

            hist_afb = fin.Get("hist_afb")
            hist_afb.UseCurrentStyle()
            gaus_afb = ROOT.TF1("gaus_afb", "gaus(0)", -0.5, 0.5)
            hist_afb.Fit(gaus_afb, "MR")

            syst_randEffi = {
                'syst_randEffi_fl': {
                    'getError': gaus_fl.GetParameter(2),
                    'getErrorHi': gaus_fl.GetParameter(2),
                    'getErrorLo': -gaus_fl.GetParameter(2),
                },
                'syst_randEffi_afb': {
                    'getError': gaus_afb.GetParameter(2),
                    'getErrorHi': gaus_afb.GetParameter(2),
                    'getErrorLo': -gaus_afb.GetParameter(2),
                }
            }
            print(syst_randEffi)

            if args.updatePlot:
                canvas = Plotter.canvas.cd()
                hist_afb.GetXaxis().SetTitle("A_{FB}")
                hist_afb.Draw("HIST")
                hist_afb.GetXaxis().SetRangeUser(-0.5, 0.5)
                gaus_afb.Draw("SAME")
                Plotter.latexCMSMark()
                Plotter.latexQ2(p.cfg['binKey'])
                Plotter.latexCMSExtra()
                canvas.Print("syst_randEffi_afb_{0}.pdf".format(args.binKey))

                hist_fl.GetXaxis().SetTitle("F_{L}")
                hist_fl.Draw("HIST")
                hist_fl.GetXaxis().SetRangeUser(0.3, 0.9)
                gaus_fl.Draw("SAME")
                Plotter.latexCMSMark()
                Plotter.latexQ2(p.cfg['binKey'])
                Plotter.latexCMSExtra()
                canvas.Print("syst_randEffi_fl_{0}.pdf".format(args.binKey))
            os.chdir(os.path.join(modulePath, p.work_dir))
            if args.updateDB:
                FitDBPlayer.UpdateToDB(os.path.join(p.dbplayer.absInputDir, p.dbplayer.odbfile), syst_randEffi)
    finally:
        p.endSeq()


# Limited MC size
# # Determinded by varying efficiency map with FitDBPlayer.fluctuateFromDB.
def func_randEffi(args):
    """ Typically less than 5% """
    p = createNewProcess("systProcess", "plots_{}".format(args.Year))
    p.cfg['args'] = deepcopy(args)
    p.cfg['sysargs'] = sys.argv
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['binKey'] = p.cfg['bins'][0]
    
    finalRandEffiFitter = fitCollection.GetFitterObjects(p, "finalFitter_WithKStar")
    setupFinalRandEffiFitter = finalRandEffiFitter.cfg
    setupFinalRandEffiFitter.update({
        'FitMinos': [False, ()],
        'argAliasInDB': {'unboundAfb': 'unboundAfb_randEffi', 'unboundFl': 'unboundFl_randEffi', 'nSig': 'nSig_randEffi', 'nBkgComb': 'nBkgComb_randEffi', 'bkgCombM_c1': 'bkgCombM_c1_randEffi'},
        'argAliasFromDB': {**fitCollection.ArgAliasGEN},
        'saveToDB': False,
    })
    finalRandEffiFitter = StdFitter(setupFinalRandEffiFitter)

    def preFitSteps_randEffi(self):
        self.args = self.pdf.getParameters(self.data)
        self._preFitSteps_initFromDB()

        # Fluctuate cross-term correction w/o considering the correlation
        effiArgs = ROOT.RooArgSet()
        FitterCore.ArgLooper(self.args, lambda iArg: effiArgs.add(iArg), targetArgs=[r"x\d{1,2}", r"^l\d+\w*", r"^k\d+\w*"])
        FitDBPlayer.fluctuateFromDB(self.process.dbplayer.odbfile, effiArgs, self.cfg['argAliasInDB'])

        self._preFitSteps_vetoSmallFs()
        self._preFitSteps_preFit()

    finalRandEffiFitter._preFitSteps = types.MethodType(preFitSteps_randEffi, finalRandEffiFitter)

    os.makedirs(os.path.join(modulePath, p.work_dir, "randEffi"), exist_ok=True)
    foutName = "syst_randEffi_{0}.root".format(args.binKey)
    class effiStudier(AbsToyStudier):
        def _preSetsLoop(self):
            self.hist_afb = ROOT.TH1F("hist_afb", "", 300, -1., 1.)
            self.hist_afb.GetXaxis().SetTitle("A_{6}")
            self.hist_fl = ROOT.TH1F("hist_fl", "", 200, 0., 1.)
            self.hist_fl.GetXaxis().SetTitle("F_{L}")

        def _preRunFitSteps(self, setIndex):
            pass

        def _postRunFitSteps(self, setIndex):
            if self.fitter.fitResult['{}.StdFitter'.format(self.fitter.name)]['covQual'] == 3:
                unboundAfb = self.fitter.args.find('unboundAfb').getVal()
                unboundFl = self.fitter.args.find('unboundFl').getVal()
                Fl = unboundFlToFl(unboundFl)
                Afb = unboundAfbToAfb(unboundAfb, Fl)
                afb = self.process.sourcemanager.get('afb.{}'.format(args.Year))
                fl = self.process.sourcemanager.get('fl.{}'.format(args.Year))
                self.hist_afb.Fill(afb.getVal())
                self.hist_fl.Fill(fl.getVal())

        def _postSetsLoop(self):
            os.chdir(os.path.join(modulePath, p.work_dir, "randEffi"))
            fout = ROOT.TFile(foutName, "RECREATE")
            fout.cd()
            self.hist_afb.Write()
            self.hist_fl.Write()
            fout.Close()

        def getSubDataEntries(self, setIndex, Type, Year=2016):
            return 1

        def getSubData(self, idx):
            while True:
                yield self.data[0]

    setupStudier = deepcopy(effiStudier.templateConfig())
    setupStudier.update({
        'name': "effiStudier",
        'data': ["dataReader.{}.Fit".format(args.Year)],
        'Type': [(0, 'nSig', 'Sim')],
        'fitter': finalRandEffiFitter,
        'nSetOfToys': 20 if args.isBatchTask else 300,
    })
    studier = effiStudier(setupStudier)

    sequence = Instantiate(p, ['dataReader', 'stdWspaceReader'])
    sequence.append(studier)
    p.setSequence(sequence)
    try:
        p.beginSeq()
        if os.path.exists("{0}".format(foutName)):
            print("{0} exists, skip fitting procedure".format(foutName))
        else:
            p.runSeq()

        if not args.isBatchTask:
            ROOT.gStyle.SetOptStat("r")
            ROOT.gStyle.SetOptFit(11)

            fin = ROOT.TFile("{0}".format(foutName))

            hist_fl = fin.Get("hist_fl")
            hist_fl.UseCurrentStyle()
            gaus_fl = ROOT.TF1("gaus_fl", "gaus(0)", .3, .9)
            hist_fl.Fit(gaus_fl, "MR")

            hist_afb = fin.Get("hist_afb")
            hist_afb.UseCurrentStyle()
            gaus_afb = ROOT.TF1("gaus_afb", "gaus(0)", -0.5, 0.5)
            hist_afb.Fit(gaus_afb, "MR")

            syst_randEffi = {
                'syst_randEffi_fl': {
                    'getError': gaus_fl.GetParameter(2),
                    'getErrorHi': gaus_fl.GetParameter(2),
                    'getErrorLo': -gaus_fl.GetParameter(2),
                },
                'syst_randEffi_afb': {
                    'getError': gaus_afb.GetParameter(2),
                    'getErrorHi': gaus_afb.GetParameter(2),
                    'getErrorLo': -gaus_afb.GetParameter(2),
                }
            }
            print(syst_randEffi)

            if args.updatePlot:
                canvas = Plotter.canvas.cd()
                hist_afb.GetXaxis().SetTitle("A_{FB}")
                hist_afb.Draw("HIST")
                hist_afb.GetXaxis().SetRangeUser(-0.5, 0.5)
                gaus_afb.Draw("SAME")
                Plotter.latexCMSMark()
                Plotter.latexQ2(p.cfg['binKey'])
                Plotter.latexCMSExtra()
                canvas.Print("syst_randEffi_afb_{0}.pdf".format(args.binKey))

                hist_fl.GetXaxis().SetTitle("F_{L}")
                hist_fl.Draw("HIST")
                hist_fl.GetXaxis().SetRangeUser(0.3, 0.9)
                gaus_fl.Draw("SAME")
                Plotter.latexCMSMark()
                Plotter.latexQ2(p.cfg['binKey'])
                Plotter.latexCMSExtra()
                canvas.Print("syst_randEffi_fl_{0}.pdf".format(args.binKey))
            os.chdir(os.path.join(modulePath, p.work_dir))
            if args.updateDB:
                FitDBPlayer.UpdateToDB(os.path.join(p.dbplayer.absInputDir, p.dbplayer.odbfile), syst_randEffi)
    finally:
        p.endSeq()

# Alternate efficiency map
# # Use uncorrelated efficiency map and compare the difference
def updateToDB_altShape(p, tag):
    """ Template db entry maker for syst """
    db = shelve.open(p.dbplayer.odbfile)
    nominal_fl = unboundFlToFl(db['unboundFl']['getVal'])
    nominal_afb = unboundAfbToAfb(db['unboundAfb']['getVal'], nominal_fl)
    # afb = p.sourcemanager.get('afb').getVal()
    # fl = p.sourcemanager.get('fl').getVal()
    fl = unboundFlToFl(db['unboundFl_{}'.format(tag)]['getVal'])
    afb = unboundAfbToAfb(db['unboundAfb_{}'.format(tag)]['getVal'], fl)
    db.close()

    syst_altShape = {}
    syst_altShape['syst_{0}_afb'.format(tag)] = {
        'getError': math.fabs(afb - nominal_afb),
        'getErrorHi': math.fabs(afb - nominal_afb),
        'getErrorLo': -1 * math.fabs(afb - nominal_afb),
    }
    syst_altShape['syst_{0}_fl'.format(tag)] = {
        'getError': math.fabs(fl - nominal_fl),
        'getErrorHi': math.fabs(fl - nominal_fl),
        'getErrorLo': -1 * math.fabs(fl - nominal_fl),
    }
    print(syst_altShape)

    if args.updateDB:
        FitDBPlayer.UpdateToDB(p.dbplayer.odbfile, syst_altShape)

def func_altEffi(args):
    """ Typically less than 1% """
    p = createNewProcess("systProcess", "plots_simultaneous")
    p.cfg['args'] = deepcopy(args)
    p.cfg['sysargs'] = sys.argv
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['binKey'] = p.cfg['bins'][0]
    
    finalAltEffFitter = fitCollection.SimFitter_Final_WithKStar
    finalAltEffFitter.cfg.update({
        'argAliasInDB': {'unboundAfb': 'unboundAfb_altEffi', 'unboundFl': 'unboundFl_altEffi'},
        'saveToDB': True,
    })

    def preFitSteps_altEffi(self):
        self.args = self.minimizer.getParameters(self.dataWithCategories)
        
        for pdf, data, Year in zip(self.pdf, self.data, self.Years):
            args = pdf.getParameters(self.dataWithCategories)
            odbfile = os.path.join(self.process.cwd, "plots_{0}".format(Year), self.process.dbplayer.odbfile)
            if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(odbfile, args, aliasDict=self.cfg['argAliasFromDB'])

            args.find("hasXTerm_ts").setVal(0)

            self.ToggleConstVar(args, True)
            # Rename parameter names
            FitterCore.ArgLooper(args, lambda p: p.SetName(p.GetName()+"_{0}".format(Year)), targetArgs=self.cfg['argPattern'], inverseSel=True) 
        self.ToggleConstVar(self.minimizer.getParameters(self.dataWithCategories), False, self.cfg['argPattern'])

    finalAltEffFitter._preFitSteps = types.MethodType(preFitSteps_altEffi, finalAltEffFitter)

    def runSimSequences():
        for Year in [2016, 2017, 2018]:
            p.cfg['args'].Year=Year
            GetInputFiles(p)
            sequence=Instantiate(p, ['dataReader', 'stdWspaceReader'])
            p.setSequence(sequence)
            p.beginSeq()
            p.runSeq()
        p.cfg['args'].Year=args.Year
    runSimSequences()
    p.setSequence([finalAltEffFitter])

    try:
        p.beginSeq()
        p.runSeq()

        updateToDB_altShape(p, "altEffi")
    finally:
        p.endSeq()

# Simulation mismodeling
# # Quote the difference between fitting results of unfiltered GEN and that of high stat RECO.
def func_simMismodel(args):
    p = createNewProcess("systProcess", "plots_{}".format('simultaneous' if args.SimFit else args.Year))
    p.cfg['args'] = deepcopy(args)
    p.cfg['sysargs'] = sys.argv
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['binKey'] = p.cfg['bins'][0]
    
    p.setSequence([])
    try:
        p.beginSeq()
        db = shelve.open(p.dbplayer.odbfile)
        fl_GEN = unboundFlToFl(db['unboundFl_GEN']['getVal'])
        fl_RECO = unboundFlToFl(db['unboundFl_RECO']['getVal'])
        afb_GEN = unboundAfbToAfb(db['unboundAfb_GEN']['getVal'], fl_GEN)
        afb_RECO = unboundAfbToAfb(db['unboundAfb_RECO']['getVal'], fl_RECO)
        db.close()
        syst_simMismodel = {
            'syst_simMismodel_fl': {
                'getError': math.fabs(fl_GEN - fl_RECO),
                'getErrorHi': math.fabs(fl_GEN - fl_RECO),
                'getErrorLo': -math.fabs(fl_GEN - fl_RECO),
            },
            'syst_simMismodel_afb': {
                'getError': math.fabs(afb_GEN - afb_RECO),
                'getErrorHi': math.fabs(afb_GEN - afb_RECO),
                'getErrorLo': -math.fabs(afb_GEN - afb_RECO),
            }
        }
        print(syst_simMismodel)

        if args.updateDB:
            FitDBPlayer.UpdateToDB(p.dbplayer.odbfile, syst_simMismodel)
    finally:
        p.endSeq()

# Alternate sigM shape
# # Use single Gaussian instead of double Gaussian
def func_altSigM(args):
    """ Not used """
    setupFinalAltSigMFitter = deepcopy(fitCollection.setupFinalFitter)
    setupFinalAltSigMFitter.update({
        'argAliasInDB': {'afb': 'afb_altSigM', 'fl': 'fl_altSigM'},
        'saveToDB': False,
    })
    finalAltSigMFitter = StdFitter(setupFinalAltSigMFitter)
    def _preFitSteps_altSigM(self):
        StdFitter._preFitSteps(self)
        sigM_frac = self.args.find("sigM_frac")
        sigM_frac.setVal(0)
    finalAltSigMFitter._preFitSteps = types.MethodType(_preFitSteps_altSigM, finalAltSigMFitter)

    p.setSequence([
        pdfCollection.stdWspaceReader,
        dataCollection.dataReader,
        finalAltSigMFitter,
    ])

    try:
        p.beginSeq()
        p.runSeq()

        updateToDB_altShape(args, "altSigM")
    finally:
        p.endSeq()


# Alternate bkgCombM shape
# # versus expo+linear
def func_altBkgCombM(args):
    """ Not used """
    setupFinalAltBkgCombMFitter = deepcopy(fitCollection.setupFinalFitter)
    setupFinalAltBkgCombMFitter.update({
        'pdf': "f_finalAltBkgCombM",
        'argAliasInDB': {'afb': 'afb_altBkgCombM', 'fl': 'fl_altBkgCombM'},
        'saveToDB': False,
    })
    finalAltBkgCombMFitter = StdFitter(setupFinalAltBkgCombMFitter)
    p.setSequence([
        pdfCollection.stdWspaceReader,
        dataCollection.dataReader,
        finalAltBkgCombMFitter,
    ])

    try:
        p.beginSeq()
        p.runSeq()

        updateToDB_altShape(args, "altBkgCombM")
    finally:
        p.endSeq()

# Alternate bkgCombA shape
# # Smooth function versus analytic function
def func_altBkgCombA(args):
    """ Typically less than 10% """
    p = createNewProcess("systProcess", "plots_simultaneous")
    p.cfg['args'] = deepcopy(args)
    p.cfg['sysargs'] = sys.argv
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['binKey'] = p.cfg['bins'][0]
    
    finalAltBkgCombAFitter = fitCollection.SimFitter_Final_WithKStar_AltA
    setupFinalAltBkgCombAFitter = finalAltBkgCombAFitter.cfg
    setupFinalAltBkgCombAFitter.update({
        # 'argAliasInDB': {'unboundAfb': 'afb_altBkgCombA', 'unboundFl': 'fl_altBkgCombA'},
        'saveToDB': True,
    })

    def runSimSequences():
        for Year in [2016, 2017, 2018]:
            p.cfg['args'].Year=Year
            GetInputFiles(p)
            sequence=Instantiate(p, ['dataReader', 'stdWspaceReader'])
            p.setSequence(sequence)
            p.beginSeq()
            p.runSeq()
        p.cfg['args'].Year=args.Year
    runSimSequences()
    p.setSequence([finalAltBkgCombAFitter])

    try:
        p.beginSeq()
        p.runSeq()
        updateToDB_altShape(p, "altBkgCombA")
    finally:
        p.endSeq()

# Bmass range
# # Vary Fit range
def func_altFitRange(args):
    """ Take wider Fit region """
    dataReaderCfg = deepcopy(dataCollection.dataReaderCfg)
    dataReaderCfg.update({
        'preloadFile': None
    })
    dataReader = DataReader(dataReaderCfg)
    dataReader.customize = types.MethodType(
        functools.partial(dataCollection.customizeOne,
                          targetBMassRegion=['^altFit$'],
                          extraCuts=cut_kshortWindow),
        dataReader
    )
    fitterCfg = deepcopy(fitCollection.setupFinalFitter)
    fitterCfg.update({
        'data': "dataReader.altFit",
        'saveToDB': False
    })
    fitter = StdFitter(fitterCfg)
    p.setSequence([
        pdfCollection.stdWspaceReader,
        dataReader,
        fitter,
    ])

    try:
        p.beginSeq()
        p.runSeq()

        updateToDB_altShape(args, "altFitRange")
    finally:
        p.endSeq()

# Mis-include B -> Jpsi+X backgroud
# # Remove LSB from Fit region
def func_vetoJpsiX(args):
    """ Remvoe LSB from Fit region """
    dataReaderCfg = deepcopy(dataCollection.dataReaderCfg)
    dataReaderCfg.update({
        'preloadFile': None
    })
    dataReader = DataReader(dataReaderCfg)
    dataReader.customize = types.MethodType(
        functools.partial(dataCollection.customizeOne,
                          targetBMassRegion=['altFit_vetoJpsiX'],
                          extraCuts=cut_kshortWindow),
        dataReader
    )
    fitterCfg = deepcopy(fitCollection.setupFinalFitter)
    fitterCfg.update({
        'data': "dataReader.altFit_vetoJpsiX",
        'saveToDB': False
    })
    fitter = StdFitter(fitterCfg)
    p.setSequence([
        pdfCollection.stdWspaceReader,
        dataReader,
        fitter,
    ])

    try:
        p.beginSeq()
        p.runSeq()

        updateToDB_altShape(args, "vetoJpsiX")
    finally:
        p.endSeq()

# Make latex table
def func_makeLatexTable(args):
    """ Make table. Force the input db files from StdProcess.dbplayer.absInputDir """
    for var in ["fl", "afb"]:
        dbKeyToLine = {
            'syst_randEffi': [r"Limited MC size"],
            'syst_simMismodel': [r"Simu.\ mismodel"],
            'syst_altBkgCombA': [r"Comb.\ Bkg.\ shape"],
            'syst_altEffi': [r"Eff.\ mapping"],
            'syst_vetoJpsiX': [r"$B$ mass range"],
            'syst_datamcDev': [r"Data-MC Discrepancy"],
        }
        totalErrorLine = ["Total"]
        for binKey in ['belowJpsiA', 'belowJpsiB', 'belowJpsiC', 'betweenPeaks', 'summaryLowQ2']:
            db = shelve.open("{0}/fitResults_{1}.db".format("plots_simultaneous", q2bins[binKey]['label']))
            totalSystErr = 0.
            for systKey, latexLine in dbKeyToLine.items():
                try:
                    err = db["{0}_{1}".format(systKey, var)]['getError']
                except KeyError:
                    err = 0
                latexLine.append("{0:.04f}".format(err))
                totalSystErr += pow(err, 2)
            db.close()
            totalErrorLine.append("{0:.03f}".format(math.sqrt(totalSystErr)))

        print("Printing table of syst. unc. for {0}".format(var))
        indent = "  "
        print(indent * 2 + r"\begin{tabular}{|l|c|c|c|c|c|}")
        print(indent * 3 + r"\hline")
        print(indent * 3 + r"Syst.\ err.\ $\backslash$ $q^2$ bin & 1A & 1B & 1C & 3 & LowQ2 \\")
        print(indent * 3 + r"\hline")
        print(indent * 3 + r"\hline")
        print(indent * 3 + r"\multicolumn{5}{|c|}{Uncorrelated systematic uncertainties} \\")
        print(indent * 3 + r"\hline")
        for systKey, latexLine in dbKeyToLine.items():
            print(indent * 3 + " & ".join(latexLine) + r" \\")
        print(indent * 3 + r"\hline")
        print(indent * 3 + " & ".join(totalErrorLine) + r" \\")
        print(indent * 3 + r"\hline")
        print(indent * 2 + r"\end{tabular}")

if __name__ == '__main__':
    from BsToPhiMuMuFitter.python.ArgParser import SetParser, GetBatchTaskParser
    parser = GetBatchTaskParser()
    args   = parser.parse_known_args()[0]
    if args.OneStep is False: args.TwoStep = True

    if args.SimFit and args.Function_name=="systematics":
        if args.type == "randEffi":       args.func = func_randEffi_simultaneous
        if args.type == "simMismodel":    args.func = func_simMismodel
        if args.type == "makeLatexTable": args.func = func_makeLatexTable
        if args.type == "altBkgCombA":    args.func = func_altBkgCombA
        if args.type == "altEffi":    args.func = func_altEffi

    elif args.Function_name=="systematics":
        if args.type == "randEffi": args.func = func_randEffi
    args.func(args)
    sys.exit()