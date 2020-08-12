# Description: Plot variables from a file
#
#
#
##################################################################################################

import os, pdb, ROOT
from BsToPhiMuMuFitter.seqCollection import args as Args
from datainput import sigMC, dataFilePath, UnfilteredMC
from BsToPhiMuMuFitter.anaSetup import q2bins, cuts, ExtraCuts, ExtraCutsKStar
ROOT.gStyle.SetOptTitle(0)               # turn off the title
ROOT.gROOT.SetBatch(True)

def Decorate(hist, name):
    hist.GetXaxis().SetName(name)
f=ROOT.TChain()
for ch in dataFilePath:
    f.Add(ch)
print dataFilePath
c1=ROOT.TCanvas("c1", "c1"); c1.cd()

Var=['CosThetaK', 'CosThetaL', 'Bmass', 'Phimass']
tcut=cuts[-1]+" && "+ExtraCuts
for var in Var:
    for binKey in q2bins.keys():
        f.Draw(var, q2bins[binKey]['cutString']+" && "+tcut)
        hist=ROOT.gPad.GetPrimitive("htemp"); 
        if type(hist) is not ROOT.TObject: hist.SetName(var)
        ROOT.TLatex().DrawLatexNDC(.45, .85, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        c1.SaveAs("python/{0}_{1}_{binKey}.pdf".format(var, str(Args.Year), binKey=q2bins[binKey]['label']))
os.system("root -l")
