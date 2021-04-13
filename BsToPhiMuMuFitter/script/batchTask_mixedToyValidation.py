#!/usr/bin/env python
# vim: set sts=4 sw=4 fdm=indent fdl=1 fdn=3 et:

import os, pdb, sys, shelve, math, glob
from subprocess import call
from copy import deepcopy

from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
import BsToPhiMuMuFitter.StdFitter as StdFitter
import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper

#from BsToPhiMuMuFitter.StdProcess import p
import ROOT
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.toyCollection as toyCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection
import BsToPhiMuMuFitter.plotCollection as plotCollection
from BsToPhiMuMuFitter.plotCollection import Plotter
import v2Fitter.Fitter.AbsToyStudier as AbsToyStudier
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

from ROOT import addressof

class MixedToyStudier(AbsToyStudier.AbsToyStudier):
    """"""
    def __init__(self, cfg):
        super(MixedToyStudier, self).__init__(cfg)
        self.plotflag = True
        self.DBFlag = True
        self.proceedFlag = True
        # Define
        ROOT.gROOT.ProcessLine(
        """struct MyTreeContent {
           Int_t        index;
           Double_t     fl;
           Double_t     afb;
           Double_t     status;
           Double_t     hesse;
           Double_t     minos;
           Double_t     entries;
           Double_t     sigEntries;
           Double_t     events16;           
           Double_t     events17;           
           Double_t     events18;
           Double_t     Wevents16;
           Double_t     Wevents17;
           Double_t     Wevents18;
           Double_t     nSig16;
           Double_t     nSig17;
           Double_t     nSig18;
           Double_t     nBkgComb16;
           Double_t     nBkgComb17;
           Double_t     nBkgComb18;
           Double_t     nBkgPeak16;
           Double_t     nBkgPeak17;
           Double_t     nBkgPeak18;
           Double_t     nSig;
           Double_t     nBkgComb;
           Double_t     nBkgPeak;
           Double_t     nll;
        };""")

    def getSubDataEntries(self, setIdx, Type, Year=2016):
        expectedYield = 0
        yieldSpread = 0
        try:
            if self.process.cfg['args'].SimFit:
                db = shelve.open(os.path.join(modulePath, "plots_{}".format(Year), self.process.dbplayer.odbfile), "r")
            else:
                db = shelve.open(self.process.dbplayer.odbfile, "r")
            expectedYield += db['PeakFrac']['getVal']*db['nSig']['getVal'] if Type=='nBkgPeak' else db[Type]['getVal']
            PeakError = math.sqrt((db['PeakFrac']['getVal']*db['nSig']['getError'])**2 + (db['PeakFrac']['getError']*db['nSig']['getVal'])**2)
            yieldSpread += PeakError if Type=='nBkgPeak' else db[Type]['getError']
        finally:
            if self.cfg['Spread'] == 'Gaus':
                if Type=="nSig": #fixing total no. of entries and randomizing only nSig
                    yields = ROOT.gRandom.Gaus(expectedYield, yieldSpread/3.)
                else:
                    yields = round(self.sigEntries*db['PeakFrac']['getVal']) if Type=='nBkgPeak' else round((db['nSig']['getVal']*(1.+db['PeakFrac']['getVal'])+db[Type]['getVal']) - (self.sigEntries*(1+db['PeakFrac']['getVal'])))
                    if yields<0: self.proceedFlag = False
            else:
                yields = ROOT.gRandom.Poisson(expectedYield)
            db.close()
        self.logger.logINFO("SubDataSet has expected yields {0} in set {1}".format(yields, setIdx))
        return yields

    def _preSetsLoop(self):
        self.otree = ROOT.TTree("tree", "")
        self.treeContent = ROOT.MyTreeContent()
        self.otree.Branch("index", ROOT.addressof(self.treeContent, 'index'), 'index/I')
        self.otree.Branch("fl", addressof(self.treeContent, 'fl'), 'fl/D')
        self.otree.Branch("afb", addressof(self.treeContent, 'afb'), 'afb/D')
        self.otree.Branch("status", addressof(self.treeContent, 'status'), 'status/D')
        self.otree.Branch("hesse", addressof(self.treeContent, 'hesse'), 'hesse/D')
        #self.otree.Branch("minos", addressof(self.treeContent, 'minos'), 'minos/D')
        if self.process.cfg['args'].SimFit: 
            self.otree.Branch("events16", ROOT.addressof(self.treeContent, 'events16'), 'events16/D')
            self.otree.Branch("events17", ROOT.addressof(self.treeContent, 'events17'), 'events17/D')
            self.otree.Branch("events18", ROOT.addressof(self.treeContent, 'events18'), 'events18/D')
            self.otree.Branch("Wevents16", ROOT.addressof(self.treeContent, 'Wevents16'), 'Wevents16/D') 
            self.otree.Branch("Wevents17", ROOT.addressof(self.treeContent, 'Wevents17'), 'Wevents17/D') 
            self.otree.Branch("Wevents18", ROOT.addressof(self.treeContent, 'Wevents18'), 'Wevents18/D') 
            self.otree.Branch("nSig16", ROOT.addressof(self.treeContent, 'nSig16'), 'nSig16/D') 
            self.otree.Branch("nSig17", ROOT.addressof(self.treeContent, 'nSig17'), 'nSig17/D') 
            self.otree.Branch("nSig18", ROOT.addressof(self.treeContent, 'nSig18'), 'nSig18/D') 
            self.otree.Branch("nBkgComb16", ROOT.addressof(self.treeContent, 'nBkgComb16'), 'nBkgComb16/D') 
            self.otree.Branch("nBkgComb17", ROOT.addressof(self.treeContent, 'nBkgComb17'), 'nBkgComb17/D') 
            self.otree.Branch("nBkgComb18", ROOT.addressof(self.treeContent, 'nBkgComb18'), 'nBkgComb18/D') 
            self.otree.Branch("nBkgPeak16", ROOT.addressof(self.treeContent, 'nBkgPeak16'), 'nBkgPeak16/D') 
            self.otree.Branch("nBkgPeak17", ROOT.addressof(self.treeContent, 'nBkgPeak17'), 'nBkgPeak17/D') 
            self.otree.Branch("nBkgPeak18", ROOT.addressof(self.treeContent, 'nBkgPeak18'), 'nBkgPeak18/D') 
        else:
            self.otree.Branch("entries", addressof(self.treeContent, 'entries'), 'entries/D')
            self.otree.Branch("sigEntries", addressof(self.treeContent, 'sigEntries'), 'sigEntries/D')
        self.otree.Branch("nSig", addressof(self.treeContent, 'nSig'), 'nSig/D')
        self.otree.Branch("nBkgComb", addressof(self.treeContent, 'nBkgComb'), 'nBkgComb/D')
        self.otree.Branch("nBkgPeak", addressof(self.treeContent, 'nBkgPeak'), 'nBkgPeak/D')
        self.otree.Branch("nll", addressof(self.treeContent, 'nll'), 'nll/D')
        pass

    def _preRunFitSteps(self, setIdx):
        import shutil
        cwd=os.getcwd()
        workdir = os.path.join(modulePath, "plots_{}".format(self.process.cfg['args'].Year))
        if self.DBFlag:
            self.DBFlag = False
            shutil.copy(os.path.join(workdir, self.process.dbplayer.odbfile), self.process.dbplayer.odbfile)
            print(self.process.dbplayer.odbfile, "copied from", workdir, "to work area: ", cwd)
        elif os.path.exists(self.process.dbplayer.odbfile):
            print(self.process.dbplayer.odbfile, "already exists! Not copied.")

    def _runToyCreater(self, Type, Year): 
        """Creating Toy Samples"""
        print(">>>> Creating Toy Sample of Type: ", Type, " and Year:", Year)
        from BsToPhiMuMuFitter.toyCollection import GetToyObject
        if Type=='nBkgComb':
            obj = GetToyObject(self.process, 'bkgCombToyGenerator', self.currentSubDataEntries, Year)
            obj.cfg['mixWith'] = "bkgCombToy.{}.Fit".format(Year)
            obj.cfg['scale'] = 1.
        if Type=='nBkgPeak':
            obj = GetToyObject(self.process, 'bkgPeakToyGenerator', self.currentSubDataEntries, Year)
            obj.cfg['mixWith'] = "bkgPeakToy.{}.Fit".format(Year)
            obj.cfg['scale'] = 1.
        obj.hookProcess(self.process)
        setattr(obj, "logger", self.process.logger)
        obj.customize(self.currentSubDataEntries, Year)
        obj._runPath()
        return obj.data

    def _postRunFitPlotter(self, idx):
        self.plotflag = False
        from BsToPhiMuMuFitter.Plotter import Plotter, defaultPlotRegion, plotterCfg_styles
        import BsToPhiMuMuFitter.plotCollection as plotCollection

        Year = self.process.cfg['args'].Year
        self.process.cfg['args'].list = ['plot_final_WithKStar']
        plotter = plotCollection.GetPlotterObject(self.process)
        plotter.cfg['plots']['plot_final_WithKStar']['kwargs']['pltName'] = "plot_final_{}.{}".format(idx, Year)
        plotter.cfg['plots']['plot_final_WithKStar']['kwargs']['dataReader'] = "SubSampleData.{}".format(Year)

        self.process.cfg['args'].NoImport = True
        self.process.sourcemanager.update("SubSampleData.{}.Fit".format(Year), self.fitter.data)
        self.process.sourcemanager.update("f_final_WithKStar.{}".format(Year), self.fitter.pdf)
        plotter.hookProcess(self.process)
        setattr(plotter, "logger", self.process.logger)
        plotter._runPath()

    def _postRunFitSteps(self, setIdx):
        SimFit = self.process.cfg['args'].SimFit
        if not SimFit: self.fitter._nll = self.fitter._nll.getVal()
        if math.fabs(self.fitter._nll) < 1e20:
            unboundAfb = self.fitter.minimizer.getParameters(self.fitter.dataWithCategories).find('unboundAfb').getVal() if SimFit else self.fitter.args.find('unboundAfb').getVal()
            unboundFl  = self.fitter.minimizer.getParameters(self.fitter.dataWithCategories).find('unboundFl').getVal() if SimFit else self.fitter.args.find('unboundFl').getVal()
            self.treeContent.fl = StdFitter.unboundFlToFl(unboundFl)
            self.treeContent.afb = StdFitter.unboundAfbToAfb(unboundAfb, self.treeContent.fl)
            self.treeContent.index = setIdx
            self.treeContent.status = self.fitter.migradResult if SimFit else self.fitter.fitResult['{}.migrad'.format(self.fitter.name)]['status']
            self.treeContent.hesse = self.fitter.hesseResult if SimFit else self.fitter.fitResult['{}.hesse'.format(self.fitter.name)]['status']
            #self.treeContent.minos = self.fitter.minosResult.status() if SimFit else self.fitter.fitResult['{}.minos'.format(self.fitter.name)]['status']
            if SimFit:
                simargs = self.fitter.minimizer.getParameters(self.fitter.dataWithCategories)
                self.treeContent.events16 = self.fitter.data[0].numEntries()
                self.treeContent.events17 = self.fitter.data[1].numEntries()
                self.treeContent.events18 = self.fitter.data[2].numEntries()
                self.treeContent.Wevents16 = self.fitter.data[0].sumEntries()
                self.treeContent.Wevents17 = self.fitter.data[1].sumEntries()
                self.treeContent.Wevents18 = self.fitter.data[2].sumEntries()
                self.treeContent.nSig16 = simargs.find('nSig_2016').getVal()
                self.treeContent.nSig17 = simargs.find('nSig_2017').getVal()
                self.treeContent.nSig18 = simargs.find('nSig_2018').getVal()
                self.treeContent.nBkgComb16 = simargs.find('nBkgComb_2016').getVal()
                self.treeContent.nBkgComb17 = simargs.find('nBkgComb_2017').getVal()
                self.treeContent.nBkgComb18 = simargs.find('nBkgComb_2018').getVal()
                self.treeContent.nBkgPeak16 = self.fitter.pdf[0].servers().findByName("nBkgPeak").getVal()
                self.treeContent.nBkgPeak17 = self.fitter.pdf[1].servers().findByName("nBkgPeak").getVal()
                self.treeContent.nBkgPeak18 = self.fitter.pdf[2].servers().findByName("nBkgPeak").getVal()
            else:
                self.treeContent.entries = self.fitter.data.sumEntries()
                self.treeContent.sigEntries = self.sigEntries
                self.treeContent.nSig = self.fitter.args.find('nSig').getVal()
                self.treeContent.nBkgComb = self.fitter.args.find('nBkgComb').getVal()
                self.treeContent.nBkgPeak = self.fitter.pdf.servers().findByName("nBkgPeak").getVal()
            self.treeContent.nll = self.fitter._nll
            self.otree.Fill()
            if not SimFit:
                if (self.treeContent.fl > 0.97 and abs(self.treeContent.afb) < 0.05 and self.plotflag): self._postRunFitPlotter(setIdx)
            print("Status: ", self.treeContent.status, self.treeContent.hesse)

    def _postSetsLoop(self):
        SimFit = self.process.cfg['args'].SimFit
        ofile = ROOT.TFile("setSummary_{}_{}.root".format("Simult" if SimFit else self.process.cfg['args'].Year, q2bins[self.process.cfg['binKey']]['label']), 'RECREATE')
        ofile.cd()
        self.otree.Write()
        ofile.Close()

    getSubData = AbsToyStudier.getSubData_random

