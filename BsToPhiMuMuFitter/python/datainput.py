# Description: Input data files
# 
# Author     : Pritam Kalbhor (physics.pritam@gmail.com)
#
#
##################################################################################################

import os
import subprocess
#GITDIR=subprocess.check_output("git rev-parse --show-toplevel", shell=True).strip()

genSel          = "fabs(genMupEta)<2.5 && fabs(genMumEta)<2.5 && genMupPt>2.5 && genMumPt>2.5 && genKpPt>0.4 && genKmPt>0.4 && fabs(genKpEta)<2.5 && fabs(genKmEta)<2.5"
recBaseSel      = "fabs(Mupeta)<2.5&&fabs(Mumeta)<2.5 && Muppt>2.5&&Mumpt>2.5 && Kppt>0.4&&Kmpt>0.4 && fabs(Kpeta)<2.5&&fabs(Kmeta)<2.5"
ExtraCuts       = "mtrkqual==1 && ptrkqual==1 && dr0<0.1 && dr1<0.1"
ExtraCutsKStar  = "mtrkqual==1 && ptrkqual==1 && ((JpsiTriggersdr0 < 101 && JpsiTriggersdr1 <101)||(PsiPTriggersdr0 <101 && PsiPTriggersdr1 <101)||(LMNTTriggersdr0< 101 && LMNTTriggersdr1< 101))"

