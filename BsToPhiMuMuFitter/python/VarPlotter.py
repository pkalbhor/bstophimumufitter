# Description: Plot variables from a file
#
#
#
##################################################################################################

import os, pdb, ROOT
from BsToPhiMuMuFitter.seqCollection import args as Args
from BsToPhiMuMuFitter.StdProcess import p
from BsToPhiMuMuFitter.python.datainput import GetInputFiles, ExtraCuts, ExtraCutsKStar
p.cfg['args'] = Args
GetInputFiles(p)

from BsToPhiMuMuFitter.anaSetup import q2bins, bMassRegions
ROOT.gStyle.SetOptTitle(0)               # turn off the title
ROOT.gROOT.SetBatch(True)

def Decorate(hist, name):
    hist.GetXaxis().SetName(name)
f=ROOT.TChain()
files=[]
Var=['Bmass']
if Args.seqKey=='KStar':
    files = p.cfg['KStarSigMC']
    Var=['Kst0mass'] #, 'Phimass', 'CosThetaK', 'CosThetaL', 'Bmass']
if Args.seqKey=='Data':
    files = p.cfg['dataFilePath']
    Var=['Bmass']
for ch in files:
    f.Add(ch)
c1=ROOT.TCanvas("c1", "c1"); c1.cd()

XXTra = "(1)"
if True: XXTra = '!(CosThetaL >-.5 && CosThetaL <.5)'
tcut    =" && ".join([p.cfg['cuts'][-1], ExtraCutsKStar if Args.seqKey=='KStar' else ExtraCuts, XXTra])
for var in Var:
    for binKey in q2bins.keys():
        #if not binKey in ['belowJpsiB']: continue
        finalcut=" && ".join([q2bins[binKey]['cutString'], tcut, bMassRegions['Fit']['cutString']])
        #finalcut=q2bins[binKey]['cutString']
        print(finalcut)
        f.Draw(var, finalcut)#, 'E1')
        hist=ROOT.gPad.GetPrimitive("htemp"); 
        if type(hist) is not ROOT.TObject: 
            hist.SetName(var)
            #hist.Rebin(5)
        ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        ROOT.TLatex().DrawLatexNDC(.45, .84, r"#scale[0.8]{{Events = {0:.2f}}}".format(f.GetEntries(finalcut)) )
        c1.SaveAs("python/{2}_{0}_{1}_{binKey}.pdf".format(var, Args.Year, Args.seqKey, binKey=q2bins[binKey]['label']))
os.system("root -l")
