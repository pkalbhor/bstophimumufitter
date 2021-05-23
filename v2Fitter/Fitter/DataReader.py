#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

# Description     : Creating RooDataSet for fitting
# Author          : Pritam Kalbhor (physics.pritam@gmail.com)
# Original Author : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
# Last Modified   : 04 Aug 2020 19:06 17:36

from v2Fitter.FlowControl.Path import Path

import os, pdb, tempfile
from copy import deepcopy
import ROOT
from ROOT import TChain
from ROOT import TIter
from ROOT import RooDataSet

class DataReader(Path):
    """Create RooDataSet from a TChain"""
    def __init__(self, cfg):
        """Init"""
        super(DataReader, self).__init__(cfg)
        self.argset = cfg['argset']
        self.reset()
        return

    def reset(self):
        super(DataReader, self).reset()
        self.ch = None
        self.friend = None
        self.dataset = {}

    def __str__(self):
        list_of_files = self.ch.GetListOfFiles()
        next_file = TIter(list_of_files)
        self.logger.logDEBUG("Input file list is given below.")
        self.logger.logDEBUG("Absolute path: ", os.path.dirname(next_file.GetTitle()))
        ifile = next_file.Begin()
        for f in range(list_of_files.GetEntries()):
            self.logger.logDEBUG("\t{0}".format(os.path.basename(ifile.GetTitle())), Stamp=False)
            ifile = next_file.Next()
        self.logger.logDEBUG("End of the input file list.")
        return 1

    @classmethod
    def templateConfig(cls):
        cfg = {
            'name': "DataReader",
            'ifile': [],
            'ifriend': [],
            'ifriendIndex': ["Run", "Event"],
            'argset': [],
            'dataset': [],
            'preloadFile': None,
        }
        return cfg

    def createDataSet(self, dname, dcut):
        """Return named dataset, create if not exist"""
        if dname in self.dataset.keys() and not self.process.cfg['args'].force:
            self.logger.logINFO("\033[0;34;47m Dataset: ", dname, " Already Exists! \033[0m. Total Entries:",  self.dataset[dname].sumEntries())
            self.logger.logDEBUG(dcut, Stamp=False)
            return 1
        tempfile_preload = ROOT.TFile(tempfile.gettempdir()+"/temp.root", 'RECREATE') #Pritam
        RooCut = ROOT.RooFit.Cut(dcut)
        Import = ROOT.RooFit.Import(self.ch)
        Range  = ROOT.RooFit.CutRange(dname.split(".")[2]) # Not taking effect, need review
        Weight = ROOT.RooFit.WeightVar(self.cfg['weight'])
        if self.argset.find("Bmass"): self.argset.find("Bmass").removeRange() # Analysis specific line introduced
        if "dataReader" in dname or "sigMCGENReader" in dname:
            data = RooDataSet(dname, "", self.argset, Import, RooCut, Range)
        else:
            data = RooDataSet(dname, "Weighted dataset", self.argset, Import, RooCut, Range, Weight)

        if self.argset.find("Phimass"): 
            self.argset.find("Phimass").setBins(20)
            datahist = ROOT.RooDataHist(dname+".hist", "", ROOT.RooArgSet(self.argset.find("Phimass")), data)
            self.dataset[dname+".hist"] = deepcopy(datahist)
        data.Write()
        self.dataset[dname] = deepcopy(data)
        self.logger.logINFO("\033[0;34;47m Creating Dataset: ", dname, ": \033[0m. Total Entries:", data.sumEntries())
        self.logger.logDEBUG(dcut, Stamp=False)
        tempfile_preload.Close() #Pritam
        return 1

    def createDataSets(self, dataset):
        """Get named dataset"""
        for name, cut in dataset:
            if self.cfg['preloadFile'] and os.path.exists(self.cfg['preloadFile']):
                file_preload = ROOT.TFile(self.cfg['preloadFile'])
                data = file_preload.Get(name)
                datahist = file_preload.Get(name+'.hist')
                if not data == None:
                    self.dataset[name] = deepcopy(data)
                    if self.argset.find("Phimass"): self.dataset[name+'.hist'] = deepcopy(datahist)
                file_preload.Close()
            self.createDataSet(name, cut)
        return self.dataset
    
    def _runPath(self):
        self.ch = TChain()
        print("Name: ", self.cfg['name'])
        for f in self.cfg['ifile']:
            self.ch.Add(f)
        if len(self.cfg['ifriend']) > 0:
            self.friend = TChain("tree")
            for f in self.cfg['ifriend']:
                self.friend.Add(f)
            self.friend.BuildIndex(*self.cfg['ifriendIndex'])
            self.ch.AddFriend(self.friend)
        self.createDataSets(self.cfg['dataset'])
        self.__str__()
        pass

    def _addSource(self):
        """Add dataset and arguments to source pool"""
        if self.cfg['preloadFile'] and not os.path.exists(self.cfg['preloadFile']):
            file_out = ROOT.TFile.Open(self.cfg['preloadFile'], 'RECREATE')
            for dname, d in self.dataset.items():
                d.Write()
            file_out.Close()
        elif os.path.exists(self.cfg['preloadFile']):
            file_out = ROOT.TFile(self.cfg['preloadFile'], 'UPDATE')
            for dname, d in self.dataset.items():
                if file_out.Get(dname) and self.process.cfg['args'].force: 
                    file_out.Delete(dname+';*')     # Delete old objects if exists
                    file_out.Delete('ProcessID*;*') # Delete old Pids if exists
                    d.Write()
                elif not file_out.Get(dname):
                    print("Freshly booking an object")
                    d.Write()
            file_out.Close()
           
        if not 'source' in self.cfg.keys():
            self.cfg['source'] = {}
        #self.cfg['source']['{0}.tree'.format(self.name)] = self.ch
        self.cfg['source']['{0}.argset'.format(self.name)] = self.argset
        if len(self.cfg['ifriend']) > 0:
            self.cfg['source']['{0}.friend'.format(self.name)] = self.friend
        for dname, d in self.dataset.items():
            self.cfg['source'][dname] = d
            self.logger.logINFO("{0} events in {1}.".format(d.sumEntries(), dname))
        super(DataReader, self)._addSource()
