import ROOT 
ROOT.gStyle.SetOptTitle(0)         
ROOT.gStyle.SetOptStat(0)          
ROOT.gStyle.SetPadTickX(1)         
ROOT.gStyle.SetPadTickY(1)         
#ROOT.gStyle.SetLabelFont(52, "XYZ")
ROOT.gStyle.SetTitleFontSize(0.17) 
            
h = ROOT.TH1D("name", "title", 100, -1, 1)
h.GetXaxis().SetTitle("A_{6}")     
h.GetYaxis().SetTitle("F_{L}")     
h.GetYaxis().SetRangeUser(-0.1, 1.1)
            
from array import array            
x = array('d', [-1, 0., 1., -1])   
y = array('d', [0., 1., 0., 0])    
pline = ROOT.TPolyLine(4, x, y);   
pline.SetFillColorAlpha(3, .8)     
pline.SetLineColor(4)              
pline.SetLineWidth(6)              
h.Draw()    
pline.Draw("f")                    
ROOT.gPad.SaveAs("/tmp/PhaseSpace.pdf")
            
            
ROOT.gPad.Clear()
f = ROOT.TF1("f", "0.5+(atan(x)/pi)", -30, 30)
f2 = ROOT.TF2("f2", "(1.-(0.5+(atan(x)/pi)))*(2./pi)*atan(y)", -30, 30, -30, 30)

f.Draw()
f.GetXaxis().SetTitle("Unbound F_{L}")
f.GetYaxis().SetTitle("F_{L}")
f.GetYaxis().SetRangeUser(0, 1.05)
fBox = ROOT.TBox(-3., 0., 3., 1.05)
fBox.SetFillColorAlpha(17, .35)
fBox.Draw("same")
ROOT.gPad.SaveAs("/tmp/FlTransform.pdf")

f2.Draw("surf1")
f2.GetXaxis().SetTitleOffset(2)
f2.GetXaxis().SetTitle("Unbound F_{L}")
f2.GetYaxis().SetTitleOffset(2)
f2.GetYaxis().SetTitle("Unbound A_{6}")
f2.GetZaxis().SetTitle("A_{6}")

ROOT.gPad.SaveAs("/tmp/A6Transform.pdf")

