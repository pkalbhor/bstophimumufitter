#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

# Description     : Fitter template without specification
# Author          : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
#                 : Pritam Kalbhor (physics.pritam@gmail.com)

import functools, math, ROOT, pdb
import BsToPhiMuMuFitter.cpp
ROOT.PyConfig.IgnoreCommandLineOptions = True
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

class StdFitter(FitterCore):
    """Implementation to standard fitting procdeure for BsToPhimumu angular analysis"""

    @classmethod
    def templateConfig(cls):
        cfg = FitterCore.templateConfig()
        cfg.update({
            'name': "StdFitter",
            'data': "dataReader.Fit",
            'pdf': "f",
            'FitHesse': False,
            'FitMinos': [False, ()],
            'createNLLOpt': [ROOT.RooFit.Extended(1), ],
            'argPattern': [r'^.+$', ],
            'argAliasInDB': {}, # When writes result to DB.
            'argAliasFromDB': {}, # Overwrite argAliasInDB only when initFromDB, or set to None to skip this variable.
            'saveToDB': True,
            'argAliasSaveToDB': True,
        })
        return cfg

    def _bookMinimizer(self):
        """_bookMinimizer from StdFitter"""
        #-----------------------------------------------------------------------------------------
        import ctypes
        def myfunc(iArg):
            lo=ctypes.c_double(0.)
            hi=ctypes.c_double(1.) 
            self.data.getRange(iArg, lo, hi)
            iArg.setRange(lo, hi)
        FitterCore.ArgLooper(self.data.get(), myfunc)
        try:
            FitterCore.ArgLooper(self.pdf.getObservables(self.data), myfunc)
        except AttributeError:
            print("Error: PDF '{}' not found. Please make sure you have generated mentioned pdf in RooWorkspaces stored in './input' folder".format(self.cfg['pdf']))
            exit()
        #-----------------------------------------------------------------------------------------

        self.fitter = ROOT.StdFitter()
        for opt in self.cfg.get("createNLLOpt", []):
            self.fitter.addNLLOpt(opt)
        minuit=self.fitter.Init(self.pdf, self.data)
        #minuit.setLogFile(self.name+'_minimizer.log')
        minuit.setStrategy(2)
        self._nll = self.fitter.GetNLL()

    def _preFitSteps_initFromDB(self):
        """Initialize from DB"""
        if not self.process.cfg['args'].NoImport: 
            #FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, self.args, self.cfg['argAliasInDB'], exclude=['nBkgComb', 'nSig', 'nBkgPeak', 'PeakFrac', 'unboundFl', 'unboundAfb'])
            FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, self.args, self.cfg['argAliasFromDB'])
        self.ToggleConstVar(self.args, True)
        self.ToggleConstVar(self.args, False, self.cfg.get('argPattern'))

    def _preFitSteps_preFit(self):
        """ Standard prefit steps """
        unboundFl = self.args.find("unboundFl")
        unboundAfb = self.args.find("unboundAfb")
        if unboundFl == None or unboundAfb == None:
            return
        def isPhysical(uA, uF):
            f = unboundFlToFl(uF)
            a = unboundAfbToAfb(uA, f)
            return abs(a) < (1 - f)*2.
        while not isPhysical(unboundAfb.getVal(), unboundFl.getVal()):
            fl = unboundFlToFl(unboundFl.getVal())
            afb = unboundAfbToAfb(unboundAfb.getVal(), fl)
            unboundAfb.setVal(afbToUnboundAfb(0.5 * afb, fl))
            unboundFl.setVal(flToUnboundFl(0.5 * fl))

    def _preFitSteps_vetoSmallFs(self):
        """ fs is usually negligible, set the fraction to 0"""
        if "fs" in self.cfg.get('argPattern'):
            fs = self.args.find("fs")
            transAs = self.args.find("transAs")
            fs.setVal(fs.getMin() * 2)  # Exact min go out-of-domain while setting transAs=0
            fs.setConstant(True)
            transAs.setVal(0)
            transAs.setConstant(True)

    def _preFitSteps(self):
        """ Prefit steps """
        self.args = self.pdf.getParameters(self.data)
        self._preFitSteps_initFromDB()
        self._preFitSteps_vetoSmallFs()
        self._preFitSteps_preFit()

    def _postFitSteps(self):
        """Post-processing"""
        #FitterCore.ArgLooper(self.args, lambda arg: arg.Print())
        self.ToggleConstVar(self.args, True)
        FloatedArgs = ROOT.RooArgSet()
        FitterCore.ArgLooper(self.args, lambda p: FloatedArgs.add(p), self.cfg['argPattern'])
        if self.cfg['saveToDB']:
            FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, FloatedArgs,
                                   self.cfg['argAliasInDB'] if self.cfg['argAliasSaveToDB'] else None)
            FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.fitResult)

    def _runFitSteps(self):
        if False:
            RooList = [ROOT.RooFit.Minimizer("Minuit2"), ROOT.RooFit.Save(1)]
            for opt in self.cfg.get("createNLLOpt", []):
                RooList.append(opt)
            FitResult = self.pdf.fitTo(self.data,  *RooList)
            self.fitResult = FitterCore.GetFitResult(self.name, "StdFitter", FitResult)
        else:
            self.FitMigrad()
            if self.cfg.get('FitHesse', False):
                self.FitHesse()
            if self.cfg.get('FitMinos', [False, ()])[0]:
                self.FitMinos()

    def FitMigrad(self):
        """Migrad"""
        migradResult = self.fitter.FitMigrad()
        migradResult = self.fitter.FitMigrad()
        self.fitResult = FitterCore.GetFitResult(self.name, "StdFitter", migradResult)
        print("Migrad Result: ", self.fitResult)

    def FitHesse(self):
        """Hesse"""
        hesseResult = self.fitter.FitHesse()
        self.fitResult = FitterCore.GetFitResult(self.name, "StdFitter", hesseResult)

    def FitMinos(self):
        """Minos"""
        if len(self.cfg['FitMinos']) > 1 and self.cfg['FitMinos'][1]:
            par = ROOT.RooArgSet()
            FitterCore.ArgLooper(self.args, lambda var: par.add(var), self.cfg['FitMinos'][1])
        else:
            par = self.args
        minosResult = self.fitter.FitMinos(par)
        self.fitResult = FitterCore.GetFitResult(self.name, "StdFitter", minosResult)

        # Dont' draw profiled likelihood scanning with following link
        # https://root.cern.ch/root/html/tutorials/roofit/rf605_profilell.C.html
        # This build-in function doesn't handle variable transformation and unphysical region.

