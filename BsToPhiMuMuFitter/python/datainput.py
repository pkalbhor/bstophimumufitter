import os
import subprocess

sigMC=["/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/sel_BsToPhiMuMu_OfficialMC_signal_2016Mini_Presel_mc.lite_cut_bdt-s01.root/tree"]
dataFilePath = ["/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/sel_Combine_2016_Mini_Presel_data_cut_bdt-s01_checktrig.root/tree"]
UnfilteredMC = ["/afs/cern.ch/work/p/pkalbhor/public/Modified_sel_BsToPhiMuMu_NofilterMC_signal_2016_mc.lite_nocut.root/events"]       

GITDIR=subprocess.check_output("git rev-parse --show-toplevel", shell=True).strip()

path="/eos/home-c/ckar/BSTOPHIMUMU/FileForGroup/gentree/"
sigMCD=os.listdir(path)
for i in range(len(sigMCD)):
    sigMCD[i]=path+sigMCD[i]+"/gentree"


