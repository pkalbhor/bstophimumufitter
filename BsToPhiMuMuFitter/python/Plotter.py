import os, ROOT
from datainput import sigMC, dataFilePath, UnfilteredMC
ROOT.gStyle.SetOptTitle(0)               # turn off the title
ROOT.gROOT.SetBatch(True)

def Decorate(hist, name):
    hist.GetXaxis().SetName(name)
f=ROOT.TChain()
f.Add(sigMC[0])
hgenCosL=ROOT.TH1D("genCosThetaL","genCosThetaL", 20, -1,1)
hgenCosK=ROOT.TH1D("genCosThetaK","genCosThetaK", 20, -1,1)
hCosL=ROOT.TH1D("CosThetaL","CosThetaL", 20, -1,1)
hCosK=ROOT.TH1D("CosThetaK","CosThetaK", 20, -1,1)

#print f.GetListOfLeaves()[0]
#exit()
CosThetaL=0
f.SetBranchAddress("CosThetaL", CosThetaL)
n=f.GetEntries()

f.Draw("{0}>>{1}".format(hgenCosL.GetName(), hgenCosL.GetName()), "", "goff")
f.Draw("{0}>>{1}".format(hgenCosK.GetName(), hgenCosK.GetName()), "", "goff")
f.Draw("{0}>>{1}".format(hCosL.GetName(), hCosL.GetName()), "", "goff")
f.Draw("{0}>>{1}".format(hCosK.GetName(), hCosK.GetName()), "", "goff")
#for i in range(n):
    #f.GetEvent(i)
    #hCosL.Fill("CosThetaL", 1)
    #hCosK.Fill("CosThetaK", 1)
    #hgenCosL.Fill("genCosThetaL", 1)
    #hgenCosK.Fill("genCosThetaK", 1)
Decorate(hgenCosL, hgenCosL.GetName())
Decorate(hgenCosK, hgenCosK.GetName())

#f.Draw("CosThetaL")
c1=ROOT.TCanvas("c1", "c1"); c1.cd()
hgenCosL.Divide(hCosL)
hgenCosL.Draw()
c2=ROOT.TCanvas("c2", "c2"); c2.cd()
hgenCosK.Divide(hCosK)
hgenCosK.Draw()
#f.Draw("genCosThetaK")
#c3=ROOT.TCanvas(); c3.cd(); f.Draw("CosThetaK")
c1.SaveAs("CosThetaL.pdf")
c2.SaveAs("CosThetaK.pdf")
os.system("root -l")
#hCosL.Print()
