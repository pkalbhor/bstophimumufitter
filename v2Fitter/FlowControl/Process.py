#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

from __future__ import print_function

import os, pdb
from collections import OrderedDict
from v2Fitter.FlowControl.Logger import Logger
from v2Fitter.FlowControl.SourceManager import SourceManager, FileManager
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer
from BsToPhiMuMuFitter.anaSetup import modulePath

import ROOT

class Process:
    """A unit of a run-able job."""
    def __init__(self, name="myProcess", work_dir="testProcess", cfg=None):
        self.name = name
        self.work_dir = work_dir
        self.cwd = modulePath
        self.cfg = cfg if cfg is not None else Process.templateConfig()

        # Register services
        self._services = OrderedDict()

        self.addService('logger', Logger("runtime.log"))
        self.addService('filemanager', FileManager())
        self.addService('sourcemanager', SourceManager())

    def __str__(self):
        return self._sequence.__str__()

    def reset(self):
        pass

    @classmethod
    def templateConfig(cls):
        cfg = {}
        return cfg

    def setSequence(self, seq):
        """Define a sequence of path to be run."""
        self._sequence = seq
        for seq_obj in self._sequence: # Loops over all the object contained in the sequence
            seq_obj.hookProcess(self)  # Find hookProcess method in respective Class(of that seq_obj) 

    def addService(self, name, obj):
        """Put object to the dictionary of services."""
        if name in self._services.keys() and name !="logger":
            print("WARNING\t: NOT Overwritting service with key={0}".format(name))
            return 0
        elif name in self._services.keys() and name =="logger":
            print("WARNING\t: Overwritting service with key={0}".format(name))
        setattr(self, name, obj)
        self._services[name] = obj

    def getService(self, name):
        """Get object from the dictionary of services."""
        try:
            return self._services[name]
        except KeyError:
            self.logger.logERROR("No service labelled with {0} is found.".format(name))

    def beginSeq_registerServices(self):
        """Initialize all services."""
        if not 'dbplayer' in self._services.keys(): 
            dbplayer = FitDBPlayer(absInputDir=os.path.join(modulePath, self.work_dir))
            self.addService("dbplayer", dbplayer)
        self.addService('logger', Logger("runtime.log"))
        self.addService('filemanager', FileManager())
        self.addService('sourcemanager', SourceManager())

        for seq_obj in self._sequence:
            if seq_obj.logger is None: setattr(seq_obj, "logger", self.logger)
        for key, s in self._services.items():
            setattr(s, "process", self)
            if s.logger is None:
                setattr(s, "logger", self.logger)
            s._beginSeq()

    def beginSeq(self):
        """Initialize all services. Start logging."""
        if not os.path.exists(os.path.join(self.cwd, self.work_dir)):
            os.makedirs(self.work_dir)
        os.chdir(os.path.join(self.cwd, self.work_dir))
        self.beginSeq_registerServices()
        ROOT.gRandom.SetSeed(0)
        self.logger.logINFO("New process initialized with random seed {0}".format(ROOT.gRandom.GetSeed()))

    def runSeq(self):
        """Run all path. Process.runSeq() MainProcess"""
        print(">>>> MainProcess-> Object: ", self.cfg['args'].seqKey, " Bin: ", self.cfg['binKey'])
        for seq_obj in self._sequence:
            print (">> Entering Path: {0}".format(seq_obj.cfg['name']))
            self.logger.logDEBUG("Entering Path: {0}".format(seq_obj.cfg['name']))
            seq_obj.customize()
            seq_obj._runPath()
            seq_obj._addSource()

    def endSeq(self):
        """Terminate all services in a reversed order."""
        while self._services:
            key, s = self._services.popitem(True)
            self.logger.logDEBUG("Entering endSeq: {0}".format(key))
            s._endSeq()
        os.chdir(self.cwd)
