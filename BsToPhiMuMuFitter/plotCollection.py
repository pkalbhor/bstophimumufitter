#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 sts=4 fdm=indent fdl=0 fdn=3 ft=python et:

import os, sys, pdb, copy, re, math, types, functools, shelve 
from array import array
from math import sqrt
import ROOT

import BsToPhiMuMuFitter.cpp
from v2Fitter.FlowControl.Path import Path
from v2Fitter.Fitter.FitterCore import FitterCore
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath, bMassRegions
from BsToPhiMuMuFitter.StdFitter import unboundFlToFl, unboundAfbToAfb, flToUnboundFl, afbToUnboundAfb
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.varCollection import Bmass, CosThetaK, CosThetaL, Mumumass, Phimass, genCosThetaK, genCosThetaL

from BsToPhiMuMuFitter.StdProcess import p, setStyle
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection

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
    def latexQ2(self, x=0.45, y=0.89):
        Plotter.latex.DrawLatexNDC(x, y, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[self.process.cfg['binKey']]['latexLabel']))
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
    def latexDataMarks(marks):
        if 'sim' in marks:
            Plotter.latexCMSSim()
            Plotter.latexCMSExtra()
        elif 'toy' in marks:
            Plotter.latexCMSToy()
            Plotter.latexCMSExtra()
        elif 'mix' in marks:
            Plotter.latexCMSMix()
            Plotter.latexCMSExtra()
        else:
            Plotter.latexCMSMark()
            Plotter.latexLumi()
            Plotter.latexCMSExtra()

    frameB = Bmass.frame(ROOT.RooFit.Range(defaultPlotRegion))
    #frameB.SetMinimum(0)
    frameB_binning = 20

    frameK = CosThetaK.frame()
    #frameK.SetMinimum(0)
    frameK_binning = 20

    frameL = CosThetaL.frame()
    #frameL.SetMinimum(0)
    frameL.SetTitle("")
    frameL_binning = 20

    legend = ROOT.TLegend(.75, .70, .95, .90)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)

    def initPdfPlotCfg(self, p):
        print(""" [Name, plotOnOpt, argAliasInDB, LegendName] """)
        pdfPlotTemplate = ["", plotterCfg_allStyle, None, None]
        p = p + pdfPlotTemplate[len(p):]
        if isinstance(p[0], str):
            self.logger.logDEBUG("Initialize pdfPlot {0}".format(p[0]))
            p[0] = self.process.sourcemanager.get(p[0])
            if p[0] == None:
                self.logger.logERROR("pdfPlot not found in source manager.")
                raise RuntimeError
        args = p[0].getParameters(ROOT.RooArgSet(Bmass, CosThetaK, CosThetaL, Mumumass, Phimass))
        FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args, p[2])
        return p

    def initDataPlotCfg(self, p):
        print(""" [Name, plotOnOpt, LegendName] """)
        dataPlotTemplate = ["", plotterCfg_dataStyle, "Data"]
        p = p + dataPlotTemplate[len(p):]

        if isinstance(p[0], str):
            self.logger.logDEBUG("Initialize dataPlot {0}".format(p[0]))
            p[0] = self.process.sourcemanager.get(p[0])
            if p[0] == None:
                self.logger.logERROR("dataPlot not found in source manager.")
                raise RuntimeError
        return p

    @staticmethod
    def plotFrame(frame, binning, dataPlots=None, pdfPlots=None, marks=None, scaleYaxis=1.8):
        print("""
            Use initXXXPlotCfg to ensure elements in xxxPlots fit the format
        """)
        # Major plot
        cloned_frame = frame.emptyClone("cloned_frame")
        marks = [] if marks is None else marks
        dataPlots = [] if dataPlots is None else dataPlots
        pdfPlots = [] if pdfPlots is None else pdfPlots

        for pIdx, p in enumerate(dataPlots):
            p[0].plotOn(cloned_frame,
                        ROOT.RooFit.Name("dataP{0}".format(pIdx)),
                        ROOT.RooFit.Binning(binning),
                        *p[1])
        for pIdx, p in enumerate(pdfPlots):
            p[0].plotOn(cloned_frame,
                        ROOT.RooFit.Name("pdfP{0}".format(pIdx)),
                        *p[1])
        cloned_frame.SetMaximum(scaleYaxis * cloned_frame.GetMaximum())
        #cloned_frame.Draw() #
        DrawWithResidue(plotter, cloned_frame) 

        # Legend
        Plotter.legend.Clear()
        for pIdx, p in enumerate(dataPlots):
            if p[2] is not None:
                Plotter.legend.AddEntry("dataP{0}".format(pIdx), p[2], "LPFE")
        for pIdx, p in enumerate(pdfPlots):
            if p[3] is not None:
                Plotter.legend.AddEntry("pdfP{0}".format(pIdx), p[3], "LF")
        Plotter.legend.Draw()
        Plotter.latex.DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(dataPlots[0][0].sumEntries()) )
        #Plotter.latex.DrawLatexNDC(.45, .74, r"#scale[0.8]{{#chi^{{2}}/NDF = {0:.2f}}}".format(cloned_frame.chiSquare()/(binning-pdfPlots[0][0].getParameters(dataPlots[0][0]).getSize()))) #pdfPlots[0][0].getParameters(dataPlots[0][0]).getSize()
        # Some marks
        Plotter.latexDataMarks(marks)

    plotFrameB = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameB, 'binning': frameB_binning}))
    plotFrameK = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameK, 'binning': frameK_binning}))
    plotFrameL = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameL, 'binning': frameL_binning}))
    plotFrameB_fine = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameB, 'binning': frameB_binning * 2}))
    plotFrameK_fine = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameK, 'binning': frameK_binning * 2}))
    plotFrameL_fine = staticmethod(functools.partial(plotFrame.__func__, **{'frame': frameL, 'binning': frameL_binning * 2}))

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
                func(self, **pCfg['kwargs'])
                Plotter.canvas.Clear("d")


