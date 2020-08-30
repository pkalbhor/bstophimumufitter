#!/usr/bin/env python
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
ArgAliasGEN ={'unboundAfb': 'unboundAfb_GEN', 'unboundFl': 'unboundFl_GEN'}
def GetFitterObjects(self, seq):
    Year=self.cfg['args'].Year
    if seq is 'effiFitter':
        setupEffiFitter = deepcopy(EfficiencyFitter.templateConfig())
        setupEffiFitter.update({
            'name'  : "effiFitter.{0}".format(Year),
            'data'  : "effiHistReader.accXrec.{0}".format(Year), # 2D RooDataHist
            'dataX' : "effiHistReader.h_accXrec_fine_ProjectionX.{0}".format(Year), # TH1D CosThetaL 
            'dataY' : "effiHistReader.h_accXrec_fine_ProjectionY.{0}".format(Year), # TH1D CosThetaK
            'pdf'   : "effi_sigA.{0}".format(Year),
            'pdfX'  : "effi_cosl.{0}".format(Year),
            'pdfY'  : "effi_cosK.{0}".format(Year),
        })
        effiFitter = EfficiencyFitter(setupEffiFitter)
        return effiFitter
    if seq is 'sig2DFitter':
        setupSig2DFitter = deepcopy(setupTemplateFitter)
        setupSig2DFitter.update({
            'name': "sig2DFitter.{0}".format(Year),
            'data': "sigMCReader.{0}.Fit".format(Year),
            'pdf': "f_sig2D.{0}".format(Year),
            'FitHesse': True,
            'FitMinos': [True, ()],
            'argPattern': ['unboundAfb', 'unboundFl'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasRECO,
        })
        return StdFitter(setupSig2DFitter)
    if seq is 'sigAFitter':
        setupSigAFitter = deepcopy(setupTemplateFitter)
        setupSigAFitter.update({
            'name': "sigAFitter.{0}".format(Year),
            'data': "sigMCGENReader.{0}.Fit".format(Year),
            'pdf': "f_sigA.{0}".format(Year),
            'FitHesse': True,
            'argPattern': ['unboundAfb', 'unboundFl'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasGEN,
        })
        sigAFitter=StdFitter(setupSigAFitter)
        sigAFitter._bookPdfData = types.MethodType(sigAFitter_bookPdfData, sigAFitter)
        return sigAFitter
    if seq is 'bkgCombAFitter':
        setupBkgCombAFitter = deepcopy(setupTemplateFitter)
        setupBkgCombAFitter.update({
            'name': "bkgCombAFitter.{0}".format(Year),
            'data': "dataReader.{0}.SB".format(Year),
            'pdf': "f_bkgCombA.{0}".format(Year),
            'argPattern': [r'bkgComb[KL]_c[\d]+', ],
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgCombAFitter)



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

setupFinalFitter = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigM) + nBkg(fBkgM*fBkgA)
setupFinalFitter.update({
    'name': "finalFitter",
    'data': "dataReader.Fit",
    'pdf': "f_final",
    'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True), ],
    'FitHesse': True,
    'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
    'argAliasInDB': {**setupSigMFitter['argAliasInDB'], **ArgAliasGEN},
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
    'argAliasInDB': {**setupSigMDCBFitter['argAliasInDB'], **ArgAliasGEN},
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
    'argAliasInDB': {**setupSigMDCBFitter['argAliasInDB'], **ArgAliasGEN},
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
    'argAliasInDB': setupSigMFitter['argAliasInDB'],
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
    'argAliasInDB': setupSigMDCBFitter['argAliasInDB'],
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
    'argAliasInDB': setupSigMDCBFitter['argAliasInDB'],
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
    'argAliasInDB': {**setupSigMFitter['argAliasInDB'], **ArgAliasGEN},
    'argAliasSaveToDB': False,
})
finalFitter_WithKStar = StdFitter(setupFinalFitter_WithKStar)

from v2Fitter.Fitter.SimultaneousFitter import SimultaneousFitter
setupTemplateSimFitter = SimultaneousFitter.templateConfig()

setupSimultaneousFitter = deepcopy(setupTemplateSimFitter)
setupSimultaneousFitter.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCReader.2016.Fit", "sigMCReader.2017.Fit", "sigMCReader.2018.Fit"],
    'pdf'       : ["f_sig2D.2016", "f_sig2D.2017", "f_sig2D.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasInDB': ArgAliasRECO,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit2', 'migradimproved'), ROOT.RooFit.Minos(1)],],
})
SimultaneousFitter_sig2D = SimultaneousFitter(setupSimultaneousFitter)

setupSimulFitter_sigGEN = deepcopy(setupTemplateSimFitter)
setupSimulFitter_sigGEN.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCGENReader.2016.Fit", "sigMCGENReader.2017.Fit", "sigMCGENReader.2018.Fit"],
    'pdf'       : ["f_sigA.2016", "f_sigA.2017", "f_sigA.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasInDB': ArgAliasGEN,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.Minimizer('Minuit', 'minimize')], ],
})
SimulFitter_sigGEN = SimultaneousFitter(setupSimulFitter_sigGEN)

setupSimulFitter_bkgCombA = deepcopy(setupTemplateSimFitter)
setupSimulFitter_bkgCombA.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.SB", "dataReader.2017.SB", "dataReader.2018.SB"],
    'pdf'       : ["f_bkgCombA.2016", "f_bkgCombA.2017", "f_bkgCombA.2018"],
    'argPattern': [r'bkgComb[KL]_c[\d]+', ],
    'fitToCmds' : [],
})
SimulFitter_bkgCombA = SimultaneousFitter(setupSimulFitter_bkgCombA)



if __name__ == '__main__':
    p.setSequence([dataCollection.effiHistReader, pdfCollection.stdWspaceReader, effiFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sigMFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sig2DFitter])
    #  p.setSequence([dataCollection.dataReader, pdfCollection.stdWspaceReader, bkgCombAFitter])
    p.beginSeq()
    p.runSeq()
    p.endSeq()
