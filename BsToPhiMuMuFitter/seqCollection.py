#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=1 fdn=3 ft=python et:

import sys
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.toyCollection as toyCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection

from BsToPhiMuMuFitter.StdProcess import p
import pdb

# Standard fitting procedures
predefined_sequence = {}
loadData        = predefined_sequence['loadData'] = [dataCollection.dataReader]
buildAllPdfs    = predefined_sequence['buildAllPdfs'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, pdfCollection.stdPDFBuilder]
buildEfficiecyHist = predefined_sequence['buildEfficiecyHist'] = [dataCollection.effiHistReader]

fitEfficiency   = predefined_sequence['fitEfficiency'] = [dataCollection.effiHistReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter]
fitSigM         = predefined_sequence['fitSigM'] = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sigMFitter]
fitBkgCombA     = predefined_sequence['fitBkgCombA'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.bkgCombAFitter]
fitFinal3D      = predefined_sequence['fitFinal3D'] = [dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.finalFitter]

stdFit          = predefined_sequence['stdFit'] = [dataCollection.effiHistReader, dataCollection.sigMCReader, dataCollection.dataReader, pdfCollection.stdWspaceReader, fitCollection.effiFitter, fitCollection.sigMFitter, fitCollection.bkgCombAFitter, fitCollection.sig2DFitter, dataCollection.sigMCGENReader, fitCollection.sigAFitter, fitCollection.finalFitter]

# For fitter validation and syst
fitSig2D        = predefined_sequence['fitSig2D'] = [dataCollection.sigMCReader, pdfCollection.stdWspaceReader, fitCollection.sig2DFitter]
fitSigMCGEN     = predefined_sequence['fitSigMCGEN'] = [dataCollection.sigMCGENReader, pdfCollection.stdWspaceReader, fitCollection.sigAFitter]

predefined_sequence['fitMCGEN'] = [dataCollection.sigMCGENReader, pdfCollection.stdWspaceReader, fitCollection.sigGENFitter]

if __name__ == '__main__':
    FitSequence = [fitSigMCGEN] #[fitEfficiency, fitSig2D, fitSigMCGEN]
    binKey = [sys.argv[1]]
    for sequence in FitSequence:
        for b in binKey:
            p.cfg['binKey'] = b
            p.setSequence(sequence)
            # p.setSequence(predefined_sequence['buildEfficiecyHist'])
            # p.setSequence(predefined_sequence['fitBkgCombA'])
            # p.setSequence(predefined_sequence['fitFinal3D'])
            # p.setSequence(predefined_sequence['fitSigM'])
            # p.setSequence(predefined_sequence['stdFit'])
            # p.setSequence(predefined_sequence['fitMCGEN'])
            try:
                p.beginSeq()
                p.runSeq()
            finally:
                p.endSeq()