def plotSpectrumWithSimpleFit(self, pltName, dataPlots, marks):
    """ Assuming len(dataPlots) == 1, fit to the data. """
    for pIdx, plt in enumerate(dataPlots):
        dataPlots[pIdx] = self.initDataPlotCfg(plt)
    wspace = ROOT.RooWorkspace("wspace")
    getattr(wspace, 'import')(Bmass)
    wspace.factory("RooGaussian::gauss1(Bmass,mean[5.28,5.25,5.39],sigma1[0.02,0.01,0.05])")
    wspace.factory("RooGaussian::gauss2(Bmass,mean,sigma2[0.08,0.05,0.40])")
    wspace.factory("SUM::sigM(sigFrac[0.8,0,1]*gauss1,gauss2)")
    wspace.factory("c1[-5.6,-30,30]")
    wspace.factory("EXPR::bkgCombM('exp(c1*Bmass)',{Bmass,c1})")
    wspace.factory("SUM::model(tmp_nSig[1,1e5]*sigM,tmp_nBkg[20,1e5]*bkgCombM)")
    wspace.factory("cbs_mean[5.28, 5.25, 5.39]")
    wspace.factory("RooCBShape::cbs_1(Bmass, cbs_mean, cbs1_sigma[0.8, 0.0001, 0.60], cbs1_alpha[0.8, -6.0, 6.0], cbs1_n[10, 0, 1000])")
    wspace.factory("RooCBShape::cbs_2(Bmass, cbs_mean, cbs2_sigma[0.005, 0.0001, 0.60], cbs2_alpha[-0.8, -2.4, 5.6], cbs2_n[100, 0, 1000])")
    wspace.factory("SUM::f_sigMDCB(sigMDCB_frac[0.8,0, 1]*cbs_1, cbs_2)")
    wspace.factory("SUM::model2(tmp_nSig*f_sigMDCB,tmp_nBkg*bkgCombM)")
    
    #pdb.set_trace()
    
    if False:
        pdfPlots = [
            [wspace.pdf('model'), plotterCfg_allStyle, None, "Total fit"],
            [wspace.pdf('model'), (ROOT.RooFit.Components('sigM'),) + plotterCfg_sigStyle, None, "Signal"],
            [wspace.pdf('model'), (ROOT.RooFit.Components('bkgCombM'),) + plotterCfg_bkgStyle, None, "Background"],
        ]
    else:
         pdfPlots = [
            [wspace.pdf('model2'), plotterCfg_allStyle, None, "Total fit"],
            [wspace.pdf('model2'), (ROOT.RooFit.Components('f_sigMDCB'),) + plotterCfg_sigStyle, None, "Signal"],
            [wspace.pdf('model2'), (ROOT.RooFit.Components('bkgCombM'),) + plotterCfg_bkgStyle, None, "Background"],
        ]
   
    fitter=pdfPlots[0][0].fitTo(dataPlots[0][0], ROOT.RooFit.Range("signal"), ROOT.RooFit.Minos(True), ROOT.RooFit.Extended(True), ROOT.RooFit.PrintLevel(-1), ROOT.RooFit.Save(True))
    fitter.Print("v")
    Plotter.plotFrameB(dataPlots=dataPlots, pdfPlots=pdfPlots, marks=marks)
    self.canvasPrint(pltName)
types.MethodType(plotSpectrumWithSimpleFit, None, Plotter)

def plotSimpleBLK(self, pltName, dataPlots, pdfPlots, marks, frames='BLK'):
    for pIdx, plt in enumerate(dataPlots):
        dataPlots[pIdx] = self.initDataPlotCfg(plt)
    for pIdx, plt in enumerate(pdfPlots):
        pdfPlots[pIdx] = self.initPdfPlotCfg(plt)

    plotFuncs = {
        'B': {'func': Plotter.plotFrameB_fine, 'tag': ""},
        'L': {'func': Plotter.plotFrameL, 'tag': "_cosl"},
        'K': {'func': Plotter.plotFrameK, 'tag': "_cosK"},
    }
    ############################--------TEST---------###########################
    """mmFrame=Mumumass.frame(sqrt(q2bins[self.process.cfg['binKey']]['q2range'][0]), sqrt(q2bins[self.process.cfg['binKey']]['q2range'][1]))
    phiFrame=Phimass.frame(1.01, 1.03)
    dataPlots[0][0].plotOn(mmFrame, ROOT.RooFit.Name("dataMuMuMass"))
    cmm=ROOT.TCanvas("cmm", "cmm"); mmFrame.Draw(); self.latexQ2(); cmm.Print("MuMuMass_{0}.pdf".format(q2bins[self.process.cfg['binKey']]['label']))
    dataPlots[0][0].plotOn(phiFrame, ROOT.RooFit.Name("dataPhiMass"))
    cphi=ROOT.TCanvas("cphi", "cphi"); phiFrame.Draw(); self.latexQ2(); cphi.Print("PhiMass_{0}.pdf".format(q2bins[self.process.cfg['binKey']]['label']))"""
    ############################--------TEST---------###########################
    cwd=os.getcwd()
    for frame in frames:
        plotFuncs[frame]['func'](dataPlots=dataPlots, pdfPlots=pdfPlots, marks=marks)
        self.latexQ2()
        #if not frame =='B': self.DrawParams(pdfPlots)
        ####################################
        if pltName=="angular3D_bkgCombA":
            path=modulePath+"/Plots/SideBandBkg/"
            if not os.path.exists(path):                                                                                                       
                os.mkdir(path)   
            os.chdir(path)
        if pltName=="angular3D_sigM" or pltName=="angular3D_sig2D":
            path=modulePath+"/Plots/SignalFits/"
            if not os.path.exists(path):                                                        
                os.mkdir(path)                                                                 
            os.chdir(path)
        ####################################
        self.canvasPrint(pltName + plotFuncs[frame]['tag'])
        Plotter.canvas.cd()
    os.chdir(cwd)

types.MethodType(plotSimpleBLK, None, Plotter)

def plotSimpleGEN(self, pltName, dataPlots, pdfPlots, marks, frames='LK'): #Pritam
    for pIdx, plt in enumerate(dataPlots):
        dataPlots[pIdx] = self.initDataPlotCfg(plt)
    for pIdx, plt in enumerate(pdfPlots):
        pdfPlots[pIdx] = self.initPdfPlotCfg(plt)
    
    dataPlots[0][0].changeObservableName("genCosThetaK", "CosThetaK")
    dataPlots[0][0].changeObservableName("genCosThetaL", "CosThetaL")
    plotFuncs = {
        'L': {'func': Plotter.plotFrameL, 'tag': "_gencosl"},
        'K': {'func': Plotter.plotFrameK, 'tag': "_gencosK"},
    }

    cwd=os.getcwd()
    for frame in frames:
        plotFuncs[frame]['func'](dataPlots=dataPlots, pdfPlots=pdfPlots, marks=marks)
        self.latexQ2()
        self.DrawParams(pdfPlots)
        ########################################
        if pltName=="angular3D_GEN":
            path=modulePath+"/Plots/SignalFits/"
            if not os.path.exists(path):                                                        
                os.mkdir(path)                                                                 
            os.chdir(path)
        ######################################33
        self.canvasPrint(pltName + plotFuncs[frame]['tag'])
        Plotter.canvas.cd()
    os.chdir(cwd)
