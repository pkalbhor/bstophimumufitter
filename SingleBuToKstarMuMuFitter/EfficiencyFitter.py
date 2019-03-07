#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Description     : Fitter template without specification
# Author          : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
# Last Modified   : 07 Mar 2019 21:25 01:24

from v2Fitter.Fitter.FitterCore import FitterCore
from varCollection import CosThetaL, CosThetaK

import os
import re
import shelve
import functools
import itertools

import ROOT

class EfficiencyFitter(FitterCore):
    """Implementation to standard efficiency fitting procdeure to BuToKstarMuMu angular analysis"""

    @classmethod
    def templateConfig(cls):
        cfg = FitterCore.templateConfig()
        cfg.update({
            'name': "EfficiencyFitter",
            'data': "effiHistReader.accXrec",
            'dataX': "effiHistReader.accXrec",
            'dataY': "effiHistReader.accXrec",
            'pdf' : "effi_sigA",
            'pdfX' : "effi_sigA",
            'pdfY' : "effi_sigA",
            'db'  : "fitResults.db",
        })
        del cfg['createNLLOpt']
        return cfg

    def _bookMinimizer(self):
        """Pass complicate fitting control."""
        pass

    def _initArgs(self, args):
        """Parameter initialization from db file"""
        db = shelve.open(self.cfg.get('db', "fitResults.db"))
        def initFromDB(iArg):
            argName = iArg.GetName()
            funcPair = [
                ('setVal', 'getVal'),
                ('setError', 'getError'),
                ('setAsymError', 'getErrorHi'),
                ('setAsymError', 'getErrorLo'),
                ('setConstant', 'isConstant'),
                ('setMax', 'getMax'),
                ('setMin', 'getMin')]
            if argName in db:
                for setter, getter in funcPair:
                    getattr(iArg, setter)(
                        *{
                            'getErrorHi': (db[argName]['getErrorLo'], db[argName][getter]),
                            'getErrorLo': (db[argName][getter], db[argName]['getErrorHi']),
                        }.get(getter, (db[argName][getter],))
                    )
            else:
                self.logger.logINFO("Found new variable {0}".format(argName))
        FitterCore.ArgLooper(args, initFromDB)
        db.close()

    def _preFitSteps(self):
        """Prefit uncorrelated term"""
        args = self.pdf.getParameters(self.data)
        self._initArgs(args)
        self.ToggleConstVar(args, isConst=True)

        # Disable xTerm correction and fit to 1-D
        args.find('hasXTerm').setVal(0)
        self.ToggleConstVar(args, isConst=False, targetArgs=[r"^k\d+$"])
        self.ToggleConstVar(args, isConst=False, targetArgs=[r"^l\d+$"])
        
        h_accXrec_fine_ProjectionX = self.process.sourcemanager.get(self.cfg['dataX'])
        h_accXrec_fine_ProjectionY = self.process.sourcemanager.get(self.cfg['dataY'])
        effi_cosl = self.process.sourcemanager.get(self.cfg['pdfX'])
        effi_cosK = self.process.sourcemanager.get(self.cfg['pdfY'])
        for proj, pdf, var in [(h_accXrec_fine_ProjectionX, effi_cosl, CosThetaL), (h_accXrec_fine_ProjectionY, effi_cosK, CosThetaK)]:
            hdata = ROOT.RooDataHist("hdata", "", ROOT.RooArgList(var), ROOT.RooFit.Import(proj))
            pdf.chi2FitTo(hdata, ROOT.RooLinkedList())

        self.ToggleConstVar(args, isConst=True, targetArgs=[r"^l\d+$"])
        self.ToggleConstVar(args, isConst=True, targetArgs=[r"^k\d+$"])
        args.find('effi_norm').setConstant(False)
        self.pdf.chi2FitTo(self.data, ROOT.RooFit.Minos(True))

        # Fix uncorrelated term and for later update with xTerms in main fit step
        args.find('hasXTerm').setVal(1)
        self.ToggleConstVar(args, isConst=False, targetArgs=[r"^x\d+$"])
        args.find('effi_norm').setConstant(True)

    def _updateArgs(self, args):
        """Update fit result to db file"""
        db = shelve.open(self.cfg.get('db', "fitResults.db"), writeback=True)
        def updateToDB(iArg):
            argName = iArg.GetName()
            funcPair = [
                ('setVal', 'getVal'),
                ('setError', 'getError'),
                ('setAsymError', 'getErrorHi'),
                ('setAsymError', 'getErrorLo'),
                ('setConstant', 'isConstant'),
                ('setMax', 'getMax'),
                ('setMin', 'getMin')]
            if argName not in db:
                self.logger.logINFO("Book new variable {0} to db file".format(argName))
                db[argName] = {}
            for setter, getter in funcPair:
                db[argName][getter] = getattr(iArg, getter)()
        FitterCore.ArgLooper(args, updateToDB)
        db.close()

    def _postFitSteps(self):
        """Post-processing"""
        args = self.pdf.getParameters(self.data)
        self.ToggleConstVar(args, True)
        self._updateArgs(args)

    def _runFitSteps(self):
        h2_accXrec = self.process.sourcemanager.get("effiHistReader.h2_accXrec")

        effi_sigA_formula = self.pdf.formula().GetExpFormula().Data()
        args = self.pdf.getParameters(self.data)
        args_it = args.createIterator()
        arg = args_it.Next()
        nPar = 0
        while arg:
            if any(re.match(pat, arg.GetName()) for pat in ["effi_norm", "hasXTerm", "^l\d+$", "^k\d+$"]):
                effi_sigA_formula = re.sub(arg.GetName(), "({0})".format(arg.getVal()), effi_sigA_formula)
            elif re.match("^x\d+$", arg.GetName()):
                nPar += 1
            arg = args_it.Next()
        effi_sigA_formula = re.sub(r"x(\d{1,2})", r"[\1]", effi_sigA_formula)
        effi_sigA_formula = re.sub(r"CosThetaL", r"x", effi_sigA_formula)
        effi_sigA_formula = re.sub(r"CosThetaK", r"y", effi_sigA_formula)
        f2_effi_sigA = ROOT.TF2("f2_effi_sigA", effi_sigA_formula, -1, 1, -1, 1)

        if os.path.exists(os.path.abspath(os.path.dirname(__file__))+"/cpp/EfficiencyFitter_cc.so"):
            ROOT.gROOT.ProcessLine(".L "+os.path.abspath(os.path.dirname(__file__))+"/cpp/EfficiencyFitter_cc.so")
        else:
            ROOT.gROOT.ProcessLine(".L "+os.path.abspath(os.path.dirname(__file__))+"/cpp/EfficiencyFitter.cc+")
        fitter = ROOT.EfficiencyFitter()
        minuit = fitter.Init(nPar, h2_accXrec, f2_effi_sigA)
        for xIdx in range(nPar):
            minuit.DefineParameter(xIdx, "x{0}".format(xIdx), 0.,  1E-4,    -1E+1, 1E+1)
        minuit.Command("MINI")
        minuit.Command("MINI")
        minuit.Command("MINOS")

        parVal = ROOT.Double(0)
        parErr = ROOT.Double(0)
        for xIdx in range(nPar):
            minuit.GetParameter(xIdx, parVal, parErr)
            arg = args.find("x{0}".format(xIdx))
            arg.setVal(parVal)
            arg.setError(parErr)

