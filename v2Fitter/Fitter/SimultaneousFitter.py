#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Ref: rf501_simultaneouspdf.C

import ROOT, os, pdb
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.Plotter import Plotter
from BsToPhiMuMuFitter.varCollection import CosThetaK, CosThetaL, Bmass

class SimultaneousFitter(FitterCore):
    """A fitter object acts as a path, to be queued in a process.
Following functions to be overloaded to customize the full procedure...
    _preFitSteps
    _runFitSteps
    _postFitSteps
"""
    def __init__(self, cfg):
        super(SimultaneousFitter, self).__init__(cfg)
        self.reset()

    def reset(self):
        super(SimultaneousFitter, self).reset()
        self.category = None
        self.data = []
        self.pdf = []
        self.dataWithCategories = None
        self.minimizer = None

    def _bookPdfData(self):
        """ """
        self.category = ROOT.RooCategory("{0}.category".format(self.name), "")
        dataWithCategoriesCmdArgs = (ROOT.RooFit.Index(self.category),)
        if len(self.cfg['category']) == len(self.cfg['data']) == len(self.cfg['pdf']):
            for category, dataName, pdfName in zip(self.cfg['category'], self.cfg['data'], self.cfg['pdf']):
                self.process.sourcemanager.get(pdfName).SetName(pdfName)    # Rename pdf as per the year
                self.pdf.append(self.process.sourcemanager.get(pdfName))
                if not hasattr(dataName, "__iter__"):
                    self.data.append(self.process.sourcemanager.get(dataName))
                else:
                    # Alternative way to merge list of input data/toy
                    for dataIdx, dataNameInList in enumerate(dataName):
                        if dataIdx != 0:
                            self.data[-1].append(self.process.sourcemanager.get(data))
                        else:
                            self.data.append(self.process.sourcemanager.get(data).Clone())
                dataWithCategoriesCmdArgs += (ROOT.RooFit.Import(category, self.data[-1]),)
            self.dataWithCategories = ROOT.RooDataSet("{0}.dataWithCategories".format(self.name), "", self.pdf[-1].getObservables(self.data[-1]), *dataWithCategoriesCmdArgs)
        else:
            raise RuntimeError("Number of category/data/pdf doesn't match")

    def _bookMinimizer(self):
        """Bind a RooSimultaneous object to bind to self.minimizer at Runtime"""
        self.minimizer = ROOT.RooSimultaneous(self.name, "", self.category)
        for cat, pdf in zip(self.cfg['category'], self.pdf):
            self.minimizer.addPdf(pdf, cat)

    def _preFitSteps(self):
        """Abstract: Do something before main fit loop"""
        cwd=os.getcwd()
        for pdf, data, Year in zip(self.pdf, self.data, ['2016', '2017', '2018']):
            args = pdf.getParameters(ROOT.RooArgSet(CosThetaK, CosThetaL, Bmass))
            os.chdir(os.path.join(self.process.cwd, "plots_{0}".format(Year)))
            if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args, aliasDict=self.cfg['argAliasInDB']) #, exclude=self.cfg['argPattern'])
            self.ToggleConstVar(args, True)
            self.ToggleConstVar(args, False, self.cfg['argPattern'])
        os.chdir(cwd)
    def _runFitSteps(self):
        """Standard fitting procedure to be overwritten."""
        if len(self.cfg['fitToCmds']) == 0:
            self.minimizer.fitTo(self.dataWithCategories)
        else:
            if True:
                for cmd in self.cfg['fitToCmds']:
                    self.minimizer.fitTo(self.dataWithCategories, *cmd)
            else:
                self.fitter = ROOT.StdFitter()
                self.fitter.Init(self.minimizer, self.dataWithCategories)
                self._nll = self.fitter.GetNLL()
                self.fitter.FitMigrad()
                self.fitter.FitHesse()

    def _postFitSteps(self):
        """ Abstract: Do something after main fit loop"""
        for pdf, data in zip(self.pdf, self.data):
            self.ToggleConstVar(pdf.getParameters(data), True)
        FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.minimizer.getParameters(self.dataWithCategories), self.cfg['argAliasInDB'])
    
        self.cfg['source']["{0}.dataWithCategories".format(self.name)]=self.dataWithCategories
        self.cfg['source'][self.name] = self.minimizer
        self.cfg['source']["{0}.category".format(self.name)] = self.category
        sampleSet = ROOT.RooArgSet(self.category)
        self.cfg['source']['ProjWData'] = ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories)
        
        #Attach ProjWData Argument to plotter for getting combined fit
        self.process._sequence[1].cfg['plots'][self.process._sequence[1].cfg['switchPlots'][0]]['kwargs']['pdfPlots'][0][1]=(ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))

        frameL = CosThetaL.frame(ROOT.RooFit.Bins(30)) 
        frameK = CosThetaK.frame(ROOT.RooFit.Bins(30)) 
        c1=ROOT.TCanvas()
        for ID, Category, Year in zip([0, 1, 2], self.cfg['category'], ['2016', '2017', '2018']):
            CopyFrameL = frameL.Clone()
            self.dataWithCategories.plotOn(CopyFrameL, ROOT.RooFit.Cut("{0}=={0}::{1}".format(self.category.GetName(), Category)))
            self.minimizer.plotOn(CopyFrameL, ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components(
    self.pdf[ID].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
            #CopyFrameL.Draw()
            CopyFrameL.SetMaximum(1.5 * CopyFrameL.GetMaximum())
            c1.Clear()
            Plotter.DrawWithResidue(CopyFrameL)
            Plotter.latexQ2(self.process.cfg['binKey'])
            Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
            Plotter.latexCMSSim()
            Plotter.latexCMSExtra()
            c1.SaveAs("Simultaneous_Cosl_{0}_{1}_{2}.pdf".format(Year, self.process.cfg['args'].seqKey, self.process.cfg['args'].binKey))

            CopyFrameK = frameK.Clone()
            self.dataWithCategories.plotOn(CopyFrameK, ROOT.RooFit.Cut("{0}=={0}::{1}".format(self.category.GetName(), Category)))
            self.minimizer.plotOn(CopyFrameK, ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components(
    self.pdf[ID].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
            #CopyFrameK.Draw()
            CopyFrameK.SetMaximum(1.5 * CopyFrameK.GetMaximum())
            c1.Clear()
            Plotter.DrawWithResidue(CopyFrameK)
            Plotter.latexQ2(self.process.cfg['binKey'])
            Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
            Plotter.latexCMSSim()
            Plotter.latexCMSExtra()
            c1.SaveAs("Simultaneous_CosK_{0}_{1}_{2}.pdf".format(Year, self.process.cfg['args'].seqKey, self.process.cfg['args'].binKey))

        self.dataWithCategories.plotOn(frameL)
        self.minimizer.plotOn(frameL, ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
        frameL.SetMaximum(1.5 * frameL.GetMaximum())
        c1.Clear()
        #if self.process.cfg['args'].seqKey=='fitSigMCGEN' or self.process.cfg['args'].seqKey=='fitSig2D': 
        #    PlotParams()
        Plotter.DrawWithResidue(frameL)
        Plotter.latexQ2(self.process.cfg['binKey'])
        Plotter.latexCMSSim()
        Plotter.latexCMSExtra()
        Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries()) )
        c1.SaveAs("Combined_{0}_cosl_{1}.pdf".format(self.process.cfg['args'].seqKey, self.process.cfg['args'].binKey))

        self.dataWithCategories.plotOn(frameK)
        self.minimizer.plotOn(frameK, ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
        frameK.SetMaximum(1.5 * frameK.GetMaximum())
        c1.Clear()
        #if self.process.cfg['args'].seqKey=='fitSigMCGEN' or self.process.cfg['args'].seqKey=='fitSig2D': 
        #    PlotParams()
        Plotter.DrawWithResidue(frameK)
        Plotter.latexQ2(self.process.cfg['binKey'])
        Plotter.latexCMSSim()
        Plotter.latexCMSExtra()
        Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries()) )
        c1.SaveAs("Combined_{0}_cosK_{1}.pdf".format(self.process.cfg['args'].seqKey, self.process.cfg['args'].binKey))

    @classmethod
    def templateConfig(cls):
        cfg = {
            'name': "SimultaneousFitter",
            'category': ['cat1', 'cat2', 'cat3'],
            'data': ["data1", "data2", "data3"],
            'pdf': ["f1", "f2", "f3"],
            'argPattern': [r'^.+$'],
            'fitToCmds': [[],],
        }
        return cfg

    def ChangeObservables(self):
        """for GEN Level Fitter"""
        for data, pdf in zip(self.cfg['data'], self.cfg['pdf']):
            self.process.sourcemanager.get(data).changeObservableName("genCosThetaK", "CosThetaK")
            self.process.sourcemanager.get(data).changeObservableName("genCosThetaL", "CosThetaL")

    def _runPath(self):
        """Stardard fitting procedure to be overlaoded."""
        if self.process.cfg['args'].seqKey=='fitSigMCGEN': 
            self.ChangeObservables()
        self._bookPdfData()
        self._bookMinimizer()
        self._preFitSteps()
        self._runFitSteps()
        self._postFitSteps()

