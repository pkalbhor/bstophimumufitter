#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 sts=4 fdm=indent fdl=0 fdn=1 ft=python et:

import functools, pdb, time
from array import array

import ROOT

import BsToPhiMuMuFitter.cpp
from v2Fitter.FlowControl.Path import Path
from BsToPhiMuMuFitter.anaSetup import q2bins

from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.varCollection import Bmass, CosThetaK, CosThetaL, Mumumass, Phimass, genCosThetaK, genCosThetaL

#from SingleBuToKstarMuMuFitter.StdProcess import p, setStyle, isPreliminary
from BsToPhiMuMuFitter.StdProcess import p, setStyle

defaultPlotRegion = "Fit"
plotterCfg_styles = {}
plotterCfg_styles['dataStyle'] = (ROOT.RooFit.XErrorSize(0.),)
plotterCfg_styles['mcStyleBase'] = ()
plotterCfg_styles['allStyleBase'] = (ROOT.RooFit.LineColor(1),)
plotterCfg_styles['sigStyleNoFillBase'] = (ROOT.RooFit.LineColor(4),)
plotterCfg_styles['sigStyleBase'] = (ROOT.RooFit.LineColor(4), ROOT.RooFit.FillColor(4), ROOT.RooFit.DrawOption("FL"), ROOT.RooFit.FillStyle(3003), ROOT.RooFit.VLines())
plotterCfg_styles['bkgStyleBase'] = (ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))