types.MethodType(plotSimpleGEN, None, Plotter)

def DrawWithResidue(self, frame1):
    #pdb.set_trace()
    Plotter.canvas.cd()
    frame2 = frame1.emptyClone("frame_for_residue")
    hresid = frame1.pullHist(frame1.getObject(0).GetName(), frame1.getObject(1).GetName()) #residHist() #Get Pull
    frame2.addPlotable(hresid, "P")
    res=ROOT.NewResPlot('RooPlot')(frame1, frame2); res.Draw();
    res.fUpperPad.cd()
    return res
types.MethodType(DrawWithResidue, None, Plotter)

def plotEfficiency(self, data_name, pdf_name):
    pltName = "effi"
    data = self.process.sourcemanager.get(data_name)
    pdf = self.process.sourcemanager.get(pdf_name)
    if data == None or pdf == None:
        self.logger.logWARNING("Skip plotEfficiency. pdf or data not found")
        return
    args = pdf.getParameters(data)
    FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args)

    #####################################
    cwd=os.getcwd()
    path=modulePath+"/Plots/Efficiency/"
    if not os.path.exists(path):
        os.mkdir(path)  
    os.chdir(path)  
    #####################################

    binningL = ROOT.RooBinning(len(dataCollection.accXEffThetaLBins) - 1, dataCollection.accXEffThetaLBins)
    binningK = ROOT.RooBinning(len(dataCollection.accXEffThetaKBins) - 1, dataCollection.accXEffThetaKBins)

    data_accXrec = self.process.sourcemanager.get("effiHistReader.h2_accXrec")
    Plotter.canvas.cd()
    #data_accXrec.Scale(100)
    #data_accXrec.SetMinimum(0)
    #data_accXrec.SetMaximum(100 * 0.00015)  # Z axis in percentage
    data_accXrec.SetTitleOffset(1.6, "X")
    data_accXrec.SetTitleOffset(1.8, "Y")
    data_accXrec.SetTitleOffset(1.8, "Z")
    data_accXrec.SetZTitle("Efficiency [%]")
    data_accXrec.Draw("LEGO2")
    h2_effi_sigA_fine = pdf.createHistogram("h2_effi_sigA_fine", CosThetaL, ROOT.RooFit.Binning(20), ROOT.RooFit.YVar(CosThetaK, ROOT.RooFit.Binning(20)))
    h2_effi_sigA_fine.Scale(100)
    h2_effi_sigA_fine.SetLineColor(2)
    h2_effi_sigA_fine.Draw("SURF SAME dm(1,10) pa(2,1,1) ci(1,4,8) a(0,0,0)")
    Plotter.latexCMSSim(.08, .93)
    Plotter.latexCMSExtra(.08, .89)
    #Plotter.latex.DrawLatexNDC(.85, .89, "#chi^{{2}}={0:.2f}".format(cloned_frameL.chiSquare()))
    self.latexQ2(.40, .93)
    self.canvasPrint(pltName + "_2D")
    data_accXrec.Scale(0.01)
    
    #Cos_L Efficiency
    cloned_frameL = Plotter.frameL.emptyClone("cloned_frameL")
    h_accXrec_fine_ProjectionX = self.process.sourcemanager.get("effiHistReader.h_accXrec_fine_ProjectionX")
    data_accXrec_fine_ProjectionX = ROOT.RooDataHist("data_accXrec_fine_ProjectionX", "", ROOT.RooArgList(CosThetaL), ROOT.RooFit.Import(h_accXrec_fine_ProjectionX))
    data_accXrec_fine_ProjectionX.plotOn(cloned_frameL, ROOT.RooFit.Rescale(100), ROOT.RooFit.MarkerStyle(7))
    pdfL = self.process.sourcemanager.get("effi_cosl")
    pdfL.plotOn(cloned_frameL, ROOT.RooFit.Normalization(100, ROOT.RooAbsReal.Relative), *plotterCfg_sigStyleNoFill) 
    cloned_frameL.GetYaxis().SetTitle("Efficiency [%]")
    cloned_frameL.SetMaximum(1.5 * cloned_frameL.GetMaximum())

    cloned_frameL.Draw() #DrawWithResidue(self, cloned_frameL)
    self.latexQ2()
    Plotter.latex.DrawLatexNDC(.85, .89, "#chi^{{2}}={0:.2f}".format(cloned_frameL.chiSquare()))
    Plotter.latexCMSSim()
    Plotter.latexCMSExtra()
    self.canvasPrint(pltName + "_cosl")
   
    #Cos_K Efficiency 
    Plotter.canvas.cd()
    cloned_frameK = Plotter.frameK.emptyClone("cloned_frameK")
    h_accXrec_fine_ProjectionY = self.process.sourcemanager.get("effiHistReader.h_accXrec_fine_ProjectionY") 
    data_accXrec_fine_ProjectionY = ROOT.RooDataHist("data_accXrec_fine_ProjectionY", "", ROOT.RooArgList(CosThetaK), ROOT.RooFit.Import(h_accXrec_fine_ProjectionY))
    data_accXrec_fine_ProjectionY.plotOn(cloned_frameK, ROOT.RooFit.Rescale(100), ROOT.RooFit.MarkerStyle(7))
    pdfK = self.process.sourcemanager.get("effi_cosK")
    pdfK.plotOn(cloned_frameK, ROOT.RooFit.Normalization(100, ROOT.RooAbsReal.Relative), *plotterCfg_sigStyleNoFill)#, ROOT.RooFit.LineWidth(2))
    cloned_frameK.GetYaxis().SetTitle("Efficiency [%]")
    cloned_frameK.SetMaximum(1.5 * cloned_frameK.GetMaximum())
    #cloned_frameK.SetMaximum(10 + cloned_frameK.GetMaximum())
    #cloned_frameK.SetMinimum(h_accXrec_fine_ProjectionY.GetMinimum()*100-10)

    cloned_frameK.Draw() #DrawWithResidue(self, cloned_frameK)
    self.latexQ2()
    Plotter.latex.DrawLatexNDC(.85, .89, "#chi^{{2}}={0:.2f}".format(cloned_frameK.chiSquare()))
    Plotter.latexCMSSim()
    Plotter.latexCMSExtra()
    self.canvasPrint(pltName + "_cosK")
    Plotter.canvas.cd()
    os.chdir(cwd)

