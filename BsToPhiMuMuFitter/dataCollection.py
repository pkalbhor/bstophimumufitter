#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent foldnestmax=3 ft=python et:

import re, pdb, types, functools, itertools, math
from array import array
from copy import copy

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import BsToPhiMuMuFitter.cpp
from v2Fitter.Fitter.DataReader import DataReader
from v2Fitter.Fitter.ObjProvider import ObjProvider
from BsToPhiMuMuFitter.varCollection import dataArgs, Bmass, CosThetaL, CosThetaK, Phimass, dataArgsGEN, dataArgsKStar, dataArgsGENoff
from BsToPhiMuMuFitter.anaSetup import q2bins, bMassRegions, modulePath 
from BsToPhiMuMuFitter.python.datainput import genSel, ExtraCuts, ExtraCutsKStar

from ROOT import TChain, TEfficiency, TH2D, RooArgList, RooDataHist
#from __main__ import args as Args
#from BsToPhiMuMuFitter.StdProcess import p

CFG = DataReader.templateConfig()
CFG.update({
    'argset': dataArgs,
    'lumi': -1,  # Keep a record, useful for mixing simulations samples
    #'ifriendIndex': ["Bmass", "Mumumass"],
})

# dataReader
def customizeOne(self, targetBMassRegion=None, extraCuts=None):
    """Define datasets with arguments."""
    if targetBMassRegion is None:
        targetBMassRegion = []
    if not self.process.cfg['binKey'] in q2bins.keys():
        self.logger.logERROR("Bin {0} is not defined.\n".format(self.process.cfg['binKey']))
        raise ValueError

    # With shallow copied CFG, have to bind cfg['dataset'] to a new object.
    self.cfg['dataset'] = []
    for key, val in bMassRegions.items():
        finalcut = self.process.cfg['cuts'][-1] if not key in ['USB', 'LSB'] else self.process.cfg['cuts'][-1].replace(re.search("Bdt \>(.*?)\)\&\&", self.process.cfg['cuts'][-1]).group(0).strip(), 'Bdt > 0.30)&&')
        if any([re.match(pat, key) for pat in targetBMassRegion]):
            self.cfg['dataset'].append(
                (
                    "{0}.{1}".format(self.cfg['name'], key),
                    "({0}) && ({1}) && ({2}) && ({3})".format(
                        val['cutString'],
                        q2bins[self.process.cfg['binKey']]['cutString'],
                        self.process.cfg['cuts'][-1],
                        "1" if not extraCuts else extraCuts,
                    )
                )
            )
    if "ResVeto" in targetBMassRegion and self.process.cfg['binKey']=='full':
        self.cfg['dataset'].append(
            (
                "{0}.Fit_ResVeto".format(self.cfg['name'], key),
                "({0}) && ({1}) && ({2}) && ({3})".format(
                    bMassRegions['Fit']['cutString'],
                    q2bins[self.process.cfg['binKey']]['cutString'],
                    self.process.cfg['cuts_Signal'],
                    extraCuts,
                )
            )
        )
    if "antiResVeto" in targetBMassRegion and self.process.cfg['binKey'] in ['jpsi', 'psi2s']:
        self.cfg['dataset'].append(
            (
                "{0}.Fit_antiResVeto".format(self.cfg['name'], key),
                "({0}) && ({1}) && ({2}) && ({3})".format(
                    bMassRegions['Fit']['cutString'],
                    q2bins[self.process.cfg['binKey']]['cutString'],
                    self.process.cfg['cuts_antiResVeto'],
                    extraCuts,
                )
            )
        )    
    # Customize preload TFile
    self.cfg['preloadFile'] = modulePath + "/data/preload_{datasetName}_{Year}_{binLabel}.root".format(datasetName=self.cfg['name'].split('.')[0], Year=self.process.cfg['args'].Year,  binLabel=q2bins[self.process.cfg['binKey']]['label'])

# sigMCGENReader
def customizeGEN(self):
    """Define datasets with arguments."""
    if not self.process.cfg['binKey'] in q2bins.keys():
        print("ERROR\t: Bin {0} is not defined.\n".format(self.process.cfg['binKey']))
        raise AttributeError

    # With shallow copied CFG, have to bind cfg['dataset'] to a new object.
    self.cfg['dataset'] = []
    self.cfg['dataset'].append(
        (
            "{0}.Fit".format(self.cfg['name']),
            re.sub("Q2", "genQ2", q2bins[self.process.cfg['binKey']]['cutString']) + " && genKpPt>0 && genKmPt>0"
        )
    )
    # Customize preload TFile
    self.cfg['preloadFile'] = modulePath + "/data/preload_{datasetName}_{Year}_{binLabel}.root".format(datasetName=self.cfg['name'].split('.')[0], Year=self.process.cfg['args'].Year, binLabel=q2bins[self.process.cfg['binKey']]['label'])

