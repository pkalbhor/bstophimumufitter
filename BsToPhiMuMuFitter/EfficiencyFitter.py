#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

import os, re, itertools, pdb, ctypes
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from v2Fitter.Fitter.FitterCore import FitterCore

import BsToPhiMuMuFitter.cpp
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from BsToPhiMuMuFitter.StdProcess import setStyle
from BsToPhiMuMuFitter.varCollection import CosThetaL, CosThetaK
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

class EfficiencyFitter(FitterCore):
    """Implementation to standard efficiency fitting procdeure to BuToKstarMuMu angular analysis"""

    @classmethod
    def templateConfig(cls):
        cfg = FitterCore.templateConfig()
        cfg.update({
            'name': "EfficiencyFitter",
            'datahist': "effiHistReader.h2_accXrec",
            'data': "effiHistReader.accXrec",
            'dataX': "effiHistReader.h_accXrec_fine_ProjectionX",
            'dataY': "effiHistReader.h_accXrec_fine_ProjectionY",
            'pdf': "effi_sigA",
            'pdfX': "effi_cosl",
            'pdfY': "effi_cosK",
            'updateArgs': True,
        })
        del cfg['createNLLOpt']
        return cfg

    def _bookMinimizer(self):
        """Pass complicate fitting control."""
        pass

    def _preFitSteps(self):
        """Prefit uncorrelated term"""
        args = self.pdf.getParameters(self.data)
        if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args)
        self.ToggleConstVar(args, isConst=True)
        
        # Disable xTerm correction and fit to 1-D
        args.find('hasXTerm{}'.format(self.cfg['label'])).setVal(0)

        h_accXrec_fine_ProjectionX = self.process.sourcemanager.get(self.cfg['dataX'])
        h_accXrec_fine_ProjectionY = self.process.sourcemanager.get(self.cfg['dataY'])
        effi_cosl = self.process.sourcemanager.get(self.cfg['pdfX'])
        effi_cosK = self.process.sourcemanager.get(self.cfg['pdfY'])
        for proj, pdf, var, argPats in [(h_accXrec_fine_ProjectionX, effi_cosl, CosThetaL, [r"^l\d+\w*"]), (h_accXrec_fine_ProjectionY, effi_cosK, CosThetaK, [r"^k\d+\w*"])]:
            hdata = ROOT.RooDataHist("hdata", "", ROOT.RooArgList(var), ROOT.RooFit.Import(proj))
            self.ToggleConstVar(args, isConst=False, targetArgs=argPats)
            
            theList = ROOT.RooLinkedList()
            Err     = ROOT.RooFit.Minos(True)
            theSave = ROOT.RooFit.Save() #Python discards temporary objects
            Verbose   = ROOT.RooFit.Verbose(0)
            Strategy = ROOT.RooFit.Strategy(2)
            PrintLevel= ROOT.RooFit.PrintLevel(-1)
            theList.Add(theSave);  theList.Add(Verbose); theList.Add(PrintLevel); theList.Add(Err); theList.Add(Strategy)
            Res=pdf.chi2FitTo(hdata, theList)
            Res=pdf.chi2FitTo(hdata, theList)
            Res.Print("v")

            ################## AlTernatively #######################     
            #chi2 = pdf.createChi2(hdata, ROOT.RooFit.Save(1))
            #m=ROOT.RooMinuit(chi2)
            #m.setPrintLevel(3)
            #m.migrad()
            #m.hesse()
            #m.minos()
            #RooRes=m.save()

            self.ToggleConstVar(args, isConst=True, targetArgs=argPats)

        effi_norm='effi_norm{}'.format(self.cfg['label'])
        args.find('hasXTerm{}'.format(self.cfg['label'])).setVal(1)
        args.find(effi_norm).setConstant(False)
        Res2D=self.pdf.chi2FitTo(self.data, ROOT.RooFit.Minos(True), ROOT.RooFit.Save(), ROOT.RooFit.Strategy(2), ROOT.RooFit.PrintLevel(-1))
        Res2D.Print()
        #args.find(effi_norm).setVal(args.find(effi_norm).getVal() / 4.)
        args.find(effi_norm).setConstant(True)

        # Fix uncorrelated term and for later update with xTerms in main fit step
        self.ToggleConstVar(args, isConst=False, targetArgs=[r"^x\d+\w*"])

    def _postFitSteps(self):
        """Post-processing"""
        args = self.pdf.getParameters(self.data)
        self.ToggleConstVar(args, True)
        FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, args)

    def _runFitSteps(self):
        h2_accXrec = self.process.sourcemanager.get(self.cfg['datahist']) 
        args = self.pdf.getParameters(self.data)
        nPar = 0
        floaters = {} #Saving indices for cross terms
        def GetTFunction():
            nonlocal nPar
            args_it = args.createIterator()
            arg = args_it.Next()
            effi_sigA_formula = self.pdf.formula().formulaString()
            paramDict ={}
            for p in range(self.pdf.formula().actualDependents().getSize()):
                paramDict[self.pdf.formula().getParameter(p).GetName()]=p
            effi_sigA_formula = effi_sigA_formula.replace("x[{0}]".format(paramDict['CosThetaL']), "x")
            effi_sigA_formula = effi_sigA_formula.replace("x[{0}]".format(paramDict['CosThetaK']), "y")
            while arg:
                if any(re.match(pat, arg.GetName()) for pat in ["effi_norm", "hasXTerm", r"^l\d+\w*", r"^k\d+\w*"]):
                    effi_sigA_formula = effi_sigA_formula.replace('x[{0}]'.format(paramDict[arg.GetName()]), "({0})".format(arg.getVal()))
                elif re.match(r"^x\d+\w*$", arg.GetName()):
                    effi_sigA_formula = effi_sigA_formula.replace('x[{0}]'.format(paramDict[arg.GetName()]), "[{0}]".format(nPar))
                    floaters[nPar] = arg.GetName()
                    nPar = nPar + 1
                arg = args_it.Next()
            f2_effi_sigA = ROOT.TF2("f2_effi_sigA", effi_sigA_formula, -1, 1, -1, 1)
            return f2_effi_sigA

        if True:  #Using RooMinuit
            if False: #Using NLL optimization
                self.fitter = ROOT.StdFitter()
                minuit=self.fitter.Init(self.pdf, self.data)
                minuit.setStrategy(2)
                minuit.optimizeConst(1)
                minuit.setPrintLevel(0)
                self._nll = self.fitter.GetNLL()
                migrad=self.fitter.FitMigrad()
                self.fitter.FitHesse()
                self.fitter.FitMinos(self.pdf.getParameters(self.data).selectByAttrib("Constant",0))
            else: #Using chi2 optimization
                self.fitter = self.pdf.chi2FitTo(self.data, ROOT.RooFit.Minos(1), ROOT.RooFit.Strategy(2), ROOT.RooFit.Save(1), ROOT.RooFit.PrintLevel(-1))
                self.fitter = self.pdf.chi2FitTo(self.data, ROOT.RooFit.Minos(1), ROOT.RooFit.Strategy(2), ROOT.RooFit.Save(1), ROOT.RooFit.PrintLevel(-1))
            self.fitter.Print("v")

            setStyle()
            canvas = ROOT.TCanvas()
            latex = ROOT.TLatex()
            h2_effi_2D_comp = h2_accXrec.Clone("h2_effi_2D_comp")
            h2_effi_2D_comp.Reset("ICESM")
            pdfhist = h2_accXrec.Clone("pdfhist")
            pdfhist.Reset("ICESM")
            self.pdf.fillHistogram(pdfhist, ROOT.RooArgList(CosThetaL,CosThetaK))

            #Text plot comparison
            canvas2 = ROOT.TCanvas()
            for lBin, KBin in itertools.product(list(range(1, h2_effi_2D_comp.GetNbinsX() + 1)), list(range(1, h2_effi_2D_comp.GetNbinsY() + 1))):
                if h2_accXrec.GetBinContent(lBin, KBin)==0:                                                                                
                    h2_effi_2D_comp.SetBinContent(lBin, KBin, 0)                                                                           
                    print (">> ** Warning ** Empty bins: (l, k)", lBin, KBin)                                                              
                else:                                                                                                                      
                    h2_effi_2D_comp.SetBinContent(lBin, KBin, pdfhist.GetBinContent(lBin, KBin) / h2_accXrec.GetBinContent(lBin, KBin))

            ROOT.gStyle.SetPalette(ROOT.kLightTemperature) #kColorPrintableOnGrey)
            h2_effi_2D_text = h2_effi_2D_comp.Clone("h2_effi_2D_text")#; h2_effi_2D_text.Reset("ICESM")
            h2_effi_2D_text.Draw("COLZ")
            h2_effi_2D_text.GetYaxis().SetTitleOffset(1)
            ROOT.gStyle.SetPaintTextFormat("6.4g")
            pdfhist.SetBarOffset(0.25); pdfhist.Draw("TEXT SAME")
            canvas2.SetRightMargin(0.115)
            canvas2.SetLeftMargin(0.1)
            h2_accXrec.SetBarOffset(0.); h2_accXrec.Draw("TEXT SAME")
            h2_effi_2D_comp.SetBarOffset(-0.25); h2_effi_2D_comp.Draw("TEXT SAME")
            ROOT.TLatex().DrawLatexNDC(0.12, 0.96, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[self.process.cfg['binKey']]['latexLabel']))

            canvas.cd() 
            h2_effi_2D_comp.SetMinimum(0)                
            h2_effi_2D_comp.SetMaximum(1.5)              
            h2_effi_2D_comp.SetTitleOffset(1.6, "X")     
            h2_effi_2D_comp.SetTitleOffset(1.8, "Y")     
            h2_effi_2D_comp.SetTitleOffset(1.5, "Z")     
            h2_effi_2D_comp.SetZTitle("#varepsilon_{fit}/#varepsilon_{measured}")
            h2_effi_2D_comp.Draw("LEGO2")                
            latex.DrawLatexNDC(.08, .93, "#font[61]{CMS} #font[52]{#scale[0.8]{Simulation}}")
            chi2ndf = self.fitter.minNll()/(h2_effi_2D_comp.GetNbinsX()*h2_effi_2D_comp.GetNbinsY()-self.pdf.getParameters(self.data).selectByAttrib("Constant",0).getSize())
            latex.DrawLatexNDC(.08, .89, "#chi^{{2}}/ndf={0:.2f}".format(chi2ndf))
            print("2D Efficiency Chi^2/ndf: ", chi2ndf)
        
        else: #Using TMinuit (This section can be used only if pdf is defined in terms of expression (e.g. RooFormulaVar). Does not work for RooProdPdf or RooProduct)
            f2_effi_sigA = GetTFunction()
            fitter = ROOT.EfficiencyFitter()
            self.minimizer = fitter.Init(nPar, h2_accXrec, f2_effi_sigA)
            self.minimizer.SetPrintLevel(0) #Pritam
            self.minimizer.mnexcm("SET STR",ctypes.c_double(2.),1, ctypes.c_int(0))
            for xIdx in range(nPar):
                self.minimizer.DefineParameter(xIdx, floaters[xIdx], 0., 1E-4, -1E+2, 1E+2)
            MigStatus=self.minimizer.Migrad ()
            MigStatus=self.minimizer.Migrad ()
            MinosStatus=self.minimizer.Command("MINOS")

            # Check if efficiency is positive definite
            f2_max_x, f2_max_y = ctypes.c_double(0.), ctypes.c_double(.0)
            f2_min_x, f2_min_y = ctypes.c_double(0.), ctypes.c_double(.0)
            f2_effi_sigA.GetMaximumXY(f2_max_x, f2_max_y)
            f2_effi_sigA.GetMinimumXY(f2_min_x, f2_min_y)
            print("Sanitary check: Efficiency ranges from {0:.2e} to {1:.2e}".format(f2_effi_sigA.Eval(f2_min_x, f2_min_y), f2_effi_sigA.Eval(f2_max_x, f2_max_y)))
            EfficiencyFitter.isPosiDef(f2_effi_sigA)

            #Update parameter values
            parVal, parErr = ctypes.c_double(.0), ctypes.c_double(.0)
            eplus, eminus, eparab, gcc = ctypes.c_double(0.), ctypes.c_double(0.), ctypes.c_double(.0), ctypes.c_double(0.)
            for xIdx in range(nPar):
                self.minimizer.GetParameter(xIdx, parVal, parErr)
                self.minimizer.mnerrs(xIdx, eplus, eminus, eparab, gcc)
                arg = args.find(floaters[xIdx])
                arg.setVal(parVal.value)
                arg.setError(parErr.value)
                arg.setAsymError(eplus.value, eminus.value)

            # Plot comparison between fitting result to data
            setStyle()
            canvas = ROOT.TCanvas()
            latex = ROOT.TLatex()
            h2_effi_2D_comp = h2_accXrec.Clone("h2_effi_2D_comp")
            h2_effi_2D_comp.Reset("ICESM")
            pdfhist = h2_accXrec.Clone("pdfhist")
            pdfhist.Reset("ICESM")
            self.pdf.fillHistogram(pdfhist, ROOT.RooArgList(CosThetaL,CosThetaK))
            print ("2D Efficiency Chi^2/ndf: ", fitter.GetChi2()/(h2_effi_2D_comp.GetNbinsX()*h2_effi_2D_comp.GetNbinsY()-nPar))
            print ("TMinuit Status: ", self.minimizer.GetStatus(), MigStatus, MinosStatus)

            #Text plot comparison
            canvas2 = ROOT.TCanvas()
            for lBin, KBin in itertools.product(list(range(1, h2_effi_2D_comp.GetNbinsX() + 1)), list(range(1, h2_effi_2D_comp.GetNbinsY() + 1))):
                if h2_accXrec.GetBinContent(lBin, KBin)==0:                                                                                
                    h2_effi_2D_comp.SetBinContent(lBin, KBin, 0)                                                                           
                    print (">> ** Warning ** Empty bins: (l, k)", lBin, KBin)                                                              
                else:                                                                                                                      
                    h2_effi_2D_comp.SetBinContent(lBin, KBin, f2_effi_sigA.Eval(h2_accXrec.GetXaxis().GetBinCenter(lBin), h2_accXrec.GetYaxis().GetBinCenter(KBin)) / h2_accXrec.GetBinContent(lBin, KBin))

            ROOT.gStyle.SetPalette(ROOT.kLightTemperature) #kColorPrintableOnGrey)
            h2_effi_2D_text = h2_effi_2D_comp.Clone("h2_effi_2D_text")#; h2_effi_2D_text.Reset("ICESM")
            h2_effi_2D_text.Draw("COLZ")
            h2_effi_2D_text.GetYaxis().SetTitleOffset(1)
            ROOT.gStyle.SetPaintTextFormat("6.4g")
            pdfhist.SetBarOffset(0.25); pdfhist.Draw("TEXT SAME")
            canvas2.SetRightMargin(0.115)
            canvas2.SetLeftMargin(0.1)
            h2_accXrec.SetBarOffset(0.); h2_accXrec.Draw("TEXT SAME")
            h2_effi_2D_comp.SetBarOffset(-0.25); h2_effi_2D_comp.Draw("TEXT SAME")
            ROOT.TLatex().DrawLatexNDC(0.12, 0.96, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[self.process.cfg['binKey']]['latexLabel']))

            canvas.cd() 
            h2_effi_2D_comp.SetMinimum(0)
            h2_effi_2D_comp.SetMaximum(1.5)
            h2_effi_2D_comp.SetTitleOffset(1.6, "X")
            h2_effi_2D_comp.SetTitleOffset(1.8, "Y")
            h2_effi_2D_comp.SetTitleOffset(1.5, "Z")
            h2_effi_2D_comp.SetZTitle("#varepsilon_{fit}/#varepsilon_{measured}")
            h2_effi_2D_comp.Draw("LEGO2")
            latex.DrawLatexNDC(.08, .93, "#font[61]{CMS} #font[52]{#scale[0.8]{Simulation}}")
            latex.DrawLatexNDC(.08, .89, "#chi^{{2}}/ndf={0:.2f}".format(fitter.GetChi2()/(h2_effi_2D_comp.GetNbinsX()*h2_effi_2D_comp.GetNbinsY()-nPar)))
            FitterCore.ArgLooper(args, lambda p: p.Print())
        
        ####################################
        cwd=os.getcwd()
        path=os.path.join(modulePath, self.process.work_dir, "Efficiency")
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        ####################################
        canvas.Print("effi_2D_comp{}_{}.pdf".format(self.cfg['label'], q2bins[self.process.cfg['binKey']]['label']))
        canvas2.cd(); canvas2.Print("effi_2D_TEXT{}_{}.pdf".format(self.cfg['label'], q2bins[self.process.cfg['binKey']]['label']))
        os.chdir(cwd) 

    @staticmethod
    def isPosiDef(formula2D):
        f2_min_x, f2_min_y = ctypes.c_double(0.), ctypes.c_double(0.)
        formula2D.GetMinimumXY(f2_min_x, f2_min_y)
        f2_min = formula2D.Eval(f2_min_x, f2_min_y)
        if f2_min > 0:
            return True
        else:
            print("WARNING\t: Sanitary check failed: Minimum of efficiency map is {0:.2e} at {1}, {2}".format(f2_min, f2_min_x, f2_min_y))
        return False

