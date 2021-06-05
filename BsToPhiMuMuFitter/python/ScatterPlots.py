"""Scatter plot for Bmass vs Q2"""
import ROOT
from BsToPhiMuMuFitter.python.ArgParser import SetParser, GetBatchTaskParser
parser=GetBatchTaskParser()
args = parser.parse_known_args()[0]
#import pdb; pdb.set_trace()

from BsToPhiMuMuFitter.StdProcess import p, setStyle
setStyle()
ROOT.gStyle.SetPadRightMargin(0.15)

p.work_dir="plots_"+str(args.Year)
p.cfg['args'] = args
from BsToPhiMuMuFitter.python.datainput import GetInputFiles, ExtraCuts

GetInputFiles(p)
ifile = ROOT.TChain()
for f in p.cfg['dataFilePath']: ifile.Add(f)
Cuts = p.cfg['cuts'][-1] + " && " + ExtraCuts
cuts =  p.cfg['cuts']
# Without AR cut
#Cuts = "({0})".format(")&&(".join([cuts[0], cuts[2], cuts[3], cuts[4], ExtraCuts]))
# Omitting SL Cut
Cuts = "({0})".format(")&&(".join([cuts[0], cuts[1], cuts[2], cuts[3], ExtraCuts]))

print(Cuts)
hist2d = ROOT.TH2D("hist2d", "Bmss scatter plot", 200, 4.7, 6.0, 200, 1, 19.)
ifile.Draw("Q2:Bmass>>hist2d", Cuts)
hist2d.GetXaxis().SetTitle("M_{B}(#phi#mu#mu) GeV")
hist2d.GetYaxis().SetTitle("q^{2} GeV^{2}")
hist2d.Draw("COLZ")
bin3Box = ROOT.TBox(4.7, 11., 6.0, 12.5); bin3Box.SetFillColorAlpha(17, .35); bin3Box.Draw("same")
ROOT.gPad.SaveAs("Bmass_scatterPlot.pdf")
ROOT.gPad.Clear();

cosl2d = ROOT.TH2D("cosl2d", "CosL scatter plot", 200, -1, 1, 200, 1, 19.)
ifile.Draw("Q2:CosThetaL>>cosl2d", Cuts)
cosl2d.GetXaxis().SetTitle("Cos(#theta_{L}) GeV")
cosl2d.GetYaxis().SetTitle("q^{2} GeV^{2}")
cosl2d.Draw("COLZ")
print("CosL Entries", cosl2d.GetEntries())
bin3Box = ROOT.TBox(4.7, 11., 6.0, 12.5); bin3Box.SetFillColorAlpha(17, .35); bin3Box.Draw("same")
ROOT.gPad.SaveAs("Cosl_scatterPlot.pdf")
ROOT.gPad.Clear();

cosK2d = ROOT.TH2D("cosK2d", "CosK scatter plot", 200, -1, 1, 200, 1, 19.)
ifile.Draw("Q2:CosThetaK>>cosK2d", Cuts)
cosK2d.GetXaxis().SetTitle("Cos(#theta_{K}) GeV")
cosK2d.GetYaxis().SetTitle("q^{2} GeV^{2}")
cosK2d.Draw("COLZ")
print("CosK Entries", cosK2d.GetEntries())
bin3Box = ROOT.TBox(4.7, 11., 6.0, 12.5); bin3Box.SetFillColorAlpha(17, .35); bin3Box.Draw("same")
ROOT.gPad.SaveAs("CosK_scatterPlot.pdf")