plotterCfg_styles['mcStyle'] = plotterCfg_styles['mcStyleBase'] + (ROOT.RooFit.ProjectionRange(defaultPlotRegion), ROOT.RooFit.Range(defaultPlotRegion))
plotterCfg_styles['allStyle'] = plotterCfg_styles['allStyleBase'] + (ROOT.RooFit.ProjectionRange(defaultPlotRegion), ROOT.RooFit.Range(defaultPlotRegion))
plotterCfg_styles['sigStyle'] = plotterCfg_styles['sigStyleBase'] + (ROOT.RooFit.ProjectionRange(defaultPlotRegion), ROOT.RooFit.Range(defaultPlotRegion))
plotterCfg_styles['sigStyleNoFill'] = plotterCfg_styles['sigStyleNoFillBase'] + (ROOT.RooFit.ProjectionRange(defaultPlotRegion), ROOT.RooFit.Range(defaultPlotRegion))
plotterCfg_styles['bkgStyle'] = plotterCfg_styles['bkgStyleBase'] + (ROOT.RooFit.ProjectionRange(defaultPlotRegion), ROOT.RooFit.Range(defaultPlotRegion))
class Plotter(Path):
    """The plotter"""
    setStyle()
    canvas = ROOT.TCanvas()

    def canvasPrint(self, name, withBinLabel=True):
        Plotter.canvas.Update()
        if withBinLabel:
            Plotter.canvas.Print("{0}_{1}.pdf".format(name, q2bins[self.process.cfg['binKey']]['label']))
        else:
            Plotter.canvas.Print("{0}.pdf".format(name))

    latex = ROOT.TLatex()
    latexCMSMark = staticmethod(lambda x=0.19, y=0.89: Plotter.latex.DrawLatexNDC(x, y, "#font[61]{CMS}"))
    latexCMSSim = staticmethod(lambda x=0.19, y=0.89: Plotter.latex.DrawLatexNDC(x, y, "#font[61]{CMS} #font[52]{#scale[0.8]{Simulation}}"))
    latexCMSToy = staticmethod(lambda x=0.19, y=0.89: Plotter.latex.DrawLatexNDC(x, y, "#font[61]{CMS} #font[52]{#scale[0.8]{Post-fit Toy}}"))
    latexCMSMix = staticmethod(lambda x=0.19, y=0.89: Plotter.latex.DrawLatexNDC(x, y, "#font[61]{CMS} #font[52]{#scale[0.8]{Toy + Simu.}}"))
    latexCMSExtra = staticmethod(lambda x=0.19, y=0.85: Plotter.latex.DrawLatexNDC(x, y, "#font[52]{#scale[0.8]{Preliminary}}") if True else None)
    latexLumi = staticmethod(lambda x=0.78, y=0.96: Plotter.latex.DrawLatexNDC(x, y, "#scale[0.8]{35.9 fb^{-1} (13 TeV)}"))

    @staticmethod
    def latexQ2(binKey, x=0.45, y=0.89):
        Plotter.latex.DrawLatexNDC(x, y, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
    @staticmethod
    def DrawParams(self, pdfPlots):
        x=0.45; y=0.84
        args = pdfPlots[0][0].getParameters(ROOT.RooArgSet(Bmass, CosThetaK, CosThetaL)) #N3 Lines by Pritam
        unboundFl=args.find('unboundFl').getVal(); unboundFlError=args.find('unboundFl').getError(); print unboundFlError
        FlError=(unboundFlToFl(unboundFl+unboundFlError)-unboundFlToFl(unboundFl-unboundFlError))/2.
        flDB=unboundFlToFl(args.find('unboundFl').getVal()); print type(flDB)
        
        unboundAfb=args.find('unboundAfb').getVal(); unboundAfbError=args.find('unboundAfb').getError(); print unboundAfbError
        l1=(unboundAfbToAfb((unboundAfb+unboundAfbError), flDB)-unboundAfbToAfb((unboundAfb-unboundAfbError), flDB))/2.
        l2=(unboundAfbToAfb(unboundAfb, (flDB+FlError))-unboundAfbToAfb(unboundAfb, (flDB-FlError)))/2.
        AfbError=math.sqrt((l1*l1)+(l2*l2))                                #Error
        afbDB=unboundAfbToAfb(args.find('unboundAfb').getVal(), flDB) #Value

        Plotter.latex.DrawLatexNDC(x, y, r"#scale[0.8]{{F_{{l}} = {0}\pm {1}}}".format(round(flDB, 5), round(FlError, 5)))
        Plotter.latex.DrawLatexNDC(x, 0.79, r"#scale[0.8]{{A_{{6}}= {0}\pm {1}}}".format(round(afbDB, 5), round(AfbError, 5)))
       
    @staticmethod
    def latexDataMarks(marks=None, extraArgs=None, **kwargs):
        if marks is None:
            marks = []
        if extraArgs is None:
            extraArgs = {}

        if 'sim' in marks:
            Plotter.latexCMSSim()
            Plotter.latexCMSExtra(**extraArgs)
        elif 'toy' in marks:
            Plotter.latexCMSToy()
            Plotter.latexCMSExtra(**extraArgs)
        elif 'mix' in marks:
            Plotter.latexCMSMix()
            Plotter.latexCMSExtra(**extraArgs)
        else:
            Plotter.latexCMSMark()
            Plotter.latexLumi()
            Plotter.latexCMSExtra(**extraArgs)

    Bmass.setRange(Bmass.getMin(defaultPlotRegion), Bmass.getMax(defaultPlotRegion))
    frameB = Bmass.frame(ROOT.RooFit.Range(defaultPlotRegion))
    frameB.SetMinimum(0)
    frameB.SetTitle("")
    frameB_binning_array = array('d', [4.52, 4.60, 4.68] + [4.76 + 0.08*i for i in range(14)] + [5.88, 5.96])
    frameB_binning = ROOT.RooBinning(len(frameB_binning_array)-1, frameB_binning_array)
    frameB_binning_fine_array = array('d', [4.52 + 0.04*i for i in range(38)])
    frameB_binning_fine = ROOT.RooBinning(16, Bmass.getMin(defaultPlotRegion), Bmass.getMax(defaultPlotRegion)) #(len(frameB_binning_fine_array)-1, frameB_binning_fine_array)

    frameK = CosThetaK.frame()
    frameK.SetMinimum(0)
    frameK.SetTitle("")
    frameK_binning_array = array('d', [-1 + 0.125*i for i in range(16+1)])
    frameK_binning = ROOT.RooBinning(len(frameK_binning_array)-1, frameK_binning_array)

    frameL = CosThetaL.frame()
    frameL.SetMinimum(0)
    frameL.SetTitle("")
    frameL_binning_array = array('d', [-1 + 0.125*i for i in range(16+1)])
    frameL_binning = ROOT.RooBinning(len(frameL_binning_array)-1, frameL_binning_array)

    legend = ROOT.TLegend(.72, .72, .92, .92)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)

    @staticmethod
    def DrawWithResidue(frame1):
        Plotter.canvas.cd()
        frame2 = frame1.emptyClone("frame_for_residue")
        hresid = frame1.pullHist(frame1.getObject(0).GetName(), frame1.getObject(1).GetName()) #residHist() #Get Pull
        frame2.addPlotable(hresid, "P")
        res=ROOT.NewResPlot('RooPlot')(frame1, frame2); res.Draw();
        res.fUpperPad.cd()
        return res

    def initPdfPlotCfg(self, p):
        """ [Name, plotOnOpt, argAliasInDB, LegendName] """
        pdfPlotTemplate = ["", plotterCfg_styles['allStyle'], None, None]
        p = p + pdfPlotTemplate[len(p):]
        if isinstance(p[0], str):
            self.logger.logDEBUG("Initialize pdfPlot {0}".format(p[0]))
            p[0] = self.process.sourcemanager.get(p[0])
            if p[0] == None:
                errorMsg = "pdfPlot not found in source manager."
                self.logger.logERROR(errorMsg)
                raise RuntimeError("pdfPlot not found in source manager.")
        args = p[0].getParameters(ROOT.RooArgSet(Bmass, CosThetaK, CosThetaL, Mumumass, Phimass))
        FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args, p[2])
        if self.process.cfg['args'].SimFit: p[1]=(ROOT.RooFit.ProjWData(ROOT.RooArgSet(self.process.sourcemanager.get("SimultaneousFitter.category")), self.process.sourcemanager.get("SimultaneousFitter.dataWithCategories")),)+p[1] 
        return p

    def initDataPlotCfg(self, p):
        """ [Name, plotOnOpt, LegendName] """
        dataPlotTemplate = ["", plotterCfg_styles['dataStyle'], "Data"]
        p = p + dataPlotTemplate[len(p):]
        if isinstance(p[0], str):
            self.logger.logDEBUG("Initialize dataPlot {0}".format(p[0]))
            plt = self.process.sourcemanager.get(p[0])
            if plt == None:
                errorMsg = "dataPlot {0} not found in source manager.".format(p[0])
                self.logger.logERROR(errorMsg)
                raise RuntimeError(errorMsg)
            else:
                p[0] = plt
        return p

    @staticmethod
    def plotFrame(frame, binning, dataPlots=None, pdfPlots=None, marks=None, legend=False, scaleYaxis=1.4):
        """
            Use initXXXPlotCfg to ensure elements in xxxPlots fit the format
        """
        # Major plot
        cloned_frame = frame.emptyClone("cloned_frame") # No need to call RefreshNorm
        if frame is Plotter.frameB:
            cloned_frame.SetNdivisions(510, "X")
            cloned_frame.SetYTitle("Events / {0} GeV".format(binning.averageBinWidth()))
        elif frame is Plotter.frameL:
            cloned_frame.SetYTitle("Events / {0}".format(binning.averageBinWidth()))
        elif frame is Plotter.frameK:
            cloned_frame.SetYTitle("Events / {0}".format(binning.averageBinWidth()))
        marks = {} if marks is None else marks
        dataPlots = [] if dataPlots is None else dataPlots
        pdfPlots = [] if pdfPlots is None else pdfPlots
        for pIdx, p in enumerate(dataPlots):
            p[0].plotOn(cloned_frame,
                        ROOT.RooFit.Name("dataP{0}".format(pIdx)),
                        ROOT.RooFit.Binning(binning),
                        *p[1])
        for pIdx, p in enumerate(pdfPlots):
            pdb.set_trace()
            time.sleep(5) # somehow object loading need some time, 
            p[0].plotOn(cloned_frame,
                        ROOT.RooFit.Name("pdfP{0}".format(pIdx)),
                        *p[1])
        p0 = cloned_frame.findObject("pdfP0" if pdfPlots else "dataP0").GetHistogram()
        #cloned_frame.SetMaximum(scaleYaxis * p0.GetMaximum())
        cloned_frame.SetMaximum(scaleYaxis * cloned_frame.GetMaximum())
        #cloned_frame.Draw()
        Plotter.DrawWithResidue(cloned_frame)
        
        # Legend
        if legend:
            if isinstance(legend, bool):
                legendInstance = Plotter.legend
            else:
                legendInstance = legend
            legendInstance.Clear()
            for pIdx, p in enumerate(dataPlots):
                if p[2] is not None:
                    legendInstance.AddEntry("dataP{0}".format(pIdx), p[2], "LPFE")
            for pIdx, p in enumerate(pdfPlots):
                if p[3] is not None:
                    legendInstance.AddEntry("pdfP{0}".format(pIdx), p[3], "LF")
            legendInstance.Draw()
        Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(dataPlots[0][0].sumEntries()) )
        # Some marks
        Plotter.latexDataMarks(**marks)

    plotFrameB = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameB, 'binning': frameB_binning}))
    plotFrameK = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameK, 'binning': frameK_binning}))
    plotFrameL = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameL, 'binning': frameL_binning}))
    plotFrameB_fine = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameB, 'binning': frameB_binning_fine}))
    plotFrameK_fine = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameK, 'binning': frameK_binning}))
    plotFrameL_fine = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameL, 'binning': frameL_binning}))

    @classmethod
    def templateConfig(cls):
        cfg = Path.templateConfig()
        cfg.update({
            'db': "fitResults.db",
            'plotFuncs': [],  # (function, kwargs)
        })
        return cfg

    def _runPath(self):
        """"""
        for pltName, pCfg in self.cfg['plots'].items():
            if pltName not in self.cfg['switchPlots']:
                continue
            for func in pCfg['func']:
                self.logger.logINFO("Plotting {0}".format(pltName))
                func(self, **pCfg['kwargs'])