def unboundFlToFl(unboundFl):
    return 0.5 + ROOT.TMath.ATan(unboundFl) / ROOT.TMath.Pi()

def flToUnboundFl(fl):
    return ROOT.TMath.Tan((fl - 0.5) * ROOT.TMath.Pi())

def unboundAfbToAfb(unboundAfb, fl):
    return 2. * (1 - fl) * ROOT.TMath.ATan(unboundAfb) / ROOT.TMath.Pi()

def afbToUnboundAfb(afb, fl):
    return ROOT.TMath.Tan((afb * ROOT.TMath.Pi()) / (2.*(1. - fl)))

def decorator_bookMinimizer_addGausConstraints(varNames, vals=None, valerrs=None):
    """ For quick adding gaussian constrint to createNLLOpt.
Assuming no ROOT.RooFit.ExternalConstraints in createNLLOpt by default.
This would be quite useful for proflied Feldman-Cousins method"""
    if vals is None:
        vals = [None] * len(varNames)
    if valerrs is None:
        valerrs = [None] * len(varNames)
    def wrapper(func):
        @functools.wraps(func)
        def wrapped_f(self):
            gausConstraints = ROOT.RooArgSet()
            for varName, val, valerr in zip(varNames, vals, valerrs):
                # assuming all variables are read by WspaceReader
                if varName == "afb":
                    var = self.process.sourcemanager.get("afb")
                    gausC = ROOT.RooGaussian("gausC_afb", "", var, ROOT.RooFit.RooConst(val), ROOT.RooFit.RooConst(valerr if valerr else 0.01))
                elif varName == "fl":
                    var = self.process.sourcemanager.get("fl")
                    gausC = ROOT.RooGaussian("gausC_fl", "", var, ROOT.RooFit.RooConst(val), ROOT.RooFit.RooConst(valerr if valerr else 0.01))
                else:
                    var = self.pdf.getParameters(self.data).find(varName)
                    gausC = ROOT.RooGaussian("gausC_{0}".format(varName), "", var, ROOT.RooFit.RooConst(val if val else var.getVal()), ROOT.RooFit.RooConst(valerr if valerr else var.getError()))
                self.cfg['source'][gausC.GetName()] = gausC
                gausC.Print()
                gausConstraints.add(gausC)
            self.cfg['createNLLOpt'].append(ROOT.RooFit.ExternalConstraints(gausConstraints))
            func(self)
        return wrapped_f
    return wrapper
