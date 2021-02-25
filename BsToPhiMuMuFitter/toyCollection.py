#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import types, pdb, os
from copy import deepcopy
import functools
import shelve

from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from BsToPhiMuMuFitter.varCollection import Bmass, CosThetaL, CosThetaK

from v2Fitter.Fitter.ToyGenerator import ToyGenerator
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

import ROOT

from BsToPhiMuMuFitter.StdProcess import p
import BsToPhiMuMuFitter.pdfCollection as pdfCollection

CFG = deepcopy(ToyGenerator.templateConfig())
CFG.update({
    'db': "{0}/input/selected/fitResults_{{binLabel}}.db".format(modulePath),
    'argset': ROOT.RooArgSet(Bmass, CosThetaL, CosThetaK),
    'argAliasInDB': {},
    'generateOpt': [],
    'mixWith': "ToyGenerator.mixedToy",
    'scale': 1,
})

def decorator_initParameters(func):
    @functools.wraps(func)
    def wrapped_f(self, Year):
        self.pdf = self.process.sourcemanager.get(self.cfg['pdf'])
        self.argset = self.cfg['argset']
        self.params = self.pdf.getParameters(self.argset)
        dbfile = os.path.join(self.process.cwd, "plots_{0}".format(Year), self.cfg['db'].format(binLabel=q2bins[self.process.cfg['binKey']]['label']))
        FitDBPlayer.initFromDB(dbfile, self.params, self.cfg.get('argAliasInDB', []))
        func(self, Year)
    return wrapped_f

def decorator_fluctuateParams(parList=None):
    """ fluctuate parameters for systematic study """
    if parList is None:
        parList = []
    def wrapper(func):
        @functools.wraps(func)
        def wrapped_f(self):
            func(self)

            targetParams = ROOT.RooArgSet()
            def setParamsToFluc(arg):
                if arg.GetName() in parList:
                    targetParams.add(arg)
            FitterCore.ArgLooper(self.params, setParamsToFluc)
            FitDBPlayer.fluctuateFromDB(self.cfg['db'].format(binLabel=q2bins[self.process.cfg['binKey']]['label']), targetParams, self.cfg.get('argAliasInDB', []))
        return wrapped_f
    return wrapper

def decorator_setExpectedEvents(yieldVars=None):
    """Generate from fixed dbfile. Default yieldVars  = ["nSig", "nBkgComb"]"""
    if yieldVars is None:
        yieldVars = ["nSig", "nBkgComb", "nBkgPeak"]
    def wrapper(func):
        @functools.wraps(func)
        def wrapped_f(self, Year):
            func(self, Year)

            expectedYields = 0
            #YieldError = 0.
            try:        
                db = shelve.open(self.cfg['db'].format(binLabel=q2bins[self.process.cfg['binKey']]['label']))
                for yVar in yieldVars:
                    try:
                        expectedYields += self.params.find(yVar).getVal()
                        #YieldError += self.params.find(yVar).getError()
                    except AttributeError:
                        if yVar=="nBkgPeak":
                            expectedYields += db['PeakFrac']['getVal']*db['nSig']['getVal']
                            PeakFrac = db['PeakFrac']['getVal']
                            nSig = db['nSig']['getVal']
                            nSigError = db['nSig']['getError']
                            #YieldError += (nSig*0.0118) + (PeakFrac*nSigError) + (nSigError*0.0118)
                        else:
                            expectedYields += db[self.cfg['argAliasInDB'].get(yVar, yVar)]['getVal']
                            #YieldError += db[self.cfg['argAliasInDB'].get(yVar, yVar)]['getError']
            finally:
                self.cfg['expectedYields'] = expectedYields
                #  self.logger.logINFO("Will generate {0} events from p.d.f {1}.".format(expectedYields, self.pdf.GetName()))
                db.close()
        return wrapped_f
    return wrapper

