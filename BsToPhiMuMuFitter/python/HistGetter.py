import os, re, math, ROOT
from BsToPhiMuMuFitter.anaSetup import q2bins

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.16)
ROOT.gStyle.SetPadRightMargin(0.02)
ROOT.gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetTitleYOffset(1.25)

f=ROOT.TFile("/afs/cern.ch/work/p/pkalbhor/BtoPhiMuMuFitter_For6Bins/BsToPhiMuMuFitterv6/BsToPhiMuMuFitter/BsToPhiMuMuFitter/data/accXrecEffHists_Run2012.root", "READ")
f2=ROOT.TFile("/afs/cern.ch/work/p/pkalbhor/BtoPhiMuMuFitter_For6Bins/BsToPhiMuMuFitterv6/BsToPhiMuMuFitter/BsToPhiMuMuFitter/data/accXrecEffHists_Run2016.root", "READ")
f.Print()
#f.ls()

os.chdir(os.getcwd()+"/python")
#ROOT.gPad.cd()
print f.GetListOfKeys().At(0), f.GetNkeys()
List=f.GetListOfKeys()
List2=f2.GetListOfKeys()

for i in range(0, f.GetNkeys()):
    name=f.GetListOfKeys().At(i).GetName()
    obj=List.FindObject(name)
    #obj=f.Get(name)
    if obj.InheritsFrom(ROOT.TEfficiency.Class()):
        List.Remove(obj)
#for i in List: print i.GetName()

for i in List:
    #obj=f.Get(i.GetName())
    obj=f.Get(i.GetName())
    if obj.InheritsFrom(ROOT.TH1D.Class()):
        print "TH1D: ", obj.GetName()
        for j in List2:
            obj2=f2.Get(j.GetName())
            if j.GetName()==i.GetName():
                #scale =float(obj.GetXaxis().GetBinWidth(1))/(obj.GetIntegral())
                #scale2=float(obj2.GetXaxis().GetBinWidth(1))/(obj2.GetIntegral())  
                scale = 1./obj.Integral()
                scale2= 1./obj2.Integral()
                obj.Scale(scale)
                obj2.Scale(scale2)
                obj.Divide(obj2)
                obj.Draw("HIST")
                obj.GetXaxis().SetTitle("cos#theta_{l}" if "ProjectionX" in obj.GetName() else "cos#theta_{K}")
                obj.GetYaxis().SetTitle("Total Efficiency Ratio")
                key=[k for k in q2bins.keys() if k in obj.GetName()]
                ROOT.TLatex().DrawLatexNDC(0.45, 0.89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[key[0]]['latexLabel']))
                ROOT.gPad.SaveAs(obj.GetName().replace(key[0], q2bins[key[0]]['label'])+".pdf")
    elif obj.InheritsFrom(ROOT.TH2D.Class()): 
        print "TH2D: ", obj.GetName() 
    elif obj.InheritsFrom(ROOT.TEfficiency.Class()) and False: 
        print "TEfficiency: ", obj.GetName()
        if "ProjectionX" in obj.GetName() or "ProjectionY" in obj.GetName():
            h=obj.GetPassedHistogram().Clone(obj.GetName()); h.Reset("ICESM")
            for b in range(1, h.GetNbinsX() + 1):
                h.SetBinContent(b, obj.GetEfficiency(b))
                h.SetBinError(b, h.GetBinContent(b)*math.sqrt(1 / obj.GetTotalHistogram().GetBinContent(b) + 1 / obj.GetPassedHistogram().GetBinContent(b)))
            h.Draw()
            h.GetXaxis().SetTitle("cos#theta_{l}" if "ProjectionX" in obj.GetName() else "cos#theta_{K}")
            h.GetYaxis().SetTitle("Acceptance Efficiency" if "acc_" in obj.GetName() else "Reco Efficiency")
            key=[k for k in q2bins.keys() if k in obj.GetName()]
            ROOT.TLatex().DrawLatexNDC(0.45, 0.89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[key[0]]['latexLabel']))
            ROOT.gPad.SaveAs(obj.GetName().replace(key[0], q2bins[key[0]]['label'])+".pdf")
    else:
        print "False"
   #print type(f.Get("h_accXrec_belowJpsiA_ProjectionX"))
