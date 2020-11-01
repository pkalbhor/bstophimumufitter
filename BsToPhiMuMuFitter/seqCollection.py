#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import sys, os, pdb
import ROOT
#ROOT.EnableImplicitMT()

#Supress RooFit related info messages
ROOT.gEnv.SetValue("RooFit.Banner", 0)
ROOT.RooMsgService.instance().setGlobalKillBelow(3)

# Standard fitting procedures
predefined_sequence = {}
def SetSequences():

    # For fitter validation and syst
    predefined_sequence['fitBkgCombM']      = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.bkgCombMFitter]

    predefined_sequence['fitFinalMDCB']     = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalMDCBFitter]
    predefined_sequence['fitFinalM_AltMM']  = [dataCollection.dataReader, pdfCollection.stdWspaceReader, 
                                              fitCollection.finalMDCB_AltBkgCombM_Fitter]
    predefined_sequence['fitFinal_altMMA']  = [dataCollection.dataReader,
                                               pdfCollection.stdWspaceReader,
                                               fitCollection.final_AltM_AltBkgCombM_AltA_Fitter]
    predefined_sequence['fitFinal3D'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalFitter]



from BsToPhiMuMuFitter.python.ArgParser import SetParser, GetBatchTaskParser
parser=GetBatchTaskParser()
args = parser.parse_known_args()[0]
predefined_sequence['loadData']  = ['dataReader']
predefined_sequence['loadMC']    = ['sigMCReader']
predefined_sequence['loadMCGEN'] = ['sigMCGENReader']
predefined_sequence['loadMCk']   = ['KsigMCReader']
predefined_sequence['loadMCJ']   = ['bkgJpsiMCReader']
predefined_sequence['loadMCP']   = ['bkgPsi2sMCReader']
predefined_sequence['buildPdfs'] = ['dataReader', 'stdWspaceReader', 'stdPDFBuilder']
predefined_sequence['buildEff']  = ['effiHistReader']

predefined_sequence['fitEff']    = ['effiHistReader', 'stdWspaceReader', 'effiFitter']
predefined_sequence['fitSig2D']  = (['sigMCReader', 'stdWspaceReader'], ['SimultaneousFitter_sig2D'] if args.SimFit else ['sig2DFitter'])
predefined_sequence['fitSigMCGEN']=(['sigMCGENReader', 'stdWspaceReader'], ['SimulFitter_sigGEN'] if args.SimFit else ['sigAFitter'])
predefined_sequence['fitBkgCombA']=(['dataReader', 'stdWspaceReader'], ['SimulFitter_bkgCombA'] if args.SimFit else ['bkgCombAFitter'])
predefined_sequence['fitSigMDCB']    = ['sigMCReader', 'stdWspaceReader', 'sigMDCBFitter']
predefined_sequence['fitSigM']    = ['sigMCReader', 'stdWspaceReader', 'sigMFitter']
predefined_sequence['fitBkgM_KStar'] = ['KsigMCReader', 'stdWspaceReader', 'bkgM_KStarFitter']
predefined_sequence['fitBkgA_KStar'] = ['KsigMCReader', 'stdWspaceReader', 'bkgA_KStarFitter']

predefined_sequence['fitFinal3D_AltM']          = (['dataReader', 'stdWspaceReader'], ['SimulFitter_Final_AltM'] if args.SimFit else ['finalFitter_AltM'])
predefined_sequence['fitFinal3D_WithKStar']     = ['dataReader', 'stdWspaceReader', 'finalFitter_WithKStar']
predefined_sequence['fitFinal3D_AltM_WithKStar']= (['dataReader', 'stdWspaceReader'], ['SimFitter_Final_AltM_WithKStar'] if args.SimFit else ['finalFitter_AltM_WithKStar'])
predefined_sequence['fitFinalM']     = ['dataReader', 'stdWspaceReader', 'finalMFitter']

predefined_sequence['loadAll'] = ['dataReader', 'sigMCReader', 'KsigMCReader', 'effiHistReader', 'stdWspaceReader', 'stdPDFBuilder']
predefined_sequence['fitAll']  = predefined_sequence['loadAll'] + ['effiFitter', 'sig2DFitter', 'sigAFitter']
predefined_sequence['fitFinalAll'] = predefined_sequence['loadAll'] + ['fitSigMDCB', 'bkgCombAFitter', 'fitBkgM_KStar', 'fitBkgA_KStar', 'finalFitter_AltM_WithKStar']

predefined_sequence['createplots']=['effiHistReader', 
                                    'dataReader', 
                                    'sigMCReader', 
                                    #'sigMCGENReader', 
                                    'KsigMCReader', 
                                    #'bkgJpsiMCReader', 
                                    'stdWspaceReader', 'plotter']
#'effiHistReader', 'KsigMCReader', 'sigMCReader', 'sigMCGENReader', 
predefined_sequence['sigMCValidation'] = ['stdWspaceReader', 'sigMCReader', 'sigMCStudier']
predefined_sequence['seqCollection']   = []
predefined_sequence['FinalDataResult'] = ['FinalDataResult']
predefined_sequence['EffiTable']       = ['EffiTable']

