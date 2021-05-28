#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import sys, os, pdb, datetime, importlib
import ROOT
#ROOT.EnableImplicitMT()

#Supress RooFit related info messages
ROOT.gEnv.SetValue("RooFit.Banner", 0)
ROOT.RooMsgService.instance().setGlobalKillBelow(3)

#Verify if PYTHONPATH is set
if importlib.util.find_spec("BsToPhiMuMuFitter") is None:
    raise ModuleNotFoundError("Please source setup_ROOTEnv.sh script and come back again!")

import v2Fitter.FlowControl.Logger as Logger
log = Logger.Logger("runtime_temp.log", 999) #Logger.VerbosityLevels.DEBUG)

from BsToPhiMuMuFitter.python.ArgParser import SetParser, GetBatchTaskParser
parser=GetBatchTaskParser()
args = parser.parse_known_args()[0]

# Standard sequences; To be pre-defined
predefined_sequence = {}
predefined_sequence['loadData']  = ['dataReader']
predefined_sequence['loadMC']    = ['sigMCReader']
predefined_sequence['loadMCGEN'] = ['sigMCGENReader']
predefined_sequence['loadMCGENc']= ['sigMCGENcReader'] # from official GEN MC
predefined_sequence['loadMCk']   = ['KsigMCReader']
predefined_sequence['loadMCJ']   = ['sigMCReader_JP']
predefined_sequence['loadMCP']   = ['sigMCReader_PP']
predefined_sequence['buildPdfs'] = ['dataReader', 'stdWspaceReader', 'stdPDFBuilder']
predefined_sequence['buildEff']  = ['effiHistReader']
predefined_sequence['buildTotEff'] = ['TotalEffiReader']

predefined_sequence['fitEff']    = ['effiHistReader', 'stdWspaceReader', 'effiFitter']
predefined_sequence['fitEff2']    = ['effiHistReader', 'stdWspaceReader', 'effiFitter2']
predefined_sequence['fitAccEff'] = ['effiHistReader', 'stdWspaceReader', 'accEffiFitter']
predefined_sequence['fitRecEff'] = ['effiHistReader', 'stdWspaceReader', 'recEffiFitter']
predefined_sequence['fitSig2D']  = (['sigMCReader', 'stdWspaceReader'], ['SimultaneousFitter_sig2D'] if args.SimFit else ['sig2DFitter'])
predefined_sequence['fitSig3D']  = (['sigMCReader', 'stdWspaceReader'], ['SimultaneousFitter_sig3D'] if args.SimFit else ['sig3DFitter'])
predefined_sequence['fitSigMCGEN']=(['sigMCGENReader', 'stdWspaceReader'], ['SimulFitter_sigGEN'] if args.SimFit else ['sigAFitter'])
predefined_sequence['fitSigMCGENc']=['sigMCGENReader', 'stdWspaceReader', 'sigAFitterCorrected'] # Corrected Decay Formula
predefined_sequence['fitBkgCombA']=(['dataReader', 'stdWspaceReader'], ['SimulFitter_bkgCombA'] if args.SimFit else ['bkgCombAFitter'])
predefined_sequence['fitSigMDCB']    = ['sigMCReader', 'stdWspaceReader', 'sigMDCBFitter']
predefined_sequence['fitSigM']       = ['sigMCReader', 'stdWspaceReader', 'sigMFitter']
predefined_sequence['fitBkgM_KStar'] = ['KsigMCReader', 'stdWspaceReader', 'bkgM_KStarFitter']
predefined_sequence['fitBkgA_KStar'] = ['KsigMCReader', 'stdWspaceReader', 'bkgA_KStarFitter']
predefined_sequence['fitBkgPeak3D'] = ['KsigMCReader', 'stdWspaceReader', 'bkgPeak3DFitter']

predefined_sequence['fitFinal3D_AltM']          = (['dataReader', 'stdWspaceReader'], ['SimulFitter_Final_AltM'] if args.SimFit else ['finalFitter_AltM'])
predefined_sequence['fitFinal3D_WithKStar']     = (['dataReader', 'stdWspaceReader'], ['SimFitter_Final_WithKStar'] if args.SimFit else ['finalFitter_WithKStar'])
predefined_sequence['fitFinal3D_AltM_WithKStar']= (['dataReader', 'stdWspaceReader'], ['SimFitter_Final_AltM_WithKStar'] if args.SimFit else ['finalFitter_AltM_WithKStar'])
predefined_sequence['fitFinalM']     = ['dataReader', 'stdWspaceReader', 'finalMFitter'] #1D Bmass Fit

predefined_sequence['loadAll'] = ['dataReader', 'sigMCReader', 'KsigMCReader', 'effiHistReader', 'stdWspaceReader', 'stdPDFBuilder']
predefined_sequence['fitAll']  = predefined_sequence['loadAll'] + ['effiFitter', 'sig2DFitter', 'sigAFitter']
predefined_sequence['fitFinalAll'] = predefined_sequence['loadAll'] + ['fitSigMDCB', 'bkgCombAFitter', 'fitBkgM_KStar', 'fitBkgA_KStar', 'finalFitter_AltM_WithKStar']

