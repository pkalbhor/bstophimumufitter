#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

import os, re, itertools, pdb
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
        print("""Prefit uncorrelated term""")
        args = self.pdf.getParameters(self.data)
        if not self.process.cfg['args'].NoImport: FitDBPlayer.initFromDB(self.process.dbplayer.odbfile, args)
        self.ToggleConstVar(args, isConst=True)
        
        # Disable xTerm correction and fit to 1-D
        args.find('hasXTerm').setVal(0)

        h_accXrec_fine_ProjectionX = self.process.sourcemanager.get(self.cfg['dataX'])
        h_accXrec_fine_ProjectionY = self.process.sourcemanager.get(self.cfg['dataY'])
        effi_cosl = self.process.sourcemanager.get(self.cfg['pdfX'])
        effi_cosK = self.process.sourcemanager.get(self.cfg['pdfY'])
        for proj, pdf, var, argPats in [(h_accXrec_fine_ProjectionX, effi_cosl, CosThetaL, [r"^l\d+$"]), (h_accXrec_fine_ProjectionY, effi_cosK, CosThetaK, [r"^k\d+$"])]:
            hdata = ROOT.RooDataHist("hdata", "", ROOT.RooArgList(var), ROOT.RooFit.Import(proj))
            self.ToggleConstVar(args, isConst=False, targetArgs=argPats)
            
            theList = ROOT.RooLinkedList()
            Err     = ROOT.RooFit.Minos(True)
            theSave = ROOT.RooFit.Save() #Python discards temporary objects
            Verbose   = ROOT.RooFit.Verbose(0)
            PrintLevel= ROOT.RooFit.PrintLevel(-1)
            theList.Add(theSave);  theList.Add(Verbose); theList.Add(PrintLevel); theList.Add(Err)
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

        args.find('effi_norm').setConstant(False)
        Res2D=self.pdf.chi2FitTo(self.data, ROOT.RooFit.Minos(True), ROOT.RooFit.Save(), ROOT.RooFit.PrintLevel(-1))
        Res2D.Print()
        args.find('effi_norm').setVal(args.find('effi_norm').getVal() / 4.)
        args.find('effi_norm').setConstant(True)

        # Fix uncorrelated term and for later update with xTerms in main fit step
        args.find('hasXTerm').setVal(1)
        self.ToggleConstVar(args, isConst=False, targetArgs=[r"^x\d+$"])

    def _postFitSteps(self):
        """Post-processing"""
        args = self.pdf.getParameters(self.data)
        self.ToggleConstVar(args, True)
        FitDBPlayer.UpdateToDB(self.process.dbplayer.odbfile, args)

    def _runFitSteps(self):
        h2_accXrec = self.process.sourcemanager.get("effiHistReader.h2_accXrec.{0}".format(self.process.cfg['args'].Year))
        effi_sigA_formula = self.pdf.formula().GetExpFormula().Data()
        args = self.pdf.getParameters(self.data)
        args_it = args.createIterator()
        arg = args_it.Next()
        nPar = 0
        Formula=effi_sigA_formula
        while arg:
            if any(re.match(pat, arg.GetName()) for pat in ["effi_norm", "hasXTerm", r"^l(\d{1,2})$", r"^k\d+$"]):
                Formula = Formula.replace(arg.GetName()+"*", "({0})*".format(arg.getVal()))
                Formula = Formula.replace(arg.GetName()+")", "({0}))".format(arg.getVal()))
                Formula = Formula.replace(arg.GetName()+",", "({0}),".format(arg.getVal()))
            elif re.match(r"^x\d+$", arg.GetName()):
                nPar = nPar + 1
            arg = args_it.Next()
        effi_sigA_formula = Formula
        effi_sigA_formula = re.sub(r"x(\d{1,2})", r"[\1]", effi_sigA_formula)
        effi_sigA_formula = re.sub(r"CosThetaL", r"x", effi_sigA_formula)
        effi_sigA_formula = re.sub(r"CosThetaK", r"y", effi_sigA_formula)
        f2_effi_sigA = ROOT.TF2("f2_effi_sigA", effi_sigA_formula, -1, 1, -1, 1)

        fitter = ROOT.EfficiencyFitter()
        minuit = fitter.Init(nPar, h2_accXrec, f2_effi_sigA)
        minuit.SetPrintLevel(-1) #Pritam
        for xIdx in range(nPar):
            minuit.DefineParameter(xIdx, "x{0}".format(xIdx), 0., 1E-4, -1E+1, 1E+1)
        MigStatus=minuit.Migrad ()
        MinosStatus=minuit.Command("MINOS")
        
        print """    Floating Parameter  InitialValue    FinalValue +/-  Error     GblCorr.
  --------------------  ------------  --------------------------  --------"""
        parVal, parErr = ROOT.Double(0), ROOT.Double(0)
        eplus, eminus, eparab, gcc = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
        for xIdx in range(nPar):
            minuit.GetParameter(xIdx, parVal, parErr)
            minuit.mnerrs(xIdx, eplus, eminus, eparab, gcc)
            arg = args.find("x{0}".format(xIdx))
            print "{0:>21}".format('x'+str(xIdx)), "  " if arg.getVal()<0 else "   ", \
                  "{:.4e}".format(arg.getVal()), \
                  "" if parVal<0 else " ", "{:.4e} +/-".format(parVal), \
                  "{:.4e}".format(parErr), \
                  " {:.4e}".format(gcc)

            arg.setVal(parVal)
            arg.setError(parErr)
        print "TMinuit Status: ", minuit.GetStatus(), MigStatus, MinosStatus
        # Check if efficiency is positive definite
        f2_max_x, f2_max_y = ROOT.Double(0), ROOT.Double(0)
        f2_min_x, f2_min_y = ROOT.Double(0), ROOT.Double(0)
        f2_effi_sigA.GetMaximumXY(f2_max_x, f2_max_y)
        f2_effi_sigA.GetMinimumXY(f2_min_x, f2_min_y)
        self.logger.logINFO("Sanitary check: Efficiency ranges from {0:.2e} to {1:.2e}".format(f2_effi_sigA.Eval(f2_min_x, f2_min_y), f2_effi_sigA.Eval(f2_max_x, f2_max_y)))

        # Plot comparison between fitting result to data
        setStyle()
        canvas = ROOT.TCanvas()
        latex = ROOT.TLatex()
        h2_effi_2D_comp = h2_accXrec.Clone("h2_effi_2D_comp")
        h2_effi_2D_comp.Reset("ICESM")
        for lBin, KBin in itertools.product(list(range(1, h2_effi_2D_comp.GetNbinsX() + 1)), list(range(1, h2_effi_2D_comp.GetNbinsY() + 1))):
            if h2_accXrec.GetBinContent(lBin, KBin)==0:
                h2_effi_2D_comp.SetBinContent(lBin, KBin, 0)
                print ">> ** Warning ** Empty bins: (l, k)", lBin, KBin
            else:
                h2_effi_2D_comp.SetBinContent(lBin, KBin, f2_effi_sigA.Eval(h2_accXrec.GetXaxis().GetBinCenter(lBin), h2_accXrec.GetYaxis().GetBinCenter(KBin)) / h2_accXrec.GetBinContent(lBin, KBin))
        h2_effi_2D_comp.SetMinimum(0)
        h2_effi_2D_comp.SetMaximum(1.5)
        h2_effi_2D_comp.SetTitleOffset(1.6, "X")
        h2_effi_2D_comp.SetTitleOffset(1.8, "Y")
        h2_effi_2D_comp.SetTitleOffset(1.5, "Z")
        h2_effi_2D_comp.SetZTitle("#varepsilon_{fit}/#varepsilon_{measured}")
        h2_effi_2D_comp.Draw("LEGO2")
        latex.DrawLatexNDC(.08, .93, "#font[61]{CMS} #font[52]{#scale[0.8]{Simulation}}")
        latex.DrawLatexNDC(.08, .89, "#chi^{{2}}={0:.2f}".format(fitter.GetChi2()))
        
        ####################################
        cwd=os.getcwd()
        path=modulePath+"/"+self.process.work_dir+"/Efficiency/"
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)
        ####################################
        canvas.Print("effi_2D_comp_{0}.pdf".format(q2bins[self.process.cfg['binKey']]['label']))
        os.chdir(cwd)
        print "2D Efficiency Chi^2: ", fitter.GetChi2()

    @staticmethod
    def isPosiDef(formula2D):
        f2_min_x, f2_min_y = ROOT.Double(0), ROOT.Double(0)
        formula2D.GetMinimumXY(f2_min_x, f2_min_y)
        f2_min = formula2D.Eval(f2_min_x, f2_min_y)
        if f2_min > 0:
            return True
        else:
            print("WARNING\t: Sanitary check failed: Minimum of efficiency map is {0:.2e} at {1}, {2}".format(f2_min, f2_min_x, f2_min_y))
        return False