#For Validation Study
predefined_sequence['fitSigM_JP'] = ['sigMCReader_JP', 'stdWspaceReader', 'sigMFitter_JP']
predefined_sequence['fitBkgM_JK'] = ['bkgMCReader_JK', 'stdWspaceReader', 'bkgMFitter_JK']
predefined_sequence['fitSigM_PP'] = ['sigMCReader_PP', 'stdWspaceReader', 'sigMFitter_PP']
predefined_sequence['fitBkgM_PK'] = ['bkgMCReader_PK', 'stdWspaceReader', 'bkgMFitter_PK']
predefined_sequence['fitFinalM_JP'] = ['dataReader', 'stdWspaceReader', 'finalMFitter_JP']
predefined_sequence['fitFinalM_PP'] = ['dataReader', 'stdWspaceReader', 'finalMFitter_PP']

def Instantiate(self, seq):
    """All objects are initalized here. This is needed when you want to run over all the bins in one go. Or if you want to run over different year dataset"""
    # Classes in use are: DataReader, WSpaceReader, StdFitter, ObjectProvider, EfficiencyFitter, Plotter
    import BsToPhiMuMuFitter.dataCollection as dataCollection
    import BsToPhiMuMuFitter.pdfCollection  as pdfCollection
    import BsToPhiMuMuFitter.fitCollection  as fitCollection
    from BsToPhiMuMuFitter.plotCollection import GetPlotterObject
    sequence=[]
    dataSequence=['sigMCReader', 'dataReader', 'sigMCGENReader', 'KsigMCReader', 'sigMCReader_JP', 'sigMCReader_PP', 'bkgMCReader_JK', 'bkgMCReader_PK']
    fitSequence=['sig2DFitter', 'sigAFitter', 'bkgCombAFitter', 'effiFitter', 'sigMFitter', 'sigMDCBFitter', 'finalFitter_AltM', 
                'bkgM_KStarFitter', 'bkgA_KStarFitter', 'finalFitter_WithKStar', 'finalFitter_AltM_WithKStar', 'finalMFitter', 'sigMFitter_JP',
                'bkgMFitter_JK', 'sigMFitter_PP', 'bkgMFitter_PK', 'finalMFitter_JP', 'finalMFitter_PP',
                'SimulFitter_bkgCombA']
    for s in seq:
        if s in dataSequence:
            sequence.append(dataCollection.GetDataReader(self, s))
        if s is 'stdWspaceReader':
            sequence.append(pdfCollection.GetWspaceReader(self))
        if s is 'stdPDFBuilder':
            sequence.append(pdfCollection.stdPDFBuilder)
        if s is 'effiHistReader':
            sequence.append(dataCollection.effiHistReaderOneStep) if not args.TwoStep else sequence.append(dataCollection.effiHistReader)
        if s in fitSequence:
            sequence.append(fitCollection.GetFitterObjects(self, s))
        if s is 'plotter':
            sequence.append(GetPlotterObject(self))
        if s is 'SimultaneousFitter_sig2D':
            sequence.append(fitCollection.SimultaneousFitter_sig2D)
        if s is 'SimulFitter_sigGEN':
            sequence.append(fitCollection.SimulFitter_sigGEN)
        if s is 'SimulFitter_Final_AltM':
            sequence.append(fitCollection.SimultaneousFitter_Final_AltM)
        if s is 'SimFitter_Final_AltM_WithKStar':
            sequence.append(fitCollection.SimFitter_Final_AltM_WithKStar)
        if s is 'sigMCStudier':
            sequence.append(batchTask_sigMCValidation.GetToyObject(self))
        if s is 'FinalDataResult': sequence.append(dataCollection.FinalDataResult)
        if s is 'EffiTable': sequence.append(dataCollection.EffiTable)
    return sequence

if __name__ == '__main__':
    from BsToPhiMuMuFitter.StdProcess import p
    from BsToPhiMuMuFitter.anaSetup import q2bins
    from BsToPhiMuMuFitter.python.datainput import GetInputFiles
    from copy import deepcopy

    p.work_dir="plots_"+str(args.Year)
    p.cfg['args'] = deepcopy(args)
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
                p.cfg['args'].Year=args.Year
                sequence=Instantiate(p, predefined_sequence[args.seqKey][1])
                p.setSequence(sequence)
                p.beginSeq()
            elif args.Function_name in ['submit', 'run']:
                print("INFO: Processing {0} year data".format(args.Year))
                from BsToPhiMuMuFitter.anaSetup import modulePath
                import BsToPhiMuMuFitter.script.batchTask_sigMCValidation as batchTask_sigMCValidation
                import BsToPhiMuMuFitter.script.batchTask_seqCollection as batchTask_seqCollection
                if p.name=='sigMCValidationProcess':
                    wrappedTask = batchTask_sigMCValidation.BatchTaskWrapper(
                        "myBatchTask",
                        os.path.join(modulePath, "batchTask_sigMCValidation"),
                        cfg=batchTask_sigMCValidation.setupBatchTask)
                else:
                    wrappedTask = batchTask_seqCollection.BatchTaskWrapper(
                        "BatchTaskseqCollection",
                        os.path.join(modulePath, "batchTask_seqCollection"),
                        cfg=batchTask_seqCollection.setupBatchTask )
                parser.set_defaults(
                    wrapper=wrappedTask,
                    process=p)
                p.cfg['args'] = args = parser.parse_args()   
                sequence=Instantiate(p, predefined_sequence[args.seqKey])
                p.setSequence(sequence)
                args.func(args) 
                continue
            else:
                print("INFO: Processing {0} year data".format(args.Year))
                sequence=Instantiate(p, predefined_sequence[args.seqKey])
                p.setSequence(sequence)
                p.beginSeq()
            p.runSeq()
        finally:
            p.endSeq()
            for obj in p._sequence: obj.reset()