def GetDataReader(self, seq):
    if seq is 'dataReader':
        dataReaderCfg = copy(CFG)
        dataReaderCfg.update({
            'name': "dataReader.{Year}".format(Year=self.cfg['args'].Year),
            'ifile': self.cfg['dataFilePath'],
            'lumi': 35.9,    })
        dataReader = DataReader(dataReaderCfg)
        customizeData = functools.partial(customizeOne, targetBMassRegion=['^Fit$', '^.{0,1}SB$', 'ResVeto', 'antiResVeto'], extraCuts=ExtraCuts) #'^Fit$', '^.{0,1}SB$',
        dataReader.customize = types.MethodType(customizeData, dataReader)
        return dataReader

    # sigMCReader
    if seq is 'sigMCReader':
        sigMCReaderCfg = copy(CFG)
        sigMCReaderCfg.update({
            'name': "sigMCReader.{Year}".format(Year=self.cfg['args'].Year),
            'ifile': self.cfg['sigMC'],
            'lumi': 66226.56,
        })
        sigMCReader = DataReader(sigMCReaderCfg)
        customizeSigMC = functools.partial(customizeOne, targetBMassRegion=['^Fit$', 'ResVeto'], extraCuts=ExtraCuts)
        sigMCReader.customize = types.MethodType(customizeSigMC, sigMCReader)
        return sigMCReader

    # KStar0MuMu-sigMCReader
    if seq is 'KsigMCReader':
        KsigMCReaderCfg = copy(CFG)
        KsigMCReaderCfg.update({
            'name': "KsigMCReader.{Year}".format(Year=self.cfg['args'].Year),
            'ifile': self.cfg['peaking']['KstarMuMu'],
            'argset': dataArgsKStar,
            'lumi': 2765.2853,
        })
        KsigMCReader = DataReader(KsigMCReaderCfg)
        customizeKSigMC = functools.partial(customizeOne, targetBMassRegion=['^Fit$'], extraCuts=ExtraCuts)
        KsigMCReader.customize = types.MethodType(customizeKSigMC, KsigMCReader)
        return KsigMCReader
    if seq is 'sigMCGENReader':
        sigMCGENReaderCfg = copy(CFG)
        sigMCGENReaderCfg.update({
            'name': "sigMCGENReader.{Year}".format(Year=self.cfg['args'].Year),
            'ifile': self.cfg['genonly']['PhiMuMu'],
            'argset': dataArgsGEN,
        })
        sigMCGENReader = DataReader(sigMCGENReaderCfg)
        sigMCGENReader.customize = types.MethodType(customizeGEN, sigMCGENReader)
        return sigMCGENReader
    if seq is 'sigMCGENcReader':
        sigMCGENcReaderCfg = copy(CFG)
        sigMCGENcReaderCfg.update({
            'name': "sigMCGENcReader.{Year}".format(Year=self.cfg['args'].Year),
            'ifile': self.cfg['genOff']['PhiMuMu'],
            'argset': dataArgsGENoff,
        })
        sigMCGENcReader = DataReader(sigMCGENcReaderCfg)
        sigMCGENcReader.customize = types.MethodType(customizeGEN, sigMCGENcReader)
        return sigMCGENcReader
    if seq is 'sigMCReader_JP':
        bkgJpsiMCReaderCfg = copy(CFG)
        bkgJpsiMCReaderCfg.update({
            'name': "sigMCReader_JP.{}".format(self.cfg['args'].Year),
            'ifile': self.cfg['control']['JpsiPhi'],
            'lumi': 295.761,
        })
        bkgJpsiMCReader = DataReader(bkgJpsiMCReaderCfg)
        customizeBkgPeakMC = functools.partial(customizeOne, targetBMassRegion=['^Fit$', 'antiResVeto'], extraCuts=ExtraCuts)
        bkgJpsiMCReader.customize = types.MethodType(customizeBkgPeakMC, bkgJpsiMCReader)
        return bkgJpsiMCReader
    if seq is 'sigMCReader_PP':
        bkgPsi2sMCReaderCfg = copy(CFG)
        bkgPsi2sMCReaderCfg.update({
            'name': "sigMCReader_PP.{}".format(self.cfg['args'].Year),
            'ifile': self.cfg['control']['PsiPhi'],
            'lumi': 218.472,
        })
        bkgPsi2sMCReader = DataReader(bkgPsi2sMCReaderCfg)
        customizeBkgPeakMC = functools.partial(customizeOne, targetBMassRegion=['^Fit$', 'antiResVeto'], extraCuts=ExtraCuts)
        bkgPsi2sMCReader.customize = types.MethodType(customizeBkgPeakMC, bkgPsi2sMCReader)
        return bkgPsi2sMCReader
    if seq is 'bkgMCReader_JK':
        bkgJpsiKstMCReaderCfg = copy(CFG)
        bkgJpsiKstMCReaderCfg.update({
            'name': "bkgMCReader_JK.{}".format(self.cfg['args'].Year),
            'ifile': self.cfg['peaking']['JpsiKstar'],
            'lumi': 218.472,
        })
        bkgJpsiKstMCReader = DataReader(bkgJpsiKstMCReaderCfg)
        customizeBkgPeakMC = functools.partial(customizeOne, targetBMassRegion=['^Fit$', 'antiResVeto'], extraCuts=ExtraCuts)
        bkgJpsiKstMCReader.customize = types.MethodType(customizeBkgPeakMC, bkgJpsiKstMCReader)
        return bkgJpsiKstMCReader
    if seq is 'bkgMCReader_PK':
        bkgPsi2sKstMCReaderCfg = copy(CFG)
        bkgPsi2sKstMCReaderCfg.update({
            'name': "bkgMCReader_PK.{}".format(self.cfg['args'].Year),
            'ifile': self.cfg['peaking']['PsiKstar'],
            'lumi': 218.472,
        })
        bkgPsi2sKstMCReader = DataReader(bkgPsi2sKstMCReaderCfg)
        customizeBkgPeakMC = functools.partial(customizeOne, targetBMassRegion=['^Fit$', 'antiResVeto'], extraCuts=ExtraCuts)
        bkgPsi2sKstMCReader.customize = types.MethodType(customizeBkgPeakMC, bkgPsi2sKstMCReader)
        return bkgPsi2sKstMCReader

