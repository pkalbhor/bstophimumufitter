#
# Description: Comparing variables in two different ntuples. 
# Warning: Ratio plot is not working. Need relook to this code.
#

import os, re, math, ROOT, pdb
from copy import deepcopy
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath, bMassRegions
from BsToPhiMuMuFitter.python.datainput import GetInputFiles, ExtraCuts, ExtraCutsKStar, genSel
from BsToPhiMuMuFitter.varCollection import Phimass
def SetStyles(obj1, obj2):
    obj1.SetMarkerStyle(8); obj1.SetMarkerColor(4); obj1.SetLineColor(ROOT.kBlue); obj1.SetLineWidth(1);obj1.SetFillColorAlpha(4,.2)
    obj2.SetMarkerStyle(8); obj2.SetMarkerColor(2); obj2.SetLineColor(2); obj2.SetLineWidth(1); obj2.SetFillColorAlpha(2, .2)

def Decorate(self, hist1, hist2):
    hist1.SetLineColor(4)
    hist2.SetLineColor(1)
    hist1.SetFillColorAlpha(4,.2)
    hist2.SetFillColorAlpha(1,.0)
    pass

def FitHists(self, hist1, hist2):
    hist1.SetName("hist1"); hist2.SetName("hist2")
    #wspace = self.process.sourcemanager.get('wspace.2017.{}'.format(self.process.cfg['args'].binKey))
    #obj = wspace.obj('f_sigM_DCBG.2017')
    #getattr(wspace, 'import')(wspace.obj('f_sigM_DCBG'), ROOT.RooFit.RenameAllNodes('phifit'), ROOT.RooFit.RenameAllVariablesExcept('phifit', 'Bmass,CosThetaL,CosThetaK'))
    
    #pdf = wspace.obj('f_sigM_DCBG_phifit')

    fcmd = ["sigMGauss_mean[1.02, 1.0, 1.04]",
    "RooGaussian::f_sigMGauss1(Phimass, sigMGauss_mean, sigMGauss1_sigma[0.0284, 0.0001, 0.05])",
    "RooGaussian::f_sigMGauss2(Phimass, sigMGauss_mean, sigMGauss2_sigma[0.0667, 0.0005, 0.40])",
    "SUM::f_sigM(sigM_frac[0.7, 0.,1.]*f_sigMGauss1, f_sigMGauss2)",                                                                       
    "cbs_mean[1.02, 1.0, 1.04]",
    "RooCBShape::cbs_1(Phimass, cbs_mean, cbs1_sigma[0.0268, 0.0001, 0.60], cbs1_alpha[0.89, -6.0, 6.0], cbs1_n[4, 0, 1000])",
    "RooCBShape::cbs_2(Phimass, cbs_mean, cbs2_sigma[0.0296, 0.0001, 0.60], cbs2_alpha[-0.87, -9.4, 9.6], cbs2_n[133, 0, 1000])",
    "SUM::f_sigMDCB(sigMDCB_frac[0.4, 0.0, 1.0]*cbs_1, cbs_2)",
    "SUM::f_sigM_DCBG(sigM_frac1[.5,0,1]*cbs_1, sigM_frac2[.1,0.,1.]*f_sigMGauss1, cbs_2)"]
    wspace = ROOT.RooWorkspace("test")
    getattr(wspace, 'import')(globals()['Phimass'])
    for cmd in fcmd:
        wspace.factory(cmd)
    pdf = wspace.obj('f_sigMDCB')
    pdb.set_trace()


    data = ROOT.RooDataHist("hdata", "", ROOT.RooArgList(Phimass), ROOT.RooFit.Import(hist1))
    #args = pdf.getParameters(data)
    #args.find('cbs_mean_phifit').setVal(1.01)
    #args.find('sigMGauss_mean_phifit').setVal(1.01)
    
    fitter = ROOT.StdFitter()
    minuit=fitter.Init(pdf, data)
    nll = fitter.GetNLL()
    fitter.FitMigrad()
    #pdf.chi2FitTo(data)
    c=ROOT.TCanvas(); c.cd()
    frame = Phimass.frame()
    data.plotOn(frame)
    pdf.plotOn(frame)
    frame.Draw()
    c.SaveAs("test.pdf")
    
def GetCompPlots(self):
    fname1=self.process.cfg['control']['JpsiPhi']
    fname2=self.process.cfg['dataFilePath']
    f1=ROOT.TChain()
    f2=ROOT.TChain()
    for f in fname1:
        f1.Add(f)
    for f in fname2:
        f2.Add(f)

    binKey=self.process.cfg['binKey']
    #os.chdir(os.getcwd()+"/python")
    finalcut1 = q2bins[binKey]['cutString'] + "&&"+ bMassRegions['Fit']['cutString']+"&&" +self.process.cfg['cuts_antiResVeto']
    finalcut2 = q2bins[binKey]['cutString'] + "&&"+ bMassRegions['Fit']['cutString']+"&&" +self.process.cfg['cuts_antiResVeto']
    List1=[f1.GetListOfLeaves()[i].GetName() for i in range(f1.GetListOfLeaves().GetSize())]
    List2=[f2.GetListOfLeaves()[i].GetName() for i in range(f2.GetListOfLeaves().GetSize())]
    List1=['Phimass']
    List2=List1
    print(List1, '\n', List2)
    for var1 in List1:
        if not var1=="Phimass": continue
        for var2 in List2:
            if not var2=="Phimass": continue
            if var1==var2:
                if not var1=="Phimass": continue
                h1Canvas = ROOT.TCanvas(); h1Canvas.cd()
                f1.Draw(var1, finalcut1)
                hist1=deepcopy(ROOT.gPad.GetPrimitive("htemp"))
                f2.Draw(var2, finalcut2)
                hist2=deepcopy(ROOT.gPad.GetPrimitive("htemp"))
                scale = 1./hist1.Integral();          scale2= 1./hist2.Integral()
                hist1.Scale(scale);                   hist2.Scale(scale2)
                FitHists(self, hist1, hist2)
                """res=ROOT.NewResPlot('TH1F')(hist1, hist2)
                res.fUpperPad.Draw(); res.fLowerPad.Draw(); res.fUpperPad.cd()
                hist1.Draw("E1 HIST");                hist2.Draw("E1 HIST same");
                SetStyles(hist1, hist2)
                h2 = hist1.Clone("Ratio")
                h2.Divide(hist2)
                h2.GetYaxis().SetTitle("Ratio"); h2.SetMarkerColor(1)
                res.fLowerPad.cd(); h2.Draw(); res.frame2=h2; res.PostDrawDecoration()                                                         
                res.fUpperPad.cd()"""
                hist1.Draw("E1 HIST");                hist2.Draw("E1 HIST same");
                hist1.GetYaxis().SetTitle("Events")
                leg=ROOT.TLegend(0.77,0.87,.99,.99)
                leg.AddEntry(hist1,"Simulation");leg.AddEntry(hist2,"Data")
                leg.Draw()
                Decorate(self, hist1, hist2)
                h1Canvas.SaveAs("../python/{0}_{1}_{binKey}.pdf".format(var1, self.process.cfg['args'].Year, binKey=binKey))
