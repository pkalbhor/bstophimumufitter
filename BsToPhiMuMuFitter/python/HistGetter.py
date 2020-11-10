# Description: Shows comparison between two step efficiency and one step efficiency
# 
# Author     : Pritam Kalbhor (physics.pritam@gmail.com)
#
#
##################################################################################################

import os, re, math, ROOT, pdb
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from BsToPhiMuMuFitter.seqCollection import args
from BsToPhiMuMuFitter.varCollection import CosThetaL, CosThetaK

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.13)
ROOT.gStyle.SetPadLeftMargin(0.16)
ROOT.gStyle.SetPadRightMargin(0.02)
ROOT.gStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetTitleYOffset(1.25)

print("Warning:: Please make sure efficiency files for both 1 Step and 2 Step are already produced. If not code will fail to produce desired output.")
fname=modulePath+"/data/accXrecEffHists_{0}.root".format(str(args.Year))
fname2=modulePath+"/data/TotalEffHists_{0}.root".format(str(args.Year))
if not os.path.exists(fname):
    os.system("hadd {0} {1}".format(fname, modulePath+"/data/accXrecEffHists_{0}_*.root".format(str(args.Year))))
if not os.path.exists(fname2):
    os.system("hadd {0} {1}".format(fname2, modulePath+"/data/TotalEffHists_{0}_*.root".format(str(args.Year))))

f=ROOT.TFile(fname, "READ")
f2=ROOT.TFile(fname2, "READ")
print("Will use {}".format(f.GetName()))

os.chdir(os.getcwd()+"/python")
List=f.GetListOfKeys()
List2=f2.GetListOfKeys()

for i in range(0, f.GetNkeys()):
    name=f.GetListOfKeys().At(i).GetName()
    obj=List.FindObject(name)
    if obj.InheritsFrom(ROOT.TEfficiency.Class()):
        List.Remove(obj)
def SetStyles(obj, obj2):
    obj.GetXaxis().SetTitle("cos#theta_{l}" if "ProjectionX" in obj.GetName() else "cos#theta_{K}")
    obj.SetMarkerStyle(8); obj.SetMarkerColor(4); obj.SetLineColor(ROOT.kBlue); obj.SetLineWidth(1);obj.SetFillColorAlpha(4,.2)
    obj2.SetMarkerStyle(8); obj2.SetMarkerColor(2); obj2.SetLineColor(2); obj2.SetLineWidth(1); obj2.SetFillColorAlpha(2, .2)

def GetPDFlist(binkey):
    from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
    cwd=os.getcwd()
    os.chdir("../input/")
    mfile = "wspace_{}_{}.root".format(args.Year, binkey)
    ifile = ROOT.TFile.Open(mfile, 'READ')
    wspace = ifile.Get("wspace.{}.{}".format(args.Year, binkey))
    pdf = { 'pdfL': wspace.obj("effi_cosl"),
            'pdfK': wspace.obj("effi_cosK"),
            'pdfL_ts': wspace.obj("effi_cosl_ts"),
            'pdfK_ts': wspace.obj("effi_cosK_ts")}
    os.chdir(cwd)
    os.chdir('../plots_{}/'.format(args.Year))
    odbfile = 'fitResults_{}.db'.format(binkey)
    
    for key in pdf.keys():
        arguments = pdf[key].getParameters(ROOT.RooArgSet(CosThetaL, CosThetaK))
        FitDBPlayer.initFromDB(odbfile, arguments)
    os.chdir(cwd)
    return pdf

