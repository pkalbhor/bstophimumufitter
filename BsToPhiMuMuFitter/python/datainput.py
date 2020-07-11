import os
import subprocess

allBins = ["belowJpsiA", "belowJpsiB", "belowJpsiC", "betweenPeaks", "abovePsi2sA", "abovePsi2sB", "summary", "summaryLowQ2", "Test1", "Test2", "Test3"]

sigMC=["/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/sel_BsToPhiMuMu_OfficialMC_signal_2016Mini_Presel_mc.lite_cut_bdt-s03.root/tree"]
dataFilePath = ["/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/sel_Combine_2016_Mini_Presel_data_cut_bdt-s03.root/tree"]
UnfilteredMC = ["/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/sel_BsToPhiMuMu_2016MC_Nofilter_mc.lite_genonly.root/gentree"]       

#GITDIR=subprocess.check_output("git rev-parse --show-toplevel", shell=True).strip()

path="/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/gentree/"
sigMCD=os.listdir(path)
for i in range(len(sigMCD)):
    sigMCD[i]=path+sigMCD[i]+"/gentree"
