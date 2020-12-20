#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import os, pdb

import abc
import ROOT

from v2Fitter.FlowControl.Path import Path
from BsToPhiMuMuFitter.anaSetup import q2bins

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
    def _runToyCreater(self, Type):
        """Get Toy DataSets"""
        raise NotImplementedError

    @abc.abstractmethod
    def _postRunFitPlotter(self, idx):
        """Run Plotter code."""
        raise NotImplementedError

    def _runSetsLoop(self):
        #for iSet in range(max(self.cfg['nSetOfToys'], self.process.cfg['args'].nSetOfToys)):
        iSet=0; rSet=0
        while rSet < max(self.cfg['nSetOfToys'], self.process.cfg['args'].nSetOfToys):
            self._preRunFitSteps(iSet)
            self.fitter.hookProcess(self.process)
            self.fitter.customize()

            for idx, YieldType, Type in self.cfg['Type']:
                self.currentSubDataEntries = self.getSubDataEntries(iSet, YieldType)
                if idx==0:
                    self.fitter.data = next(self.getSubData(idx)) if Type=='Sim' else self._runToyCreater(YieldType)
                else:
                    TempData = next(self.getSubData(idx)) if Type=='Sim' else self._runToyCreater(YieldType)
                    self.fitter.data.append(TempData)

            self.fitter.pdf = self.process.sourcemanager.get(self.fitter.cfg['pdf'])
            self.fitter._bookMinimizer()
            self.fitter._preFitSteps()
            self.fitter._runFitSteps()
            self._postRunFitSteps(iSet)
            self.fitter.reset()
            iSet += 1
            if not self.fitter.fitResult['{}.migrad'.format(self.fitter.name)]['status']: rSet += 1
        print("Failed subsamples: ", iSet-rSet)

    @abc.abstractmethod
    def _postSetsLoop(self):
        raise NotImplementedError

    def _runPath(self):
        """ Chain of pre-run-post steps"""
        self.fitter = self.cfg['fitter']
        self.data = [self.process.sourcemanager.get(i) for i in self.cfg['data']]

        self._preSetsLoop()
        self._runSetsLoop()
        self._postSetsLoop()

def getSubData_random(self, idx, checkCollision=True):
    """ Pick random subset. Input dataset is asseumed to be large enough to avoid collision."""
    sumEntries = int(self.data[idx].sumEntries())
    evtBits = ROOT.TBits(int(sumEntries))
    while True:
        outputBits = ROOT.TBits(sumEntries)
        for entry in range(self.currentSubDataEntries):
            rnd_collisions = 0
            while True:
                rnd = ROOT.gRandom.Integer(sumEntries)
                if checkCollision and evtBits.TestBitNumber(rnd):
                    rnd_collisions = rnd_collisions + 1
                else:
                    evtBits.SetBitNumber(rnd)
                    outputBits.SetBitNumber(rnd)
                    break

            if checkCollision and rnd_collisions * 5 > self.currentSubDataEntries:
                self.logger.logWARNING("Rate of random number collision may over 20%, please consider use larger input")

        # Sequential reading is highly recommanded by ROOT author
        output = self.data[idx].emptyClone("{0}Subset".format(self.data[idx].GetName()))
        startBit = outputBits.FirstSetBit(0)
        while startBit < sumEntries:
            output.add(self.data[idx].get(startBit))
            startBit = outputBits.FirstSetBit(startBit + 1)
        yield output

def getSubData_seqential(self):
    """Not suggested since source could be mixed with RooDataSet::add() """
    sumEntries = int(self.data.sumEntries())
    currentEntry = 0
    while True:
        output = self.data.emptyClone("{0}Subset".format(self.data.GetName()))
        if currentEntry + self.currentSubDataEntries > sumEntries:
            self.logger.logERROR("Running out of source dataset")
            raise RuntimeError
        for entry in range(self.currentSubDataEntries):
            output.add(self.data.get(currentEntry))
            currentEntry = currentEntry + 1
        yield output