predefined_sequence['createplots']=['effiHistReader', 
                                    'dataReader', 
                                    'sigMCReader', 
                                    #'sigMCGENReader', 
                                    'KsigMCReader', 
                                    #'sigMCReader_JP', 
                                    'stdWspaceReader', 'plotter']
#'effiHistReader', 'KsigMCReader', 'sigMCReader', 'sigMCGENReader', 
predefined_sequence['sigMCValidation'] = (['stdWspaceReader', 'sigMCReader'], ['sigMCStudier'])
predefined_sequence['mixedToyValidation'] = (['stdWspaceReader', 'sigMCReader', 'bkgCombToyGenerator', 'bkgPeakToyGenerator'], ['mixedToyStudier']) if not args.Toy2 else (['stdWspaceReader', 'sigMCReader'], ['mixedToyStudier'])
predefined_sequence['seqCollection']   = []
predefined_sequence['FinalDataResult'] = ['FinalDataResult']
predefined_sequence['EffiTable']       = ['EffiTable']
predefined_sequence['PeakFracTable']   = ['PeakFracTable']
predefined_sequence['CompPlots']       = ['stdWspaceReader', 'GetCompPlots']
predefined_sequence['StatusTable']  = ['StatusTableMaker']

#For Validation Study
predefined_sequence['fitSigM_JP'] = ['sigMCReader_JP', 'stdWspaceReader', 'sigMFitter_JP']
predefined_sequence['fitBkgM_JK'] = ['bkgMCReader_JK', 'stdWspaceReader', 'bkgMFitter_JK']
predefined_sequence['fitSigM_PP'] = ['sigMCReader_PP', 'stdWspaceReader', 'sigMFitter_PP']
predefined_sequence['fitBkgM_PK'] = ['bkgMCReader_PK', 'stdWspaceReader', 'bkgMFitter_PK']
predefined_sequence['fitFinalM_JP'] = ['dataReader', 'stdWspaceReader', 'finalMFitter_JP']
predefined_sequence['fitFinalM_PP'] = ['dataReader', 'stdWspaceReader', 'finalMFitter_PP']
predefined_sequence['fitSigPhiM_JP'] = ['sigMCReader_JP', 'stdWspaceReader', 'sigPhiMFitter_JP']
predefined_sequence['fitFinalPhiM_JP'] = ['dataReader', 'stdWspaceReader', 'finalPhiMFitter_JP']

def Instantiate(self, seq):
    """All objects from 'predefined_sequence' are initalized here"""
    # Classes in use are: DataReader, WSpaceReader, StdFitter, ObjectProvider, EfficiencyFitter, Plotter
    import BsToPhiMuMuFitter.dataCollection as dataCollection
    import BsToPhiMuMuFitter.pdfCollection  as pdfCollection
    import BsToPhiMuMuFitter.fitCollection  as fitCollection
    from BsToPhiMuMuFitter.plotCollection import GetPlotterObject
    sequence=[]
    dataSequence=['sigMCReader', 'dataReader', 'sigMCGENReader', 'KsigMCReader',
                'sigMCReader_JP', 'sigMCReader_PP', 'bkgMCReader_JK', 'bkgMCReader_PK', 
                'sigMCGENcReader', 'StatusTableMaker', 'TotalEffiReader']
    fitSequence=['sig2DFitter', 'sigAFitter', 'bkgCombAFitter', 'effiFitter', 'accEffiFitter', 'recEffiFitter', 'sigMFitter', 
                'sigMDCBFitter', 'finalFitter_AltM', 'sigAFitterCorrected', 'sig3DFitter', 'bkgM_KStarFitter', 
                'bkgA_KStarFitter', 'finalFitter_WithKStar', 'finalFitter_AltM_WithKStar', 'finalMFitter', 'sigMFitter_JP',
                'bkgMFitter_JK', 'sigMFitter_PP', 'bkgMFitter_PK', 'finalMFitter_JP', 'finalMFitter_PP', 'sigPhiMFitter_JP', 
                'finalPhiMFitter_JP', 'SimulFitter_bkgCombA', 'bkgPeak3DFitter', 'effiFitter2']
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
        if s is 'SimultaneousFitter_sig3D':
            sequence.append(fitCollection.SimultaneousFitter_sig3D)
        if s is 'SimulFitter_sigGEN':
            sequence.append(fitCollection.SimulFitter_sigGEN)
        if s is 'SimulFitter_Final_AltM':
            sequence.append(fitCollection.SimultaneousFitter_Final_AltM)
        if s is 'SimFitter_Final_AltM_WithKStar':
            sequence.append(fitCollection.SimFitter_Final_AltM_WithKStar)
        if s is 'SimFitter_Final_WithKStar':
            sequence.append(fitCollection.SimFitter_Final_WithKStar)
        if s is 'sigMCStudier':
            sequence.append(sigMCValidation.GetToyObject(self))
        if s is 'mixedToyStudier':
            sequence.append(mixedToyValidation.GetMixedToyObject(self))
        if s in ['bkgCombToyGenerator', 'bkgPeakToyGenerator']:
            import BsToPhiMuMuFitter.toyCollection as toyCollection
            sequence.append(toyCollection.GetToyObject(self, s))
        if s is 'FinalDataResult': sequence.append(dataCollection.FinalDataResult)
        if s is 'EffiTable': sequence.append(dataCollection.EffiTable)
        if s is 'PeakFracTable': sequence.append(dataCollection.PeakFracTable)
        if s is 'GetCompPlots': sequence.append(dataCollection.GetCompPlots)
    return sequence

