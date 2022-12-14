#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 sts=4 fdm=indent fdl=0 fdn=3 ft=python et:

import types
from copy import deepcopy

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import BsToPhiMuMuFitter.cpp
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.StdFitter import StdFitter, flToUnboundFl, afbToUnboundAfb
from BsToPhiMuMuFitter.EfficiencyFitter import EfficiencyFitter

from BsToPhiMuMuFitter.StdProcess import p
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
from BsToPhiMuMuFitter.anaSetup import bMassRegions

setupTemplateFitter = StdFitter.templateConfig()

def sigAFitter_bookPdfData(self):
    self.process.dbplayer.saveSMPrediction()
    StdFitter._bookPdfData(self)
    self.data.changeObservableName("genCosThetaK", "CosThetaK")
    self.data.changeObservableName("genCosThetaL", "CosThetaL")

ArgAliasRECO={'unboundAfb': 'unboundAfb_RECO', 'unboundFl': 'unboundFl_RECO'}
ArgAliasRECO_Alt={'unboundAfb': 'unboundAfb_RECO_Alt', 'unboundFl': 'unboundFl_RECO_Alt'}
ArgAliasGEN ={'unboundAfb': 'unboundAfb_GEN', 'unboundFl': 'unboundFl_GEN'}
ArgAliasSigM={'sigMGauss1_sigma': 'sigMGauss1_sigma_RECO', 'sigMGauss2_sigma': 'sigMGauss2_sigma_RECO', 'sigMGauss_mean': 'sigMGauss_mean_RECO', 'sigM_frac': 'sigM_frac_RECO'}
ArgAliasDCB ={'cbs1_sigma': 'cbs1_sigma_RECO', 'cbs2_sigma': 'cbs2_sigma_RECO', 'cbs1_alpha': 'cbs1_alpha_RECO', 'cbs2_alpha': 'cbs2_alpha_RECO', 'cbs1_n': 'cbs1_n_RECO', 'cbs2_n': 'cbs2_n_RECO', 'cbs_mean': 'cbs_mean_RECO', 'sigMDCB_frac': 'sigMDCB_frac_RECO'}
ArgAliasJP = {}
ArgAliasJK = {}
ArgAlias_PhiM_JP = {'Phicbs1_alpha': 'Phicbs1_alpha_MC', 'Phicbs1_n':'Phicbs1_n_MC', 'Phicbs1_sigma':'Phicbs1_sigma_MC', 
        'Phicbs2_alpha':'Phicbs2_alpha_MC', 'Phicbs2_n':'Phicbs2_n_MC', 'Phicbs2_sigma':'Phicbs2_sigma_MC', 
        'Phicbs_mean':'Phicbs_mean_MC', 'sigPhiM_DCB_frac':'sigPhiM_DCB_frac_MC', 
        'sigPhiM_TCB_frac1':'sigPhiM_TCB_frac1_MC', 'sigPhiM_TCB_frac2':'sigPhiM_TCB_frac2_MC',
        'Phicbs3_alpha': 'Phicbs3_alpha_MC', 'Phicbs3_n':'Phicbs3_n_MC', 'Phicbs3_sigma':'Phicbs3_sigma_MC',
        'sigPhiMG_mean':'sigPhiMG_mean_MC', 'sigPhiM_frac':'sigPhiM_frac_MC', 
        'sigPhiMG1_sigma':'sigPhiMG1_sigma_MC', 'sigPhiMG2_sigma':'sigPhiMG2_sigma_MC', 'sigPhiMG3_sigma':'sigPhiMG3_sigma_MC', 
        'sigPhiM3_frac1':'sigPhiM3_frac1_MC', 'sigPhiM3_frac2':'sigPhiM3_frac2_MC'}

