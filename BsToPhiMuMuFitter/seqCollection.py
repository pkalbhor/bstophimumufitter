#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import sys, os, pdb
from BsToPhiMuMuFitter.python.datainput import allBins
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.toyCollection as toyCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection
import BsToPhiMuMuFitter.plotCollection as plotCollection
from BsToPhiMuMuFitter.anaSetup import q2bins
from BsToPhiMuMuFitter.StdProcess import p
from argparse import ArgumentParser

# Standard fitting procedures
predefined_sequence = {}
dataCollection.effiHistReader=dataCollection.effiHistReaderOneStep   # Use One step efficiency
loadData        = predefined_sequence['loadData'] = [dataCollection.dataReader]
loadMC          = predefined_sequence['loadMC'] = [dataCollection.sigMCReader]
loadMCGEN       = predefined_sequence['loadMCGEN'] = [dataCollection.sigMCGENReader]
buildAllPdfs    = predefined_sequence['buildAllPdfs'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, pdfCollection.stdPDFBuilder]
buildEfficiencyHist = predefined_sequence['buildEfficiencyHist'] = [dataCollection.effiHistReader]

fitEfficiency   = predefined_sequence['fitEfficiency'] = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter]
fitSigM         = predefined_sequence['fitSigM'] = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMFitter]
fitSigMDCB         = predefined_sequence['fitSigMDCB'] = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMDCBFitter]
fitSigMBinned   = predefined_sequence['fitSigMBinned'] = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMBinnedFitter]
fitBkgCombA     = predefined_sequence['fitBkgCombA'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.bkgCombAFitter]
fitBkgCombM     = predefined_sequence['fitBkgCombM'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.bkgCombMFitter]

predefined_sequence['fitFinalM'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalMFitter]
predefined_sequence['fitFinalMDCB'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalMDCBFitter]
predefined_sequence['fitFinalM_AltMM'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalMDCB_AltBkgCombM_Fitter]
predefined_sequence['fitFinal_altMMA']=[dataCollection.dataReader,pdfCollection.stdWspaceReader,fitCollection.final_AltM_AltBkgCombM_AltA_Fitter]
predefined_sequence['fitFinal3D'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalFitter]

stdFit          = predefined_sequence['stdFit'] = [dataCollection.effiHistReader, dataCollection.sigMCReader, dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter, fitCollection.sigMFitter, fitCollection.bkgCombAFitter, fitCollection.sig2DFitter, dataCollection.sigMCGENReader, fitCollection.sigAFitter, fitCollection.finalFitter]

# For fitter validation and syst
fitSig2D        = predefined_sequence['fitSig2D'] = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sig2DFitter]
fitSigMCGEN     = predefined_sequence['fitSigMCGEN'] = [dataCollection.sigMCGENReader, pdfCollection.stdWspaceReader, fitCollection.sigAFitter]
fitall          = predefined_sequence['fitall'] = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter, dataCollection.sigMCReader, fitCollection.sig2DFitter]

createplots = predefined_sequence['createplots'] = [plotCollection.Bkgplotter]#myplotter]

if __name__ == '__main__':
    parser = ArgumentParser(prog='seqCollection')
    parser.add_argument('-b', '--binKey', dest='binKey', type=str, default=p.cfg['binKey'])
    parser.add_argument('-s', '--seq', dest='seqKey', type=str, default=None)
    args = parser.parse_args()
    if args.binKey =="all":                                                                                                                    
        p.cfg['bins'] = allBins
    else: 
        p.cfg['bins'] = [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['seqKey']= args.seqKey
    #pdb.set_trace()
    for b in p.cfg['bins']:
        p.cfg['binKey'] = b
        p.setSequence(predefined_sequence[args.seqKey])
        try:
            p.beginSeq()
            p.runSeq()
        finally:
            p.endSeq()
            for obj in p._sequence: obj.reset()