setupEfficiencyBuildProcedure = {}
setupEfficiencyBuildProcedure['acc'] = {
    'ifiles': None,
    'baseString': None,
    'cutString' : None,
    'fillXY': "genCosThetaK:genCosThetaL",  # Y:X
    'weight': None
}
setupEfficiencyBuildProcedure['rec'] = {
    'ifiles': None,
    'dfiles': None,
    'baseString': None,
    'cutString': None,
    'fillXY': "CosThetaK:CosThetaL",  # Y:X
    'fillXYDen': "genCosThetaK:genCosThetaL",  # Y:X
    'weight': None
}
# effiHistReader
accXEffThetaLBins = array('d', [-1., -0.8, -0.6, -0.4, -0.2, 0., 0.2, 0.4, 0.6, 0.8, 1.])
accXEffThetaKBins = array('d', [-1., -0.8, -0.6, -0.4, -0.2, 0., 0.2, 0.4, 0.6, 0.8, 1.])
ThetaLBins = array('d', [-1., -0.7, -0.4, -0.2, 0., 0.2, 0.4, 0.7, 1.])
ThetaKBins = array('d', [-1., -0.7, -0.4, -0.2, 0., 0.2, 0.4, 0.7, 1.])

def buildTotalEffiHist(self):
    """Build one step efficiency histograms for later fitting/plotting"""
    binKey=self.process.cfg['binKey']
    fin = self.process.filemanager.open("buildAccXRecEffiHist", modulePath + "/data/TotalEffHists_{0}_{1}.root".format(str(self.process.cfg['args'].Year), q2bins[binKey]['label']), "UPDATE")

    # Build acceptance, reco efficiency, and accXrec
    forceRebuild = False
    h2_accXrec = fin.Get("h2_accXrec1_{0}".format(binKey))
    if h2_accXrec == None or forceRebuild:
        # Fill histograms
        setupEfficiencyBuildProcedure['acc'].update({
            'ifiles'    : self.process.cfg['genonly']['PhiMuMu'],
            'baseString': re.sub("Q2", "genQ2", q2bins[binKey]['cutString']) + " && genKpPt>0 && genKmPt>0",
            'cutString' : "({0}) && ({1})".format(re.sub("Q2", "genQ2", q2bins[binKey]['cutString']), genSel)})
        setupEfficiencyBuildProcedure['rec'].update({
            'ifiles'    : self.process.cfg['sigMC'],
            'baseString': "({0}) && ({1})".format(re.sub("Q2", "genQ2", q2bins[binKey]['cutString']), genSel),
            'cutString' : "({0}) && ({1}) && ({2})".format(self.process.cfg['cuts'][-1], q2bins[binKey]['cutString'], 1 if ExtraCuts==None else ExtraCuts)})

        label='accXrec'
        treein = TChain()
        for f in setupEfficiencyBuildProcedure['acc']['ifiles']:
            treein.Add(f)
        treein.Draw(">>totEvtList", setupEfficiencyBuildProcedure['acc']['baseString'])
        totEvtList = ROOT.gDirectory.Get("totEvtList")

        treeinPassed = TChain()
        for f in setupEfficiencyBuildProcedure['rec']['ifiles']:
            treeinPassed.Add(f)
        treeinPassed.Draw(">>accEvtList", setupEfficiencyBuildProcedure['rec']['cutString'])
        accEvtList = ROOT.gDirectory.Get("accEvtList")

        LBins=accXEffThetaLBins #if not binKey=="belowJpsiA" else ThetaLBins
        KBins=accXEffThetaKBins #if not binKey=="belowJpsiA" else ThetaKBins
        h2_total = TH2D("h2_{0}_{1}_total".format(label, binKey), "", len(LBins)-1, LBins, len(KBins)-1, KBins)
        h2_passed = h2_total.Clone("h2_{0}_{1}_passed".format(label, binKey))
        h2_fine_total = TH2D("h2_{0}_fine_{1}_total".format(label, binKey), "", 20, -1, 1, 20, -1, 1)
        h2_fine_passed = h2_fine_total.Clone("h2_{0}_fine_{1}_passed".format(label, binKey))

        treein.SetEventList(totEvtList) 
        for hist in h2_total, h2_fine_total:
            treein.Draw("{0}>>{1}".format(setupEfficiencyBuildProcedure['acc']['fillXY'], hist.GetName()), "", "goff")

        treeinPassed.SetEventList(accEvtList)
        for hist in h2_passed, h2_fine_passed:
            treeinPassed.Draw("{0}>>{1}".format(setupEfficiencyBuildProcedure['rec']['fillXY'], hist.GetName()), "", "goff")

        print("\033[0;34;47m Total: \033[0m", accEvtList.GetN(),"/",totEvtList.GetN())
        print("\033[0;34;47m Base String: \033[0m", setupEfficiencyBuildProcedure['acc']['baseString'])
        print("\033[0;34;47m Cut String : \033[0m", setupEfficiencyBuildProcedure['rec']['cutString'])

        h2_eff = TEfficiency(h2_passed, h2_total)
        h2_eff_fine = TEfficiency(h2_fine_passed, h2_fine_total)

        fin.cd()
        for proj, var in [("ProjectionX", CosThetaL), ("ProjectionY", CosThetaK)]:
            proj_fine_total = getattr(h2_fine_total, proj)("{0}_{1}".format(h2_fine_total.GetName(), proj), 0, -1, "e")
            proj_fine_passed = getattr(h2_fine_passed, proj)("{0}_{1}".format(h2_fine_passed.GetName(), proj), 0, -1, "e")
            h_eff = TEfficiency(proj_fine_passed, proj_fine_total)
            h_eff.Write("h_{0}_fine_{1}_{2}".format(label, binKey, proj), ROOT.TObject.kOverwrite)

        h2_eff.Write("h2Eff_{0}_{1}".format(label, binKey), ROOT.TObject.kOverwrite)           #Binned 2D Eff
        h2_eff_fine.Write("h2_{0}_fine_{1}".format(label, binKey), ROOT.TObject.kOverwrite) #2D Efficiency Total 

        # : Converting TEff to TH1D
        fin.cd()
        for proj in ["ProjectionX", "ProjectionY"]:
            h_accXrec_fineEff = fin.Get("h_accXrec_fine_{0}_{1}".format(binKey, proj))
            h_accXrec_fine = h_accXrec_fineEff.GetPassedHistogram().Clone("h_accXrec_fine_{0}_{1}".format(binKey, proj))
            h_accXrec_fine.Reset("ICESM")
            for b in range(1, h_accXrec_fine.GetNbinsX() + 1):
                h_accXrec_fine.SetBinContent(b, h_accXrec_fineEff.GetEfficiency(b))
                h_accXrec_fine.SetBinError(b, h_accXrec_fine.GetBinContent(b) * math.sqrt(1 / h_accXrec_fineEff.GetTotalHistogram().GetBinContent(b) + 1 / h_accXrec_fineEff.GetPassedHistogram().GetBinContent(b)))
            h_accXrec_fine.Write("h_accXrec_{0}_{1}".format(binKey, proj), ROOT.TObject.kOverwrite)

        h2_accXrecEff1 = fin.Get("h2Eff_accXrec_{0}".format(binKey))        #2D Binned Eff
        h2_accXrec1 = h2_accXrecEff1.GetPassedHistogram().Clone("h2_accXrec1_{0}".format(binKey)) 
        h2_accXrec1.Reset("ICESM")
        for iL, iK in itertools.product(range(1, len(LBins)), range(1, len(KBins))):
            if h2_accXrecEff1.GetTotalHistogram().GetBinContent(iL, iK) == 0:
                h2_accXrec1.SetBinContent(iL, iK, 0)
                h2_accXrec1.SetBinError(iL, iK, 1)
            else:
                iLK = h2_accXrecEff1.GetGlobalBin(iL, iK)
                h2_accXrec1.SetBinContent(iL, iK, h2_accXrecEff1.GetEfficiency(iLK))
                h2_accXrec1.SetBinError(iL, iK, h2_accXrec1.GetBinContent(iL, iK) * math.sqrt(1. / h2_accXrecEff1.GetTotalHistogram().GetBinContent(iLK) + 1. / h2_accXrecEff1.GetPassedHistogram().GetBinContent(iLK)))
        h2_accXrec1.SetXTitle("cos#theta_{l}")
        h2_accXrec1.SetYTitle("cos#theta_{K}")
        h2_accXrec1.SetZTitle("Overall efficiency")
        h2_accXrec1.Write("h2_accXrec1_{0}".format(binKey), ROOT.TObject.kOverwrite)
        self.logger.logINFO("Overall efficiency is built.")

        h2_accXrecEff = fin.Get("h2Eff_accXrec_{0}".format(binKey))        #2D Binned Eff: Same as h2_accXrec1_binKey, but using CreateHistogram()
        h2_accXrec = h2_accXrecEff.CreateHistogram(); h2_accXrec.SetTitle("Created from CreateHistogram() method")
        h2_accXrec.SetXTitle("cos#theta_{l}")
        h2_accXrec.SetYTitle("cos#theta_{K}")
        h2_accXrec.SetZTitle("Overall efficiency")
        h2_accXrec.Write("h2_accXrec_{0}".format(binKey), ROOT.TObject.kOverwrite)  # We are not going to use this as of now
        self.logger.logINFO("Overall efficiency is built.")

    # Register the chosen one to sourcemanager
    h2_accXrec = fin.Get("h2_accXrec1_{0}".format(self.process.cfg['binKey']))
    self.cfg['source']['effiHistReader.h2_accXrec.{0}'.format(str(self.process.cfg['args'].Year))] = h2_accXrec
    self.cfg['source']['effiHistReader.accXrec.{0}'.format(str(self.process.cfg['args'].Year))] = RooDataHist("accXrec", "", RooArgList(CosThetaL, CosThetaK), ROOT.RooFit.Import(h2_accXrec)) # Effi 2D RooDataHist
    self.cfg['source']['effiHistReader.h_accXrec_fine_ProjectionX.{0}'.format(str(self.process.cfg['args'].Year))] = fin.Get("h_accXrec_{0}_ProjectionX".format(self.process.cfg['binKey'])) #Effi of CosThetaL
    self.cfg['source']['effiHistReader.h_accXrec_fine_ProjectionY.{0}'.format(str(self.process.cfg['args'].Year))] = fin.Get("h_accXrec_{0}_ProjectionY".format(self.process.cfg['binKey'])) # Effi of CosThetaK