types.MethodType(plotEfficiency, None, Plotter)

def plotPostfitBLK(self, pltName, dataReader, pdfPlots, frames='BLK'):
    """Specification of plotSimpleBLK for post-fit plots"""
    for pIdx, plt in enumerate(pdfPlots):
        pdfPlots[pIdx] = self.initPdfPlotCfg(plt)

    # Calculate normalization and then draw
    args = pdfPlots[0][0].getParameters(ROOT.RooArgSet(Bmass, CosThetaK, CosThetaL))
    nSigDB = args.find('nSig').getVal()
    nSigErrorDB = args.find('nSig').getError()
    nBkgCombDB = args.find('nBkgComb').getVal()
    nBkgCombErrorDB = args.find('nBkgComb').getError()
    if 'L' in frames or 'K' in frames:
        flDB = unboundFlToFl(args.find('unboundFl').getVal())
        afbDB = unboundAfbToAfb(args.find('unboundAfb').getVal(), flDB)
    sigFrac = {}
    bkgCombFrac = {}
    for regionName in ["Fit", "SR", "SB", "LSB", "USB"]:
        dataPlots = [["{0}.{1}".format(dataReader, regionName), plotterCfg_dataStyle, "Data"], ]
        for pIdx, p in enumerate(dataPlots):
            dataPlots[pIdx] = self.initDataPlotCfg(p)

        # Bind the 'Bmass' defined in PDF with 'getObservables' to createIntegral
        obs = pdfPlots[1][0].getObservables(dataPlots[0][0])
        FitterCore.ArgLooper(obs, lambda p: p.setRange(regionName, *bMassRegions[regionName]['range']), ["Bmass"])
        sigFrac[regionName] = pdfPlots[1][0].createIntegral(
            obs,
            ROOT.RooFit.NormSet(obs),
            ROOT.RooFit.Range(regionName)).getVal()

        obs = pdfPlots[2][0].getObservables(dataPlots[0][0])
        FitterCore.ArgLooper(obs, lambda p: p.setRange(regionName, *bMassRegions[regionName]['range']), ["Bmass"])
        bkgCombFrac[regionName] = pdfPlots[2][0].createIntegral(
            obs,
            ROOT.RooFit.NormSet(obs),
            ROOT.RooFit.Range(regionName)).getVal()
        nTotal_local = nSigDB * sigFrac[regionName] + nBkgCombDB * bkgCombFrac[regionName]
        # Correct the shape of f_final
        args.find("nSig").setVal(nSigDB * sigFrac[regionName])
        args.find("nBkgComb").setVal(nBkgCombDB * bkgCombFrac[regionName])

        modified_pdfPlots = [
            [pdfPlots[0][0],
             pdfPlots[0][1] + (ROOT.RooFit.Normalization(nTotal_local, ROOT.RooAbsReal.NumEvent),),
             None,
             "Total fit"],
            [pdfPlots[0][0],
             pdfPlots[1][1] + (ROOT.RooFit.Normalization(nTotal_local, ROOT.RooAbsReal.NumEvent), ROOT.RooFit.Components(pdfPlots[1][0].GetName())),
             None,
             "Sigal"],
            [pdfPlots[0][0],
             pdfPlots[2][1] + (ROOT.RooFit.Normalization(nTotal_local, ROOT.RooAbsReal.NumEvent), ROOT.RooFit.Components(pdfPlots[2][0].GetName())),
             None,
             "Background"],
        ]

        plotFuncs = {
            'B': {'func': Plotter.plotFrameB, 'tag': ""},
            'L': {'func': Plotter.plotFrameL, 'tag': "_cosl"},
            'K': {'func': Plotter.plotFrameK, 'tag': "_cosK"},
        }

        drawLatexFitResults = True
        cwd=os.getcwd()
        for frame in frames:
            plotFuncs[frame]['func'](dataPlots=dataPlots, pdfPlots=modified_pdfPlots)
            if drawLatexFitResults:
                if frame == 'B':
                    Plotter.latex.DrawLatexNDC(.19, .77, "Y_{Signal}")
                    Plotter.latex.DrawLatexNDC(.35, .77, "= {0:.2f}".format(nSigDB * sigFrac[regionName]))
                    Plotter.latex.DrawLatexNDC(.50, .77, "#pm {0:.2f}".format(nSigErrorDB * sigFrac[regionName]))
                    Plotter.latex.DrawLatexNDC(.19, .70, "Y_{Background}")
                    Plotter.latex.DrawLatexNDC(.35, .70, "= {0:.2f}".format(nBkgCombDB * bkgCombFrac[regionName]))
                    Plotter.latex.DrawLatexNDC(.50, .70, "#pm {0:.2f}".format(nBkgCombErrorDB * bkgCombFrac[regionName]))
                elif frame == 'L':
                    Plotter.latex.DrawLatexNDC(.19, .77, "A_{{FB}} = {0:.2f}".format(afbDB))
                elif frame == 'K':
                    Plotter.latex.DrawLatexNDC(.19, .77, "F_{{L}} = {0:.2f}".format(flDB))
            self.latexQ2()
            
            ##################################
            path=modulePath+"/Plots/FinalFit/" 
            if not os.path.exists(path):
                os.mkdir(path)
            os.chdir(path)
            ##################################
            self.canvasPrint(pltName + '_' + regionName + plotFuncs[frame]['tag'])
        os.chdir(cwd)
types.MethodType(plotPostfitBLK, None, Plotter)

