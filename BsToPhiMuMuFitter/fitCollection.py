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
ArgAliasGEN ={'unboundAfb': 'unboundAfb_GEN', 'unboundFl': 'unboundFl_GEN'}
ArgAliasSigM={'sigMGauss1_sigma': 'sigMGauss1_sigma_RECO', 'sigMGauss2_sigma': 'sigMGauss2_sigma_RECO', 'sigMGauss_mean': 'sigMGauss_mean_RECO', 'sigM_frac': 'sigM_frac_RECO'}
ArgAliasDCB ={'cbs1_sigma': 'cbs1_sigma_RECO', 'cbs2_sigma': 'cbs2_sigma_RECO', 'cbs1_alpha': 'cbs1_alpha_RECO', 'cbs2_alpha': 'cbs2_alpha_RECO', 'cbs1_n': 'cbs1_n_RECO', 'cbs2_n': 'cbs2_n_RECO', 'cbs_mean': 'cbs_mean_RECO', 'sigMDCB_frac': 'sigMDCB_frac_RECO'}
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
            'FitMinos': [True, ()],
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
    if seq is 'sigMFitter':
        setupSigMFitter = deepcopy(setupTemplateFitter)
        setupSigMFitter.update({
            'name': "sigMFitter.{}".format(Year),
            'data': "sigMCReader.{}.Fit".format(Year),
            'pdf': "f_sigM.{}".format(Year),
            'FitHesse': True,
            'argPattern': ['sigMGauss[12]_sigma', 'sigMGauss_mean', 'sigM_frac'],
            'createNLLOpt': [ROOT.RooFit.Range(5.2546, 5.4746),],
            'argAliasInDB': ArgAliasSigM,
        })
        return StdFitter(setupSigMFitter)
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
            'argAliasInDB': {**ArgAliasSigM, **ArgAliasGEN},
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
            'argPattern': ['cbs[12]_sigma', 'cbs[12]_alpha', 'cbs[12]_n', 'cbs_mean', 'sigMDCB_frac'],
            'createNLLOpt': [],
            'argAliasInDB': ArgAliasDCB,
            'argAliasSaveToDB': True,
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
    if seq is 'bkgM_KStarFitter':
        setupBkgMFitter_KStar = deepcopy(setupTemplateFitter)
        setupBkgMFitter_KStar.update({
            'name': "bkgM_KStarFitter.{}".format(Year),
            'data': "KsigMCReader.{}.Fit".format(Year),
            'pdf': "f_bkgM_KStar.{}".format(Year),
            'FitHesse': True,
            'FitMinos': [False, ()],
            'argPattern': ['cbs[12]_sigma_KStar', 'cbs[12]_alpha_KStar', 'cbs[12]_n_KStar', 'cbs_mean_KStar', 'bkgM_frac_KStar', 'bkgM_frac[\d]_KStar', r'bkgMKStar_c[\d]+'],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgMFitter_KStar)
    if seq is 'bkgA_KStarFitter':
        setupBkgA_KStarFitter = deepcopy(setupTemplateFitter)
        setupBkgA_KStarFitter.update({
            'name': "bkgA_KStarFitter.{}".format(Year),
            'data': "KsigMCReader.{}.Fit".format(Year),
            'pdf': "f_bkgA_KStar.{}".format(Year),
            'argPattern': [r'bkgKStar[KL]_c[\d]+', r'bkgA_frac[\d]_KStar',],
            'FitHesse': True,
            'FitMinos': [False, ()],
            'createNLLOpt': [],
        })
        return StdFitter(setupBkgA_KStarFitter)
    if seq is 'finalFitter_WithKStar':
        setupFinalFitter_WithKStar = deepcopy(setupTemplateFitter)                         # 3D = nSig(Sig2D*SigM) + nBkg(fBkgM*fBkgA)
        setupFinalFitter_WithKStar.update({
            'name': "finalFitter_WithKStar.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_final_WithKStar.{}".format(Year),
            'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombM_c[\d]+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitHesse': True,
            'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
            'argAliasInDB': {**setupSigMFitter['argAliasInDB'], **ArgAliasGEN},
            'argAliasSaveToDB': False,
        })
        return StdFitter(setupFinalFitter_WithKStar)
    if seq is 'finalFitter_AltM_WithKStar':
        setupFinalFitter_AltM_WithKStar = deepcopy(setupTemplateFitter)                 #3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgM*fBkgA)
        setupFinalFitter_AltM_WithKStar.update({
            'name': "finalFitter_AltM_WithKStar.{}".format(Year),
            'data': "dataReader.{}.Fit".format(Year),
            'pdf': "f_final_AltM_WithKStar.{}".format(Year),
            'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', 'nBkgKStar', r'bkgCombM_c[\d]+'],
            'createNLLOpt': [ROOT.RooFit.Extended(True), ],
            'FitHesse': True,
            'FitMinos': [False, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
            'argAliasInDB': {**ArgAliasDCB, **ArgAliasGEN},
            'argAliasSaveToDB': False,
        })
        return StdFitter(setupFinalFitter_AltM_WithKStar)



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


setupFinal_AltM_AltBkgCombM_AltA_Fitter = deepcopy(setupTemplateFitter)  #Alternate 3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgAltM*fBkgAltA)
setupFinal_AltM_AltBkgCombM_AltA_Fitter.update({
    'name': "final_AltM_AltBkgCombM_AltA_Fitter",
    'data': "dataReader.Fit",
    'pdf': "f_finalAltM_AltBkgCombM_AltBkgCombA",
    'argPattern': ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb', r'bkgCombMAltM_c[\d]+'],
    'createNLLOpt': [ROOT.RooFit.Extended(True),],
    'FitMinos': [True, ('nSig', 'unboundAfb', 'unboundFl', 'nBkgComb')],
    'argAliasInDB': {**ArgAliasDCB, **ArgAliasGEN},
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
    'argAliasInDB': ArgAliasSigM,
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
    'argAliasInDB': ArgAliasDCB,
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
    'argAliasInDB': ArgAliasDCB,
    'argAliasSaveToDB': False,
})
finalMDCB_AltBkgCombM_Fitter = StdFitter(setupFinalMDCB_AltBkgCombM_Fitter)

## Fitter Objects for SimultaneousFitter
from v2Fitter.Fitter.SimultaneousFitter import SimultaneousFitter
setupTemplateSimFitter = SimultaneousFitter.templateConfig()

setupSimultaneousFitter = deepcopy(setupTemplateSimFitter)
setupSimultaneousFitter.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCReader.2016.Fit", "sigMCReader.2017.Fit", "sigMCReader.2018.Fit"],
    'pdf'       : ["f_sig2D.2016", "f_sig2D.2017", "f_sig2D.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasInDB': ArgAliasRECO,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)],],
})
SimultaneousFitter_sig2D = SimultaneousFitter(setupSimultaneousFitter)