def buildAccXRecEffiHist(self):
    """Build two step efficiency histograms for later fitting/plotting"""
    binKey = self.process.cfg['binKey']
    fin = self.process.filemanager.open("buildAccXRecEffiHist", modulePath + "/data/accXrecEffHists_{0}_{1}.root".format(str(self.process.cfg['args'].Year), q2bins[binKey]['label']), "UPDATE")
    # Build acceptance, reco efficiency, and accXrec
    forceRebuild = False

    h2_accXrec = fin.Get("h2_accXrec_{0}".format(binKey))
    if h2_accXrec == None or forceRebuild:
        h2_acc = fin.Get("h2_acc_{0}".format(binKey))
        h2_rec = fin.Get("h2_rec_{0}".format(binKey))

        # Fill histograms
        setupEfficiencyBuildProcedure['acc'].update({
            'ifiles'    : self.process.cfg['genonly']['PhiMuMu'],
            'baseString': re.sub("Q2", "genQ2", q2bins[binKey]['cutString']) + " && genKpPt>0 && genKmPt>0",
            'cutString' : "({0}) && ({1})".format(re.sub("Q2", "genQ2", q2bins[binKey]['cutString']), genSel)})
        setupEfficiencyBuildProcedure['rec'].update({
            'ifiles'    : self.process.cfg['sigMC'],
            'dfiles'    : self.process.cfg['genOff']['PhiMuMu'],
            'baseString': "({0}) && ({1})".format(re.sub("Q2", "genQ2", q2bins[binKey]['cutString']), genSel),
            'cutString' : "({0}) && ({1}) && ({2})".format(cuts_antiResVeto if binKey in ['jpsi', 'psi2s'] else self.process.cfg['cuts'][-1], q2bins[binKey]['cutString'], 1 if ExtraCuts==None else ExtraCuts)})

        LBins=accXEffThetaLBins #if not binKey=="belowJpsiA" else ThetaLBins
        KBins=accXEffThetaKBins #if not binKey=="belowJpsiA" else ThetaKBins
        for h2, label in (h2_acc, 'acc'), (h2_rec, 'rec'):
            if h2 == None or forceRebuild:
                treein = TChain("tree")
                for f in setupEfficiencyBuildProcedure[label]['ifiles']:
                    treein.Add(f)

                treeDen = TChain()
                if label=="rec":
                    for f in setupEfficiencyBuildProcedure[label]['dfiles']:
                        treeDen.Add(f)
                UseDataFrame=True
                if UseDataFrame:
                    if setupEfficiencyBuildProcedure[label]['weight'] is None and label=="acc":
                        df_tot = ROOT.RDataFrame(treein).Define('weight', "1").Filter(setupEfficiencyBuildProcedure[label]['baseString'])
                    elif label=="acc":
                        df_tot = ROOT.RDataFrame(treein).Define('weight', *setupEfficiencyBuildProcedure[label]['weight']).Filter(setupEfficiencyBuildProcedure[label]['baseString'])
                    elif setupEfficiencyBuildProcedure[label]['weight'] is None and label=="rec":
                        df_tot = ROOT.RDataFrame(treeDen).Define('weight', "1").Filter(setupEfficiencyBuildProcedure[label]['baseString'])
                    elif label=="rec":
                        df_tot = ROOT.RDataFrame(treeDen).Define('weight', *setupEfficiencyBuildProcedure[label]['weight']).Filter(setupEfficiencyBuildProcedure[label]['baseString'])
                    df_acc = ROOT.RDataFrame(treein).Define('weight', "1").Filter(setupEfficiencyBuildProcedure[label]['cutString'])

                    fillXY = setupEfficiencyBuildProcedure[label]['fillXY'].split(':')
                    if label=="rec": fillXYDen = setupEfficiencyBuildProcedure[label]['fillXYDen'].split(':')
                    h2_total_config = ("h2_{0}_{1}_total".format(label, binKey), "", len(LBins) - 1, LBins, len(KBins) - 1, KBins)
                    h2_passed_config  = ("h2_{0}_{1}_passed".format(label, binKey), "", len(LBins) - 1, LBins, len(KBins) - 1, KBins)
                    h2_fine_total_config = ("h2_{0}_fine_{1}_total".format(label, binKey), "", 20, -1, 1, 20, -1, 1)
                    h2_fine_passed_config = ("h2_{0}_fine_{1}_passed".format(label, binKey), "", 20, -1, 1, 20, -1, 1)

                    h2ptr_total = df_tot.Histo2D(h2_total_config, fillXY[1], fillXY[0], "weight") if label=="acc" else df_tot.Histo2D(h2_total_config, fillXYDen[1], fillXYDen[0], "weight")
                    h2ptr_passed = df_acc.Histo2D(h2_passed_config, fillXY[1], fillXY[0], "weight")
                    h2ptr_fine_total = df_tot.Histo2D(h2_fine_total_config, fillXY[1], fillXY[0], "weight") if label=="acc" else df_tot.Histo2D(h2_fine_total_config, fillXYDen[1], fillXYDen[0], "weight")
                    h2ptr_fine_passed = df_acc.Histo2D(h2_fine_passed_config, fillXY[1], fillXY[0], "weight")

                    h2_total = h2ptr_total.GetValue()
                    h2_passed = h2ptr_passed.GetValue()
                    h2_fine_total = h2ptr_fine_total.GetValue()
                    h2_fine_passed = h2ptr_fine_passed.GetValue()
                    print("{2}: {0}/{1}".format(df_acc.Count().GetValue(), df_tot.Count().GetValue(), label))
                else:
                    if label=='acc':
                        treein.Draw(">>totEvtList", setupEfficiencyBuildProcedure['acc']['baseString'])
                        totEvtList = ROOT.gDirectory.Get("totEvtList")
                        treein.Draw(">>accEvtList", setupEfficiencyBuildProcedure['acc']['cutString'])
                        accEvtList = ROOT.gDirectory.Get("accEvtList")
                    if label=='rec':
                        treeDen.Draw(">>totEvtList", setupEfficiencyBuildProcedure['rec']['baseString'])
                        totEvtList = ROOT.gDirectory.Get("totEvtList")
                        treein.Draw(">>accEvtList", setupEfficiencyBuildProcedure['rec']['cutString'])
                        accEvtList = ROOT.gDirectory.Get("accEvtList")
                    h2_total = TH2D("h2_{0}_{1}_total".format(label,binKey), "", len(LBins)-1, LBins, len(KBins)-1, KBins)
                    h2_passed = h2_total.Clone("h2_{0}_{1}_passed".format(label, binKey))
                    h2_fine_total = TH2D("h2_{0}_fine_{1}_total".format(label, binKey), "", 20, -1, 1, 20, -1, 1)
                    h2_fine_passed = h2_fine_total.Clone("h2_{0}_fine_{1}_passed".format(label, binKey))
                    
                    treeDen.SetEventList(totEvtList) if label=='rec' else treein.SetEventList(totEvtList)
                    for hist in h2_total, h2_fine_total:
                        if label=='rec':
                            treeDen.Draw("{0}>>{1}".format(setupEfficiencyBuildProcedure['rec']['fillXYDen'], hist.GetName()), "", "goff")
                        else:
                            treein.Draw("{0}>>{1}".format(setupEfficiencyBuildProcedure['acc']['fillXY'], hist.GetName()), "", "goff")
                    treein.SetEventList(accEvtList)
                    for hist in h2_passed, h2_fine_passed:
                        treein.Draw("{0}>>{1}".format(setupEfficiencyBuildProcedure[label]['fillXY'], hist.GetName()), "", "goff")
                    print("{2}: {0}/{1}".format(accEvtList.GetN(), totEvtList.GetN(), label))
                print("Base String: ", setupEfficiencyBuildProcedure[label]['baseString'])
                print("Cut String:  ", setupEfficiencyBuildProcedure[label]['cutString'])
                h2_eff = TEfficiency(h2_passed, h2_total)
                h2_eff_fine = TEfficiency(h2_fine_passed, h2_fine_total)

                fin.cd()
                for proj, var in [("ProjectionX", CosThetaL), ("ProjectionY", CosThetaK)]:
                    proj_fine_total = getattr(h2_fine_total, proj)("{0}_{1}".format(h2_fine_total.GetName(), proj), 0, -1, "e")
                    proj_fine_passed = getattr(h2_fine_passed, proj)("{0}_{1}".format(h2_fine_passed.GetName(), proj), 0, -1, "e")
                    h_eff = TEfficiency(proj_fine_passed, proj_fine_total)
                    h_eff.Write("h_{0}_fine_{1}_{2}".format(label, binKey, proj), ROOT.TObject.kOverwrite)

                h2_eff.Write("h2_{0}_{1}".format(label, binKey), ROOT.TObject.kOverwrite)
                h2_eff_fine.Write("h2_{0}_fine_{1}".format(label, binKey), ROOT.TObject.kOverwrite)
                h2_eff.CreateHistogram().Write("hist2_{0}_{1}".format(label, binKey), ROOT.TObject.kOverwrite)
                h2_eff_fine.CreateHistogram().Write("hist2_{0}_fine_{1}".format(label, binKey), ROOT.TObject.kOverwrite)
                if UseDataFrame: del df_acc, df_tot

        # Merge acc and rec to accXrec
        fin.cd()
        for proj in ["ProjectionX", "ProjectionY"]:
            h_acc_fine = fin.Get("h_acc_fine_{0}_{1}".format(binKey, proj))
            h_rec_fine = fin.Get("h_rec_fine_{0}_{1}".format(binKey, proj))
            hist_acc_fine = h_acc_fine.GetPassedHistogram().Clone("hist_acc_fine_{0}_{1}".format(binKey, proj))
            hist_rec_fine = h_rec_fine.GetPassedHistogram().Clone("hist_rec_fine_{0}_{1}".format(binKey, proj))
            h_accXrec_fine = h_acc_fine.GetPassedHistogram().Clone("h_accXrec_fine_{0}_{1}".format(binKey, proj))
            hist_acc_fine.Reset("ICESM")
            hist_rec_fine.Reset("ICESM")
            h_accXrec_fine.Reset("ICESM")
            for b in range(1, h_accXrec_fine.GetNbinsX() + 1):
                hist_acc_fine.SetBinContent(b, h_acc_fine.GetEfficiency(b))
                hist_acc_fine.SetBinError(b, max(h_acc_fine.GetEfficiencyErrorLow(b), h_acc_fine.GetEfficiencyErrorUp(b)))
                hist_rec_fine.SetBinContent(b, h_rec_fine.GetEfficiency(b))
                hist_rec_fine.SetBinError(b, max(h_rec_fine.GetEfficiencyErrorLow(b), h_rec_fine.GetEfficiencyErrorUp(b)))
                if h_rec_fine.GetTotalHistogram().GetBinContent(b) == 0 or h_rec_fine.GetPassedHistogram().GetBinContent(b) == 0:
                    h_accXrec_fine.SetBinContent(b, 0)
                    h_accXrec_fine.SetBinError(b, 1)
                    print(">> Empty reco eff bin #", b)
                else:
                    h_accXrec_fine.SetBinContent(b, h_acc_fine.GetEfficiency(b) * h_rec_fine.GetEfficiency(b))
                    h_accXrec_fine.SetBinError(b, h_accXrec_fine.GetBinContent(b) * math.sqrt(1 / h_acc_fine.GetTotalHistogram().GetBinContent(b) + 1 / h_acc_fine.GetPassedHistogram().GetBinContent(b) + 1 / h_rec_fine.GetTotalHistogram().GetBinContent(b) + 1 / h_rec_fine.GetPassedHistogram().GetBinContent(b)))
            hist_acc_fine.Write("hist_acc_{0}_{1}".format(binKey, proj), ROOT.TObject.kOverwrite)
            hist_rec_fine.Write("hist_rec_{0}_{1}".format(binKey, proj), ROOT.TObject.kOverwrite)
            h_accXrec_fine.Write("h_accXrec_{0}_{1}".format(binKey, proj), ROOT.TObject.kOverwrite)

        h2_acc = fin.Get("h2_acc_{0}".format(binKey))
        h2_rec = fin.Get("h2_rec_{0}".format(binKey))
        h2_accXrec = h2_acc.GetPassedHistogram().Clone("h2_accXrec_{0}".format(binKey))
        h2_accXrec.Reset("ICESM")
        for iL, iK in itertools.product(range(1, len(LBins)), range(1, len(KBins))):
            if h2_rec.GetTotalHistogram().GetBinContent(iL, iK) == 0 or h2_rec.GetPassedHistogram().GetBinContent(iL, iK) == 0 or h2_acc.GetTotalHistogram().GetBinContent(iL, iK) == 0 or h2_acc.GetPassedHistogram().GetBinContent(iL, iK) == 0:
                h2_accXrec.SetBinContent(iL, iK, 0)
                h2_accXrec.SetBinError(iL, iK, 1)
                print(">> Empty recoORacc eff bin #", iL, iK)
            else:
                iLK = h2_acc.GetGlobalBin(iL, iK)
                h2_accXrec.SetBinContent(iL, iK, h2_acc.GetEfficiency(iLK) * h2_rec.GetEfficiency(iLK))
                h2_accXrec.SetBinError(iL, iK, h2_accXrec.GetBinContent(iL, iK) * math.sqrt(1 / h2_acc.GetTotalHistogram().GetBinContent(iLK) + 1 / h2_acc.GetPassedHistogram().GetBinContent(iLK) + 1 / h2_rec.GetTotalHistogram().GetBinContent(iLK) + 1 / h2_rec.GetPassedHistogram().GetBinContent(iLK)))
        h2_accXrec.SetXTitle("cos#theta_{l}")
        h2_accXrec.SetYTitle("cos#theta_{K}")
        h2_accXrec.SetZTitle("Overall efficiency")

        h2_accXrec.Write("h2_accXrec_{0}".format(binKey), ROOT.TObject.kOverwrite)
        self.logger.logINFO("Overall efficiency is built.")

    # Register the chosen one to sourcemanager
    #  h2_accXrec = fin.Get("h2_accXrec_{0}".format(self.process.cfg['binKey']))
    Year=str(self.process.cfg['args'].Year)
    self.cfg['source'][self.name + '.h2_accXrec.{0}'.format(Year)] = h2_accXrec
    self.cfg['source'][self.name + '.accXrec.{0}'.format(Year)] = RooDataHist("accXrec", "", RooArgList(CosThetaL, CosThetaK), ROOT.RooFit.Import(h2_accXrec))
    self.cfg['source'][self.name + '.h_accXrec_fine_ProjectionX.{0}'.format(Year)] = fin.Get("h_accXrec_{0}_ProjectionX".format(self.process.cfg['binKey']))
    self.cfg['source'][self.name + '.h_accXrec_fine_ProjectionY.{0}'.format(Year)] = fin.Get("h_accXrec_{0}_ProjectionY".format(self.process.cfg['binKey']))
   
    hist2_acc_fine = fin.Get("hist2_acc_fine_{0}".format(binKey))
    self.cfg['source'][self.name + '.hist2_acc_fine.{}'.format(Year)] = hist2_acc_fine
    self.cfg['source'][self.name + '.acc_fine.{0}'.format(Year)] = RooDataHist("acc_fine", "", RooArgList(CosThetaL, CosThetaK), ROOT.RooFit.Import(hist2_acc_fine))
    self.cfg['source'][self.name + '.h_acc_fine_ProjectionX.{0}'.format(Year)] = fin.Get("hist_acc_{0}_ProjectionX".format(self.process.cfg['binKey']))
    self.cfg['source'][self.name + '.h_acc_fine_ProjectionY.{0}'.format(Year)] = fin.Get("hist_acc_{0}_ProjectionY".format(self.process.cfg['binKey']))

    hist2_rec_fine = fin.Get("hist2_rec_fine_{0}".format(binKey))
    self.cfg['source'][self.name + '.hist2_rec_fine.{}'.format(Year)] = hist2_rec_fine
    self.cfg['source'][self.name + '.rec_fine.{0}'.format(Year)] = RooDataHist("rec_fine", "", RooArgList(CosThetaL, CosThetaK), ROOT.RooFit.Import(hist2_rec_fine))
    self.cfg['source'][self.name + '.h_rec_fine_ProjectionX.{0}'.format(Year)] = fin.Get("hist_rec_{0}_ProjectionX".format(self.process.cfg['binKey']))
    self.cfg['source'][self.name + '.h_rec_fine_ProjectionY.{0}'.format(Year)] = fin.Get("hist_rec_{0}_ProjectionY".format(self.process.cfg['binKey']))

    hist2_acc = fin.Get("hist2_acc_{0}".format(binKey))
    self.cfg['source'][self.name + '.hist2_acc.{}'.format(Year)] = hist2_acc
    self.cfg['source'][self.name + '.acc.{0}'.format(Year)] = RooDataHist("acc", "", RooArgList(CosThetaL, CosThetaK), ROOT.RooFit.Import(hist2_acc))
    hist2_rec = fin.Get("hist2_rec_{0}".format(binKey))
    self.cfg['source'][self.name + '.hist2_rec.{}'.format(Year)] = hist2_rec
    self.cfg['source'][self.name + '.rec.{0}'.format(Year)] = RooDataHist("rec", "", RooArgList(CosThetaL, CosThetaK), ROOT.RooFit.Import(hist2_rec))

effiHistReaderOneStep = ObjProvider({
    'name': "effiHistReaderOneStep",
    'obj': {
        'effiHistReaderOneStep.h2_accXrec': [buildTotalEffiHist, ],
    }
})

effiHistReader = ObjProvider({
    'name': "effiHistReader",
    'obj': {
        'effiHistReader.h2_accXrec': [buildAccXRecEffiHist, ],
    }
})
import BsToPhiMuMuFitter.script.latex.makeTables as makeTables
FinalDataResult = ObjProvider({
    'name': "FinalDataResult",
    'obj': {'FinalDataResult': [makeTables.table_dataresAFBFL, ], }
})
EffiTable = ObjProvider({
    'name': "EffiTable",
    'obj': {'EffiTable': [makeTables.EffiTable, ], }
})

import BsToPhiMuMuFitter.python.CompVar as CompVar
GetCompPlots = ObjProvider({
    'name': "GetCompPlots",
    'obj': {'GetCompPlots': [CompVar.GetCompPlots, ], }
})

if __name__ == '__main__':
    p.setSequence([effiHistReader])
    p.beginSeq()
    p.runSeq()
    p.endSeq()