for i in List: # 2 Step list
    obj=f.Get(i.GetName())
    if obj.InheritsFrom(ROOT.TH1D.Class()):
        for j in List2: # One Step list
            obj2=f2.Get(j.GetName())
            key=[k for k in q2bins.keys() if k in obj.GetName()]
            if j.GetName()==i.GetName():
                pdf = GetPDFlist(q2bins[key[0]]['label'])
                print(pdf)
                h1Canvas = ROOT.TCanvas(); h1Canvas.cd()
                res=ROOT.NewResPlot('TH1D')(obj, obj2)
                scale = 1./obj.Integral();          scale2= 1./obj2.Integral()
                obj.Scale(scale);                   obj2.Scale(scale2)

                res.fUpperPad.Draw(); res.fLowerPad.Draw(); res.fUpperPad.cd()
                obj.Draw("HIST");   
                if "ProjectionX" in obj.GetName():
                    pdfhist = pdf['pdfL_ts'].createHistogram("pdfL_ts", CosThetaL, ROOT.RooFit.Binning(20))
                else:
                    pdfhist = pdf['pdfK_ts'].createHistogram("pdfK_ts", CosThetaK, ROOT.RooFit.Binning(20))
                pdfhist.Draw('c same')
                pdfhist.SetLineColor(ROOT.kBlue)

                obj2.Draw("HIST same")
                if "ProjectionX" in obj.GetName():
                    pdfhist2 = pdf['pdfL'].createHistogram("pdfL", CosThetaL, ROOT.RooFit.Binning(20))
                else:
                    pdfhist2 = pdf['pdfK'].createHistogram("pdfK", CosThetaK, ROOT.RooFit.Binning(20))
                pdfhist2.Draw('c same')
                pdfhist2.SetLineColor(2)
                SetStyles(obj, obj2)
                obj.GetYaxis().SetTitle("Total Efficiency")
                leg=ROOT.TLegend(0.77,0.87,.99,.99)
                leg.AddEntry(obj,"Two Step Efficiency");leg.AddEntry(obj2,"One Step Efficiency")
                leg.Draw()
                h2 = obj.Clone("Ratio")
                h2.Divide(obj2)
                h2.GetYaxis().SetTitle("Ratio"); h2.SetMarkerColor(1)
                h2Can=ROOT.TCanvas(); h2Can.cd(); h2.Draw()
                h2Can.SaveAs("Ratio2by1_{1}_{0}_".format("cosl" if "ProjectionX" in obj.GetName() else "cosK", str(args.Year))+q2bins[key[0]]['label']+".pdf")
                res.fLowerPad.cd(); h2.Draw(); res.frame2=h2; res.PostDrawDecoration()
                res.fUpperPad.cd()
                ROOT.TLatex().DrawLatexNDC(0.45, 0.89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[key[0]]['latexLabel']))
                h1Canvas.SaveAs("Overlay_{1}_{0}_".format("cosl" if "ProjectionX" in obj.GetName() else "cosK", str(args.Year))+q2bins[key[0]]['label']+".pdf")

    elif obj.InheritsFrom(ROOT.TH2D.Class()) : 
        for j in List2:
            obj2=f2.Get(j.GetName())
            key=[k for k in q2bins.keys() if k in obj.GetName()]
            if j.GetName()==i.GetName():
                canvas = ROOT.TCanvas()             
                latex = ROOT.TLatex()
                scale = 100./obj.Integral();        scale2= 100./obj2.Integral()
                obj.Scale(scale);                   obj2.Scale(scale2)

                h2_effi_2D_comp = obj.Clone("h2_effi_2D_comp")
                h2_effi_2D_comp.Divide(obj2)
                h2_effi_2D_comp.SetMinimum(0)
                h2_effi_2D_comp.SetMaximum(1.5)
                h2_effi_2D_comp.SetTitleOffset(1.6, "X")
                h2_effi_2D_comp.SetTitleOffset(1.8, "Y")
                h2_effi_2D_comp.SetTitleOffset(1., "Z")
                h2_effi_2D_comp.SetZTitle("2 Step Eff / 1 Step Eff")
                h2_effi_2D_comp.Draw("LEGO2")
                canvas.SetRightMargin(0.032)
                ROOT.TLatex().DrawLatexNDC(0.12, 0.89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[key[0]]['latexLabel']))
                canvas.SaveAs("2DRatio_{1}_{0}".format(q2bins[key[0]]['label'], str(args.Year))+".pdf")

                canvas2 = ROOT.TCanvas()
                ROOT.gStyle.SetPalette(ROOT.kBlackBody)
                h2_effi_2D_comp.Draw("COLZ") #("LEGO2")
                obj.SetBarOffset(0.2);    obj.Draw("TEXT SAME"); h2_effi_2D_comp.GetXaxis().SetTitleOffset(1)
                canvas2.SetRightMargin(0.1)
                canvas2.SetLeftMargin(0.1)
                h2_effi_2D_comp.GetYaxis().SetTitleOffset(1)
                obj2.SetMarkerColor(2); obj2.SetBarOffset(-0.2); obj2.Draw("TEXT SAME")
                ROOT.TLatex().DrawLatexNDC(0.12, 0.96, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[key[0]]['latexLabel']))
                canvas2.SaveAs("2DRatioTEXT_{1}_{0}".format(q2bins[key[0]]['label'], str(args.Year))+".pdf")
 
    elif obj.InheritsFrom(ROOT.TEfficiency.Class()): 
        if "ProjectionX" in obj.GetName() or "ProjectionY" in obj.GetName():
            c1=ROOT.TCanvas()
            h=obj.GetPassedHistogram().Clone(obj.GetName()); h.Reset("ICESM")
            for b in range(1, h.GetNbinsX() + 1):
                h.SetBinContent(b, obj.GetEfficiency(b))
                h.SetBinError(b, h.GetBinContent(b)*math.sqrt(1 / obj.GetTotalHistogram().GetBinContent(b) + 1 / obj.GetPassedHistogram().GetBinContent(b)))
            h.Draw("E1 HIST")
            h.GetXaxis().SetTitle("cos#theta_{l}" if "ProjectionX" in obj.GetName() else "cos#theta_{K}")
            h.GetYaxis().SetTitle("Acceptance Efficiency" if "acc_" in obj.GetName() else "Reco Efficiency")
            h.SetMarkerStyle(8); h.SetMarkerColor(4); h.SetLineColor(ROOT.kBlue)
            h.SetLineWidth(1); h.SetFillColorAlpha(6,.2)
            h.GetYaxis().SetTitleOffset(1.3)

            key=[k for k in q2bins.keys() if k in obj.GetName()]
            ROOT.TLatex().DrawLatexNDC(0.45, 0.89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[key[0]]['latexLabel']))
            c1.SaveAs("{0}Eff_{2}_{1}_".format("Acc_" if "acc_" in obj.GetName() else "Rec_", "cosl" if "ProjectionX" in obj.GetName() else "cosK", str(args.Year))+q2bins[key[0]]['label']+".pdf")
    else:
        pass
