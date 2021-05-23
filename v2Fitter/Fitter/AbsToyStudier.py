#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import os, math, pdb

import abc
import ROOT

from v2Fitter.Fitter.FitterCore import FitterCore
from v2Fitter.FlowControl.Path import Path
from BsToPhiMuMuFitter.anaSetup import q2bins
from BsToPhiMuMuFitter.varCollection import Puw8

class AbsToyStudier(Path):
    """
A mock of RooFit::RooMCStudy which is useful for low stat analysis.
    Generate a lot of subset from input RooDataSet and run fitter for each.
    """

    def __init__(self, cfg):
        """Init"""
        super(AbsToyStudier, self).__init__(cfg)
        self.reset()

    def reset(self):
        super(AbsToyStudier, self).reset()
        self.data = None
        self.fitter = None

    @classmethod
    def templateConfig(cls):
        cfg = {
            'name': "ToyStudier",
            'data': None,
            'fitter': None,
            'nSetOfToys': 1,
        }
        return cfg

    @abc.abstractmethod
    def getSubData(self):
        """
Decide how the input dataset transform into subsets.
    return an instance of RooFit::RooDataSet
        """
        raise NotImplementedError

    @abc.abstractmethod
    def getSubDataEntries(self, setIdx):
        """
Decide the number of entries of this subset.
    return an integer
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _preSetsLoop(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _preRunFitSteps(self, setIndex):
        """ Run at the begining of each loop """
        raise NotImplementedError

    @abc.abstractmethod
    def _postRunFitSteps(self, setIndex):
        """ Run at the end of each loop (only before the fitter reset)"""
        raise NotImplementedError

    @abc.abstractmethod
    def _runToyCreater(self, Type, Year):
        """Get Toy DataSets"""
        raise NotImplementedError

    @abc.abstractmethod
    def _postRunFitPlotter(self, idx):
        """Run Plotter code."""
        raise NotImplementedError

    def _runSetsLoop(self):
        iSet=0 #Total subsamples
        rSet=0 #Converged subsamples
        while rSet < max(self.cfg['nSetOfToys'], self.process.cfg['args'].nSetOfToys):
            print(">>>> Running for sub-sample number:", iSet+1)
            self._preRunFitSteps(iSet)
            self.fitter.hookProcess(self.process)
            self.fitter.customize()

            for idx, YieldType, Type in self.cfg['Type']:
                self.currentSubDataEntries = self.getSubDataEntries(iSet, YieldType)
                if self.proceedFlag==False: break
                if idx==0:
                    self.fitter.data = next(self.getSubData(idx)) if Type=='Sim' else self._runToyCreater(YieldType, self.process.cfg['args'].Year)
                else:
                    TempData = next(self.getSubData(idx)) if Type=='Sim' else self._runToyCreater(YieldType, self.process.cfg['args'].Year)
                    self.fitter.data.append(TempData)
            self.SaveSubsamples(iSet, self.fitter.data, "FinalSubSample_{}".format(self.process.cfg['args'].Year))
            if self.proceedFlag==False: 
                self.proceedFlag=True
                print(">> Got negative expected entries. Subsample is Flagged Bad")
                continue
            if not self.process.cfg['args'].NoFit:
                self.fitter.pdf = self.process.sourcemanager.get(self.fitter.cfg['pdf'])
                self.fitter._bookMinimizer()
                self.fitter._preFitSteps()
                self.fitter._runFitSteps()
                self._postRunFitSteps(iSet)
            iSet += 1
            if (self.treeContent.status==0 and self.treeContent.hesse==0 and self.treeContent.covQual==3) or (self.process.cfg['args'].NoFit): rSet += 1
            self.fitter.reset()
            print(">>>> Successful sub-samples:", rSet, "Failed sub-samples:", iSet-rSet)
        print("Failed subsamples: ", iSet-rSet)

    def BookSimData(self, iSet, func):
        def inner():
            self.fitter.Years = self.fitter.cfg['Years']
            for Id, Year in enumerate(self.fitter.Years):
                self.data = [self.process.sourcemanager.get(i.format(Year)) for i in self.cfg['data']] #Position of line is important
                for idx, YieldType, Type in self.cfg['Type']:
                    self.currentSubDataEntries = self.getSubDataEntries(iSet, YieldType, Year)
                    if self.proceedFlag==False: break
                    if idx==0:
                        TempData = next(self.getSubData(idx)) if Type=='Sim' else self._runToyCreater(YieldType, Year)
                        TempData2 = TempData
                    else:
                        TempData2 = next(self.getSubData(idx)) if Type=='Sim' else self._runToyCreater(YieldType, Year)
                        TempData.append(TempData2)
                    self.SaveSubsamples(iSet, TempData2, TempData2.GetName())
                if self.proceedFlag==False: break
                self.fitter.cfg['data'][Id] = TempData
                self.SaveSubsamples(iSet, TempData, "FinalSubSample_{}".format(Year))
            func()
        return inner

    def _runSetsLoop_SimFit(self):
        iSet=0 #Total subsamples
        rSet=0 #Converged subsamples
        cwd = self.process.work_dir #Avoid using os.getcwd() which gives problems in condor jobs
        while rSet < max(self.cfg['nSetOfToys'], self.process.cfg['args'].nSetOfToys):
            print(">>>> Running for sub-sample number:", iSet+1)
            self._preRunFitSteps(iSet)
            self.fitter.hookProcess(self.process)
            self.fitter.customize()
            self.BookSimData(iSet, self.fitter._bookPdfData)()
            if self.proceedFlag==False: 
                self.proceedFlag=True
                print(">> Got negative expected entries. Subsample is Flagged Bad")
                continue
            if not self.process.cfg['args'].NoFit:
                self.fitter._bookMinimizer()
                self.fitter._preFitSteps()

                #To keep signal and background yields floating
                self.fitter.ToggleConstVar(self.fitter.minimizer.getParameters(self.fitter.dataWithCategories), False, self.fitter.cfg['argPattern']) 

                self.fitter._runFitSteps(); #self.fitter.minosResult = self.fitter.fitter.FitMinos(self.fitter.data[-1].get())
                self._postRunFitSteps(iSet)

            #Remove a year tag from parameters
            for pdf, data, Year in zip(self.fitter.pdf, self.fitter.data, self.fitter.Years): 
                FitterCore.ArgLooper(pdf.getParameters(data), lambda p: p.SetName(p.GetName().split("_{0}".format(Year))[0]), targetArgs=self.fitter.cfg['argPattern'], inverseSel=True)
            iSet += 1
            if (self.treeContent.status==0 and self.treeContent.hesse==0 and self.treeContent.covQual==3) or (self.process.cfg['args'].NoFit): rSet += 1
            self.fitter.reset()
            print(">>>> Successful sub-samples:", rSet, "Failed sub-samples:", iSet-rSet)
        print("Failed subsamples: ", iSet-rSet)

    def SaveSubsamples(self, index, subdata, Name):
        subdata.SetName(Name.replace(".", "_")+"_{}".format(index))
        if self.process.cfg['args'].NoFit:
            ofile = ROOT.TFile.Open("{}_subsamples_{}.root".format(self.process.name, index), "UPDATE")
            subdata.Write()
            ofile.Close()


    @abc.abstractmethod
    def _postSetsLoop(self):
        raise NotImplementedError

    def _runPath(self):
        """ Chain of pre-run-post steps"""
        SimFit = self.process.cfg['args'].SimFit
        self.fitter = self.cfg['fitter']
        self.data = None if SimFit else [self.process.sourcemanager.get(i) for i in self.cfg['data']]
        self._preSetsLoop()
        self._runSetsLoop_SimFit() if SimFit else self._runSetsLoop()
        self._postSetsLoop()

def getSubData_random(self, idx, checkCollision=True):
    """ Pick random subset. Input dataset is asseumed to be large enough to avoid collision."""
    numEntries = int(self.data[idx].numEntries())
    evtBits = ROOT.TBits(int(numEntries))
    while True:
        outputBits = ROOT.TBits(numEntries)
        for entry in range(math.ceil(self.currentSubDataEntries)*2): #Factor 2 to take care of weighted yield
            rnd_collisions = 0
            while True:
                rnd = ROOT.gRandom.Integer(numEntries)
                if checkCollision and evtBits.TestBitNumber(rnd):
                    rnd_collisions = rnd_collisions + 1
                else:
                    evtBits.SetBitNumber(rnd)
                    outputBits.SetBitNumber(rnd)
                    break

            if checkCollision and rnd_collisions * 5 > math.ceil(self.currentSubDataEntries):
                self.logger.logWARNING("Rate of random number collision may over 20%, please consider use larger input")

        # Sequential reading is highly recommanded by ROOT author
        output = self.data[idx].emptyClone("{0}Subset".format(self.data[idx].GetName()))
        startBit = outputBits.FirstSetBit(0)
        while startBit < numEntries:
            if True: #Dataset with weights
                output.add(self.data[idx].get(startBit), self.data[idx].weight(), self.data[idx].weightError())
                if output.sumEntries() >= (self.currentSubDataEntries - 0.5): break
            else: # Dataset without weights
                output.add(self.data[idx].get(startBit))
                if output.sumEntries() == self.currentSubDataEntries: break
            startBit = outputBits.FirstSetBit(startBit + 1)
        self.sigEntries = self.currentSubDataEntries #output.sumEntries()
        self.logger.logINFO("SubDataSet has actual yield {0} created from sample {1}".format(output.sumEntries(), output.GetName()))
        yield output

def getSubData_seqential(self):
    """Not suggested since source could be mixed with RooDataSet::add() """
    numEntries = int(self.data.numEntries())
    currentEntry = 0
    while True:
        output = self.data.emptyClone("{0}Subset".format(self.data.GetName()))
        if currentEntry + self.currentSubDataEntries > numEntries:
            self.logger.logERROR("Running out of source dataset")
            raise RuntimeError
        for entry in range(self.currentSubDataEntries):
            output.add(self.data.get(currentEntry))
            currentEntry = currentEntry + 1
        yield output