def plotSummaryAfbFl(self, pltName, dbSetup, drawSM=False, marks=None):
    print(""" Check carefully the keys in 'dbSetup' """)
    if marks is None:
        marks = []
    print self.process.cfg['binKey']
    binKeys = ['belowJpsiA', 'belowJpsiB', 'belowJpsiC', 'betweenPeaks', 'abovePsi2sA', 'abovePsi2sB'] #, 'summaryLowQ2']

    xx = array('d', [sum(q2bins[binKey]['q2range']) / 2 for binKey in binKeys])
    xxErr = array('d', map(lambda t: (t[1] - t[0]) / 2, [q2bins[binKey]['q2range'] for binKey in binKeys]))

    grFls = []
    grAfbs = []

    def quadSum(lst):
        return math.sqrt(sum(map(lambda i: i**2, lst)))

    def calcSystError(db):
        """ FlErrHi, FlErrLo, AfbErrHi, AfbErrLo"""
        flSystErrorHi = []
        flSystErrorLo = []
        afbSystErrorHi = []
        afbSystErrorLo = []
        systErrorSourceBlackList = ["^syst_altFitRange_.*$"]
        for key, val in db.items():
            if re.match("^syst_.*_afb$", key) and not any([re.match(pat, key) for pat in systErrorSourceBlackList]):
                afbSystErrorHi.append(db[key]['getErrorHi'])
                afbSystErrorLo.append(db[key]['getErrorLo'])
            if re.match("^syst_.*_fl$", key) and not any([re.match(pat, key) for pat in systErrorSourceBlackList]):
                flSystErrorHi.append(db[key]['getErrorHi'])
                flSystErrorLo.append(db[key]['getErrorLo'])
        return quadSum(flSystErrorHi), quadSum(flSystErrorLo), quadSum(afbSystErrorHi), quadSum(afbSystErrorLo)

    def getStatError_FeldmanCousins(db):
        """ FlErrHi, FlErrLo, AfbErrHi, AfbErrLo"""
        return db['stat_FC_fl']['getErrorHi'], -db['stat_FC_fl']['getErrorLo'], db['stat_FC_afb']['getErrorHi'], -db['stat_FC_afb']['getErrorLo']

    # TODO: Fix the case of one-side-fail, exceed physically allowed region, etc..
    def getStatError_Minuit(db):
        """ FlErrHi, FlErrLo, AfbErrHi, AfbErrLo"""
        unboundFl = db[argAliasInDB.get("unboundFl", "unboundFl")]
        unboundAfb = db[argAliasInDB.get("unboundAfb", "unboundAfb")]

        fl = unboundFlToFl(unboundFl['getVal'])
        afb = unboundAfbToAfb(unboundAfb['getVal'], fl)

        yyFlErrHi = unboundFlToFl(unboundFl['getVal'] + unboundFl['getErrorHi']) - fl
        yyFlErrLo = fl - unboundFlToFl(unboundFl['getVal'] + unboundFl['getErrorLo'])
        yyAfbErrHi = unboundAfbToAfb(unboundAfb['getVal'] + unboundAfb['getErrorHi'], fl) - afb
        yyAfbErrLo = afb - unboundAfbToAfb(unboundAfb['getVal'] + unboundAfb['getErrorLo'], fl)
        return yyFlErrHi, yyFlErrLo, yyAfbErrHi, yyAfbErrLo

    statErrorMethods = {
        'FeldmanCousins': getStatError_FeldmanCousins,
        'Minuit': getStatError_Minuit,
    }
    Plotter.legend.Clear()
    for dbsIdx, dbs in enumerate(dbSetup):
        title = dbs.get('title', None)
        dbPat = dbs.get('dbPat', self.process.dbplayer.absInputDir + "/fitResults_{binLabel}.db")
        argAliasInDB = dbs.get('argAliasInDB', {})
        withSystError = dbs.get('withSystError', False)
        statErrorKey = dbs.get('statErrorKey', 'Minuit')
        drawOpt = dbs.get('drawOpt', ["PO"])
        fillColor = dbs.get('fillColor', 2)
        fillStyle = dbs.get('fillStyle', 3001)
        legendOpt = dbs.get('legendOpt', None)
        dbs.update({
            'drawOpt': drawOpt,
            'legendOpt': legendOpt,
        })

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
        for binKeyIdx, binKey in enumerate(binKeys):
            if not os.path.exists(dbPat.format(binLabel=q2bins[binKey]['label'])):
                self.logger.logERROR("Input db file {0} NOT found. Skip.".format(dbPat.format(binLabel=q2bins[binKey]['label'])))
                continue
            try:
                db = shelve.open(dbPat.format(binLabel=q2bins[binKey]['label']))
                unboundFl = db[argAliasInDB.get("unboundFl", "unboundFl")]
                unboundAfb = db[argAliasInDB.get("unboundAfb", "unboundAfb")]

                fl = unboundFlToFl(unboundFl['getVal'])
                afb = unboundAfbToAfb(unboundAfb['getVal'], fl)

                yyFl[binKeyIdx] = fl
                yyAfb[binKeyIdx] = afb
                yyFlStatErrHi[binKeyIdx], yyFlStatErrLo[binKeyIdx],\
                    yyAfbStatErrHi[binKeyIdx], yyAfbStatErrLo[binKeyIdx] = statErrorMethods.get(statErrorKey, getStatError_Minuit)(db)
                if withSystError:
                    yyFlSystErrHi[binKeyIdx], yyFlSystErrLo[binKeyIdx],\
                        yyAfbSystErrHi[binKeyIdx], yyAfbSystErrLo[binKeyIdx] = calcSystError(db)
                else:
                    yyFlSystErrHi[binKeyIdx], yyFlSystErrLo[binKeyIdx],\
                        yyAfbSystErrHi[binKeyIdx], yyAfbSystErrLo[binKeyIdx] = 0, 0, 0, 0
                yyFlErrHi[binKeyIdx] = min(quadSum([yyFlStatErrHi[binKeyIdx], yyFlSystErrHi[binKeyIdx]]), 1. - yyFl[binKeyIdx])
                yyFlErrLo[binKeyIdx] = min(quadSum([yyFlStatErrLo[binKeyIdx], yyFlSystErrLo[binKeyIdx]]), yyFl[binKeyIdx])
                yyAfbErrHi[binKeyIdx] = min(quadSum([yyAfbStatErrHi[binKeyIdx], yyAfbSystErrHi[binKeyIdx]]), 0.75 - yyAfb[binKeyIdx])
                yyAfbErrLo[binKeyIdx] = min(quadSum([yyAfbStatErrLo[binKeyIdx], yyAfbSystErrLo[binKeyIdx]]), 0.75 + yyAfb[binKeyIdx])
            finally:
                db.close()

        grAfb = ROOT.TGraphAsymmErrors(len(binKeys), xx, yyAfb, xxErr, xxErr, yyAfbErrLo, yyAfbErrHi)
        grAfb.SetMarkerColor(fillColor if fillColor else 2)
        grAfb.SetLineColor(fillColor if fillColor else 2)
        grAfb.SetFillColor(fillColor if fillColor else 2)
        grAfb.SetFillStyle(fillStyle if fillStyle else 3001)
        grAfbs.append(grAfb)

        grFl = ROOT.TGraphAsymmErrors(len(binKeys), xx, yyFl, xxErr, xxErr, yyFlErrLo, yyFlErrHi)
        grFl.SetMarkerColor(fillColor if fillColor else 2)
        grFl.SetLineColor(fillColor if fillColor else 2)
        grFl.SetFillColor(fillColor if fillColor else 2)
        grFl.SetFillStyle(fillStyle if fillStyle else 3001)
        grFls.append(grFl)
        
        if legendOpt:
            Plotter.legend.AddEntry(grAfb, title, legendOpt)

    if drawSM:
        dbSetup.insert(0, {
            'drawOpt': ["2", "P0Z"],
        })
        yyFl = array('d', [0] * len(binKeys))
        yyFlErrHi = array('d', [0] * len(binKeys))
        yyFlErrLo = array('d', [0] * len(binKeys))

        yyAfb = array('d', [0] * len(binKeys))
        yyAfbErrHi = array('d', [0] * len(binKeys))
        yyAfbErrLo = array('d', [0] * len(binKeys))

        for binKeyIdx, binKey in enumerate(['belowJpsiA','belowJpsiB', 'belowJpsiC', 'betweenPeaks', 'abovePsi2sA','abovePsi2sB', 'summaryLowQ2']):
            if binKey != 'betweenPeaks':
                fl = q2bins[binKey]['sm']['fl']
                afb = q2bins[binKey]['sm']['afb']
                yyFl[binKeyIdx] = fl['getVal']
                yyAfb[binKeyIdx] = afb['getVal']
                yyFlErrHi[binKeyIdx] = fl['getError']
                yyFlErrLo[binKeyIdx] = fl['getError']
                yyAfbErrHi[binKeyIdx] = afb['getError']
                yyAfbErrLo[binKeyIdx] = afb['getError']
            else:
                yyFl[binKeyIdx] = -1
                yyAfb[binKeyIdx] = -1
                yyFlErrHi[binKeyIdx] = 0
                yyFlErrLo[binKeyIdx] = 0
                yyAfbErrHi[binKeyIdx] = 0
                yyAfbErrLo[binKeyIdx] = 0

        grAfb = ROOT.TGraphAsymmErrors(len(binKeys), xx, yyAfb, xxErr, xxErr, yyAfbErrLo, yyAfbErrHi)
        grAfb.SetMarkerColor(4)
        grAfb.SetLineColor(4)
        grAfb.SetFillColor(4)
        grAfb.SetFillStyle(3001)
        grAfbs.insert(0, grAfb)

        grFl = ROOT.TGraphAsymmErrors(len(binKeys), xx, yyFl, xxErr, xxErr, yyFlErrLo, yyFlErrHi)
        grFl.SetMarkerColor(4)
        grFl.SetLineColor(4)
        grFl.SetFillColor(4)
        grFl.SetFillStyle(3001)
        grFls.insert(0, grFl)
        Plotter.legend.AddEntry(grAfb, "SM", "LPF")

    for grIdx, gr in enumerate(grAfbs):
        gr.SetTitle("")
        gr.GetXaxis().SetTitle("q^{2} [GeV^{2}]")
        gr.GetYaxis().SetTitle("A_{6}")
        gr.GetYaxis().SetRangeUser(-.05, .05) #+-0.02
        gr.SetLineWidth(2)
        drawOpt = dbSetup[grIdx]['drawOpt'] if isinstance(dbSetup[grIdx]['drawOpt'], list) else [dbSetup[grIdx]['drawOpt']]
        for optIdx, opt in enumerate(drawOpt):
            if grIdx == 0:
                gr.Draw("A" + opt if optIdx == 0 else opt)
            else:
                gr.Draw(opt + " SAME")
    Plotter.legend.Draw()
    Plotter.latexDataMarks(marks)
    self.canvasPrint(pltName + '_afb', False)

    for grIdx, gr in enumerate(grFls):
        gr.SetTitle("")
        gr.GetXaxis().SetTitle("q^{2} [GeV^{2}]")
        gr.GetYaxis().SetTitle("F_{L}")
        gr.GetYaxis().SetRangeUser(0.3, 0.90)
        gr.SetLineWidth(2)
        drawOpt = dbSetup[grIdx]['drawOpt'] if isinstance(dbSetup[grIdx]['drawOpt'], list) else [dbSetup[grIdx]['drawOpt']]
        for optIdx, opt in enumerate(drawOpt):
            if grIdx == 0:
                gr.Draw("A" + opt if optIdx == 0 else opt)
            else:
                gr.Draw(opt + " SAME")
    Plotter.legend.Draw()
    Plotter.latexDataMarks(marks)
    self.canvasPrint(pltName + '_fl', False)