# Define Process
def GetMixedToyObject(self):
    Year = self.cfg['args'].Year
    if self.cfg['args'].SimFit:
        from BsToPhiMuMuFitter.fitCollection import SimultaneousFitter_mixedToyValidation
        setupMixedToyStudier = deepcopy(AbsToyStudier.AbsToyStudier.templateConfig())
        setupMixedToyStudier.update({
            'name': "mixedToyStudier",
            'data': ["sigMCReader.{}.Fit", "f_bkgComb.{}", "f_bkg_KStar.{}"],
            'Type': [(0, 'nSig', 'Sim'), (1, 'nBkgComb', 'Toy'), (2, 'nBkgPeak', 'Toy')],
            'fitter': SimultaneousFitter_mixedToyValidation,
            'nSetOfToys': 1,
            'Spread': 'Gaus',
        })
        mixedToyStudier = MixedToyStudier(setupMixedToyStudier)
        mixedToyStudier.cfg['fitter'].cfg['FitMinos'] = [False, ('unboundAfb', 'unboundFl')]
    else:
        setupMixedToyStudier = deepcopy(AbsToyStudier.AbsToyStudier.templateConfig())
        setupMixedToyStudier.update({
            'name': "mixedToyStudier.{}".format(Year),
            'data': ["sigMCReader.{}.Fit".format(Year), "f_bkgComb.{}".format(Year), "f_bkg_KStar.{}".format(Year)],
            'Type': [(0, 'nSig', 'Sim'), (1, 'nBkgComb', 'Toy'), (2, 'nBkgPeak', 'Toy')],
            'fitter': fitCollection.GetFitterObjects(self, 'finalFitter_WithKStar'),
            'nSetOfToys': 1,
            'Spread': 'Gaus',
        })
        mixedToyStudier = MixedToyStudier(setupMixedToyStudier)
        mixedToyStudier.cfg['fitter'].cfg['data'] = "sigMCReader.{}.Fit".format(Year)
        mixedToyStudier.cfg['fitter'].cfg['argPattern'] = ['nSig', 'unboundAfb', 'unboundFl', 'nBkgComb']
        mixedToyStudier.cfg['fitter'].cfg['FitMinos'] = [False, ('unboundAfb', 'unboundFl')]
    return mixedToyStudier

