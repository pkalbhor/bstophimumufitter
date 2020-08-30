#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import sys, os, pdb
import ROOT

#Supress Info messages for RooClasses
#ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = kUnset;")
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)

# Standard fitting procedures
predefined_sequence = {}
def SetSequences():

    # For fitter validation and syst
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

from BsToPhiMuMuFitter.python.ArgParser import SetParser, GetBatchTaskParser
parser=GetBatchTaskParser()
args = parser.parse_known_args()[0]
import BsToPhiMuMuFitter.fitCollection  as fitCollection
predefined_sequence['loadData']  = ['dataReader']
predefined_sequence['loadMC']    = ['sigMCReader']
predefined_sequence['loadMCGEN'] = ['sigMCGENReader']
predefined_sequence['loadMCk']   = ['KsigMCReader']
predefined_sequence['buildPdfs'] = ['dataReader', 'stdWspaceReader', 'stdPDFBuilder']
predefined_sequence['buildEff']  = ['effiHistReader']
predefined_sequence['fitEff']    = ['effiHistReader', 'stdWspaceReader', 'effiFitter']
predefined_sequence['fitSig2D']  = (['sigMCReader', 'stdWspaceReader'], ['SimultaneousFitter_sig2D'] if args.SimFit else ['sig2DFitter'])
predefined_sequence['fitSigMCGEN']=(['sigMCGENReader', 'stdWspaceReader'], ['SimulFitter_sigGEN', 'plotter'] if args.SimFit else ['sigAFitter'])
predefined_sequence['fitBkgCombA']=(['dataReader', 'stdWspaceReader'], ['SimulFitter_bkgCombA', 'plotter'] if args.SimFit else ['bkgCombAFitter'])
predefined_sequence['createplots']=['effiHistReader', 'dataReader', 'sigMCReader', 'sigMCGENReader', 'stdWspaceReader', 'plotter']
#'effiHistReader', 'KsigMCReader', 'sigMCReader', 'sigMCGENReader', 
predefined_sequence['sigMCValidation'] = ['stdWspaceReader', 'sigMCReader', 'sigMCStudier']

def Instantiate(self, seq):
    """All objects are initalized here"""
    # Classes in use are: DataReader, WSpaceReader, StdFitter, ObjectProvider, EfficiencyFitter, Plotter
    from BsToPhiMuMuFitter.dataCollection import GetDataReader
    import BsToPhiMuMuFitter.pdfCollection  as pdfCollection
    from BsToPhiMuMuFitter.fitCollection import GetFitterObjects
    from BsToPhiMuMuFitter.plotCollection import GetPlotterObject
    sequence=[]
    for s in seq:
        if s is 'sigMCReader' or s is 'dataReader' or s is 'sigMCGENReader' or s is 'KsigMCReader':
            sequence.append(GetDataReader(self, s))
        if s is 'stdWspaceReader':
            sequence.append(pdfCollection.GetWspaceReader(self))
        if s is 'stdPDFBuilder':
            sequence.append(pdfCollection.stdPDFBuilder)
        if s is 'effiHistReader':
            sequence.append(dataCollection.effiHistReaderOneStep)
        if s is 'sig2DFitter' or s is 'sigAFitter' or s is 'bkgCombAFitter' or s is 'effiFitter':
            sequence.append(GetFitterObjects(self, s))
        if s is 'plotter':
            sequence.append(GetPlotterObject(self))
        if s is 'SimultaneousFitter_sig2D':
            sequence.append(fitCollection.SimultaneousFitter_sig2D)
        if s is 'SimulFitter_sigGEN':
            sequence.append(fitCollection.SimulFitter_sigGEN)
        if s is 'SimulFitter_bkgCombA':
            sequence.append(fitCollection.SimulFitter_bkgCombA)
        if s is 'sigMCStudier':
            sequence.append(batchTask_sigMCValidation.GetToyObject(self))
    return sequence

if __name__ == '__main__':
    from   BsToPhiMuMuFitter.StdProcess import p; 
    import BsToPhiMuMuFitter.cpp
    import BsToPhiMuMuFitter.dataCollection as dataCollection
    from   BsToPhiMuMuFitter.anaSetup import q2bins
    from BsToPhiMuMuFitter.python.datainput import GetInputFiles
    
    p.work_dir="plots_"+str(args.Year)
    p.cfg['seqKey']= args.seqKey
    p.cfg['args'] = args
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]

    if (not args.SimFit) and (type(predefined_sequence[args.seqKey]) is tuple):
        predefined_sequence[args.seqKey]=predefined_sequence[args.seqKey][0]+predefined_sequence[args.seqKey][1]
    if args.SimFit or args.SimFitPlots:
        p.name="SimultaneousFitProcess"; p.work_dir="plots_simultaneous"
    if args.seqKey=='sigMCValidation':
        p.name='sigMCValidationProcess'

    for b in p.cfg['bins']:
        p.cfg['binKey'] = b
        try:
            if args.SimFit:
                print ("INFO: Processing simultaneously over three year data")
                for Year in [2016, 2017, 2018]:
                    p.cfg['args'].Year=Year
                    GetInputFiles(p)
                    sequence=Instantiate(p, predefined_sequence[args.seqKey][0])
                    p.setSequence(sequence)
                    p.beginSeq()
                    p.runSeq()
                sequence=Instantiate(p, predefined_sequence[args.seqKey][1])
                p.setSequence(sequence)
                p.beginSeq()
            elif p.name=='sigMCValidationProcess':
                print("INFO: Processing {0} year data".format(args.Year))
                from BsToPhiMuMuFitter.anaSetup import modulePath
                import BsToPhiMuMuFitter.script.batchTask_sigMCValidation as batchTask_sigMCValidation
                wrappedTask = batchTask_sigMCValidation.BatchTaskWrapper(
                    "myBatchTask",
                    os.path.join(modulePath, "batchTask_sigMCValidation"),
                    cfg=batchTask_sigMCValidation.setupBatchTask)
                parser.set_defaults(
                    wrapper=wrappedTask,
                    process=p)
                p.cfg['args'] = args = parser.parse_args()   
                sequence=Instantiate(p, predefined_sequence[args.seqKey])
                p.setSequence(sequence)
                args.func(args) 
                continue
            else:
                print("INFO: Processing {0} year data".format(str(args.Year)))
                sequence=Instantiate(p, predefined_sequence[args.seqKey])
                p.setSequence(sequence)
                p.beginSeq()
            p.runSeq()
        finally:
            p.endSeq()
            for obj in p._sequence: obj.reset()