def GetToyObject(self, seq, Year):
    import BsToPhiMuMuFitter.dataCollection as dataCollection

    # sigToyGenerator - validation
    if seq is 'sigToyGenerator':
        setupSigToyGenerator = deepcopy(CFG)
        setupSigToyGenerator.update({
            'name': "sigToyGenerator",
            'pdf': "f_sig3D",
            'saveAs': "sigToyGenerator.root",
        })
        sigToyGenerator = ToyGenerator(setupSigToyGenerator)
        @decorator_setExpectedEvents(["nSig"])
        @decorator_initParameters
        def sigToyGenerator_customize(self):
            pass
        sigToyGenerator.customize = types.MethodType(sigToyGenerator_customize, sigToyGenerator)

    # bkgCombToyGenerator - validation
    if seq is 'bkgCombToyGenerator':
        setupBkgCombToyGenerator = deepcopy(CFG)
        setupBkgCombToyGenerator.update({
            'name'  : "bkgCombGenerator.{}".format(Year),
            'pdf'   : "f_bkgComb.{}".format(Year),
            'mixWith':"sigMCReader.{}.Fit".format(Year),
            'scale' : dataCollection.GetDataReader(self,'sigMCReader').cfg['lumi']/dataCollection.GetDataReader(self,'dataReader').cfg['lumi'],
            'db'    : 'fitResults_{binLabel}.db',
            'saveAs': None,
        })
        bkgCombToyGenerator = ToyGenerator(setupBkgCombToyGenerator)
        @decorator_setExpectedEvents(["nBkgComb"])
        @decorator_initParameters
        def bkgCombToyGenerator_customize(self, Year):
            pass
        bkgCombToyGenerator.customize = types.MethodType(bkgCombToyGenerator_customize, bkgCombToyGenerator)
        return bkgCombToyGenerator

    # bkgPeakToyGenerator - validation
    if seq is 'bkgPeakToyGenerator':
        setupBkgPeakToyGenerator = deepcopy(CFG)
        setupBkgPeakToyGenerator.update({
            'name'  : "bkgPeakGenerator.{}".format(Year),
            'pdf'   : "f_bkg_KStar.{}".format(Year),
            'mixWith':"sigMCReader.{}.Fit".format(Year),
            'scale' : dataCollection.GetDataReader(self,'KsigMCReader').cfg['lumi']/dataCollection.GetDataReader(self,'dataReader').cfg['lumi'],
            'db'    : 'fitResults_{binLabel}.db',
            'saveAs': None,
        })
        bkgPeakToyGenerator = ToyGenerator(setupBkgPeakToyGenerator)
        @decorator_setExpectedEvents(["nBkgPeak"])
        @decorator_initParameters
        def bkgPeakToyGenerator_customize(self, Year):
            pass
        bkgPeakToyGenerator.customize = types.MethodType(bkgPeakToyGenerator_customize, bkgPeakToyGenerator)
        return bkgPeakToyGenerator

    # Systematics
    # sigAToyGenerator - systematics
    if seq is 'sigAToyGenerator':
        setupSigAToyGenerator = deepcopy(CFG)
        setupSigAToyGenerator.update({
            'name': "sigAToyGenerator",
            'pdf': "f_sigA",
            'argAliasInDB': setupSigAFitter['argAliasInDB'],
            'saveAs': "sigAToyGenerator.root",
        })
        sigAToyGenerator = ToyGenerator(setupSigAToyGenerator)
        @decorator_setExpectedEvents(["nSig"])
        @decorator_initParameters
        def sigAToyGenerator_customize(self):
            pass
        sigAToyGenerator.customize = types.MethodType(sigAToyGenerator_customize, sigAToyGenerator)

if __name__ == '__main__':
    try:
        p.setSequence([pdfCollection.stdWspaceReader, sigToyGenerator])
        #  p.setSequence([pdfCollection.stdWspaceReader, bkgCombToyGenerator])
        p.beginSeq()
        p.runSeq()
        p.sourcemanager.get('ToyGenerator.mixedToy').Print()
    finally:
        p.endSeq()