# Customize batch task
class BatchTaskWrapper(AbsBatchTaskWrapper.AbsBatchTaskWrapper):
    def createJdl(self, parser_args):
        jdl = self.createJdlBase()
        jdl += """Transfer_Input_Files = {0}/seqCollection.py""".format(modulePath)
        jdl += """
arguments = -b {binKey} -s {seqKey} -y {Year} -t {nSetOfToys}{SimFit} run $(Process)
queue {nJobs}"""
        jdl = jdl.format(binKey = q2bins[parser_args.process.cfg['binKey']]['label'],
                        nSetOfToys=parser_args.nSetOfToys, nJobs=self.cfg['nJobs'],
                        seqKey  = parser_args.process.cfg['args'].seqKey,       
                        Year    = parser_args.process.cfg['args'].Year, 
                        SimFit  = " --SimFit" if parser_args.process.cfg['args'].SimFit else "",        
                        executable=os.path.join(modulePath,"seqCollection.py"),)
        return jdl

setupBatchTask = deepcopy(BatchTaskWrapper.templateCfg())
setupBatchTask.update({
    'nJobs': 1,
    'queue': "tomorrow",
})

# Customize taskSubmitter and jobRunner if needed
def GetParams(f, h, binKey, GEN, name):
    plotCollection.Plotter.canvas.cd()
    ROOT.TLatex().DrawLatexNDC(.73, .89, r"#scale[0.7]{{#chi^{{2}} / NDF: {chi2}/{ndf}}}".format(chi2=round(f.GetChisquare(), 0),ndf=f.GetNDF()) )
    ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
    ROOT.TLatex().DrawLatexNDC(.73,.85,r"#scale[0.7]{{#color[2]{{Gen {Name}}}: {param}}}".format(Name="F_{L}" if name=="fl" else "A_{6}", param=round(GEN, 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.81,r"#scale[0.7]{{#color[4]{{Fit {Name}}}   : {param}}}".format(Name="F_{L}" if name=="fl" else "A_{6}", param=round(f.GetParameter(1), 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[3]{{Mean}}   : {param}}}".format(param=round(h.GetMean(), 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(h.GetEntries(), 0)) )

def GetSummaryGraph(binKeys, RecoResult, GenResult, args, pltName="mixedToy"):
    """Plotting a graph summarizing result for all bins"""
    binKeys.append('abovePsi2s'); RecoResult.append((2, 0, 2, 0)); GenResult.append((2, 0, 2, 0)) # added empty bin at end
    from array import array
    def quadSum(lst):
        return math.sqrt(sum(map(lambda i: i**2, lst)))

    xx = array('d', [sum(q2bins[binKey]['q2range']) / 2 for binKey in binKeys])
    xxErr = array('d', map(lambda t: (t[1] - t[0]) / 2, [q2bins[binKey]['q2range'] for binKey in binKeys]))
    grFls = []
    grAfbs = []

    Plotter.legend.Clear()
    legend = ROOT.TLegend(.78, .72, .95, .92)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)

    yyFl = array('d', [0] * len(binKeys))
    yyFlStatErrHi = array('d', [0] * len(binKeys))
    yyFlStatErrLo = array('d', [0] * len(binKeys))
    yyFlSystErrHi = array('d', [0] * len(binKeys))
    yyFlSystErrLo = array('d', [0] * len(binKeys))
    yyFlErrHi = array('d', [0] * len(binKeys))
    yyFlErrLo = array('d', [0] * len(binKeys))

    yyAfb = array('d', [0] * len(binKeys))
    yyAfbStatErrHi = array('d', [0] * len(binKeys))
    yyAfbStatErrLo = array('d', [0] * len(binKeys))
    yyAfbSystErrHi = array('d', [0] * len(binKeys))
    yyAfbSystErrLo = array('d', [0] * len(binKeys))
    yyAfbErrHi = array('d', [0] * len(binKeys))
    yyAfbErrLo = array('d', [0] * len(binKeys))
    dbSetup = [{'title': "Subsamples",
                'legendOpt': "LPE",
                'fillColor': 2,
                'drawOpt': ['2'],
                'Result': RecoResult,}, 
               {'title': "GEN",
                'legendOpt': "LPE",
                'fillColor': 4,
                'Result': GenResult,}, 
                ]
    for dbsIdx, dbs in enumerate(dbSetup):
        title = dbs.get('title', None)
        drawOpt = dbs.get('drawOpt', ["2"])
        fillColor = dbs.get('fillColor', 2)
        fillStyle = dbs.get('fillStyle', 3002)
        legendOpt = dbs.get('legendOpt', None)
        dbs.update({
            'drawOpt': drawOpt,
            'legendOpt': legendOpt,
        })
        Result = dbs.get('Result', None)

        #db = shelve.open(os.path.join(args.process.dbplayer.absInputDir, "fitResults_{0}.db".format(q2bins[binKey]['label'])), 'r')
        for binKeyIdx, (binKey, (Fl, FlError, A6, A6Error)) in enumerate(zip(binKeys, Result)):
            yyFl[binKeyIdx] = Fl
            yyAfb[binKeyIdx] = A6
            yyFlStatErrHi[binKeyIdx], yyFlStatErrLo[binKeyIdx],\
                yyAfbStatErrHi[binKeyIdx], yyAfbStatErrLo[binKeyIdx] = FlError, FlError, A6Error, A6Error
            yyFlSystErrHi[binKeyIdx], yyFlSystErrLo[binKeyIdx],\
                    yyAfbSystErrHi[binKeyIdx], yyAfbSystErrLo[binKeyIdx] = 0, 0, 0, 0
            yyFlErrHi[binKeyIdx] = min(quadSum([yyFlStatErrHi[binKeyIdx], yyFlSystErrHi[binKeyIdx]]), 1. - yyFl[binKeyIdx])
            yyFlErrLo[binKeyIdx] = min(quadSum([yyFlStatErrLo[binKeyIdx], yyFlSystErrLo[binKeyIdx]]), yyFl[binKeyIdx])
            yyAfbErrHi[binKeyIdx] = min(quadSum([yyAfbStatErrHi[binKeyIdx], yyAfbSystErrHi[binKeyIdx]]), 0.75 - yyAfb[binKeyIdx])
            yyAfbErrLo[binKeyIdx] = min(quadSum([yyAfbStatErrLo[binKeyIdx], yyAfbSystErrLo[binKeyIdx]]), 0.75 + yyAfb[binKeyIdx])


        grAfb = ROOT.TGraphAsymmErrors(len(binKeys), xx, yyAfb, xxErr, xxErr, yyAfbErrLo, yyAfbErrHi)
        grAfb.SetMarkerColor(fillColor if fillColor else 2)
        if title=='Subsamples': grAfb.SetMarkerStyle(4); grAfb.SetMarkerSize(1.2)
        if title=='GEN': grAfb.SetMarkerSize(1)
        grAfb.SetLineColor(fillColor if fillColor else 2)
        grAfb.SetFillColor(fillColor if fillColor else 2)
        grAfb.SetFillColorAlpha(2, .3)
        #grAfb.SetFillStyle(fillStyle if fillStyle else 3001)
        grAfbs.append(grAfb)

        grFl = ROOT.TGraphAsymmErrors(len(binKeys), xx, yyFl, xxErr, xxErr, yyFlErrLo, yyFlErrHi)
        grFl.SetMarkerColor(fillColor if fillColor else 2)
        if title=='Subsamples': grFl.SetMarkerStyle(4); grFl.SetMarkerSize(1.2)
        if title=='GEN': grFl.SetMarkerSize(1)
        grFl.SetLineColor(fillColor if fillColor else 2)
        grFl.SetFillColor(fillColor if fillColor else 2)
        grFl.SetFillColorAlpha(fillColor, .3)
        #grFl.SetFillStyle(fillStyle if fillStyle else 3003)
        grFls.append(grFl)
        if legendOpt:
            Plotter.legend.AddEntry(grAfb, title, legendOpt)

    A6Range = (-0.6, 0.6)
    for grIdx, gr in enumerate(grAfbs):
        gr.SetTitle("")
        gr.GetXaxis().SetTitle("q^{2} [GeV^{2}]")
        gr.GetYaxis().SetTitle("A_{6}")
        drawSM = True; gr.GetYaxis().SetRangeUser(0.3, 0.9) if not drawSM else gr.GetYaxis().SetRangeUser(*A6Range)#+-0.02
        gr.SetLineWidth(2)
        drawOpt = dbSetup[grIdx]['drawOpt'] if isinstance(dbSetup[grIdx]['drawOpt'], list) else [dbSetup[grIdx]['drawOpt']]
        for optIdx, opt in enumerate(drawOpt):
            if grIdx == 0:
                gr.Draw("A" + opt if optIdx == 0 else opt)
            else:
                gr.Draw(opt + " SAME")
        gr.Draw("p")
    jpsiBox = ROOT.TBox(8.00, -.05, 11.0, .05) if not drawSM else ROOT.TBox(8.00, A6Range[0], 11.0, A6Range[1]) 
    psi2sBox = ROOT.TBox(12.5, -.05, 15.0, .05) if not drawSM else ROOT.TBox(12.5, A6Range[0], 15.0, A6Range[1]) 
    jpsiBox.SetFillColorAlpha(17, .35)
    psi2sBox.SetFillColorAlpha(17, .35)
    jpsiBox.Draw()
    psi2sBox.Draw()
    ROOT.TLatex().DrawLatex(9., 0., r"#scale[0.7]{#color[12]{J/#psi}}")
    ROOT.TLatex().DrawLatex(13.5, 0., r"#scale[0.7]{#color[12]{#psi^{'}}}")
    legend.Draw()
    Plotter.legend.Draw()
    #Plotter.latexDataMarks(marks)
    Plotter.canvas.Print(pltName+'_SummaryGraph_{}_a6.pdf'.format('Simult' if args.process.cfg['args'].SimFit else args.process.cfg['args'].Year))

    for grIdx, gr in enumerate(grFls):
        gr.SetTitle("")
        gr.GetXaxis().SetTitle("q^{2} [GeV^{2}]")
        gr.GetYaxis().SetTitle("F_{L}")
        drawSM = True; gr.GetYaxis().SetRangeUser(0., 1.0) if not drawSM else gr.GetYaxis().SetRangeUser(0., 1.)
        gr.SetLineWidth(2)
        drawOpt = dbSetup[grIdx]['drawOpt'] if isinstance(dbSetup[grIdx]['drawOpt'], list) else [dbSetup[grIdx]['drawOpt']]
        for optIdx, opt in enumerate(drawOpt):
            if grIdx == 0:
                gr.Draw("A" + opt if optIdx == 0 else opt)
            else:
                gr.Draw(opt + " SAME")
        gr.Draw("p")
    jpsiBox.SetY1(0.3) if not drawSM else jpsiBox.SetY1(0.) 
    jpsiBox.SetY2(.9) if not drawSM else jpsiBox.SetY2(1.) 
    psi2sBox.SetY1(0.3) if not drawSM else psi2sBox.SetY1(0.) 
    psi2sBox.SetY2(.9) if not drawSM else psi2sBox.SetY2(1.) 
    jpsiBox.Draw()
    psi2sBox.Draw()
    ROOT.TLatex().DrawLatex(9., 0.5, r"#scale[0.7]{#color[12]{J/#psi}}")
    ROOT.TLatex().DrawLatex(13.5, 0.5, r"#scale[0.7]{#color[12]{#psi^{'}}}")
    legend.Draw()
    Plotter.legend.Draw()
    #Plotter.latexDataMarks(marks)
    Plotter.canvas.Print(pltName+'_SummaryGraph_{}_fl.pdf'.format('Simult' if args.process.cfg['args'].SimFit else args.process.cfg['args'].Year))




# Postproc fit results.
def func_postproc(args):
    """ Fit to fit result and make plots """
    GenResult = []    
    RecoResult = []
    os.chdir(args.wrapper.task_dir)
    args.process.addService("dbplayer", FitDBPlayer(absInputDir=os.path.join(modulePath, "plots_{}".format(args.Year))))
    binKeys = args.process.cfg['allBins'] if args.process.cfg['args'].forall else args.process.cfg['bins'] #Run over all bins if no binkey arg is supplied
    for binKey in binKeys:
        ifilename = "setSummary_{}_{}.root".format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label'])
        if not os.path.exists(ifilename) or args.forceHadd:
            call(["hadd", "-f", ifilename] + glob.glob('*/setSummary_{}_{}.root'.format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label'])))
        ifile = ROOT.TFile(ifilename)
        tree = ifile.Get("tree")

        binWidth = 0.01
        h_setSummary_afb = ROOT.TH1F("h_setSummary_afb", "", int(1.5 / binWidth), -0.75, 0.75)
        h_setSummary_fl = ROOT.TH1F("h_setSummary_fl", "", int(1. / binWidth), 0., 1.)

        tree.Draw("afb>>h_setSummary_afb", "status==0")
        tree.Draw("fl>>h_setSummary_fl", "status==0")

        f_setSummary_afb = ROOT.TF1("f_setSummary_afb", "gaus", -0.75 + binWidth, 0.75 - binWidth)
        h_setSummary_afb.Fit("f_setSummary_afb")
        h_setSummary_afb.GetFunction("f_setSummary_afb").SetLineColor(4)

        f_setSummary_fl = ROOT.TF1("f_setSummary_fl", "gaus", binWidth, 1 - binWidth)
        h_setSummary_fl.Fit("f_setSummary_fl")
        h_setSummary_fl.GetFunction("f_setSummary_fl").SetLineColor(4)

        # Draw
        db = shelve.open(os.path.join(args.process.dbplayer.absInputDir, "fitResults_{0}.db".format(q2bins[binKey]['label'])), 'r')
        fl_GEN = StdFitter.unboundFlToFl(db['unboundFl_GEN']['getVal'])
        afb_GEN = StdFitter.unboundAfbToAfb(db['unboundAfb_GEN']['getVal'], fl_GEN)
        line = ROOT.TLine()
        line.SetLineWidth(2)
        line.SetLineColor(2)
        line.SetLineStyle(9)
        plotCollection.Plotter.canvas.cd()

        h_setSummary_afb.SetXTitle("A_{6}")
        h_setSummary_afb.SetYTitle("Number of test samples")
        h_setSummary_afb.SetFillColor(ROOT.kGreen-10)
        h_setSummary_afb.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_afb.GetMaximum())
        h_setSummary_afb.Draw()
        GetParams(f_setSummary_afb, h_setSummary_afb, binKey, afb_GEN, "a6")    
        if args.drawGEN:
            line.DrawLine(afb_GEN, 0, afb_GEN, h_setSummary_afb.GetMaximum())
        plotCollection.Plotter.latexDataMarks(['mix'])
        plotCollection.Plotter.canvas.Print("h_setSummary_mixedToyValidation_a6_{}_{}.pdf".format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label']))

        h_setSummary_fl.SetXTitle("F_{L}")
        h_setSummary_fl.SetYTitle("Number of test samples")
        h_setSummary_fl.SetFillColor(ROOT.kGreen-10)
        h_setSummary_fl.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_fl.GetMaximum())
        h_setSummary_fl.Draw()
        GetParams(f_setSummary_fl, h_setSummary_fl, binKey, fl_GEN, "fl")
        if args.drawGEN:
            line.DrawLine(fl_GEN, 0, fl_GEN, h_setSummary_fl.GetMaximum())
        plotCollection.Plotter.latexDataMarks(['mix'])
        plotCollection.Plotter.canvas.Print("h_setSummary_mixedToyValidation_fl_{}_{}.pdf".format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label']))
        Fl_GENErr = abs(StdFitter.unboundFlToFl(db['unboundFl_GEN']['getVal'] + db['unboundFl_GEN']['getError']) - fl_GEN)
        A6_GENErr = abs(StdFitter.unboundAfbToAfb(db['unboundAfb_GEN']['getVal'] + db['unboundAfb_GEN']['getError'], fl_GEN) - afb_GEN)
        GenResult.append((fl_GEN, Fl_GENErr, afb_GEN, A6_GENErr)) 
        RecoResult.append((f_setSummary_fl.GetParameter(1), f_setSummary_fl.GetParameter(2), f_setSummary_afb.GetParameter(1), f_setSummary_afb.GetParameter(2)))                


        if not args.process.cfg['args'].SimFit:
            from copy import deepcopy
            tree.Draw("nSig", "status==0")
            nSigHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))
            tree.Draw("nBkgComb", "status==0")
            nBkgCombHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))
            tree.Draw("nBkgPeak", "status==0")
            nBkgPeakHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))
            tree.Draw("entries", "status==0")
            nTotalHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))

            # Signal Event Distributions
            nSigHist.Draw()
            nSigHist.SetFillColor(ROOT.kBlue-10)
            #nSigHist.SetLineColor(ROOT.kBlue)
            ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[4]{{Mean}}   : {param}}}".format(param=round(nSigHist.GetMean(), 5)) )
            ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nSigHist.GetEntries(), 0)) )
            ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nSig}} : {param}}}".format(param=round(db['nSig']['getVal'], 0)) )
            plotCollection.Plotter.canvas.Update(); line.DrawLine(db['nSig']['getVal'], 0, db['nSig']['getVal'], ROOT.gPad.GetUymax())
            ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
            plotCollection.Plotter.canvas.Print("h_nSig_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))

            #Bkg yield distribution
            nBkgCombHist.Draw()
            nBkgCombHist.SetFillColor(ROOT.kRed-10)
            #nBkgCombHist.SetLineColor(ROOT.kRed)
            ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[2]{{Mean}}   : {param}}}".format(param=round(nBkgCombHist.GetMean(), 5)) )
            ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nBkgCombHist.GetEntries(), 0)) )
            ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nBkg}} : {param}}}".format(param=round(db['nBkgComb']['getVal'], 0)) )
            plotCollection.Plotter.canvas.Update(); line.DrawLine(db['nBkgComb']['getVal'], 0, db['nBkgComb']['getVal'], ROOT.gPad.GetUymax())
            ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
            plotCollection.Plotter.canvas.Print("h_nBkgComb_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))
        
            #Peaking Bkg yield distribution
            nBkgPeakHist.Draw()
            nBkgPeakHist.SetFillColor(ROOT.kGreen-10)
            #nBkgPeakHist.SetLineColor(ROOT.kGreen)
            ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[3]{{Mean}}   : {param}}}".format(param=round(nBkgPeakHist.GetMean(), 5)) )
            ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nBkgPeakHist.GetEntries(), 0)) )
            nPeak = db['PeakFrac']['getVal']*db['nSig']['getVal']
            ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nPeak}} : {param}}}".format(param=round(nPeak, 0)) )
            plotCollection.Plotter.canvas.Update(); line.DrawLine(nPeak, 0, nPeak, ROOT.gPad.GetUymax())
            ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
            plotCollection.Plotter.canvas.Print("h_nBkgPeak_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))
            
            # Total yield distributions 
            nTotalHist.Draw()
            nTotalHist.SetFillColor(ROOT.kBlue-10)
            #nTotalHist.SetLineColor(ROOT.kBlue)
            ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[4]{{Mean}}   : {param}}}".format(param=round(nTotalHist.GetMean(), 5)) )
            ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nTotalHist.GetEntries(), 0)) )
            nTotal = db['nBkgComb']['getVal']+db['nSig']['getVal']+nPeak
            ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nTotal}} : {param}}}".format(param=round(nTotal, 0)) )
            plotCollection.Plotter.canvas.Update(); line.DrawLine(nTotal, 0, nTotal, ROOT.gPad.GetUymax())
            ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
            plotCollection.Plotter.canvas.Print("h_nTotal_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))

        db.close()
    if args.process.cfg['args'].forall: GetSummaryGraph(binKeys, RecoResult, GenResult, args, pltName="mixedToy")

if __name__ == '__main__': # Not supported anymore
    wrappedTask = BatchTaskWrapper(
        "myBatchTask",
        modulePath+"/batchTask_mixedToyValidation",
        cfg=setupBatchTask)

    parser = AbsBatchTaskWrapper.BatchTaskParser
    parser.add_argument(
        '-b', '--binKey',
        dest="binKey",
        default="summary",
        help="Select q2 bin with binKey"
    )
    parser.add_argument(
        '-t', '--nToy',
        dest="nSetOfToys",
        type=int,
        default=5,
        help="Number of subsamples to produce"    
    )
    parser.set_defaults(
        wrapper=wrappedTask,
        process=p
    )

    BatchTaskSubparserPostproc = AbsBatchTaskWrapper.BatchTaskSubparsers.add_parser('postproc')
    BatchTaskSubparserPostproc.add_argument(
        '--forceHadd',
        dest='forceHadd',
        action='store_true',
        help="Force recreate summary root file."
    )
    BatchTaskSubparserPostproc.add_argument(
        '--drawGEN',
        dest='drawGEN',
        action='store_false',
        help="Draw a line for GEN level value"
    )
    BatchTaskSubparserPostproc.set_defaults(
        func=func_postproc,
    )

    args = parser.parse_args()
    args.process._sequence[3].cfg['nSetOfToys']=args.nSetOfToys
    #p.cfg['binKey'] = args.binKey
    if args.binKey =="all":
        args.binKey = allBins
        p.cfg['bins'] = args.binKey
    else:
        p.cfg['bins'] = [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
        args.binKey = p.cfg['bins']   
    args.func(args)

    sys.exit()

