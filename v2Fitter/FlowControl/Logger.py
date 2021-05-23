#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Description     : MessageLogger service
# Author          : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
# Last Modified   : 20 Feb 2019 19:25 00:10

from v2Fitter.FlowControl.Service import Service

import os, sys
from enum import IntEnum
from functools import partial
from datetime import datetime

class VerbosityLevels(IntEnum):
    """Verbosity levels for message logger."""
    DEBUG = 999
    INFO = 0
    WARNING = -1
    ERROR = -2
    SILENT = -999
    DEFAULT = 0

class partialmethod(partial):
    """Stolen from https://gist.github.com/carymrobbins/8940382"""
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

class Logger(Service):
    """A message logger."""
    def __init__(self, logfilename=None, verbosityLevel=VerbosityLevels.DEFAULT):
        Service.__init__(self)
        if logfilename is None:
            self._logmethod = self.logPrint
        else:
            self._logmethod = self.logWrite
            self._logfilename = logfilename
        self.verbosityLevel = verbosityLevel
        self.SetTimeStamp = True

    def _endSeq(self):
        if hasattr(self, "_logfile"):
            self.logDEBUG("Close logger service for", self._logfile.name)
            self._logfile.close()

    def _compileMsg(self, msg, lv):
        """Compose message"""
        if type(msg) is tuple:
            arg_strings = []
            for value in msg: arg_strings.append(value.__str__())
            msg = " ".join(arg_strings)
        if self.SetTimeStamp:
            return "%s %s\t: %s\n"%(datetime.utcnow().strftime("UTC %d-%m-%Y %H:%M:%S"), lv.name, msg)
        else:
            return msg+"\n"

    def setAbsLogfileDir(self, dirname):
        """ In case you want to specify the directory """
        if os.path.isabs(dirname):
            self.dirname = dirname

    def logPrint(self, msg, lv):
        """Print to stdout"""
        name = lv.name
        if lv.name=='INFO' :  name = '\033[0;34;47m'+lv.name+'\033[0m'
        if lv.name=='WARNING':name = '\033[1;43m'+lv.name+'\033[1;m'
        if lv.name=='DEBUG':  name = '\033[1;41m'+lv.name+'\033[1;m'
        print(self._compileMsg(msg, lv).replace(lv.name, name))

    def logWrite(self, msg, lv):
        """Write down a log"""
        if not hasattr(self, "_logfile"):
            if hasattr(self, 'filedir'):
                if not os.path.isdir(self.filedir):
                    os.mkdir(self.filedir)
                self._logfile = open(os.path.join(self.filedir, self._logfilename), mode='w+', encoding='utf-8')
            else:
                self._logfile = open(self._logfilename, mode='w+', encoding='utf-8')
        self._logfile.write(self._compileMsg(msg, lv=lv))
        self._logfile.flush()
        if '--debug' in sys.argv: self.logPrint(msg, lv)

    def _logDefine(self, *msg, lv, Stamp=True):
        """Define a function to keep a log at given level"""
        self.SetTimeStamp = Stamp
        if self.verbosityLevel >= lv:
            self._logmethod(msg, lv)

    logINFO = partialmethod(_logDefine, lv=VerbosityLevels.INFO)
    logWARNING = partialmethod(_logDefine, lv=VerbosityLevels.WARNING)
    logERROR = partialmethod(_logDefine, lv=VerbosityLevels.ERROR)
    logDEBUG = partialmethod(_logDefine, lv=VerbosityLevels.DEBUG)