def GetInputFiles(self):
    Args=self.cfg['args']
    path0="/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/"
    path  = path0+"AfterBDT_Training_noPhimass_{}/".format(Args.Year)
    path3 = path0+"private_sample/"

    self.cfg['allBins']      = ["belowJpsiA", "belowJpsiB", "belowJpsiC", "betweenPeaks", "summaryLowQ2"]
    if Args.Year==2016:
        self.cfg['dataFilePath'] = [path+"sel_Combine_2016_Mini_Presel_data_cut_bdt-Correction-s04.root/tree"]
        self.cfg['sigMC']        = [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2016M" in File]
        self.cfg['genOff']={'PhiMuMu':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2016" in File],
                            'JpsiPhi':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2016MC_Official" in File],
                            'PsiPhi': [path+File+"/gentree" for File in os.listdir(path) if "sel_BsToPsiPhi_2016MC_Official" in File],
                            'KstarMuMu':[path+File+"/gentree" for File in os.listdir(path) if "sel_BdTokstarMuMu_2016MC_Official" in File]}
        self.cfg['genonly']      = {'PhiMuMu': [path3+"sel_BsToPhiMuMu_2016MC_Nofilter_mc.lite_genonly.root/gentree"]+[path3+"sel_BsToPhiMuMu_NofilterMC_signal_2017_mc.lite_genonly.root/gentree"]+[path3+"sel_BsToPhiMuMu_NofilterMC_signal_2018_mc.lite_genonly.root/gentree"],
                                    'JpsiPhi': [path3+"sel_BsToJpsiPhi_2016_mc_genonly_s0.root/gentree"],
                                    'PsiPhi' : [path3+"sel_BsToPsiPhi_2016_mc_genonly_s0.root/gentree"]}
        self.cfg['peaking']    ={'KstarMuMu': [path+File+"/tree" for File in os.listdir(path) if "sel_BdTokstarMuMu_2016MC_Official" in File],
                                 'JpsiKstar': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToJpsikstar_2016MC_Official" in File],
                                 'PsiKstar' : []}
        self.cfg['control']    =  {'JpsiPhi': [path+File+"/tree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2016MC_Official" in File],
                                   'PsiPhi' : [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPsiPhi_2016MC_Official" in File] }
    if Args.Year==2017:
        self.cfg['dataFilePath'] = [path+"sel_Combine_2017_Mini_Presel_data_cut_bdt-Correction-s04.root/tree"]
        self.cfg['sigMC']        = [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2017M" in File] 
        self.cfg['genOff']={'PhiMuMu':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2017" in File],
                            'JpsiPhi':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2017MC_Official" in File],
                            'PsiPhi':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToPsiPhi_2017MC_Official" in File],
                            'KstarMuMu':[path+File+"/gentree" for File in os.listdir(path) if "sel_BdTokstarMuMu_2017MC_Official" in File]}
        self.cfg['genonly']      = {'PhiMuMu': [path3+"sel_BsToPhiMuMu_2016MC_Nofilter_mc.lite_genonly.root/gentree"]+[path3+"sel_BsToPhiMuMu_NofilterMC_signal_2017_mc.lite_genonly.root/gentree"]+[path3+"sel_BsToPhiMuMu_NofilterMC_signal_2018_mc.lite_genonly.root/gentree"],
                                    'JpsiPhi': [path3+"sel_BsToJpsiPhi_2017_mc_genonly_s0.root/gentree"],
                                    'PsiPhi' : [path3+"sel_BsToPsiPhi_2017_mc_genonly_s0.root/gentree"]}
        self.cfg['peaking']    ={'KstarMuMu':[path+File+"/tree" for File in os.listdir(path) if "sel_BdTokstarMuMu_2017MC_Official" in File],
                                 'JpsiKstar': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToJpsikstar_2017MC_Official" in File],
                                 'PsiKstar' : [path+File+"/tree" for File in os.listdir(path) if "sel_BdToPsiKstar_2017MC_Official" in File]}
        self.cfg['control']     = {'JpsiPhi': [path+File+"/tree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2017MC_Official" in File],
                                   'PsiPhi' : [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPsiPhi_2017MC_Official" in File] }

    if Args.Year==2018:
        self.cfg['dataFilePath'] = [path+"sel_Combine_2018_Mini_Presel_data_cut_bdt-Correction-s04.root/tree"]
        self.cfg['sigMC']        = [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2018M" in File] 
        self.cfg['genOff']={'PhiMuMu':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToPhiMuMu_OfficialMC_signal_2018" in File],
                            'JpsiPhi':[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2018MC_Official" in File],
                            'PsiPhi' :[path+File+"/gentree" for File in os.listdir(path) if "sel_BsToPsiPhi_2018MC_Official" in File],
                            'KstarMuMu':[path+File+"/gentree" for File in os.listdir(path) if "sel_BdTokstarMuMu_2018MC_Official" in File]}
        self.cfg['genonly']      = {'PhiMuMu': [path3+"sel_BsToPhiMuMu_2016MC_Nofilter_mc.lite_genonly.root/gentree"]+[path3+"sel_BsToPhiMuMu_NofilterMC_signal_2017_mc.lite_genonly.root/gentree"]+[path3+"sel_BsToPhiMuMu_NofilterMC_signal_2018_mc.lite_genonly.root/gentree"],
                                    'JpsiPhi': [path3+"sel_BsToJpsiPhi_2018_mc_genonly_s0.root/gentree"],
                                    'PsiPhi' : [path3+"sel_BsToPsiPhi_2018_mc_genonly_s0.root/gentree"]}
        self.cfg['peaking']    ={'KstarMuMu':[path+File+"/tree" for File in os.listdir(path) if "sel_BdTokstarMuMu_2018MC_Official" in File],
                                 'JpsiKstar': [path+File+"/tree" for File in os.listdir(path) if "sel_BdToJpsikstar_2018MC_Official" in File],
                                 'PsiKstar' : [path+File+"/tree" for File in os.listdir(path) if "sel_BdToPsiKstar_2018MC_Official" in File]}
        self.cfg['control']     = {'JpsiPhi': [path+File+"/tree" for File in os.listdir(path) if "sel_BsToJpsiPhi_2018MC_Official" in File],
                                   'PsiPhi' : [path+File+"/tree" for File in os.listdir(path) if "sel_BsToPsiPhi_2018MC_Official" in File] }

    # Cut strings
    cut_passTrigger = "JpsiTriggers > 0 || PsiPTriggers > 0 || LMNTTriggers > 0"
    cut_resonanceRej = "(Mumumass > 3.0969+3.5*Mumumasserr || Mumumass < 3.0969-5.5*Mumumasserr) && (Mumumass > 3.6861+3.5*Mumumasserr || Mumumass < 3.6861-3.5*Mumumasserr)"
    cut_resonanceSel = "(Mumumass > 3.0969+2.5*Mumumasserr || Mumumass < 3.0969-2.5*Mumumasserr) && (Mumumass > 3.6861+3.0*Mumumasserr || Mumumass < 3.6861-3.0*Mumumasserr)"
    cut_antiRadiation = "abs(Bmass-Mumumass-2.270)>0.120 && abs(Bmass-Mumumass-1.681)>0.090"
    cut_phiWindow = "Phimass>1.0 && Phimass < 1.04"

    if Args.Year==2016:
        cut_Bdt = "Bdt > 0.56"
    if Args.Year==2017:
        cut_Bdt = "Bdt > 0.56"
    if Args.Year==2018:
        cut_Bdt = "Bdt > 0.52"
    cuts = [
        cut_passTrigger,
        #cut_phiWindow,
        cut_antiRadiation,
        cut_Bdt,
        recBaseSel,
    ]
    cuts.append("({0})".format(")&&(".join(cuts)))
    cuts_noResVeto = "({0})&&({1})".format(cut_passTrigger, cut_Bdt)
    cuts_Signal = "({0}) && (({1}) && ({2}))".format(cuts_noResVeto, cut_resonanceRej, cut_antiRadiation)
    cuts_antiSignal = "({0}) && !(({1}) && ({2}))".format(cuts_noResVeto, cut_resonanceRej, cut_antiRadiation)
    #cuts_antiResVeto = "({0}) && !({1}) && !({2})".format(cuts_noResVeto, cut_resonanceSel, cut_antiRadiation)
    cuts_antiResVeto = "({0}) && ({1}) && !({2})".format(cut_passTrigger, 1, cut_resonanceSel)
    self.cfg['cuts'] = cuts
    self.cfg['cuts_antiResVeto'] = cuts_antiResVeto
    self.cfg['cuts_Signal'] = cuts_Signal


def MCLumiCalc(self):
    '''K*mumu MC sample Lumi Calculation'''
    Args=self.cfg['args']
    if Args.Year==2016:
        Events = 113766386.
        FiltEff = 0.000365
        Xsec = 5.68e10
        BF = 9.4e-7
        DBF = 1. #0.489
        return Events / (FiltEff*Xsec*BF*DBF)
    if Args.Year==2017:
        Events = 127500766.
        FiltEff = 0.02833
        Xsec = 5.367e8
        BF = 9.4e-7
        DBF = 1. #0.489
        return Events / (FiltEff*Xsec*BF*DBF)
    if Args.Year==2018:
        Events = 115851869.
        FiltEff = 0.02833
        Xsec = 5.367e8
        BF = 9.4e-7
        DBF = 1. #0.489
        return Events / (FiltEff*Xsec*BF*DBF)

def GetPeakingFraction(self):
    """Getting a fraction of a Bd->K*0mumu with respect to signal mode"""
    from BsToPhiMuMuFitter.anaSetup import q2bins
    import ROOT
    import json
    from math import sqrt
    from filelock import Timeout, FileLock

    def ReadJson(ifile):
        if os.path.exists(ifile):
            rfile = open(ifile, 'r')
            try:
                return json.load(rfile)
            except:
                return {} #Exception probably due to non-JSON file
            rfile.close()
        else:
            return {}

    def LockRefreshAndWrite(ifile, data):
        lock_path = ifile+".lock"
        lock = FileLock(lock_path, timeout=50)
        lock.acquire()
        try:
            olddata = ReadJson(ifile)
            rfile = open(ifile, 'w')
            json.dump({**olddata, **data}, rfile, indent=2)
        finally:
            rfile.close()
            lock.release()
            os.remove(lock_path)

    ifile = "TotalEffValues.json"
    data = ReadJson(ifile)

    binkey = self.process.cfg['binKey']
    if binkey in data.keys():
        if 'ratio' in data[binkey].keys(): 
            if type(data[binkey]['ratio']) is float:
                return data[binkey]['ratio']
            else:
                return data[binkey]['ratio']['getVal']
    else:
        PeakNum = self.process.cfg['peaking']['KstarMuMu']
        PeakDen = self.process.cfg['genOff']['KstarMuMu']
        sigNum = self.process.cfg['sigMC']
        sigDen = self.process.cfg['genOff']['PhiMuMu']
        def GetTree(File):
            ch = ROOT.TChain()
            for f in File: ch.Add(f)
            return ch
        gensel = genSel + " && " + q2bins[binkey]['cutString'].replace('Q2', 'genQ2')
        finalcut = self.process.cfg['cuts'][-1] + " && " + q2bins[binkey]['cutString']
        print (gensel)
        print (finalcut)
        data[binkey]={}
        for val in ['PeakNum', 'PeakDen', 'sigNum', 'sigDen', 'ratio']: data[binkey][val]={}
        data[binkey]['PeakNum']['getVal'] = a = GetTree(PeakNum).GetEntries(finalcut)
        data[binkey]['PeakDen']['getVal'] = b = GetTree(PeakDen).GetEntries(gensel)
        data[binkey]['sigNum']['getVal'] = c = GetTree(sigNum).GetEntries(finalcut)
        data[binkey]['sigDen']['getVal'] = d = GetTree(sigDen).GetEntries(gensel)
        data[binkey]['genSel'] = gensel
        data[binkey]['finSel'] = finalcut
        for key in ['PeakNum', 'PeakDen', 'sigNum', 'sigDen']:
            data[binkey][key]['getError'] = 1/sqrt(data[binkey][key]['getVal'])
        data[binkey]['ratio']['getVal'] = (a/b)/(c/d)
        LockRefreshAndWrite(ifile, data)
        return (a/b)/(c/d) 