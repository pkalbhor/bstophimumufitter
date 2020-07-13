import os, ROOT
from datainput import sigMC, dataFilePath, UnfilteredMC
from BsToPhiMuMuFitter.anaSetup import q2bins
ROOT.gStyle.SetOptTitle(0)               # turn off the title
ROOT.gROOT.SetBatch(True)

def Decorate(hist, name):
    hist.GetXaxis().SetName(name)
f=ROOT.TChain()
f.Add("/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/sel_BdTokstarMuMu_2016MC_Official_Presel_mc.lite_cut_bdt-s02.root/tree")
c1=ROOT.TCanvas("c1", "c1"); c1.cd()

Var=['CosThetaK', 'CosThetaL', 'Bmass', 'Phimass']
tcut="(Bmass > 5.2 && Bmass < 5.6) && ((JpsiTriggers > 0 || PsiPTriggers > 0 || LMNTTriggers > 0)&&(Phimass>1.01 && Phimass < 1.03)&&(abs(Bmass-Mumumass-2.270)>0.120 && abs(Bmass-Mumumass-1.681)>0.090)&&(Bdt > 0.06)) && (mtrkqual==1 && ptrkqual==1 && dr0<0.1 && dr1<0.1)"
for i in Var:
    for binKey in q2bins.keys():
        f.Draw(i, q2bins[binKey]['cutString'])
        ROOT.TLatex().DrawLatexNDC(.45, .85, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        c1.SaveAs("python/{0}_{binKey}.pdf".format(i, binKey=q2bins[binKey]['label']))
os.system("root -l")
