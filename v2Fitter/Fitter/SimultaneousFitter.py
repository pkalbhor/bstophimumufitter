#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Ref: rf501_simultaneouspdf.C

import ROOT, os, pdb
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.Plotter import Plotter
from BsToPhiMuMuFitter.anaSetup import q2bins
from BsToPhiMuMuFitter.varCollection import CosThetaK, CosThetaL, Bmass, Puw8

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
        self.argset = None
        self.pdf = []
        self.Years = []
        self.dataWithCategories = None
        self.minimizer = None
        self.migradResult = None
        self.hesseResult = None
        self.minosResult = None

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
                    self.data.append(dataName)
                    #for dataIdx, dataNameInList in enumerate(dataName):
                    #    if dataIdx != 0:
                    #        self.data[-1].append(self.process.sourcemanager.get(data))
                    #    else:
                    #        self.data.append(self.process.sourcemanager.get(data).Clone())
                dataWithCategoriesCmdArgs += (ROOT.RooFit.Import(category, self.data[-1]),)
            self.argset = self.pdf[-1].getObservables(self.data[-1])
            if not self.process.cfg['args'].seqKey in ['fitSigMCGEN', 'fitFinal3D_WithKStar']:
                self.argset.add(Puw8) # No all objects are using weights
                self.dataWithCategories = ROOT.RooDataSet("{0}.dataWithCategories".format(self.name), "", self.argset, *dataWithCategoriesCmdArgs, ROOT.RooFit.WeightVar("Puw8"))
            else:
                self.dataWithCategories = ROOT.RooDataSet("{0}.dataWithCategories".format(self.name), "", self.argset, *dataWithCategoriesCmdArgs)
        
        else:
            raise RuntimeError("Number of category/data/pdf doesn't match")

    def _bookMinimizer(self):
        """Bind a RooSimultaneous object to bind to self.minimizer at Runtime"""
        self.minimizer = ROOT.RooSimultaneous(self.name, "", self.category)
        for cat, pdf in zip(self.cfg['category'], self.pdf):
            self.minimizer.addPdf(pdf, cat)

    def _preFitSteps(self):
        """Rename parameter names and import values from database"""
        for pdf, data, Year in zip(self.pdf, self.data, self.Years):
            args = pdf.getParameters(ROOT.RooArgSet(CosThetaK, CosThetaL, Bmass))
            odbfile = os.path.join(self.process.cwd, "plots_{0}".format(Year), self.process.dbplayer.odbfile)
            if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(odbfile, args, aliasDict=self.cfg['argAliasFromDB'])
            self.ToggleConstVar(args, True)
            # self.ToggleConstVar(args, False, self.cfg['argPattern'])
            # Rename parameter names
            FitterCore.ArgLooper(args, lambda p: p.SetName(p.GetName()+"_{0}".format(Year)), targetArgs=self.cfg['argPattern'], inverseSel=True) 
        self.ToggleConstVar(self.minimizer.getParameters(self.dataWithCategories), False, self.cfg['argPattern'])

    def _runFitSteps(self):
        """Standard fitting procedure to be overwritten."""
        #FitterCore.ArgLooper(self.minimizer.getParameters(self.dataWithCategories), lambda p: p.Print()) #Print all parameters
        if len(self.cfg['fitToCmds']) == 0:
            self.minimizer.fitTo(self.dataWithCategories)
        else:
            if False:
                for cmd in self.cfg['fitToCmds']:
                    mresult = self.minimizer.fitTo(self.dataWithCategories, *cmd, ROOT.RooFit.SumW2Error(0), ROOT.RooFit.Save(1))
                    self.migradResult = mresult.status()                                                                              
                    self.hesseResult  = mresult.status()
                    self._nll = mresult.minNll ()
            else:
                print(">>  Standard Fitter Begin")
                self.fitter = ROOT.StdFitter()
                minuit = self.fitter.Init(self.minimizer, self.dataWithCategories)
                minuit.setStrategy(3)
                mresult = self.fitter.FitMigrad()
                hresult = self.fitter.FitHesse()
                self._nll = self.fitter.GetNLL().getVal()
                self.fitter.fitResult = FitterCore.GetFitResult(self.name, "StdFitter", hresult)

    def _postFitSteps(self):
        """ Abstract: Do something after main fit loop"""
        
        for pdf, data in zip(self.pdf, self.data):
            self.ToggleConstVar(pdf.getParameters(data), True)

        if self.process.cfg['args'].seqKey == 'fitBkgCombA': os.chdir(os.path.join(self.process.cwd, "plots_{0}".format(self.process.cfg['args'].Year)))
        if self.cfg['saveToDB']: #Update parameters to db file
            FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, self.minimizer.getParameters(self.dataWithCategories), self.cfg['argAliasInDB'] if self.cfg['argAliasSaveToDB'] else None)

        if self.process.cfg['args'].Function_name == 'systematics': return 0

        for pdf, data in zip(self.pdf, self.data): #Get parameter values from db file
            FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, pdf.getParameters(data), aliasDict=self.cfg['argAliasInDB'] if self.cfg['argAliasSaveToDB'] else None, exclude=None)
     
        self.cfg['source']["{0}.dataWithCategories".format(self.name)]=self.dataWithCategories
        self.cfg['source'][self.name] = self.minimizer
        self.cfg['source']["{0}.category".format(self.name)] = self.category
        sampleSet = ROOT.RooArgSet(self.category)
        self.cfg['source']['ProjWData'] = ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories)
        
        #Attach ProjWData Argument to plotter for getting combined fit
        #self.process._sequence[1].cfg['plots'][self.process._sequence[1].cfg['switchPlots'][0]]['kwargs']['pdfPlots'][0][1]=(ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))

        frameL = CosThetaL.frame(ROOT.RooFit.Bins(20)) 
        frameK = CosThetaK.frame(ROOT.RooFit.Bins(20)) 
        legendInstance = Plotter.legend
        c1=ROOT.TCanvas()
        binKey= q2bins[self.process.cfg['binKey']]['label']
        if self.process.cfg['args'].seqKey in ['fitBkgCombA', 'fitFinal3D_WithKStar']:
            marks=None
        else:
            marks=['sim']
        for ID, Category, Year in zip(range(len(self.Years)), self.cfg['category'], self.Years):
            CopyFrameL = frameL.Clone()
            self.category.setIndex(ID); sampleSet = ROOT.RooArgSet(self.category)
            self.dataWithCategories.plotOn(CopyFrameL, ROOT.RooFit.Cut("({0}==({0}::{1}))".format(self.category.GetName(), Category)))
            self.minimizer.plotOn(CopyFrameL, ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components( self.pdf[ID].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kSolid), ROOT.RooFit.LineColor(2 if self.process.cfg['args'].seqKey=='fitBkgCombA' else 4)) # ROOT.RooFit.Components( self.pdf[ID].GetName())
            CopyFrameL.SetMaximum(1.5 * CopyFrameL.GetMaximum())
            c1.Clear()
            CopyFrameL.Draw() if self.process.cfg['args'].NoPull else Plotter.DrawWithResidue(CopyFrameL)
            Plotter.latexQ2(self.process.cfg['binKey'])
            Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
            Plotter.latexDataMarks(marks=marks)
            legendInstance.Clear(); legendInstance.AddEntry(CopyFrameL.getObject(0).GetName(), self.cfg['LegName'], "LPFE"); legendInstance.Draw()
            c1.SaveAs("Simultaneous_Cosl_{0}_{1}_{2}.pdf".format(Category, self.process.cfg['args'].seqKey, binKey))

            CopyFrameK = frameK.Clone()
            self.dataWithCategories.plotOn(CopyFrameK, ROOT.RooFit.Cut("{0}=={0}::{1}".format(self.category.GetName(), Category)))
            self.minimizer.plotOn(CopyFrameK, ROOT.RooFit.Slice(self.category, Category), ROOT.RooFit.Components( self.pdf[ID].GetName()), ROOT.RooFit.ProjWData(sampleSet, self.dataWithCategories), ROOT.RooFit.LineStyle(ROOT.kSolid), ROOT.RooFit.LineColor(2 if self.process.cfg['args'].seqKey=='fitBkgCombA' else 4) ) #, ROOT.RooFit.Components(self.pdf[ID].GetName())
            CopyFrameK.SetMaximum(1.5 * CopyFrameK.GetMaximum())
            c1.Clear()
            CopyFrameK.Draw() if self.process.cfg['args'].NoPull else Plotter.DrawWithResidue(CopyFrameK)
            Plotter.latexQ2(self.process.cfg['binKey'])
            Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(self.dataWithCategories.sumEntries("{0}=={0}::{1}".format(self.category.GetName(), Category))) )
            Plotter.latexDataMarks(marks=marks)
            legendInstance.Clear(); legendInstance.AddEntry(CopyFrameK.getObject(0).GetName(), self.cfg['LegName'], "LPFE"); legendInstance.Draw()
            c1.SaveAs("Simultaneous_CosK_{0}_{1}_{2}.pdf".format(Category, self.process.cfg['args'].seqKey, binKey))

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