types.MethodType(plotSummaryAfbFl, None, Plotter)

plotterCfg = {
    'name': "plotter",
    'switchPlots': [],
}
plotterCfg_dataStyle = ()
plotterCfg_mcStyle = ()
plotterCfg_allStyle = (ROOT.RooFit.LineColor(1),)
plotterCfg_sigStyleNoFill = (ROOT.RooFit.LineColor(4), ROOT.RooFit.LineWidth(2))
#plotterCfg_sigStyle = (ROOT.RooFit.LineColor(4), ROOT.RooFit.DrawOption("FL"), ROOT.RooFit.FillColor(4), ROOT.RooFit.FillStyle(3001), ROOT.RooFit.VLines()); 
plotterCfg_sigStyle = (ROOT.RooFit.LineColor(4), ROOT.RooFit.DrawOption("L"), ROOT.RooFit.VLines())
plotterCfg_bkgStyle = (ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(9))
plotterCfg['plots'] = {
    'simpleSpectrum': {
        'func': [plotSpectrumWithSimpleFit],
        'kwargs': {
            'pltName': "h_Bmass",
            'dataPlots': [["dataReader.Fit", plotterCfg_dataStyle, None], ],
            'marks': []}
    },
    'effi': {
        'func': [plotEfficiency],
        'kwargs': {
            'data_name': "effiHistReader.accXrec",
            'pdf_name': "effi_sigA"}
    },
    'angular3D_sigM': {
        'func': [functools.partial(plotSimpleBLK, frames='B')],
        'kwargs': {
            'pltName': "angular3D_sigM",
            'dataPlots': [["sigMCReader.Fit", plotterCfg_styles['mcStyle'], "Simulation"], ],
            'pdfPlots': [["f_sigM", plotterCfg_styles['sigStyle'], fitCollection.setupSigMFitter['argAliasInDB'], "Total fit"],
                        ],
            'marks': ['sim']}
    },
    'angular3D_sigMDCB': {
        'func': [functools.partial(plotSimpleBLK, frames='B')],
        'kwargs': {
            'pltName': "angular3D_sigMDCB",
            'dataPlots': [["sigMCReader.Fit", plotterCfg_mcStyle, "Simulation"], ],
            'pdfPlots': [["f_sigMDCB", plotterCfg_sigStyle, fitCollection.setupSigMDCBFitter['argAliasInDB'], "Total fit"],
                        ],
            'marks': ['sim']}
    },
   'angular3D_sig2D': {
        'func': [functools.partial(plotSimpleBLK, frames='LK')],
        'kwargs': {
            'pltName': "angular3D_sig2D",
            'dataPlots': [["sigMCReader.Fit", plotterCfg_mcStyle, "Simulation"], ],
            'pdfPlots': [["f_sig2D", plotterCfg_sigStyle, fitCollection.setupSig2DFitter['argAliasInDB'], None],
                        ],
            'marks': []}
    },
    'angular3D_GEN': { #Pritam
        'func': [functools.partial(plotSimpleGEN, frames='LK')],  #plotSimpleGEN #plotSimpleBLK
        'kwargs': {
            'pltName': "angular3D_GEN",
            'dataPlots': [["sigMCGENReader.Fit", plotterCfg_mcStyle, "Simulation"], ],
            'pdfPlots': [["f_sigA", plotterCfg_sigStyle, fitCollection.setupSigGENFitter['argAliasInDB'], None],
                        ],
            'marks': []}
    },
    'angular3D_bkgCombA': {
        'func': [functools.partial(plotSimpleBLK, frames='LK')],
        'kwargs': {
            'pltName': "angular3D_bkgCombA",
            'dataPlots': [["dataReader.SB", plotterCfg_dataStyle, "Data"], ],
            'pdfPlots': [["f_bkgCombA", plotterCfg_bkgStyle, None, "Analytic Bkg."],
                         #["f_bkgCombAltA", (ROOT.RooFit.LineColor(4), ROOT.RooFit.LineStyle(9)), None, "Smooth Bkg."],
                        ],
            'marks': []}
    }, #ROOT.RooFit.Range(bMassRegions['Fit']['range'][0], bMassRegions['Fit']['range'][1])
    'simpleBLK': {  # Most general case, to be customized by user
        'func': [functools.partial(plotSimpleBLK, frames='BLK')],
        'kwargs': {
            'pltName': "simpleBLK",
            'dataPlots': [["ToyGenerator.mixedToy", plotterCfg_mcStyle, "Toy"], ],
            'pdfPlots': [["f_sigM", plotterCfg_sigStyle, None, None],
                        ],
            'marks': ['sim']}
    },
    'angular3D_final': {
        'func': [plotPostfitBLK],
        'kwargs': {
            'pltName': "angular3D_final",
            'dataReader': "dataReader",
            'pdfPlots': [["f_final", plotterCfg_allStyle, None, "Total fit"],
                         ["f_sig3D", plotterCfg_sigStyle, None, "Sigal"],
                         ["f_bkgComb", plotterCfg_bkgStyle, None, "Background"],
                        ],
        }
    },

    'angular3D_final_AltM': {  
        'func': [plotPostfitBLK],
        'kwargs': {
            'pltName': "angular3D_final_AltM",
            'dataReader': "dataReader",
            'pdfPlots': [["f_final_AltM", plotterCfg_allStyle, None, "Total fit"],
                         ["f_sig3DAltM", plotterCfg_sigStyle, None, "Sigal"],
                         ["f_bkgComb", plotterCfg_bkgStyle, None, "Background"],
                        ],
        }
    },

    'angular3D_final_AltBkgCombA': {
        'func': [plotPostfitBLK],
        'kwargs': {
            'pltName': "angular3D_finalAlt",
            'dataReader': "dataReader",
            'pdfPlots': [["f_finalAltBkgCombA", plotterCfg_allStyle, None, "Total Alt Fit"],
                         ["f_sig3D", plotterCfg_sigStyle, None, "Sigal"],
                         ["f_bkgCombAAltA", plotterCfg_bkgStyle, None, "Alt Background"],
                        ],
        }
    },

   'angular3D_finalAltSigMAltBkgCombA': {
        'func': [plotPostfitBLK],
        'kwargs': {
            'pltName': "angular3D_finalAltSigMAltBkgCombA",
            'dataReader': "dataReader",
            'pdfPlots': [["f_finalAltMAltBkgCombA", plotterCfg_allStyle, None, "Total Alt Fit"],
                         ["f_sig3DAltM", plotterCfg_sigStyle, dict(fitCollection.setupSigMDCBFitter['argAliasInDB'].items() + fitCollection.setupSigAFitter['argAliasInDB'].items()), "Alt Sigal"],
                         ["f_bkgCombAAltA", plotterCfg_bkgStyle, None, "Alt Background"],
                        ],
        }
    },

   'angular3D_final_AltMMA': {
        'func': [plotPostfitBLK],
        'kwargs': {
            'pltName': "angular3D_final_AltMMA",
            'dataReader': "dataReader",
            'pdfPlots': [["f_finalAltM_AltBkgCombM_AltBkgCombA", plotterCfg_allStyle, None, "Total Alt Fit"],
                         ["f_sig3DAltM", plotterCfg_sigStyle, dict(fitCollection.setupSigMDCBFitter['argAliasInDB'].items() + fitCollection.setupSigAFitter['argAliasInDB'].items()), "Alt Sigal"],
                         ["f_bkgCombAltM_AltA", plotterCfg_bkgStyle, None, "Alt Background"],
                        ],
        }
    },

   'angular3D_finalM': {       # 1D BMass Final Fit: nSig(sigM)+nBkg(fBkgM)
        'func': [functools.partial(plotPostfitBLK, frames='B')],
        'kwargs': {
            'pltName': "angular3D_finalM",
            'dataReader': "dataReader",
            'pdfPlots': [["f_finalM", plotterCfg_allStyle, dict(fitCollection.setupSigMFitter['argAliasInDB'].items()), "Total Alt Fit"],
                         ["f_sigM", plotterCfg_sigStyle, dict(fitCollection.setupSigMFitter['argAliasInDB'].items()), "Alt Sigal"],
                         ["f_bkgCombM", plotterCfg_bkgStyle, None, "Alt Background"],
                        ],
        }
    },

   'angular3D_finalMDCB': {       # 1D BMass Final Fit: nSig(sigMDCB)+nBkg(fBkgM)
        'func': [functools.partial(plotPostfitBLK, frames='B')],
        'kwargs': {
            'pltName': "angular3D_finalMDCB",
            'dataReader': "dataReader",
            'pdfPlots': [["f_finalMDCB", (ROOT.RooFit.Range(*bMassRegions['Fit']['range']),)+plotterCfg_allStyle, None, "Total Alt Fit"],
                         ["f_sigMDCB", (ROOT.RooFit.Range(*bMassRegions['Fit']['range']),)+plotterCfg_sigStyle, dict(fitCollection.setupSigMDCBFitter['argAliasInDB'].items()), "Alt Sigal"],
                         ["f_bkgCombM", plotterCfg_bkgStyle, None, "Alt Background"],
                        ],
        }
    },

   'angular3D_final_AltMM': {       # 1D BMass Final Fit
        'func': [functools.partial(plotPostfitBLK, frames='B')],
        'kwargs': {
            'pltName': "angular3D_final_AltMM",
            'dataReader': "dataReader",
            'pdfPlots': [["f_finalMDCB_AltBkgCombM", plotterCfg_allStyle, None, "Total Alt Fit"],
                         ["f_sigMDCB", plotterCfg_sigStyle, dict(fitCollection.setupSigMDCBFitter['argAliasInDB'].items()), "Alt Sigal"],
                         ["f_bkgCombMAltM", plotterCfg_bkgStyle, None, "Alt Background"],
                        ],
        }
    },

    'angular3D_summary': {
        'func': [plotSummaryAfbFl],
        'kwargs': {
            'pltName': "angular3D_summary",
            'dbSetup': [{'title': "Data",
                         'statErrorKey': 'FeldmanCousins',
                         'legendOpt': "LPE",
                         'fillColor': 1,
                         },
                        {'title': "Data",
                         'statErrorKey': 'FeldmanCousins',
                         'fillColor': 1,
                         'withSystError': True,
                         },
                        ],
            'drawSM': True,
        },
    },
    'angular2D_summary_RECO2GEN': {
        'func': [plotSummaryAfbFl],
        'kwargs': {
            'pltName': "angular2D_summary_RECO2GEN",
            'dbSetup': [{'title': "RECO",
                         'argAliasInDB': {'unboundFl': 'unboundFl_RECO', 'unboundAfb': 'unboundAfb_RECO'},
                         'legendOpt': "LPE",
                         },
                        {'title': "GEN",
                         'argAliasInDB': {'unboundFl': 'unboundFl_GEN', 'unboundAfb': 'unboundAfb_GEN'},
                         'fillColor': 4,
                         'legendOpt': "LPE",
                         },
                        ],
            'marks': ['sim'],
        },
    },
}
plotter = Plotter(plotterCfg)
myplotterCfg=copy.deepcopy(plotterCfg); myplotterCfg['switchPlots'].append('angular2D_summary_RECO2GEN')
myplotter = Plotter(myplotterCfg)
BkgShapeCfg=copy.deepcopy(plotterCfg); BkgShapeCfg['switchPlots'].append('angular3D_bkgCombA')
Bkgplotter = Plotter(BkgShapeCfg)
if __name__ == '__main__':
    binKey =  [key for key in q2bins.keys() if q2bins[key]['label']==sys.argv[1]]
    for b in binKey:
        p.cfg['binKey'] = b
        plotter.cfg['switchPlots'].append('simpleSpectrum')                # Bmass 1D Fit
        #plotter.cfg['switchPlots'].append('effi')                          # Efficiency
        #plotter.cfg['switchPlots'].append('angular3D_sigM')
        #plotter.cfg['switchPlots'].append('angular3D_sigMDCB')             #Plot for Signal Mass with DCB
        #plotter.cfg['switchPlots'].append('angular3D_bkgCombA')
        #plotter.cfg['switchPlots'].append('angular3D_final')
        #plotter.cfg['switchPlots'].append('angular3D_finalAlt')            #SmoothBkg Final Fit
        #plotter.cfg['switchPlots'].append('angular3D_finalAltSigMAltBkgCombA') #SmoothBkg & DCB Signal Mass Final Fit
        #plotter.cfg['switchPlots'].append('angular3D_final_AltMM')         #AltBkgM + AltMDCB: Final 1D BMass Fit
        #plotter.cfg['switchPlots'].append('angular3D_final_AltMMA')        #AltBkgM + SmoothBkgA + AltMDCB: Final 3D Fit
        #plotter.cfg['switchPlots'].append('angular3D_summary')
        #plotter.cfg['switchPlots'].append('angular3D_sig2D')               #To Produce RECO Level Plots
        #plotter.cfg['switchPlots'].append('angular3D_GEN')                 #To Produce Gen Level Plots
        #plotter.cfg['switchPlots'].append('angular2D_summary_RECO2GEN')    #Summary of Fl and Afb
        #plotter.cfg['switchPlots'].append('angular2D_RECO_values')         #Summary of Fl and Afb
        dataCollection.effiHistReader=dataCollection.effiHistReaderOneStep
        p.setSequence([dataCollection.effiHistReader, dataCollection.sigMCReader, dataCollection.sigMCGENReader, dataCollection.dataReader, pdfCollection.stdWspaceReader, plotter])
        p.beginSeq()
        p.runSeq()
        p.endSeq()
