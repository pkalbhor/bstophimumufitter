#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Ref: rf501_simultaneouspdf.C

import ROOT, os, pdb
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
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
            FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args)
            self.ToggleConstVar(args, True)
            self.ToggleConstVar(args, False, self.cfg['argPattern'])
        os.chdir(cwd)
    def _runFitSteps(self):
        """Standard fitting procedure to be overwritten."""
        if len(self.cfg['fitToCmds']) == 0:
            self.minimizer.fitTo(self.dataWithCategories)
        else:
            for cmd in self.cfg['fitToCmds']:
                self.minimizer.fitTo(self.dataWithCategories, *cmd)

    def _postFitSteps(self):
        """ Abstract: Do something after main fit loop"""
        for pdf, data in zip(self.pdf, self.data):
            self.ToggleConstVar(pdf.getParameters(data), True)
        FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.minimizer.getParameters(self.dataWithCategories))
        self.cfg['source']["{0}.dataWithCategories".format(self.name)]=self.dataWithCategories
        self.cfg['source'][self.name] = self.minimizer
        self.cfg['source']["{0}.category".format(self.name)] = self.category
        
        """
        frame1 = CosThetaL.frame(ROOT.RooFit.Bins(30), ROOT.RooFit.Title("2016 sample"))
        self.dataWithCategories.plotOn(frame1, ROOT.RooFit.Cut("SimultaneousFitter.category==SimultaneousFitter.category::cat16"))
        sampleSet = ROOT.RooArgSet(self.category)
        self.minimizer.plotOn(frame1, ROOT.RooFit.Slice(self.category, "cat16"), ROOT.RooFit.Components(
    self.pdf[0].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
        c1=ROOT.TCanvas()
        frame1.Draw()
        c1.SaveAs("Simultaneous_2016_{0}.pdf".format(self.process.cfg['args'].binKey))        

        frame2 = CosThetaL.frame(ROOT.RooFit.Bins(30), ROOT.RooFit.Title("2017 sample"))
        self.dataWithCategories.plotOn(frame2, ROOT.RooFit.Cut("SimultaneousFitter.category==SimultaneousFitter.category::cat17"))
        self.minimizer.plotOn(frame2, ROOT.RooFit.Slice(self.category, "cat17"), ROOT.RooFit.Components(
    self.pdf[1].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
        frame2.Draw()
        c1.SaveAs("Simultaneous_2017_{0}.pdf".format(self.process.cfg['args'].binKey))        

        frame3 = CosThetaL.frame(ROOT.RooFit.Bins(30), ROOT.RooFit.Title("2018 sample"))
        self.dataWithCategories.plotOn(frame3, ROOT.RooFit.Cut("SimultaneousFitter.category==SimultaneousFitter.category::cat18"))
        self.minimizer.plotOn(frame3, ROOT.RooFit.Slice(self.category, "cat18"), ROOT.RooFit.Components(
    self.pdf[2].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
        frame3.Draw()
        c1.SaveAs("Simultaneous_2018_{0}.pdf".format(self.process.cfg['args'].binKey))   """     

        #Plotting combined plots
        def PlotParams():
            from BsToPhiMuMuFitter.StdFitter import unboundFlToFl, unboundAfbToAfb, flToUnboundFl, afbToUnboundAfb; import math
            args=self.minimizer.getParameters(self.dataWithCategories)
            unboundFl=args.find('unboundFl').getVal(); unboundFlError=args.find('unboundFl').getError();
            FlError=(unboundFlToFl(unboundFl+unboundFlError)-unboundFlToFl(unboundFl-unboundFlError))/2.
            flDB=unboundFlToFl(args.find('unboundFl').getVal());
            
            unboundAfb=args.find('unboundAfb').getVal(); unboundAfbError=args.find('unboundAfb').getError(); print unboundAfbError
            l1=(unboundAfbToAfb((unboundAfb+unboundAfbError), flDB)-unboundAfbToAfb((unboundAfb-unboundAfbError), flDB))/2.                        
            l2=(unboundAfbToAfb(unboundAfb, (flDB+FlError))-unboundAfbToAfb(unboundAfb, (flDB-FlError)))/2.
            AfbError=math.sqrt((l1*l1)+(l2*l2))                                #Error
            afbDB=unboundAfbToAfb(args.find('unboundAfb').getVal(), flDB) #Value
            ROOT.TLatex().DrawLatexNDC(.45, 0.84, r"#scale[0.8]{{F_{{l}} = {0}\pm {1}}}".format(round(flDB, 5), round(FlError, 5)))
            ROOT.TLatex().DrawLatexNDC(.45, 0.79, r"#scale[0.8]{{A_{{6}}= {0}\pm {1}}}".format(round(afbDB, 5), round(AfbError, 5)))

        frame4 = CosThetaL.frame(ROOT.RooFit.Bins(30), ROOT.RooFit.Title("Combined sample"))
        self.dataWithCategories.plotOn(frame4)
        self.minimizer.plotOn(frame4, ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kDashed))
        frame4.SetMaximum(1.5 * frame4.GetMaximum())
        frame4.Draw()
        if self.process.cfg['args'].seqKey=='fitSigMCGEN' or self.process.cfg['args'].seqKey=='fitSig2D': 
            PlotParams()
        c1.SaveAs("Combined_{0}_{1}.pdf".format(self.process.cfg['args'].seqKey, self.process.cfg['args'].binKey))

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