def GetFitterObjects(self, seq):
    Year=self.cfg['args'].Year
    AltRange = self.cfg['args'].AltRange
    binKey = self.cfg['binKey']
    TwoStep = self.cfg['args'].TwoStep
    if seq =='effiFitter':
        setupEffiFitter = deepcopy(EfficiencyFitter.templateConfig())
        setupEffiFitter.update({
            'name'  : "effiFitter.{0}".format(Year),
            'label' : '_ts' if TwoStep else '',
            'datahist': "effiHistReader.h2_accXrec.{0}".format(Year), # 2D Histogram
            'data'  : "effiHistReader.accXrec.{0}".format(Year), # 2D RooDataHist
            'dataX' : "effiHistReader.h_accXrec_fine_ProjectionX.{0}".format(Year), # TH1D CosThetaL 
            'dataY' : "effiHistReader.h_accXrec_fine_ProjectionY.{0}".format(Year), # TH1D CosThetaK
            'pdf'   : "effi_sigA{}.{}".format('_ts' if TwoStep else '', Year),
            'pdfX'  : "effi_cosl{}.{}".format('_ts' if TwoStep else '', Year),
            'pdfY'  : "effi_cosK{}.{}".format('_ts' if TwoStep else '', Year),
        })
        effiFitter = EfficiencyFitter(setupEffiFitter)
        return effiFitter
    if seq is 'accEffiFitter':
        setupEffiFitter = deepcopy(EfficiencyFitter.templateConfig())
        setupEffiFitter.update({
            'name'  : "accEffiFitter.{0}".format(Year),
            'label' : "_acc",
            'datahist': "effiHistReader.hist2_acc.{0}".format(Year) if (binKey=="belowJpsiA" or (binKey=="belowJpsiB" and Year==2018)) else "effiHistReader.hist2_acc_fine.{0}".format(Year), # 2D Histogram
            'data'  : "effiHistReader.acc.{0}".format(Year) if (binKey=="belowJpsiA" or (binKey=="belowJpsiB" and Year==2018)) else "effiHistReader.acc_fine.{0}".format(Year), # 2D RooDataHist
            'dataX' : "effiHistReader.h_acc_fine_ProjectionX.{0}".format(Year), # TH1D CosThetaL 
            'dataY' : "effiHistReader.h_acc_fine_ProjectionY.{0}".format(Year), # TH1D CosThetaK
            'pdf'   : "effi_sigA_acc.{0}".format(Year),
            'pdfX'  : "effi_cosl_acc.{0}".format(Year),
            'pdfY'  : "effi_cosK_acc.{0}".format(Year),
        })
        return EfficiencyFitter(setupEffiFitter)
    if seq is 'recEffiFitter':
        setupEffiFitter = deepcopy(EfficiencyFitter.templateConfig())
        setupEffiFitter.update({
            'name'  : "recEffiFitter.{0}".format(Year),
            'label' : "_rec",
            'datahist': "effiHistReader.hist2_rec.{0}".format(Year) if binKey=="belowJpsiA" else "effiHistReader.hist2_rec_fine.{0}".format(Year), # 2D Histogram
            'data'  : "effiHistReader.rec.{0}".format(Year) if binKey=="belowJpsiA" else "effiHistReader.rec_fine.{0}".format(Year), # 2D RooDataHist
            'dataX' : "effiHistReader.h_rec_fine_ProjectionX.{0}".format(Year), # TH1D CosThetaL 
            'dataY' : "effiHistReader.h_rec_fine_ProjectionY.{0}".format(Year), # TH1D CosThetaK
            'pdf'   : "effi_sigA_rec.{0}".format(Year),
            'pdfX'  : "effi_cosl_rec.{0}".format(Year),
            'pdfY'  : "effi_cosK_rec.{0}".format(Year),
        })
        return EfficiencyFitter(setupEffiFitter)
    if seq == 'effiFitter2':
        setupBkgCombAFitter = deepcopy(setupTemplateFitter)
        setupBkgCombAFitter.update({
            'name': "effiFitter2.{}".format(Year),
            'data': "effiHistReader.accXrec.{0}".format(Year),
            'pdf': "effi_sigA{}.{}".format('_ts' if TwoStep else '', Year),
            #'argPattern': [r'[kl][\d]_ts+'],
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgCombAFitter)
    if seq == 'sig2DFitter':
        setupSig2DFitter = deepcopy(setupTemplateFitter)
        setupSig2DFitter.update({
            'name': "sig2DFitter.{0}".format(Year),
            'data': "sigMCReader.{0}.{1}".format(Year, "altFit" if AltRange else "Fit"),
            'pdf': "f_sig2D{}.{}".format('_ts' if TwoStep else '', Year),
            'FitHesse': True,
            'FitMinos': [True, ()],
            'argPattern': ['unboundAfb', 'unboundFl'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasRECO_Alt if AltRange else ArgAliasRECO,
        })
        return StdFitter(setupSig2DFitter)
    if seq == 'sig3DFitter':
        setupSig3DFitter = deepcopy(setupTemplateFitter)
        setupSig3DFitter.update({
            'name': "sig3DFitter.{0}".format(Year),
            'data': "sigMCReader.{0}.{1}".format(Year, "altFit" if AltRange else "Fit"),
            'pdf': "f_sig3D{}.{}".format('_ts' if TwoStep else '', Year),
            'FitHesse': True,
            'FitMinos': [True if self.cfg['args'].seqKey=='sigMCValidation' else False, ()],
            'argPattern': ['unboundAfb', 'unboundFl'] if self.cfg['args'].seqKey=='sigMCValidation' else ['unboundAfb', 'unboundFl', '^sigM.*'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasRECO_Alt if AltRange else ArgAliasRECO,
        })
        return StdFitter(setupSig3DFitter)
    if seq == 'sigAFitter':
        setupSigAFitter = deepcopy(setupTemplateFitter)
        setupSigAFitter.update({
            'name': "sigAFitter.{0}".format(Year),
            'data': "sigMCGENReader.{0}.Fit".format(Year),
            'pdf': "f_sigA.{0}".format(Year),
            'FitHesse': True,
            'FitMinos': [True, ()],
            'argPattern': ['unboundAfb', 'unboundFl'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasGEN,
        })
        sigAFitter=StdFitter(setupSigAFitter)
        sigAFitter._bookPdfData = types.MethodType(sigAFitter_bookPdfData, sigAFitter)
        return sigAFitter
    if seq == 'sigAFitterCorrected':
        setupSigAFitter = deepcopy(setupTemplateFitter)
        setupSigAFitter.update({
            'name': "sigAFitterCorrected.{0}".format(Year),
            'data': "sigMCGENReader.{0}.Fit".format(Year),
            'pdf': "f_sigA_corrected.{0}".format(Year),
            'FitHesse': True,
            'FitMinos': [True, ()],
            'argPattern': ['unboundAfb', 'unboundFl'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasGEN,
        })
        sigAFitter=StdFitter(setupSigAFitter)
        sigAFitter._bookPdfData = types.MethodType(sigAFitter_bookPdfData, sigAFitter)
        return sigAFitter
    if seq == 'bkgCombAFitter':
        setupBkgCombAFitter = deepcopy(setupTemplateFitter)
        setupBkgCombAFitter.update({
            'name': "bkgCombAFitter{}.{}".format('_Alt' if AltRange else '', Year),
            'data': "dataReader.{}.{}SB".format(Year, 'alt' if AltRange else ''),
            'pdf': "f_bkgCombA{}.{}".format("_Alt" if AltRange else "", Year),
            'argPattern': [r'bkgComb[KL]_c[\d]+',  r'bkgComb[KL]_c[\d]_Alt+'],
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgCombAFitter)
    if seq == 'SimulFitter_bkgCombA':
        setupSimulFitter_bkgCombA = deepcopy(setupTemplateSimFitter)
        setupSimulFitter_bkgCombA.update({
            'category'  : ['LSB{}'.format(str(Year).strip('20')), 'USB{}'.format(str(Year).strip('20'))],
            'data'      : ["dataReader.{}.LSB".format(Year), "dataReader.{}.USB".format(Year)],
            'pdf'       : ["f_bkgCombA.{}".format(Year), "f_bkgCombA.{}".format(Year)],
            'Years'     : [Year, Year],
            #'argPattern': [r'bkgComb[KL]_c[\d]+', ],
            'argAliasInDB': None,
            'LegName'  : 'Simulation',
            'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(0)],],
        })
        return SimultaneousFitter(setupSimulFitter_bkgCombA)
    if seq is 'finalFitter':
        setupFinalFitter = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigM) + nBkg(fBkgM*fBkgA)
        setupFinalFitter.update({
            'name': "finalFitter.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_final.{}".format(Year),
            'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitHesse': True,
            'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
            'argAliasInDB': {**ArgAliasGEN},
            'argAliasSaveToDB': False,
        })
        return StdFitter(setupFinalFitter)
    if seq is 'sigMDCBFitter':
        setupSigMDCBFitter = deepcopy(setupTemplateFitter)
        setupSigMDCBFitter.update({
            'name': "sigMDCBFitter.{0}".format(Year),
            'data': "sigMCReader.{0}.Fit".format(Year),
            'pdf': "f_sigMDCB.{0}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            #'argPattern': ['cbs[12]_sigma', 'cbs[12]_alpha', 'cbs[12]_n', 'cbs_mean', 'sigMDCB_frac'],
            'createNLLOpt': [],
            #'argAliasInDB': ArgAliasDCB,
            'argAliasSaveToDB': True,
        })
        return StdFitter(setupSigMDCBFitter)
    #'_DCBG_Alt' if AltRange and binKey not in ['summary', 'summaryLowQ2'] and Year==2017 else ('_Alt' if AltRange else '')
    if seq == 'sigMFitter':
        setupSigMDCBFitter = deepcopy(setupTemplateFitter)
        setupSigMDCBFitter.update({
            'name': "sigMFitter{}.{}".format('_Alt' if AltRange else '', Year),
            'data': "sigMCReader.{}.{}Fit".format(Year, 'alt' if AltRange else ''),
            'pdf': "f_sigM{}.{}".format('_Alt' if AltRange else '', Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupSigMDCBFitter)
    if seq is 'finalFitter_AltM':
        setupFinalFitter_AltM = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgM*fBkgA)
        setupFinalFitter_AltM.update({
            'name': "finalFitter_AltM.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_final_AltM.{}".format(Year),
            'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitHesse': True,
            'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
            'argAliasInDB': {**ArgAliasDCB, **ArgAliasGEN},
            'argAliasSaveToDB': False,
        })
        return StdFitter(setupFinalFitter_AltM)
    if seq == 'bkgM_KStarFitter':
        setupBkgMFitter_KStar = deepcopy(setupTemplateFitter)
        setupBkgMFitter_KStar.update({
            'name': "bkgM_KStarFitter{}.{}".format('_Alt' if AltRange else '', Year),
            'data': "KsigMCReader.{}.{}Fit".format(Year, 'alt' if AltRange else ''),
            'pdf': "f_bkgM_KStar{}.{}".format('_Alt' if AltRange else '', Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            #'argPattern': ['cbs[12]_sigma_KStar', 'cbs[12]_alpha_KStar', 'cbs[12]_n_KStar', 'cbs_mean_KStar', 'bkgM_frac_KStar', 'bkgM_frac[\d]_KStar', r'bkgMKStar_c[\d]+'],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgMFitter_KStar)
    if seq == 'bkgA_KStarFitter':
        setupBkgA_KStarFitter = deepcopy(setupTemplateFitter)
        setupBkgA_KStarFitter.update({
            'name': "bkgA_KStarFitter{}.{}".format('_Alt' if AltRange else '', Year),
            'data': "KsigMCReader.{}.{}Fit".format(Year, 'alt' if AltRange else ''),
            'pdf': "f_bkgA_KStar{}.{}".format('_Alt' if AltRange else '', Year),
            #'argPattern': [r'bkgKStar[KL]_c[\d]+', r'bkgA_frac[\d]_KStar',],
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgA_KStarFitter)
    if seq == 'bkgPeak3DFitter':
        setupBkgPeak3DFitter = deepcopy(setupTemplateFitter)
        setupBkgPeak3DFitter.update({
            'name': "bkgPeak3DFitter{}.{}".format('_Alt' if AltRange else '', Year),
            'data': "KsigMCReader.{}.{}Fit".format(Year, 'alt' if AltRange else ''),
            'pdf': "f_bkg_KStar{}.{}".format('_Alt' if AltRange else '', Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgPeak3DFitter)
    if seq == 'finalFitter_WithKStar':
        setupFinalFitter_WithKStar = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig3D) + nBkg(fBkgM*fBkgA) + nBkgPeak(fBkgPeak)
        setupFinalFitter_WithKStar.update({
            'name': "finalFitter_WithKStar_ts.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_final_WithKStar_ts.{}".format(Year),
            'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+', r'bkgCombM_c[\d]_Alt+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitHesse': True,
            'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
            'argAliasInDB': {**ArgAliasGEN},
            'argAliasSaveToDB': False,
        })
        return StdFitter(setupFinalFitter_WithKStar)

    if seq == 'finalFitter_WithKStar_AltA': # Final PDF with non-parametric bkg shape
        setupFinalFitter_WithKStar = deepcopy(setupTemplateFitter)
        setupFinalFitter_WithKStar.update({
            'name': "finalFitter_WithKStar_AltA.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_final_WithKStar_AltA.{}".format(Year),
            'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+', r'bkgCombM_c[\d]_Alt+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitHesse': True,
            'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
            'argAliasInDB': {'unboundAfb':'unboundAfb_altBkgCombA', 'unboundFl':'unboundFl_altBkgCombA'},
            'argAliasFromDB': {**ArgAliasGEN},
            'argAliasSaveToDB': True,
        })
        return StdFitter(setupFinalFitter_WithKStar)

    #For Validation
    if seq is 'sigPhiMFitter_JP': #Phi mass for comparison
        setupSigMFitter_JP = deepcopy(setupTemplateFitter)
        setupSigMFitter_JP.update({
            'name': "sigPhiMFitter_JP.{}".format(Year),
            'data': "sigMCReader_JP.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_sigPhiM3.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'argAliasInDB': {**ArgAlias_PhiM_JP},
            'createNLLOpt': [ROOT.RooFit.Range(1.016, 1.024),],
        })
        return StdFitter(setupSigMFitter_JP)
    if seq is 'finalPhiMFitter_JP': #Phi mass from data for comparison with MC
        setupfinalPhiMFitter_JP = deepcopy(setupTemplateFitter)
        setupfinalPhiMFitter_JP.update({
            'name': "finalPhiMFitter_JP.{}".format(Year),
            'data': "dataReader.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_finalPhiM.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'argAliasInDB': {**ArgAlias_PhiM_JP},
            'createNLLOpt': [ROOT.RooFit.Range(1.016, 1.024),],
            'argAliasSaveToDB': False,
        })
        return StdFitter(setupfinalPhiMFitter_JP)
    if seq is 'sigMFitter_JP': #Singal fit for JpsiPhi peak fit
        setupSigMFitter_JP = deepcopy(setupTemplateFitter)
        setupSigMFitter_JP.update({
            'name': "sigMFitter_JP.{}".format(Year),
            'data': "sigMCReader_JP.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_sigM_DCBG_JP.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupSigMFitter_JP)
    if seq is 'bkgMFitter_JK': #Peaking bkg fit for JpsiPhi peak fit: JK = JpsiK*
        setupBkgMFitter_JK = deepcopy(setupTemplateFitter)
        setupBkgMFitter_JK.update({
            'name': "bkgMFitter_JK.{}".format(Year),
            'data': "bkgMCReader_JK.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_sigMDCB_JK.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'argPattern': [r'^.*$'], #['cbs[12]_sigma', 'cbs[12]_alpha', 'cbs[12]_n', 'cbs_mean', 'sigM_frac[12]', 'sigMGauss_mean', 'sigMGauss1_sigma'],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgMFitter_JK)
    if seq is 'sigMFitter_PP': #Singal fit for PsiPhi peak fit
        setupSigMFitter_JP = deepcopy(setupTemplateFitter)
        setupSigMFitter_JP.update({
            'name': "sigMFitter_PP.{}".format(Year),
            'data': "sigMCReader_PP.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_sigM_DCBG_PP.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupSigMFitter_JP)
    if seq is 'bkgMFitter_PK': #Peaking bkg fit for PsiPhi peak fit: PK = PsiK*
        setupBkgMFitter_PK = deepcopy(setupTemplateFitter)
        setupBkgMFitter_PK.update({
            'name': "bkgMFitter_PK.{}".format(Year),
            'data': "bkgMCReader_PK.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_sigM_DCBG_PK.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgMFitter_PK)

    if seq is 'finalMFitter':
        setupFinalMFitter = deepcopy(setupTemplateFitter)               # Final Mass PDF = nSig(SigM)+nBkg(fBkgM)+nBkgP(fBkgP)
        setupFinalMFitter.update({
            'name': "finalMFitter.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_finalM.{}".format(Year),
            'argPattern': ['nSig', 'nBkgComb', 'nBkgPeak', r'bkgCombM_c[\d]+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitMinos': [True, ('nSig', 'nBkgComb', 'nBkgPeak')],
        })
        return StdFitter(setupFinalMFitter)
    if seq is 'finalMFitter_JP':
        setupFinalMFitter_JP = deepcopy(setupTemplateFitter)                        # Final Mass PDF = nSig(SigM)+nBkg(fBkgM)
        setupFinalMFitter_JP.update({
            'name': "finalMFitter_JP.{}".format(Year),
            'data': "dataReader.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_finalM_JP.{}".format(Year),
            'argPattern': ['nSig', 'nBkgComb', 'nBkgPeak', r'bkgCombM_c[\d]_JP+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitMinos': [True, ('nSig', 'nBkgComb', 'nBkgPeak')],
            'argAliasInDB': {'nSig':'nSig_JP', 'nBkgComb':'nBkgComb_JP', 'nBkgPeak':'nBkgPeak_JP'},
            'argAliasSaveToDB': True,
        })
        return StdFitter(setupFinalMFitter_JP)
    if seq is 'finalMFitter_PP':
        setupFinalMFitter_PP = deepcopy(setupTemplateFitter)                        # Final Mass PDF = nSig(SigM)+nBkg(fBkgM)
        setupFinalMFitter_PP.update({
            'name': "finalMFitter_PP.{}".format(Year),
            'data': "dataReader.{}.Fit_antiResVeto".format(Year),
            'pdf': "f_finalM_PP.{}".format(Year),
            'argPattern': ['nSig', 'nBkgComb', 'nBkgPeak', r'bkgCombM_c[\d]_PP+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitMinos': [True, ('nSig', 'nBkgComb', 'nBkgPeak')],
            'argAliasInDB': {'nSig':'nSig_PP', 'nBkgComb':'nBkgComb_PP', 'nBkgPeak':'nBkgPeak_PP'},
            'argAliasSaveToDB': True,
        })
        return StdFitter(setupFinalMFitter_PP)


setupSigGENFitter = deepcopy(setupTemplateFitter) #Unimplemented
setupSigGENFitter.update({
    'name': "sigGENFitter",
    'data': "sigMCGENReader.Fit",
    'pdf': "f_sigA",
    'argPattern': ['unboundAfb', 'unboundFl'],
    'createNLLOpt': [],
    'argAliasInDB': {'unboundAfb': 'unboundAfb_GEN', 'unboundFl': 'unboundFl_GEN'},
})
sigGENFitter = StdFitter(setupSigGENFitter)

setupBkgCombMFitter = deepcopy(setupTemplateFitter)
setupBkgCombMFitter.update({
    'name': "bkgCombMFitter",
    'data': "dataReader.SB",
    'pdf': "f_bkgCombM",
    'argPattern': [r'bkgCombM_c[\d]+', ],
    'FitHesse': False,
    'FitMinos': [False, ()],
    'createNLLOpt': [],
})
bkgCombMFitter = StdFitter(setupBkgCombMFitter)

## Fitter Objects for SimultaneousFitter
from v2Fitter.Fitter.SimultaneousFitter import SimultaneousFitter
setupTemplateSimFitter = SimultaneousFitter.templateConfig()

setupSimultaneousFitter = deepcopy(setupTemplateSimFitter)
setupSimultaneousFitter.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCReader.2016.Fit", "sigMCReader.2017.Fit", "sigMCReader.2018.Fit"],
    'pdf'       : ["f_sig2D_ts.2016", "f_sig2D_ts.2017", "f_sig2D_ts.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasFromDB': {**ArgAliasRECO},
    'argAliasInDB': ArgAliasRECO,
    'LegName'  : 'Simulation',
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)],],
})
SimultaneousFitter_sig2D = SimultaneousFitter(setupSimultaneousFitter)

# 3D Signal fit
setupeSig3DFitter = deepcopy(setupTemplateSimFitter)
setupeSig3DFitter.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCReader.2016.Fit", "sigMCReader.2017.Fit", "sigMCReader.2018.Fit"],
    'pdf'       : ["f_sig3D_ts.2016", "f_sig3D_ts.2017", "f_sig3D_ts.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'Years'     : [2016, 2017, 2018],
    'argAliasFromDB': {**ArgAliasRECO},
    'argAliasInDB': ArgAliasRECO,
    'LegName'  : 'Simulation',
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(0)],],
})
SimultaneousFitter_sig3D = SimultaneousFitter(setupeSig3DFitter)

# sigMC Validation
Simul_sigMCValidation_setup = deepcopy(setupTemplateSimFitter)
Simul_sigMCValidation_setup.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCReader.2016.Fit", "sigMCReader.2017.Fit", "sigMCReader.2018.Fit"],
    'pdf'       : ["f_sig3D_ts.2016", "f_sig3D_ts.2017", "f_sig3D_ts.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'Years'     : [2016, 2017, 2018],
    'argAliasFromDB': {**ArgAliasRECO},
    'LegName'   : 'Simulation',
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)],],
})
SimultaneousFitter_sigMCValidation = SimultaneousFitter(Simul_sigMCValidation_setup)

# Privat MC fit
setupSimulFitter_sigGEN = deepcopy(setupTemplateSimFitter)
setupSimulFitter_sigGEN.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCGENReader.2016.Fit", "sigMCGENReader.2017.Fit", "sigMCGENReader.2018.Fit"],
    'pdf'       : ["f_sigA.2016", "f_sigA.2017", "f_sigA.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'Years'     : [2016, 2017, 2018],
    'LegName'  : 'Simulation',
    'argAliasFromDB': {**ArgAliasGEN},
    'argAliasInDB': ArgAliasGEN,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)], ],
})
SimulFitter_sigGEN = SimultaneousFitter(setupSimulFitter_sigGEN)

#Final Fit
setupSimFinalFitter_WithKStar = deepcopy(setupTemplateFitter)                 #3D = nSig(Sig3D) + nBkg(fBkgM*fBkgA)
setupSimFinalFitter_WithKStar.update({
    'name'      : 'SimultFitterFinal',
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.Fit", "dataReader.2017.Fit", "dataReader.2018.Fit"],
    'pdf'       : ["f_final_WithKStar_ts.2016", "f_final_WithKStar_ts.2017", "f_final_WithKStar_ts.2018"],
    'argPattern': ['unboundAfb', 'unboundFl', 'nBkgComb_2016', 'nBkgComb_2017', 'nBkgComb_2018', 
                    'nSig_2016', 'nSig_2017', 'nSig_2018', 'bkgCombM_c1_2016', 'bkgCombM_c1_2017', 'bkgCombM_c1_2018'],
    'Years'     : [2016, 2017, 2018],
    'argAliasFromDB': {**ArgAliasGEN},
    'LegName'   : 'Data',
    'argAliasSaveToDB': False,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(0)],],
})
SimFitter_Final_WithKStar = SimultaneousFitter(setupSimFinalFitter_WithKStar)

#Final Fit with non-parametric bkg PDF
setupSimFinalFitter_WithKStar_AltA = deepcopy(setupTemplateFitter)                 #3D = nSig(Sig3D) + nBkg(fBkgM*fBkgA)
setupSimFinalFitter_WithKStar_AltA.update({
    'name'      : 'SimultFitterFinal_AltA',
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.Fit", "dataReader.2017.Fit", "dataReader.2018.Fit"],
    'pdf'       : ["f_final_WithKStar_AltA.2016", "f_final_WithKStar_AltA.2017", "f_final_WithKStar_AltA.2018"],
    'argPattern': ['unboundAfb', 'unboundFl', 'nBkgComb_2016', 'nBkgComb_2017', 'nBkgComb_2018', 
                    'nSig_2016', 'nSig_2017', 'nSig_2018', 'bkgCombM_c1_2016', 'bkgCombM_c1_2017', 'bkgCombM_c1_2018'],
    'Years'     : [2016, 2017, 2018],
    'argAliasFromDB': {**ArgAliasGEN},
    'argAliasInDB': {'unboundAfb':'unboundAfb_altBkgCombA', 'unboundFl':'unboundFl_altBkgCombA'},
    'LegName'   : 'Data',
    'argAliasSaveToDB': True,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(0)],],
})
SimFitter_Final_WithKStar_AltA = SimultaneousFitter(setupSimFinalFitter_WithKStar_AltA)
     
# mixToy Validation
Simul_mixedToyValidation_setup = deepcopy(setupTemplateFitter)                 #3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgM*fBkgA)
Simul_mixedToyValidation_setup.update({
    'name'      : 'SimultFitterMixedToy',
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.Fit", "dataReader.2017.Fit", "dataReader.2018.Fit"],
    'pdf'       : ["f_final_WithKStar_ts.2016", "f_final_WithKStar_ts.2017", "f_final_WithKStar_ts.2018"],
    'argPattern': ['unboundAfb', 'unboundFl', 'nBkgComb_2016', 'nBkgComb_2017', 'nBkgComb_2018', 'nSig_2016', 'nSig_2017', 'nSig_2018'], #r'nBkgComb*.', r'nSig*.'], # 'bkgCombM_c1_2016', 'bkgCombM_c1_2017', 'bkgCombM_c1_2018'],
    'Years'     : [2016, 2017, 2018],
    'argAliasFromDB': {**ArgAliasGEN},
    'LegName'   : 'Data',
    'argAliasSaveToDB': False,
    'fitToCmds' : [[ROOT.RooFit.Strategy(3), ROOT.RooFit.InitialHesse(0), ROOT.RooFit.Minimizer('Minuit2', 'migrad'), ROOT.RooFit.Minos(0)],],
})
SimultaneousFitter_mixedToyValidation = SimultaneousFitter(Simul_mixedToyValidation_setup)

if __name__ == '__main__':
    p.setSequence([dataCollection.effiHistReader, pdfCollection.stdWspaceReader, effiFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sigMFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sig2DFitter])
    #  p.setSequence([dataCollection.dataReader, pdfCollection.stdWspaceReader, bkgCombAFitter])
    p.beginSeq()
    p.runSeq()
    p.endSeq()
