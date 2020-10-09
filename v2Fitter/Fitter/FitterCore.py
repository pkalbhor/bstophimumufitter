#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

import re, pdb

from ROOT import RooMinimizer
from v2Fitter.FlowControl.Path import Path

class FitterCore(Path):
    """A fitter object acts as a path, to be queued in a process.
Following functions to be overloaded to customize the full procedure...
    _preFitSteps
    _runFitSteps
    _postFitSteps
"""
    def __init__(self, cfg):
        super(FitterCore, self).__init__(cfg)
        self.reset()

    def reset(self):
        super(FitterCore, self).reset()
        self.pdf = None
        self.data = None
        self._nll = None
        self.minimizer = None

    def _bookPdfData(self):
        self.pdf = self.process.sourcemanager.get(self.cfg['pdf'])
        if type(self.cfg['data']) is str:
            self.data = self.process.sourcemanager.get(self.cfg['data'])
        elif len(self.cfg['data']) <= 1:
            self.data = self.process.sourcemanager.get(self.cfg['data'][0])
        else:
            # Alternative way to merge list of input data/toy
            for data in self.cfg['data']:
                if self.data is not None:
                    self.data.append(self.process.sourcemanager.get(data))
                else:
                    self.data = self.process.sourcemanager.get(data).Clone()

    def _bookMinimizer(self):
        """Bind a RooMinimizer object to bind to self.minimizer at Runtime"""
        if self.pdf.InheritsFrom("RooAbsPdf"):
            self._nll = self.pdf.createNLL(self.data, *(self.cfg.get('createNLLOpt', [])))
        elif self.pdf.InheritsFrom("RooAbsReal"):
            self._nll = self.pdf.createChi2(self.data, *(self.cfg.get('createNLLOpt', [])))
        else:
            self.logger.logERROR("No clear way to define the FCN value.")
            raise NotImplementedError
        self.minimizer = RooMinimizer(self._nll)
        self.minimizer.setVerbose(ROOT.kTRUE)

    def _preFitSteps(self):
        """Abstract: Do something before main fit loop"""
        self.args = self.pdf.getParameters(self.data)
        self.ToggleConstVar(self.args, True)
        self.ToggleConstVar(self.args, False, self.cfg['argPattern'])
        pass

    def _postFitSteps(self):
        """Abstract: Do something after main fit loop"""
        self.ToggleConstVar(self.args, True)
        pass

    def _runFitSteps(self):
        """Standard fitting procedure to be overwritten."""
        self.minimizer.migrad()
        self.minimizer.migrad()
        self.minimizer.hesse()
        self.minimizer.minos()

    @staticmethod
    def ArgLooper(iArgs, func, targetArgs=None, inverseSel=False):
        """Loop through RooArgSet. Select all args by default.
        targetArgs: A list of name to specify the target."""
        if targetArgs is None:
            targetArgs = []
        args_it = iArgs.createIterator()
        arg = args_it.Next()
        while arg:
            if not targetArgs or \
                    inverseSel != any([re.match(pat, arg.GetName()) for pat in targetArgs]):
                func(arg)
            arg = args_it.Next()

    @staticmethod
    def ToggleConstVar(iArgs, isConst, targetArgs=[], inverseSel=False):
        """Loop through RooDataSet and set variables to (non)const"""
        FitterCore.ArgLooper(iArgs, lambda arg: arg.setConstant(isConst), targetArgs, inverseSel)

    @classmethod
    def templateConfig(cls):
        cfg = {
            'name': "FitterCore",
            'data': "",
            'pdf': "f",
            'argPattern': [r'^.+$'],
            'AliasTag': None,
            'createNLLOpt': [],
        }
        return cfg

    def _runPath(self):
        """Stardard fitting procedure to be overlaoded."""
        self._bookPdfData()
        self._bookMinimizer()
        self._preFitSteps()
        self._runFitSteps()
        self._postFitSteps()
