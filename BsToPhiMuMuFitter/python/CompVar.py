#
# Description: Comparing variables in two different ntuples. 
# Warning: Ratio plot is not working. Need relook to this code.
#

import os, re, math, ROOT, pdb
from copy import deepcopy
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from BsToPhiMuMuFitter.python.datainput import GetInputFiles, ExtraCuts, ExtraCutsKStar, genSel

def SetStyles(obj1, obj2):
    obj1.SetMarkerStyle(8); obj1.SetMarkerColor(4); obj1.SetLineColor(ROOT.kBlue); obj1.SetLineWidth(1);obj1.SetFillColorAlpha(4,.2)
    obj2.SetMarkerStyle(8); obj2.SetMarkerColor(2); obj2.SetLineColor(2); obj2.SetLineWidth(1); obj2.SetFillColorAlpha(2, .2)

def GetCompPlots(self):
    fname1=self.process.cfg['genOff']['PhiMuMu']
    fname2=self.process.cfg['genonly']['PhiMuMu']
    f1=ROOT.TChain()
    f2=ROOT.TChain()
    for f in fname1:
        f1.Add(f)
    for f in fname2:
        f2.Add(f)

    binKey=self.process.cfg['binKey']
    #os.chdir(os.getcwd()+"/python")
    finalcut = q2bins[binKey]['cutString'].replace("Q2", "genQ2") + "&&" +genSel
    List1=[f1.GetListOfLeaves()[i].GetName() for i in range(f1.GetListOfLeaves().GetSize())]
    List2=[f2.GetListOfLeaves()[i].GetName() for i in range(f2.GetListOfLeaves().GetSize())]
    print(List1, List2)
    for var1 in List1:
        for var2 in List2:
            if var1==var2:
                if not var1=="genCosThetaL": continue
                h1Canvas = ROOT.TCanvas(); h1Canvas.cd()
                f1.Draw(var1, finalcut)
                hist1=deepcopy(ROOT.gPad.GetPrimitive("htemp"))
                f2.Draw(var2, finalcut)
                hist2=deepcopy(ROOT.gPad.GetPrimitive("htemp"))
                scale = 1./hist1.Integral();          scale2= 1./hist2.Integral()
                hist1.Scale(scale);                   hist2.Scale(scale2)

                res=ROOT.NewResPlot('TH1F')(hist1, hist2)
                res.fUpperPad.Draw(); res.fLowerPad.Draw(); res.fUpperPad.cd()
                hist1.Draw("E1 HIST");                hist2.Draw("E1 HIST same");
                SetStyles(hist1, hist2)
                hist1.GetYaxis().SetTitle("Events")
                leg=ROOT.TLegend(0.77,0.87,.99,.99)
                leg.AddEntry(hist1,"Official GEN");leg.AddEntry(hist2,"Unfiltered GEN")
                leg.Draw()
                h2 = hist1.Clone("Ratio")
                h2.Divide(hist2)
                h2.GetYaxis().SetTitle("Ratio"); h2.SetMarkerColor(1)
                res.fLowerPad.cd(); h2.Draw(); res.frame2=h2; res.PostDrawDecoration()                                                         
                res.fUpperPad.cd()
                h1Canvas.SaveAs("../python/{0}_{1}_{binKey}.pdf".format(var1, self.process.cfg['args'].Year, binKey=binKey))
