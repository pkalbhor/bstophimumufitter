#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

# Description     : Fitter template for binned fit
# Author          : Pritam Kalbhor (physics.pritam@gmail.com)

import pdb
import functools
import math
import ROOT
import BsToPhiMuMuFitter.cpp

from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.StdFitter import StdFitter

from BsToPhiMuMuFitter.varCollection import Bmass

class BinnedFitter(StdFitter):
    """Implementation to Binned fitting procdeure to BsToPhiMuMu angular analysis"""

    @classmethod
    def templateConfig(cls):
        cfg = FitterCore.templateConfig()
        cfg.update({
            'name': "BinnedFitter",
            'data': "dataReader.Fit",
            'pdf': "f",
            'FitHesse': False,
            'FitMinos': [False, ()],
            'createNLLOpt': [ROOT.RooFit.Extended(1), ],
            'argPattern': [r'^.+$', ],
            'argAliasInDB': {},
            'saveToDB': True,
            'argAliasSaveToDB': True,
        })
        return cfg

    def _bookPdfData(self):
        self.pdf = self.process.sourcemanager.get(self.cfg['pdf'])
        print "PDF", self.process.sourcemanager.get(self.cfg['pdf'])
        proj = self.process.sourcemanager.get('h_Bmass')
        self.data = ROOT.RooDataHist("hdata", "", ROOT.RooArgList(Bmass), ROOT.RooFit.Import(proj))

    def _bookMinimizer(self):
        print("""_bookMinimizer from StdFitter""")
        pass

    def _preFitSteps_initFromDB(self):
        """Initialize from DB"""
        FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, self.args, self.cfg['argAliasInDB'])
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
            return abs(a) < (1 - f) * 0.75
        while not isPhysical(unboundAfb.getVal(), unboundFl.getVal()):
            fl = unboundFlToFl(unboundFl.getVal())
            afb = unboundAfbToAfb(unboundAfb.getVal(), fl)
            unboundAfb.setVal(afbToUnboundAfb(0.5 * afb, fl))
            unboundFl.setVal(flToUnboundFl(0.5 * fl))

    def _preFitSteps_vetoSmallFs(self):
        print(""" fs is usually negligible, set the fraction to 0""")
        if "fs" in self.cfg.get('argPattern'):
            fs = self.args.find("fs")
            transAs = self.args.find("transAs")
            fs.setVal(fs.getMin() * 2)  # Exact min go out-of-domain while setting transAs=0
            fs.setConstant(True)
            transAs.setVal(0)
            transAs.setConstant(True)

    def _preFitSteps(self):
        """ Prefit steps """
        self.args = self.pdf.getParameters(self.process.sourcemanager.get(self.cfg['data']))
        self._preFitSteps_initFromDB()
        self._preFitSteps_vetoSmallFs()
        self._preFitSteps_preFit()

    def _postFitSteps(self):
        """Post-processing"""
        #  FitterCore.ArgLooper(self.args, lambda arg: arg.Print())
        self.ToggleConstVar(self.args, True)
        if self.cfg['saveToDB']:
            FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.args, self.cfg['argAliasInDB'] if self.cfg['argAliasSaveToDB'] else None)
            #FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.fitResult)

    def _runFitSteps(self):
        theList = ROOT.RooLinkedList()
        theSave = ROOT.RooFit.Save() #Python discards temporary objects.
        Verbose    = ROOT.RooFit.Verbose(0)
        theList.Add(theSave);  theList.Add(Verbose)
        self.fitResult=self.pdf.chi2FitTo(self.data, theList); 
    def FitMigrad(self):
        """Migrad"""
        migradResult = self.fitter.FitMigrad()
        self.fitResult = {
            "{0}.{1}".format(self.name, self.cfg['argAliasInDB'].get('migrad', 'migrad')): {
                'status': migradResult.status(),
                'nll': migradResult.minNll(),
            }
        }
        print "Migrad Result: ", self.fitResult

    def FitHesse(self):
        """Hesse"""
        self.fitter.FitHesse()

    def FitMinos(self):
        """Minos"""
        if len(self.cfg['FitMinos']) > 1 and self.cfg['FitMinos'][1]:
            par = ROOT.RooArgSet()
            FitterCore.ArgLooper(self.args, lambda var: par.add(var), self.cfg['FitMinos'][1])
        else:
            par = self.args
        minosResult = self.fitter.FitMinos(par)
        self.fitResult.update({
            "{0}.{1}".format(self.name, self.cfg['argAliasInDB'].get('minos', 'minos')): {
                'status': minosResult.status(),
                'nll': minosResult.minNll(),
            }
        })

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
    return ROOT.TMath.Tan(afb * ROOT.TMath.Pi() / 2. / (1. - fl))

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

