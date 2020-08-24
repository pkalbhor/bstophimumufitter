# Description: Input data files
# 
# Author     : Pritam Kalbhor (physics.pritam@gmail.com)
#
#
##################################################################################################

import os
import subprocess
#GITDIR=subprocess.check_output("git rev-parse --show-toplevel", shell=True).strip()

genSel          = "fabs(genMupEta)<2.4 && fabs(genMumEta)<2.4 && genMupPt>2.5 && genMumPt>2.5 && genKpPt>0.5 && genKmPt>0.5 && fabs(genKpEta)<2.5 && fabs(genKmEta)<2.5"
recBaseSel      = "fabs(Mupeta)<2.4&&fabs(Mumeta)<2.4 && Muppt>2.5&&Mumpt>2.5 && Kppt>0.5&&Kmpt>0.5 && fabs(Kpeta)<2.5&&fabs(Kmeta)<2.5"
ExtraCuts      = "mtrkqual==1 && ptrkqual==1 && dr0<0.1 && dr1<0.1"
ExtraCutsKStar = "mtrkqual==1 && ptrkqual==1 && ((JpsiTriggersdr0 < 101 && JpsiTriggersdr1 <101)||(PsiPTriggersdr0 <101 && PsiPTriggersdr1 <101)||(LMNTTriggersdr0< 101 && LMNTTriggersdr1< 101))"

def GetInputFiles(self):
    path="/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/"
    Args=self.cfg['args']
    if Args.Year==2016:
        self.cfg['allBins']      = ["belowJpsiA", "belowJpsiB", "belowJpsiC", "betweenPeaks", "summary", "summaryLowQ2", "Test3"]
        self.cfg['sigMC']        = [path+"sel_BsToPhiMuMu_OfficialMC_signal_2016Mini_Presel_mc.lite_cut_bdt_dcacut_s02.root/tree"]
        self.cfg['dataFilePath'] = [path+"sel_Combine_2016_Mini_Presel_data_cut_bdt_dcacut-s02.root/tree"]
        self.cfg['UnfilteredMC'] = [path+"sel_BsToPhiMuMu_2016MC_Nofilter_mc.lite_genonly.root/gentree"]       
        sigMCD = os.listdir(path+"gentree_2016/")
        for i in range(len(sigMCD)): 
            sigMCD[i]=path+"gentree_2016/"+sigMCD[i]+"/gentree"
        self.cfg['sigMCD']       = sigMCD
        self.cfg['KStarSigMC']   = [path+"sel_BdTokstarMuMu_OfficialMC_signal_2016Mini_Presel_mc.lite_cut_bdt_dcacut_s02.root/tree"]

    if Args.Year==2017:
        self.cfg['allBins']      = ["belowJpsiA", "belowJpsiB", "belowJpsiC", "betweenPeaks", "summary", "summaryLowQ2", "Test3"]
        self.cfg['sigMC']        = [path+"sel_BsToPhiMuMu_OfficialMC_signal_2017Mini_Presel_mc.lite_cut_bdt_dcacut_s02.root/tree"]
        self.cfg['dataFilePath'] = [path+"sel_Combine_2017_Mini_Presel_data_cut_bdt_dcacut-s02.root/tree"]
        self.cfg['UnfilteredMC'] = [path+"sel_BsToPhiMuMu_NofilterMC_signal_2017_mc.lite_genonly.root/gentree"]       
        sigMCD = os.listdir(path+"gentree2017/")
        for i in range(len(sigMCD)): 
            sigMCD[i]=path+"gentree2017/"+sigMCD[i]+"/gentree"
        self.cfg['sigMCD']       = sigMCD
        self.cfg['KStarSigMC']   = [path+"sel_BdTokstarMuMu_OfficialMC_signal_2017Mini_Presel_mc.lite_cut_bdt_dcacut_s02.root/tree"]

    if Args.Year==2018:
        self.cfg['allBins']      = ["belowJpsiA", "belowJpsiB", "belowJpsiC", "betweenPeaks", "summary", "summaryLowQ2", "Test3"]
        self.cfg['sigMC']        = [path+"sel_BsToPhiMuMu_OfficialMC_signal_2018Mini_Presel_mc.lite_cut_bdt_dcacut_s02.root/tree"]
        self.cfg['dataFilePath'] = [path+"sel_Combine_2018_Mini_Presel_data_cut_bdt_dcacut-s02.root/tree"]
        self.cfg['UnfilteredMC'] = [path+"sel_BsToPhiMuMu_NofilterMC_signal_2018_mc.lite_genonly.root/gentree"]       
        sigMCD       = os.listdir(path+"gentree_2018/")
        for i in range(len(sigMCD)): 
            sigMCD[i]=path+"gentree_2018/"+sigMCD[i]+"/gentree"
        self.cfg['sigMCD']       = sigMCD
        self.cfg['KStarSigMC']   = [path+"sel_BdTokstarMuMu_OfficialMC_signal_2018Mini_Presel_mc.lite_cut_bdt_dcacut_s02.root/tree"]


    # Cut strings
    cut_passTrigger = "JpsiTriggers > 0 || PsiPTriggers > 0 || LMNTTriggers > 0"
    #cut_resonanceRej = "(Mumumass > 3.096916+3.5*Mumumasserr || Mumumass < 3.096916-5.5*Mumumasserr) && (Mumumass > 3.686109+3.5*Mumumasserr || Mumumass < 3.686109-3.5*Mumumasserr)"
    cut_antiRadiation = "abs(Bmass-Mumumass-2.270)>0.110 && abs(Bmass-Mumumass-1.681)>0.080"

    if Args.Year==2016:
        cut_phiWindow = "Phimass>1.0 && Phimass < 1.04"
        cut_Bdt = "Bdt > 0.60"
    if Args.Year==2017:
        cut_phiWindow = "Phimass>1.0 && Phimass < 1.04"
        cut_Bdt = "Bdt > 0.58"
    if Args.Year==2018:
        cut_phiWindow = "Phimass>1.0 && Phimass < 1.04"
        cut_Bdt = "Bdt > 0.57"
    cuts = [
        cut_passTrigger,
        cut_phiWindow,
        cut_antiRadiation,
        cut_Bdt,
    ]
    cuts.append("({0})".format(")&&(".join(cuts)))
    cuts_noResVeto = "({0})&&({1})".format(cut_passTrigger, cut_phiWindow)
    self.cfg['cuts'] = cuts

