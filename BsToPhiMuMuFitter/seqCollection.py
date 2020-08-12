#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import sys, os, pdb
import ROOT
# Standard fitting procedures
predefined_sequence = {}
def SetSequences():
    predefined_sequence['loadData']     = [dataCollection.dataReader]
    predefined_sequence['loadMC']       = [dataCollection.sigMCReader]
    predefined_sequence['loadMCk']      = [dataCollection.KsigMCReader]
    predefined_sequence['loadMCGEN']    = [dataCollection.sigMCGENReader]
    predefined_sequence['buildEff']     = [dataCollection.effiHistReader]
    predefined_sequence['buildPdfs']    = [dataCollection.dataReader, pdfCollection.stdWspaceReader, pdfCollection.stdPDFBuilder]

    # For fitter validation and syst
    predefined_sequence['fitEff']       = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter]
    predefined_sequence['fitSig2D']     = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sig2DFitter]
    predefined_sequence['fitSigMCGEN']  = [dataCollection.sigMCGENReader, pdfCollection.stdWspaceReader, fitCollection.sigAFitter]
    predefined_sequence['fitall']       = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter, 
                                            dataCollection.sigMCReader, fitCollection.sig2DFitter]

    predefined_sequence['fitSigM']          = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMFitter]
    predefined_sequence['fitSigMDCB']       = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMDCBFitter]
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

    predefined_sequence['createplots'] = [dataCollection.effiHistReader, #dataCollection.KsigMCReader, 
                                        dataCollection.sigMCReader, dataCollection.sigMCGENReader, 
                                        dataCollection.dataReader, pdfCollection.stdWspaceReader, plotCollection.plotter]

from BsToPhiMuMuFitter.python.ArgParser import SetParser
parser=SetParser()
args = parser.parse_known_args()[0]

if __name__ == '__main__':
    from   BsToPhiMuMuFitter.StdProcess import p; p.work_dir="plots_"+str(args.Year)
    from   BsToPhiMuMuFitter.python.datainput import allBins
    import BsToPhiMuMuFitter.cpp
    import BsToPhiMuMuFitter.dataCollection as dataCollection
    import BsToPhiMuMuFitter.pdfCollection  as pdfCollection
    import BsToPhiMuMuFitter.fitCollection  as fitCollection
    import BsToPhiMuMuFitter.plotCollection as plotCollection
    from   BsToPhiMuMuFitter.anaSetup import q2bins

    if not args.TwoStep:  dataCollection.effiHistReader=dataCollection.effiHistReaderOneStep   # If True, use one step efficiency
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
            print "INFO: Processing {0} year data".format(str(args.Year))
            p.beginSeq()
            p.runSeq()
        finally:
            p.endSeq()
            for obj in p._sequence: obj.reset()
