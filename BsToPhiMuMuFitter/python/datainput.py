#UnfilteredMC = ["/afs/cern.ch/work/p/pkalbhor/BFitter/BPhysicsData/data_v6/sel_BsToPhiMuMu_NofilterMC_signal_2016_mc.lite_genonly.root/tree"]

SubSample=False
if SubSample:
    sigMC=["/eos/user/p/pkalbhor/BPData/data_v8/subsamples/Splited-MC_BsToPhiMuMu-2016_{Total}_part{Part}.root/newtree"] 
else: 
    sigMC=["/eos/user/p/pkalbhor/BPData/data_v8/sel_BsToPhiMuMu_OfficialMC_signal_2016Mini_combine_Presel_mc.lite_cut_bdt.root/tree"]

#    sigMC=["/eos/user/p/pkalbhor/BPData/data_v7/sel_BsToPhiMuMu_OfficialMC_signal_2016_Jpsi_Psi_mc.lite_cut_bdt_addgentree.root/tree", "/eos/user/p/pkalbhor/BPData/data_v7/sel_BsToPhiMuMu_OfficialMC_signal_2016_Presel_mc.lite_cut_bdt_genadded.root/tree"]
#dataFilePath = ["/afs/cern.ch/work/p/pkalbhor/public/Modified_sel_BsToPhiMuMu_2016_Rereco07Aug17_Presel_data_cut_bdt_s0.root/events"]   
dataFilePath = ["/eos/user/p/pkalbhor/BPData/data_v8/sel_Combine_2016_Mini_Presel_data_cut_bdt.root/tree"]   
UnfilteredMC = ["/afs/cern.ch/work/p/pkalbhor/public/Modified_sel_BsToPhiMuMu_NofilterMC_signal_2016_mc.lite_nocut.root/events"]        #Nairit Using This

# Using this
# sigMC = ["/afs/cern.ch/work/p/pkalbhor/BFitter/BPhysicsData/data_v5/Modified_sel_BsToPhiMuMu_2016MC_combined_Presel_mc.lite_cut_bdt.root/events"] #Was Using this initially


