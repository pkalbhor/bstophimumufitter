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
ExtraCuts       = "mtrkqual==1 && ptrkqual==1 && dr0<0.1 && dr1<0.1"
ExtraCutsKStar  = "mtrkqual==1 && ptrkqual==1 && ((JpsiTriggersdr0 < 101 && JpsiTriggersdr1 <101)||(PsiPTriggersdr0 <101 && PsiPTriggersdr1 <101)||(LMNTTriggersdr0< 101 && LMNTTriggersdr1< 101))"

def GetInputFiles(self):
    Args=self.cfg['args']
    path0="/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/"
    path  = path0+"AfterBDT_Training_{}/".format(Args.Year)
    path2 = path +"gentree_Phimumu/"
    path3 = path0+"private_sample/"
    self.cfg['allBins']      = ["belowJpsiA", "belowJpsiB", "belowJpsiC", "betweenPeaks", "summaryLowQ2"]
    if Args.Year==2016:
        self.cfg['dataFilePath'] = [path+"sel_Combine_2016_Mini_Presel_data_cut_bdt-Correction-s04.root/tree"]
        self.cfg['sigMC']        = [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2016M" in File]
        self.cfg['sigMCD']       = [path2+File+"/gentree" for File in os.listdir(path2) if "sel_BsToPhiMuMu_OfficialMC_signal_2016M" in File]
        self.cfg['genonly']      = {'PhiMuMu': [path3+"sel_BsToPhiMuMu_2016MC_Nofilter_mc.lite_genonly.root/gentree"],
                                    'JpsiPhi': [path3+"sel_BsToJpsiPhi_2016_mc_genonly_s0.root/gentree"],
                                    'PsiPhi' : [path3+"sel_BsToPsiPhi_2016_mc_genonly_s0.root/gentree"]}
        self.cfg['peaking']    ={'KstarMuMu': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToKstarMuMu_2016MC_Official" in File],
                                 'JpsiKstar': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToJpsikstar_2016MC_Official" in File],
                                 'PsiKstar' : []}
        self.cfg['control']    =  {'JpsiPhi': [path+File+"/tree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2016MC_Official" in File],
                                   'PsiPhi' : [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPsiPhi_2016MC_Official" in File] }
    if Args.Year==2017:
        self.cfg['dataFilePath'] = [path+"sel_Combine_2017_Mini_Presel_data_cut_bdt-Correction-s04.root/tree"]
        self.cfg['sigMC']        = [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2017M" in File] 
        self.cfg['sigMCD']       = [path2+File+"/gentree" for File in os.listdir(path2) if "sel_BsToPhiMuMu_OfficialMC_signal_2017M" in File]
        self.cfg['genonly']      = {'PhiMuMu': [path3+"sel_BsToPhiMuMu_NofilterMC_signal_2017_mc.lite_genonly.root/gentree"],
                                    'JpsiPhi': [path3+"sel_BsToJpsiPhi_2017_mc_genonly_s0.root/gentree"],
                                    'PsiPhi' : [path3+"sel_BsToPsiPhi_2017_mc_genonly_s0.root/gentree"]}
        self.cfg['peaking']    ={'KstarMuMu': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToKstarMuMu_2017MC_Official" in File],
                                 'JpsiKstar': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToJpsikstar_2017MC_Official" in File],
                                 'PsiKstar' : [path+File+"/tree" for File in os.listdir(path) if "sel_BdToPsiKstar_2017MC_Official" in File]}
        self.cfg['control']     = {'JpsiPhi': [path+File+"/tree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2017MC_Official" in File],
                                   'PsiPhi' : [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPsiPhi_2017MC_Official" in File] }

    if Args.Year==2018:
        self.cfg['dataFilePath'] = [path+"sel_Combine_2018_Mini_Presel_data_cut_bdt-Correction-s04.root/tree"]
        self.cfg['sigMC']        = [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2018M" in File] 
        self.cfg['sigMCD']       = [path2+File+"/gentree" for File in os.listdir(path2) if "sel_BsToPhiMuMu_OfficialMC_signal_2018M" in File]
        self.cfg['genonly']      = {'PhiMuMu': [path3+"sel_BsToPhiMuMu_NofilterMC_signal_2018_mc.lite_genonly.root/gentree"],
                                    'JpsiPhi': [path3+"sel_BsToJpsiPhi_2018_mc_genonly_s0.root/gentree"],
                                    'PsiPhi' : [path3+"sel_BsToPsiPhi_2018_mc_genonly_s0.root/gentree"]}
        self.cfg['peaking']    ={'KstarMuMu': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToKstarMuMu_2018MC_Official" in File],
                                 'JpsiKstar': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToJpsikstar_2018MC_Official" in File],
                                 'PsiKstar' : [path+File+"/tree" for File in os.listdir(path) if "sel_BdToPsiKstar_2018MC_Official" in File]}
        self.cfg['control']     = {'JpsiPhi': [path+File+"/tree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2018MC_Official" in File],
                                   'PsiPhi' : [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPsiPhi_2018MC_Official" in File] }

    # Cut strings
    cut_passTrigger = "JpsiTriggers > 0 || PsiPTriggers > 0 || LMNTTriggers > 0"
    cut_resonanceRej = "(Mumumass > 3.0969+3.5*Mumumasserr || Mumumass < 3.0969-5.5*Mumumasserr) && (Mumumass > 3.6861+3.5*Mumumasserr || Mumumass < 3.6861-3.5*Mumumasserr)"
    cut_resonanceSel = "(Mumumass > 3.0969+3.0*Mumumasserr || Mumumass < 3.0969-3.5*Mumumasserr) && (Mumumass > 3.6861+3.0*Mumumasserr || Mumumass < 3.6861-3.0*Mumumasserr)"
    cut_antiRadiation = "abs(Bmass-Mumumass-2.270)>0.120 && abs(Bmass-Mumumass-1.681)>0.090"
    cut_phiWindow = "Phimass>1.0 && Phimass < 1.04"

    if Args.Year==2016:
        cut_Bdt = "Bdt > 0.57"
    if Args.Year==2017:
        cut_Bdt = "Bdt > 0.55"
    if Args.Year==2018:
        cut_Bdt = "Bdt > 0.50"
    cuts = [
        cut_passTrigger,
        #cut_phiWindow,
        cut_antiRadiation,
        cut_Bdt,
    ]
    cuts.append("({0})".format(")&&(".join(cuts)))
    cuts_noResVeto = "({0})&&({1})&&({2})".format(cut_passTrigger, cut_Bdt)
    cuts_Signal = "({0}) && (({1}) && ({2}))".format(cuts_noResVeto, cut_resonanceRej, cut_antiRadiation)
    cuts_antiSignal = "({0}) && !(({1}) && ({2}))".format(cuts_noResVeto, cut_resonanceRej, cut_antiRadiation)
    #cuts_antiResVeto = "({0}) && !({1}) && !({2})".format(cuts_noResVeto, cut_resonanceSel, cut_antiRadiation)
    cuts_antiResVeto = "({0}) && ({1}) && !({2})".format(cut_passTrigger, cut_Bdt, cut_resonanceSel)
    self.cfg['cuts'] = cuts
    self.cfg['cuts_antiResVeto'] = cuts_antiResVeto
    self.cfg['cuts_Signal'] = cuts_Signal
