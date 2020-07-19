#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 sts=4 fdm=indent fdl=0 fdn=3 ft=python et:

import types
from copy import deepcopy

import ROOT

import BsToPhiMuMuFitter.cpp
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.StdFitter import StdFitter, flToUnboundFl, afbToUnboundAfb
from BsToPhiMuMuFitter.EfficiencyFitter import EfficiencyFitter
from BsToPhiMuMuFitter.BinnedFitter import BinnedFitter

from BsToPhiMuMuFitter.StdProcess import p
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
from BsToPhiMuMuFitter.anaSetup import bMassRegions

setupTemplateFitter = StdFitter.templateConfig()

setupEffiFitter = deepcopy(EfficiencyFitter.templateConfig())
setupEffiFitter.update({
    'name': "effiFitter",
    'data': "effiHistReader.accXrec", # 2D RooDataHist
    'dataX': "effiHistReader.h_accXrec_fine_ProjectionX", # TH1D CosThetaL 
    'dataY': "effiHistReader.h_accXrec_fine_ProjectionY", # TH1D CosThetaK
    'pdf': "effi_sigA",
    'pdfX': "effi_cosl",
    'pdfY': "effi_cosK",
})
effiFitter = EfficiencyFitter(setupEffiFitter)

setupSigMFitter = deepcopy(setupTemplateFitter)
setupSigMFitter.update({
    'name': "sigMFitter",
    'data': "sigMCReader.Fit",
    'pdf': "f_sigM",
    'FitHesse': True,
    'argPattern': ['sigMGauss[12]_sigma', 'sigMGauss_mean', 'sigM_frac'],
    'createNLLOpt': [ROOT.RooFit.Range(5.2546, 5.4746),],
    'argAliasInDB': {'sigMGauss1_sigma': 'sigMGauss1_sigma_RECO', 'sigMGauss2_sigma': 'sigMGauss2_sigma_RECO', 'sigMGauss_mean': 'sigMGauss_mean_RECO', 'sigM_frac': 'sigM_frac_RECO'},
    'argAliasSaveToDB': True,
})
sigMFitter = StdFitter(setupSigMFitter)

setupSigMDCBFitter = deepcopy(setupTemplateFitter)
setupSigMDCBFitter.update({
    'name': "sigMDCBFitter",
    'data': "sigMCReader.Fit",
    'pdf': "f_sigMDCB",
    'FitHesse': True,
    'argPattern': ['cbs[12]_sigma', 'cbs[12]_alpha', 'cbs[12]_n', 'cbs_mean', 'sigMDCB_frac'],
    'createNLLOpt': [],
    'argAliasInDB': {'cbs1_sigma': 'cbs1_sigma_RECO', 'cbs2_sigma': 'cbs2_sigma_RECO', 'cbs1_alpha': 'cbs1_alpha_RECO', 'cbs2_alpha': 'cbs2_alpha_RECO', 'cbs1_n': 'cbs1_n_RECO', 'cbs2_n': 'cbs2_n_RECO', 'cbs_mean': 'cbs_mean_RECO', 'sigMDCB_frac': 'sigMDCB_frac_RECO'},
    'argAliasSaveToDB': True,
})
sigMDCBFitter = StdFitter(setupSigMDCBFitter)

setupSigMBinnedFitter = deepcopy(setupTemplateFitter)
setupSigMBinnedFitter.update({
    'name': "sigMBinnedFitter",
    'data': "sigMCReader.Fit",
    'pdf': "f_sigM",
    'FitHesse': True,
    'argPattern': ['sigMGauss[12]_sigma', 'sigMGauss_mean', 'sigM_frac'],
    'createNLLOpt': [ROOT.RooFit.Range(5.15, 5.55),],
    'argAliasInDB': {'sigMGauss1_sigma': 'sigMGauss1_sigma_RECO', 'sigMGauss2_sigma': 'sigMGauss2_sigma_RECO', 'sigMGauss_mean': 'sigMGauss_mean_RECO', 'sigM_frac': 'sigM_frac_RECO'},
})
sigMBinnedFitter = BinnedFitter(setupSigMBinnedFitter)

setupSigAFitter = deepcopy(setupTemplateFitter)
setupSigAFitter.update({
    'name': "sigAFitter",
    'data': "sigMCGENReader.Fit",
    'pdf': "f_sigA",
    'FitHesse': True,
    'argPattern': ['unboundAfb', 'unboundFl'],
    'createNLLOpt': [],
    'argAliasInDB': {'unboundAfb': 'unboundAfb_GEN', 'unboundFl': 'unboundFl_GEN'},
})
sigAFitter = StdFitter(setupSigAFitter)

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

def sigAFitter_bookPdfData(self):
    self.process.dbplayer.saveSMPrediction()
    StdFitter._bookPdfData(self)
    print("sel.data(sigAFitter): ", self.data)
    self.data.changeObservableName("genCosThetaK", "CosThetaK")
    self.data.changeObservableName("genCosThetaL", "CosThetaL")
sigAFitter._bookPdfData = types.MethodType(sigAFitter_bookPdfData, sigAFitter)

setupSig2DFitter = deepcopy(setupTemplateFitter)
setupSig2DFitter.update({
    'name': "sig2DFitter",
    'data': "sigMCReader.Fit",
    'pdf': "f_sig2D",
    'FitHesse': True,
    'FitMinos': [False, ()],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'createNLLOpt': [],
    'argAliasInDB': {'unboundAfb': 'unboundAfb_RECO', 'unboundFl': 'unboundFl_RECO'},
})
sig2DFitter = StdFitter(setupSig2DFitter)

