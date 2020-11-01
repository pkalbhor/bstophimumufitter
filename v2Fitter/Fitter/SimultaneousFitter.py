#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Ref: rf501_simultaneouspdf.C

import ROOT, os, pdb
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.Plotter import Plotter
from BsToPhiMuMuFitter.anaSetup import q2bins
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
        self.Years = []
        self.dataWithCategories = None
        self.minimizer = None

    def _bookPdfData(self):
        """ """
        self.Years = self.cfg['Years']
        self.category = ROOT.RooCategory("{0}_category".format(self.name), "")
        dataWithCategoriesCmdArgs = (ROOT.RooFit.Index(self.category),)
        if len(self.cfg['category']) == len(self.cfg['data']) == len(self.cfg['pdf']):
            for category, dataName, pdfName in zip(self.cfg['category'], self.cfg['data'], self.cfg['pdf']):
                self.process.sourcemanager.get(pdfName).SetName(pdfName)    # Rename pdf as per the year
                self.pdf.append(self.process.sourcemanager.get(pdfName))
                if type(dataName) is str:
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
        for pdf, data, Year in zip(self.pdf, self.data, self.Years):
            args = pdf.getParameters(ROOT.RooArgSet(CosThetaK, CosThetaL, Bmass))
            os.chdir(os.path.join(self.process.cwd, "plots_{0}".format(Year)))
            if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args, aliasDict=self.cfg['argAliasInDB'], exclude=self.cfg['argPattern'] if not self.process.cfg['args'].seqKey == 'fitBkgCombA' else None)
            self.ToggleConstVar(args, True)
            self.ToggleConstVar(args, False, self.cfg['argPattern'])
            FitterCore.ArgLooper(args, lambda p: p.SetName(p.GetName()+"_{0}".format(Year)), targetArgs=self.cfg['argPattern'], inverseSel=True) # Rename parameter names
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

        cwd=os.getcwd()
        if self.process.cfg['args'].seqKey == 'fitBkgCombA': os.chdir(os.path.join(self.process.cwd, "plots_{0}".format(self.process.cfg['args'].Year)))
        if self.cfg['saveToDB']:
            FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.minimizer.getParameters(self.dataWithCategories), self.cfg['argAliasInDB'] if self.cfg['argAliasSaveToDB'] else None)
        for pdf, data in zip(self.pdf, self.data):
            FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, pdf.getParameters(data), aliasDict=self.cfg['argAliasInDB'] if self.cfg['argAliasSaveToDB'] else None, exclude=None)
        os.chdir(cwd)
     
        """ofile = ROOT.TFile("../input/Simultaneous_{0}.root".format(q2bins[self.process.cfg['binKey']]['label']), "RECREATE")
        self.minimizer.Write()
        self.dataWithCategories.Write()
        self.category.Write()
        ofile.Close()"""
    
        self.cfg['source']["{0}.dataWithCategories".format(self.name)]=self.dataWithCategories
        self.cfg['source'][self.name] = self.minimizer
        self.cfg['source']["{0}.category".format(self.name)] = self.category
        sampleSet = ROOT.RooArgSet(self.category)
        self.cfg['source']['ProjWData'] = ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories)
        
        #Attach ProjWData Argument to plotter for getting combined fit
        #self.process._sequence[1].cfg['plots'][self.process._sequence[1].cfg['switchPlots'][0]]['kwargs']['pdfPlots'][0][1]=(ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))

        frameL = CosThetaL.frame(ROOT.RooFit.Bins(24)) 
        frameK = CosThetaK.frame(ROOT.RooFit.Bins(24)) 
        c1=ROOT.TCanvas()
        binKey= q2bins[self.process.cfg['binKey']]['label']
        for ID, Category, Year in zip(range(len(self.Years)), self.cfg['category'], self.Years):
            CopyFrameL = frameL.Clone()
            self.category.setIndex(ID); sampleSet = ROOT.RooArgSet(self.category)
            self.dataWithCategories.plotOn(CopyFrameL, ROOT.RooFit.Cut("({0}==({0}::{1}))".format(self.category.GetName(), Category)))
            self.minimizer.plotOn(CopyFrameL, ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components( self.pdf[ID].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed)) # ROOT.RooFit.Components( self.pdf[ID].GetName())
            #CopyFrameL.Draw()
            CopyFrameL.SetMaximum(1.5 * CopyFrameL.GetMaximum())
            c1.Clear()
            Plotter.DrawWithResidue(CopyFrameL)
            Plotter.latexQ2(self.process.cfg['binKey'])
            Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
            Plotter.latexCMSSim()
            Plotter.latexCMSExtra()
            c1.SaveAs("Simultaneous_Cosl_{0}_{1}_{2}.pdf".format(Category, self.process.cfg['args'].seqKey, binKey))

            CopyFrameK = frameK.Clone()
            self.dataWithCategories.plotOn(CopyFrameK, ROOT.RooFit.Cut("{0}=={0}::{1}".format(self.category.GetName(), Category)))
            self.minimizer.plotOn(CopyFrameK, ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components( self.pdf[ID].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed)) #, ROOT.RooFit.Components(self.pdf[ID].GetName())
            #CopyFrameK.Draw()
            CopyFrameK.SetMaximum(1.5 * CopyFrameK.GetMaximum())
            c1.Clear()
            Plotter.DrawWithResidue(CopyFrameK)
            Plotter.latexQ2(self.process.cfg['binKey'])
            Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
            Plotter.latexCMSSim()
            Plotter.latexCMSExtra()
            c1.SaveAs("Simultaneous_CosK_{0}_{1}_{2}.pdf".format(Category, self.process.cfg['args'].seqKey, binKey))

        """
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
        c1.SaveAs("Combined_{0}_cosl_{1}.pdf".format(self.process.cfg['args'].seqKey, binKey))

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
        c1.SaveAs("Combined_{0}_cosK_{1}.pdf".format(self.process.cfg['args'].seqKey, binKey))"""

    def _getFinalFitPlots(self):
        args = self.minimizer.getParameters(self.dataWithCategories)
        from BsToPhiMuMuFitter.StdFitter import unboundFlToFl, unboundAfbToAfb, flToUnboundFl, afbToUnboundAfb
        import BsToPhiMuMuFitter.plotCollection as plotCollection
        from BsToPhiMuMuFitter.Plotter import Plotter
        flDB = unboundFlToFl(args.find('unboundFl').getVal())
        afbDB = unboundAfbToAfb(args.find('unboundAfb').getVal(), flDB)
        sigFrac = {}
        bkgCombFrac = {}

        pdfPlots = [[self.minimizer, plotCollection.plotterCfg_allStyle, None, "Total fit"],
                    ["f_sig3DAltM", plotCollection.plotterCfg_sigStyle, None, "Total fit"],
                    ["f_bkgComb", plotCollection.plotterCfg_bkgStyle, None, "Total fit"],
                    ]
        sampleSet = ROOT.RooArgSet(self.category)
        c1=ROOT.TCanvas()
        for ID, Category, Year in zip([0, 1, 2], self.cfg['category'], ['2016', '2017', '2018']):
            nSigDB = args.find('nSig_{}'.format(Year)).getVal()
            nSigErrorDB = args.find('nSig_{}'.format(Year)).getError()
            nBkgCombDB = args.find('nBkgComb_{}'.format(Year)).getVal()
            nBkgCombErrorDB = args.find('nBkgComb_{}'.format(Year)).getError()
           
            dataPlots = [[self.dataWithCategories, plotCollection.plotterCfg_dataStyle+(ROOT.RooFit.Cut("{0}=={0}::{1}".format(self.category.GetName(), Category)),), "{0} Data".format(Year)],]
            modified_pdfPlots = [
                [pdfPlots[0][0],
                 pdfPlots[0][1] + (ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components(self.pdf[ID].GetName()),),
                 None,
                 "Total fit"],
                [pdfPlots[0][0],
                 pdfPlots[1][1] + (ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components(pdfPlots[1][0])),
                 None,
                 "Sigal"],
                [pdfPlots[0][0],
                 pdfPlots[2][1] + (ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components(pdfPlots[2][0])),
                 None,
                 "Background"],
            ]
            plotFuncs = {
                'B': {'func': Plotter.plotFrameB_fine, 'tag': "Bmass"},
                'L': {'func': Plotter.plotFrameL, 'tag': "cosl"},
                'K': {'func': Plotter.plotFrameK, 'tag': "cosK"},
            }
            for frame in 'BLK':
                plotFuncs[frame]['func'](dataPlots=dataPlots, pdfPlots=modified_pdfPlots)
                if True:
                    if frame == 'B':
                        ROOT.TLatex().DrawLatexNDC(.19, .77, "Y_{Signal}")
                        ROOT.TLatex().DrawLatexNDC(.35, .77, "= {0:.2f}".format(nSigDB))
                        ROOT.TLatex().DrawLatexNDC(.50, .77, "#pm {0:.2f}".format(nSigErrorDB))
                        ROOT.TLatex().DrawLatexNDC(.19, .70, "Y_{Background}")
                        ROOT.TLatex().DrawLatexNDC(.35, .70, "= {0:.2f}".format(nBkgCombDB))
                        ROOT.TLatex().DrawLatexNDC(.50, .70, "#pm {0:.2f}".format(nBkgCombErrorDB))
                    elif frame == 'L':
                        ROOT.TLatex().DrawLatexNDC(.19, .77, "A_{{FB}} = {0:.2f}".format(afbDB))
                    elif frame == 'K':
                        ROOT.TLatex().DrawLatexNDC(.19, .77, "F_{{L}} = {0:.2f}".format(flDB))
                Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(dataPlots[0][0].sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
                Plotter.latexQ2(self.process.cfg['binKey'])
                Plotter.canvas.SaveAs("SimFitFinal3D_{0}_{1}_{2}.pdf".format(plotFuncs[frame]['tag'], Year, q2bins[self.process.cfg['binKey']]['label']))

    @classmethod
    def templateConfig(cls):
        cfg = {
            'name': "SimultaneousFitter",
            'category': ['cat1', 'cat2', 'cat3'],
            'data': ["data1", "data2", "data3"],
            'pdf': ["f1", "f2", "f3"],
            'argPattern': [r'^.+$'],
            'saveToDB': True,
            'argAliasSaveToDB': True,
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
        if 'fitFinal3D' in self.process.cfg['args'].seqKey: self._getFinalFitPlots()