def SetBatchTaskWrapper(args):
    from BsToPhiMuMuFitter.anaSetup import modulePath
    if args.seqKey=='sigMCValidation':
        import BsToPhiMuMuFitter.script.batchTask_sigMCValidation as sigMCValidation
        wrappedTask = sigMCValidation.BatchTaskWrapper(
            "myBatchTask",
            os.path.join(modulePath, "batchTask_sigMCValidation"),
            cfg=batchTask_sigMCValidation.setupBatchTask)
    elif args.seqKey=='mixedToyValidation':
        wrappedTask = mixedToyValidation.BatchTaskWrapper(
            "myBatchTask_MixedToy",
            os.path.join(modulePath, "batchTask_mixedToyValidation"),
            cfg=mixedToyValidation.setupBatchTask)
    else:
        import BsToPhiMuMuFitter.script.batchTask_seqCollection as batchTask_seqCollection
        wrappedTask = batchTask_seqCollection.BatchTaskWrapper(
            "BatchTaskseqCollection",
            os.path.join(modulePath, "batchTask_seqCollection"),
            cfg=batchTask_seqCollection.setupBatchTask )
    parser.set_defaults(wrapper=wrappedTask, process=p)

    args = parser.parse_args()
    if args.Function_name=='postproc':
        if args.seqKey=='sigMCValidation':
            args.func = sigMCValidation.func_postproc
        if args.seqKey=='mixedToyValidation':
            args.func = mixedToyValidation.func_postproc

    if args.OneStep is False: args.TwoStep = True
    return args
     
if __name__ == '__main__':
    from BsToPhiMuMuFitter.StdProcess import p
    from BsToPhiMuMuFitter.anaSetup import q2bins
    from BsToPhiMuMuFitter.python.datainput import GetInputFiles
    import BsToPhiMuMuFitter.script.batchTask_mixedToyValidation as mixedToyValidation
    from copy import deepcopy
   
    if args.OneStep is False: args.TwoStep = True
    p.work_dir="plots_{}".format(args.Year)
    p.cfg['args'] = deepcopy(args)
    p.cfg['sysargs'] = sys.argv
    GetInputFiles(p)
    p.cfg['bins'] = p.cfg['allBins'] if args.binKey=="all" else [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]

    if (not args.SimFit) and (type(predefined_sequence[args.seqKey]) is tuple):
        predefined_sequence[args.seqKey]=predefined_sequence[args.seqKey][0]+predefined_sequence[args.seqKey][1]
    if args.SimFit or args.SimFitPlots: 
        p.name="SimultaneousFitProcess"
        p.work_dir="plots_simultaneous"
    if args.seqKey=='sigMCValidation': p.name='sigMCValidationProcess'

    if args.Function_name in ['submit', 'run', 'postproc']:
        args = SetBatchTaskWrapper(args)
        p.cfg['args'] = deepcopy(args)

    for b in p.cfg['bins']:
        Stime = datetime.datetime.now()
        p.cfg['binKey'] = b
        def runSimSequences():
            for Year in [2016, 2017, 2018]:
                p.cfg['args'].Year=Year
                GetInputFiles(p)
                sequence=Instantiate(p, predefined_sequence[args.seqKey][0])
                p.setSequence(sequence)
                p.beginSeq()
                p.runSeq()
            p.cfg['args'].Year=args.Year
        if args.SimFit and not (args.Function_name in ['submit', 'run', 'postproc']):
            print ("INFO: Processing simultaneously over three year data")
            runSimSequences()
            sequence=Instantiate(p, predefined_sequence[args.seqKey][1])
            p.setSequence(sequence)
            p.beginSeq()
        elif args.Function_name in ['submit', 'run', 'postproc']:
            print("INFO: Processing {0} year data".format(args.Year))
            if p.cfg['args'].SimFit:
                if not args.Function_name=='submit':runSimSequences()
                sequence=Instantiate(p, predefined_sequence[args.seqKey][1])
            else:
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
        p.endSeq()
        for obj in p._sequence: obj.reset()
        Etime = datetime.datetime.now()
        print("Time taken to execute", args.seqKey, "in", b, "bin:", (Etime-Stime).seconds/60, "minutes!")