setupBkgCombAFitter = deepcopy(setupTemplateFitter)
setupBkgCombAFitter.update({
    'name': "bkgCombAFitter",
    'data': "dataReader.SB",
    'pdf': "f_bkgCombA",
    'argPattern': [r'bkgComb[KL]_c[\d]+', ],
    'FitHesse': True,
    'FitMinos': [False, ()],
    'createNLLOpt': [],
})
bkgCombAFitter = StdFitter(setupBkgCombAFitter)

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

setupFinalFitter = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigM) + nBkg(fBkgM*fBkgA)
setupFinalFitter.update({
    'name': "finalFitter",
    'data': "dataReader.Fit",
    'pdf': "f_final",
    'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitHesse': True,
    'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMFitter['argAliasInDB'].items() + setupSigAFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
finalFitter = StdFitter(setupFinalFitter)

setupFinalFitter_AltM = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgM*fBkgA)
setupFinalFitter_AltM.update({
    'name': "finalFitter_AltM",
    'data': "dataReader.Fit",
    'pdf': "f_final_AltM",
    'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitHesse': True,
    'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMDCBFitter['argAliasInDB'].items() + setupSigAFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
finalFitter_AltM = StdFitter(setupFinalFitter_AltM)

setupFinal_AltM_AltBkgCombM_AltA_Fitter = deepcopy(setupTemplateFitter)  #Alternate 3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgAltM*fBkgAltA)
setupFinal_AltM_AltBkgCombM_AltA_Fitter.update({
    'name': "final_AltM_AltBkgCombM_AltA_Fitter",
    'data': "dataReader.Fit",
    'pdf': "f_finalAltM_AltBkgCombM_AltBkgCombA",
    'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombMAltM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True),],
    'FitMinos': [True, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMDCBFitter['argAliasInDB'].items() + setupSigAFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
final_AltM_AltBkgCombM_AltA_Fitter = StdFitter(setupFinal_AltM_AltBkgCombM_AltA_Fitter)

setupFinalMFitter = deepcopy(setupTemplateFitter)                        # Final Mass PDF = nSig(SigM)+nBkg(fBkgM)
setupFinalMFitter.update({
    'name': "finalMFitter",
    'data': "dataReader.Fit",
    'pdf': "f_finalM",
    'argPattern': ['nSig', 'nBkgComb', r'bkgCombM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitMinos': [True, ('nSig', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
finalMFitter = StdFitter(setupFinalMFitter)

setupFinalMDCBFitter = deepcopy(setupTemplateFitter)                     # Final Mass PDF: nSig(f_sigMDCB)+nBkg(fBkgM)
setupFinalMDCBFitter.update({
    'name': "finalMDCBFitter",
    'data': "dataReader.Fit",
    'pdf': "f_finalMDCB",
    'argPattern': ['nSig', 'nBkgComb', r'bkgCombM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitMinos': [True, ('nSig', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMDCBFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
finalMDCBFitter = StdFitter(setupFinalMDCBFitter)

setupFinalMDCB_AltBkgCombM_Fitter = deepcopy(setupTemplateFitter) # Final Mass Alternate Fitter: nSig(f_sigMDCB)+nBkg(fBkgAltM)
setupFinalMDCB_AltBkgCombM_Fitter.update({
    'name': "finalMDCB_AltBkgCombM_Fitter",
    'data': "dataReader.Fit",
    'pdf': "f_finalMDCB_AltBkgCombM",
    'argPattern': ['nSig', 'nBkgComb', r'bkgCombMAltM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitMinos': [True, ('nSig', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMDCBFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
finalMDCB_AltBkgCombM_Fitter = StdFitter(setupFinalMDCB_AltBkgCombM_Fitter)

setupBkgA_KStarFitter = deepcopy(setupTemplateFitter)
setupBkgA_KStarFitter.update({
    'name': "bkgA_KStarFitter",
    'data': "KsigMCReader.Fit",
    'pdf': "f_bkgA_KStar",
    'argPattern': [r'bkgKStar[KL]_c[\d]+', ],
    'FitHesse': True,
    'FitMinos': [False, ()],
    'createNLLOpt': [],
})
bkgA_KStarFitter = StdFitter(setupBkgA_KStarFitter)

setupBkgMFitter_KStar = deepcopy(setupTemplateFitter)
setupBkgMFitter_KStar.update({
    'name': "bkgM_KStarFitter",
    'data': "KsigMCReader.Fit",
    'pdf': "f_bkgM_KStar",
    'FitHesse': True,
    'argPattern': ['cbs[12]_sigma_KStar', 'cbs[12]_alpha_KStar', 'cbs[12]_n_KStar', 'cbs_mean_KStar', 'bkgM_frac_KStar', r'bkgMKStar_c[\d]+'],
    'createNLLOpt': [],
})
bkgM_KStarFitter = StdFitter(setupBkgMFitter_KStar)

setupFinalFitter_WithKStar = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigM) + nBkg(fBkgM*fBkgA)
setupFinalFitter_WithKStar.update({
    'name': "finalFitter_WithKStar",
    'data': "dataReader.Fit",
    'pdf': "f_final_WithKStar",
    'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitHesse': True,
    'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
    'argAliasInDB': dict(setupSigMFitter['argAliasInDB'].items() + setupSigAFitter['argAliasInDB'].items()),
    'argAliasSaveToDB': False,
})
finalFitter_WithKStar = StdFitter(setupFinalFitter_WithKStar)

if __name__ == '__main__':
    p.setSequence([dataCollection.effiHistReader, pdfCollection.stdWspaceReader, effiFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sigMFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sig2DFitter])
    #  p.setSequence([dataCollection.dataReader, pdfCollection.stdWspaceReader, bkgCombAFitter])
    p.beginSeq()
    p.runSeq()
    p.endSeq()