setupSimulFitter_sigGEN = deepcopy(setupTemplateSimFitter)
setupSimulFitter_sigGEN.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["sigMCGENReader.2016.Fit", "sigMCGENReader.2017.Fit", "sigMCGENReader.2018.Fit"],
    'pdf'       : ["f_sigA.2016", "f_sigA.2017", "f_sigA.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasInDB': ArgAliasGEN,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)], ],
})
SimulFitter_sigGEN = SimultaneousFitter(setupSimulFitter_sigGEN)

setupSimulFitter_bkgCombA = deepcopy(setupTemplateSimFitter)  # Not Needed
setupSimulFitter_bkgCombA.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.SB", "dataReader.2017.SB", "dataReader.2018.SB"],
    'pdf'       : ["f_bkgCombA.2016", "f_bkgCombA.2017", "f_bkgCombA.2018"],
    'argPattern': [r'bkgComb[KL]_c[\d]+', ],
    'fitToCmds' : [],
})
SimulFitter_bkgCombA = SimultaneousFitter(setupSimulFitter_bkgCombA)

setupSimFitterFinal_AltM = deepcopy(setupTemplateSimFitter)
setupSimFitterFinal_AltM.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.Fit", "dataReader.2017.Fit", "dataReader.2018.Fit"],
    'pdf'       : ["f_final_AltM.2016", "f_final_AltM.2017", "f_final_AltM.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasInDB': {**ArgAliasDCB, **ArgAliasGEN},
    'argAliasSaveToDB': False,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)],],
})
SimultaneousFitter_Final_AltM = SimultaneousFitter(setupSimFitterFinal_AltM)

setupSimFinalFitter_AltM_WithKStar = deepcopy(setupTemplateFitter)                 #3D = nSig(Sig2D*SigMDCB) + nBkg(fBkgM*fBkgA)
setupSimFinalFitter_AltM_WithKStar.update({
    'category'  : ['cat16', 'cat17', 'cat18'],
    'data'      : ["dataReader.2016.Fit", "dataReader.2017.Fit", "dataReader.2018.Fit"],
    'pdf'       : ["f_final_AltM_WithKStar.2016", "f_final_AltM_WithKStar.2017", "f_final_AltM_WithKStar.2018"],
    'argPattern': ['unboundAfb', 'unboundFl'],
    'argAliasInDB': {**ArgAliasDCB, **ArgAliasGEN},
    'argAliasSaveToDB': False,
    'fitToCmds' : [[ROOT.RooFit.Strategy(2), ROOT.RooFit.InitialHesse(1), ROOT.RooFit.Minimizer('Minuit', 'minimize'), ROOT.RooFit.Minos(1)],],
})
SimFitter_Final_AltM_WithKStar = SimultaneousFitter(setupSimFinalFitter_AltM_WithKStar)

if __name__ == '__main__':
    p.setSequence([dataCollection.effiHistReader, pdfCollection.stdWspaceReader, effiFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sigMFitter])
    #  p.setSequence([dataCollection.sigMCReader, pdfCollection.stdWspaceReader, sig2DFitter])
    #  p.setSequence([dataCollection.dataReader, pdfCollection.stdWspaceReader, bkgCombAFitter])
    p.beginSeq()
    p.runSeq()
    p.endSeq()
