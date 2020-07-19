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
def SetSequences():
    predefined_sequence['loadData']     = [dataCollection.dataReader]
    predefined_sequence['loadMC']       = [dataCollection.sigMCReader]
    predefined_sequence['loadMCk']      = [dataCollection.KsigMCReader]
    predefined_sequence['loadMCGEN']    = [dataCollection.sigMCGENReader]
    predefined_sequence['buildEff']     = [dataCollection.effiHistReader]
    predefined_sequence['buildPdfs'] = [dataCollection.dataReader, dataCollection.KsigMCReader, pdfCollection.stdWspaceReader, 
                                        pdfCollection.stdPDFBuilder]

    # For fitter validation and syst
    predefined_sequence['fitEff']    = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter]
    predefined_sequence['fitSig2D']         = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sig2DFitter]
    predefined_sequence['fitSigMCGEN']      = [dataCollection.sigMCGENReader, pdfCollection.stdWspaceReader, fitCollection.sigAFitter]
    predefined_sequence['fitall']           = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter, dataCollection.sigMCReader, fitCollection.sig2DFitter]

    predefined_sequence['fitSigM']          = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMFitter]
    predefined_sequence['fitSigMDCB']       = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMDCBFitter]
    predefined_sequence['fitSigMBinned']    = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMBinnedFitter]
    predefined_sequence['fitBkgCombA']      = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.bkgCombAFitter]
    predefined_sequence['fitBkgCombM']      = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.bkgCombMFitter]

    predefined_sequence['fitFinalM']        = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalMFitter]
    predefined_sequence['fitFinalMDCB']     = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalMDCBFitter]
    predefined_sequence['fitFinalM_AltMM']  = [dataCollection.dataReader, pdfCollection.stdWspaceReader, 
                                              fitCollection.finalMDCB_AltBkgCombM_Fitter]
    predefined_sequence['fitFinal_altMMA']  = [dataCollection.dataReader,
                                               pdfCollection.stdWspaceReader,
                                               fitCollection.final_AltM_AltBkgCombM_AltA_Fitter]
    predefined_sequence['fitFinal3D'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalFitter]
    predefined_sequence['fitFinal3D_AltM'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalFitter_AltM]

    predefined_sequence['fitBkgM_KStar'] = [dataCollection.KsigMCReader, pdfCollection.stdWspaceReader, fitCollection.bkgM_KStarFitter]
    predefined_sequence['fitBkgA_KStar'] = [dataCollection.KsigMCReader, pdfCollection.stdWspaceReader, fitCollection.bkgA_KStarFitter]
    predefined_sequence['fitFinal3D_WithKStar'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalFitter_WithKStar]
    predefined_sequence['stdFit']     = [dataCollection.effiHistReader, 
                                        dataCollection.sigMCReader, dataCollection.dataReader, pdfCollection.stdWspaceReader, 
                                        fitCollection.effiFitter, fitCollection.sigMFitter, fitCollection.bkgCombAFitter, 
                                        fitCollection.sig2DFitter, dataCollection.sigMCGENReader, fitCollection.sigAFitter, 
                                        fitCollection.finalFitter]

    predefined_sequence['createplots'] = [dataCollection.effiHistReader, 
                                        dataCollection.sigMCReader, dataCollection.KsigMCReader, dataCollection.sigMCGENReader, 
                                        dataCollection.dataReader, pdfCollection.stdWspaceReader, plotCollection.plotter]

if __name__ == '__main__':
    parser = ArgumentParser(prog='seqCollection')
    parser.add_argument('-b', '--binKey', dest='binKey', type=str, default='bin0', help="Q2 Bin to run over")
    parser.add_argument('-s', '--seq', dest='seqKey', type=str, default=None, help="Sequence namei")
    parser.add_argument('--TwoStep', help='Use 2 Step efficiency', action='store_true')
    parser.add_argument("--list", nargs="+", default=["effi"])
    parser.add_argument('--ImportDB', help='Import variables from database', action='store_false')
    args = parser.parse_args()
    if not args.TwoStep:  dataCollection.effiHistReader=dataCollection.effiHistReaderOneStep   # Use One step efficiency
    SetSequences()
    p.cfg['bins'] = allBins if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    p.cfg['seqKey']= args.seqKey
    p.cfg['args'] = args
    if args.seqKey=="createplots":
       for plot in args.list: plotCollection.plotter.cfg['switchPlots'].append(plot) 
        
    for b in p.cfg['bins']:
        p.cfg['binKey'] = b
        p.setSequence(predefined_sequence[args.seqKey])
        try:
            p.beginSeq()
            p.runSeq()
        finally:
            p.endSeq()
            for obj in p._sequence: obj.reset()
