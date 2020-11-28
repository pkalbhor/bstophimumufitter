#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdn=3 ft=python et:

# Description     : Define PDFs
# Author          : Pritam Kalbhor (physics.pritam@gmail.com)
# Original Author : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
#                   Last Modified   : 02 Aug 2020 12:04 01:26

############
# WARNINGS #
############
# Dont call TObject.Print(), it seems the iterators leads to random crash
# In RooWorkspace.factory(), you MUST replace the calculation between numbers to a single float number, e.g. 2/3 -> 0.666667
# It is possible that the parser don't designed to handle RooAddition and RooProduct between RooConstVar

import types, sys, pdb
import functools
from copy import copy, deepcopy
from collections import OrderedDict

from v2Fitter.Fitter.ObjProvider import ObjProvider
from v2Fitter.Fitter.WspaceReader import WspaceReader

from BsToPhiMuMuFitter.StdProcess import isDEBUG
from BsToPhiMuMuFitter.anaSetup import modulePath, q2bins
from BsToPhiMuMuFitter.varCollection import Bmass, CosThetaK, CosThetaL, Phimass
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
#from __main__ import args as Args
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import RooWorkspace, RooEffProd, RooKeysPdf

#from BsToPhiMuMuFitter.StdProcess import p

def getWspace(self):
    """Read workspace"""
    wspaceName = "wspace.{0}.{1}".format(self.process.cfg['args'].Year, self.cfg.get("wspaceTag", "DEFAULT"))
    if wspaceName in self.process.sourcemanager.keys():
        wspace = self.process.sourcemanager.get(wspaceName)
    else:
        if not isDEBUG:
            self.logger.logERROR("RooWorkspace '{0}' not found".format(wspaceName))
            self.logger.logDEBUG("Please access RooWorkspace with WspaceReader")
            raise RuntimeError
        wspace = RooWorkspace(wspaceName)
        self.process.sourcemanager.update(wspaceName, wspace)
    wspace.addClassDeclImportDir(modulePath) #+ '/cpp')
    wspace.addClassImplImportDir(modulePath) #+ '/cpp')
    return wspace


#ObjProvider.getWspace = types.MethodType(getWspace, ObjProvider)
setattr(ObjProvider, 'getWspace', getWspace) 

#########################
# Now start define PDFs #
#########################


def buildGenericObj(self, objName, factoryCmd, varNames, CopyObj=None):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()
    tspace = None
    obj = wspace.obj(objName)
    def InFactory(wspace):
        for v in varNames:
            if wspace.obj(v) == None:
                getattr(wspace, 'import')(globals()[v])  #Import CosThetaK and CosThetaL 
        for cmdIdx, cmd in enumerate(factoryCmd):
            wspace.factory(cmd)
    if obj == None:
        self.logger.logINFO("Build {0} from scratch.".format(objName))
        InFactory(wspace)
        obj = wspace.obj(objName)
    elif objName=='effi_sigA':
        tspace = RooWorkspace('TempWorkSpace')
        InFactory(tspace)

    if CopyObj is not None:
        for suffix, Obj in CopyObj:
            if not tspace==None:
                getattr(wspace, 'import')(tspace.obj(Obj), ROOT.RooFit.RenameAllNodes(suffix), ROOT.RooFit.RenameAllVariablesExcept(suffix, 'Bmass,CosThetaL,CosThetaK'))
            else:
                getattr(wspace, 'import')(wspace.obj(Obj), ROOT.RooFit.RenameAllNodes(suffix), ROOT.RooFit.RenameAllVariablesExcept(suffix, 'Bmass,CosThetaL,CosThetaK'))
            self.cfg['source'][Obj+'_'+suffix]=wspace.obj(Obj+'_'+suffix)
    del tspace
    self.cfg['source'][objName] = obj

#======================================================================================================
from BsToPhiMuMuFitter.python.pdfDicts import f_effiSigA_format
def GetEffiSigAList(self):
    Args=self.process.cfg['args']
    if Args.Year==2016:
        f_effiSigA_format['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_format['belowJpsiA']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2'] #['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['belowJpsiB']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2'] #['Poly6_Poly6_XTerm']
        f_effiSigA_format['belowJpsiC']   = f_effiSigA_format['Poly9_Poly8_XTerm']
        f_effiSigA_format['betweenPeaks'] = f_effiSigA_format['Poly7_Poly6_XTerm']
        f_effiSigA_format['summaryLowQ2'] = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']

    if Args.Year==2017:
        f_effiSigA_format['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_format['belowJpsiA']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['belowJpsiB']   = f_effiSigA_format['Poly9_Poly6_XTerm']
        f_effiSigA_format['summaryLowQ2'] = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']

    if Args.Year==2018:
        f_effiSigA_format['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_format['belowJpsiA']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['belowJpsiB']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['summaryLowQ2'] = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
    return f_effiSigA_format.get(self.process.cfg['binKey'], f_effiSigA_format['DEFAULT'])

setupBuildEffiSigA = {
    'objName': "effi_sigA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [  ],
    'CopyObj': [('ts', 'effi_sigA'), ('ts', 'effi_cosl'), ('ts', 'effi_cosK')]
}

def Get_AccEff_List(self):
    Args=self.process.cfg['args']
    f_effiSigA_Acc={} # In order to avoid taking previously set `f_effiSigA_format` dict keys   
    if Args.Year==2016:
        f_effiSigA_Acc['DEFAULT']      = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Acc['belowJpsiA']   = f_effiSigA_format['Poly8_Poly8_XTerm']
        f_effiSigA_Acc['belowJpsiB']   = f_effiSigA_format['Poly9_Poly6_XTerm']
        f_effiSigA_Acc['belowJpsiC']   = f_effiSigA_format['Poly9_Poly8_XTerm']
        f_effiSigA_Acc['betweenPeaks'] = f_effiSigA_format['Poly7_Poly6_XTerm']
        f_effiSigA_Acc['summaryLowQ2'] = f_effiSigA_format['Poly7_Poly7_XTerm']

    if Args.Year==2017:
        f_effiSigA_Acc['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_Acc['belowJpsiA']   = f_effiSigA_format['Poly7_Poly7_XTerm']
        f_effiSigA_Acc['belowJpsiB']   = f_effiSigA_format['Poly7_Poly7_XTerm']
        f_effiSigA_Acc['summaryLowQ2'] = f_effiSigA_format['Poly7_Poly7_XTerm']

    if Args.Year==2018:
        f_effiSigA_Acc['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_Acc['belowJpsiA']   = f_effiSigA_format['Poly7_Poly7_XTerm']
        f_effiSigA_Acc['belowJpsiB']   = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Acc['summaryLowQ2'] = f_effiSigA_format['Poly7_Poly7_XTerm']
    return f_effiSigA_Acc.get(self.process.cfg['binKey'], f_effiSigA_Acc['DEFAULT'])

setupBuild_accEffiSigA = {
    'objName': "effi_sigA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [  ],
    'CopyObj': [('acc', 'effi_sigA'), ('acc', 'effi_cosl'), ('acc', 'effi_cosK')]
}

def Get_RecEff_List(self):
    Args=self.process.cfg['args']
    f_effiSigA_Rec = {}
    if Args.Year==2016:
        f_effiSigA_Rec['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_Rec['belowJpsiA']   = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Rec['belowJpsiB']   = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_Rec['summaryLowQ2'] = f_effiSigA_format['Poly8_Poly6_XTerm']

    if Args.Year==2017:
        f_effiSigA_Rec['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_Rec['belowJpsiA']   = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Rec['belowJpsiB']   = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Rec['summaryLowQ2'] = f_effiSigA_format['Poly6_Poly6_XTerm']

    if Args.Year==2018:
        f_effiSigA_Rec['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_Rec['belowJpsiA']   = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Rec['belowJpsiB']   = f_effiSigA_format['Poly6_Poly6_XTerm']
        f_effiSigA_Rec['summaryLowQ2'] = f_effiSigA_format['Poly7_Poly6_XTerm']
    return f_effiSigA_Rec.get(self.process.cfg['binKey'], f_effiSigA_Rec['DEFAULT'])

setupBuild_recEffiSigA = {
    'objName': "effi_sigA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [  ],
    'CopyObj': [('rec', 'effi_sigA'), ('rec', 'effi_cosl'), ('rec', 'effi_cosK')]
}
#======================================================================================================
setupBuildSigM = {
    'objName': "f_sigM",
    'varNames': ["Bmass", "Phimass"],
    'factoryCmd': [
        "sigMGauss_mean[5.36, 5.30, 5.5]",
        "RooGaussian::f_sigMGauss1(Bmass, sigMGauss_mean, sigMGauss1_sigma[0.0284, 0.0001, 0.05])",
        "RooGaussian::f_sigMGauss2(Bmass, sigMGauss_mean, sigMGauss2_sigma[0.0667, 0.0005, 0.40])",
        "SUM::f_sigM(sigM_frac[0.7, 0.,1.]*f_sigMGauss1, f_sigMGauss2)",
        "cbs_mean[5.369, 5.28, 5.4]",
        "RooCBShape::cbs_1(Bmass, cbs_mean, cbs1_sigma[0.0268, 0.0001, 0.60], cbs1_alpha[0.89, -6.0, 6.0], cbs1_n[4, 0, 1000])",
        "RooCBShape::cbs_2(Bmass, cbs_mean, cbs2_sigma[0.0296, 0.0001, 0.60], cbs2_alpha[-0.87, -9.4, 9.6], cbs2_n[133, 0, 1000])",
        "SUM::f_sigMDCB(sigMDCB_frac[0.4, 0.0, 1.0]*cbs_1, cbs_2)",
        "SUM::f_sigM_DCBG(sigM_frac1[.5,0,1]*cbs_1, sigM_frac2[.1,0.,1.]*f_sigMGauss1, cbs_2)",

        "sigPhiMG_mean[1.01944, 1.0, 1.04]",
        "Phicbs_mean[1.01944, 1.0, 1.04]",
        "RooGaussian::f_sigPhiMG1(Phimass, sigPhiMG_mean, sigPhiMG1_sigma[0.0054, 0.0001, 0.05])",
        "RooGaussian::f_sigPhiMG2(Phimass, sigPhiMG_mean, sigPhiMG2_sigma[0.0025, 0.0005, 0.40])",
        "RooGaussian::f_sigPhiMG3(Phimass, sigPhiMG_mean, sigPhiMG3_sigma[0.0047, 0.0005, 0.40])",
        #"RooPolynomial::f_sigPhiM_Poly6(Phimass, {phim1,phim2,phim3,phim4,phim5,phim6})",
        "SUM::f_sigPhiM(sigPhiM_frac[0.8, 0.,1.]*f_sigPhiMG1, f_sigPhiMG2)",
        "SUM::f_sigPhiM3(sigPhiM3_frac1[0.3, 0.,1.]*f_sigPhiMG1, sigPhiM3_frac2[0.8,0.,1.]*f_sigPhiMG2, f_sigPhiMG3)",
        "RooCBShape::Phicbs_1(Phimass, Phicbs_mean, Phicbs1_sigma[0.00250278, 0.0001, 0.60], Phicbs1_alpha[0.756767, -6.0, 6.0], Phicbs1_n[135.7, 0, 1000])",
        "RooCBShape::Phicbs_2(Phimass, Phicbs_mean, Phicbs2_sigma[0.00266792, 0.0001, 0.60], Phicbs2_alpha[-0.514313, -9.4, 9.6], Phicbs2_n[15.21, 0, 1000])",
        "RooCBShape::Phicbs_3(Phimass, Phicbs_mean, Phicbs3_sigma[0.00266792, 0.0001, 0.60], Phicbs3_alpha[-0.514313, -9.4, 9.6], Phicbs3_n[15.21, 0, 1000])",
        "SUM::f_sigPhiM_DCB(sigPhiM_DCB_frac[0.470337, 0.0, 1.0]*Phicbs_1, Phicbs_2)",
        "SUM::f_sigPhiM_TCB(sigPhiM_TCB_frac1[0.470337, 0.0, 1.0]*Phicbs_1, sigPhiM_TCB_frac2[0.46, 0,1.]*Phicbs_2, Phicbs_3)",
        "SUM::f_sigPhiM_DCBG(sigPhiM_frac1[.5,0,1]*Phicbs_1, sigPhiM_frac2[.1,0.,1.]*f_sigPhiMG1, Phicbs_2)",
        "RooBifurGauss::f_sigPhiM_BG(Phimass, sigPhiMBG_mean[1.01974, 1.0, 1.04], sigPhiMBG_sigmaL[0.00368, 0.0001, 0.60], sigPhiMBG_sigmaR[0.00174, 0.0001, 0.60])",
    ],
    'CopyObj': [('Alt', 'f_sigM'), ('Alt', 'f_sigM_DCBG'), ('JP', 'f_sigM_DCBG'), ('JK', 'f_sigM_DCBG'), ('JK', 'f_sigMDCB'), ('PP', 'f_sigM_DCBG'), ('PK', 'f_sigM_DCBG')]
}
buildSigM = functools.partial(buildGenericObj, **setupBuildSigM)

#======================================================================================================
def buildSigA(self):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()

    f_sigA = wspace.pdf("f_sigA")
    if f_sigA == None:
        wspace.factory("unboundFl[0.6978,-3e3,3e3]")
        wspace.factory("unboundAfb[0.00,-3e4,3e4]")
        wspace.factory("expr::fl('0.5+TMath::ATan(unboundFl)/TMath::Pi()',{unboundFl})")
        wspace.factory("expr::afb('2.*(1-fl)*TMath::ATan(unboundAfb)/TMath::Pi()',{unboundAfb,fl})")
        wspace.factory("EXPR::f_sigA_original('(9.0/16.0)*((0.5*(1.0-fl)*(1.0-CosThetaK*CosThetaK)*(1.0+CosThetaL*CosThetaL)) + (2.0*fl*CosThetaK*CosThetaK*(1.0-CosThetaL*CosThetaL)) + (afb*(1.0-CosThetaK*CosThetaK)*CosThetaL))', {CosThetaK, CosThetaL, fl, afb})")
        f_sigA = ROOT.RooBtosllModel("f_sigA", "", CosThetaL, CosThetaK, wspace.var('unboundAfb'), wspace.var('unboundFl'))
        getattr(wspace, 'import')(f_sigA)
        wspace.importClassCode(ROOT.RooBtosllModel.Class())
        wspace.factory("prod::f_sigA_corrected(f_sigA, effi_sigA_acc)")
    self.cfg['source']['f_sigA'] = f_sigA
    self.cfg['source']['f_sigA_corrected'] = wspace.obj("f_sigA_corrected")

def buildSig(self):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()

    f_sig2D = wspace.obj("f_sig2D")
    f_sig3D = wspace.obj("f_sig3D")
    f_sig3D = wspace.obj("f_sig3D_Alt")
    f_sig3DAltM = wspace.obj("f_sig3DAltM")
    f_sig3DAltM_Alt = wspace.obj("f_sig3DAltM_Alt")
    wspace.factory("prod::effi_sigA_comb(effi_sigA_acc, effi_sigA_rec)")
    effi_sigA_comb = wspace.obj("effi_sigA_comb")
    if f_sig3D == None or f_sig3DAltM == None or f_sig3DAltM_Alt == None:
        for k in ['effi_sigA',  'effi_sigA_ts', 'f_sigA', 'f_sigM', 'f_sigM_Alt', 'f_sigMDCB', 'f_sigM_DCBG_Alt']:
            locals()[k] = self.cfg['source'][k] if k in self.cfg['source'] else self.process.sourcemanager.get(k)
        f_sig2D         = RooEffProd("f_sig2D", "", locals()['f_sigA'], locals()['effi_sigA'])
        f_sig2D_ts      = RooEffProd("f_sig2D_ts", "", locals()['f_sigA'], locals()['effi_sigA_ts'])
        f_sig2D_ce      = RooEffProd("f_sig2D_ce", "", locals()['f_sigA'], effi_sigA_comb) 
        getattr(wspace, 'import')(f_sig2D, ROOT.RooFit.RecycleConflictNodes())
        getattr(wspace, 'import')(f_sig2D_ts, ROOT.RooFit.RecycleConflictNodes())
        getattr(wspace, 'import')(f_sig2D_ce, ROOT.RooFit.RecycleConflictNodes())
        if wspace.obj("f_sigM") == None:
            getattr(wspace, 'import')(locals()['f_sigM'])
        if wspace.obj("f_sigM_Alt") == None:
            getattr(wspace, 'import')(locals()['f_sigM_Alt'])
        if wspace.obj("f_sigMDCB") == None:
            getattr(wspace, 'import')(locals()['f_sigMDCB'])
        if wspace.obj("f_sigM_DCBG_Alt") == None:
            getattr(wspace, 'import')(locals()['f_sigM_DCBG_Alt'])
        wspace.factory("PROD::f_sig3D(f_sigM, f_sig2D)")
        wspace.factory("PROD::f_sig3D_ts(f_sigM, f_sig2D_ts)")
        wspace.factory("PROD::f_sig3D_ce(f_sigM, f_sig2D_ce)")
        wspace.factory("PROD::f_sig3DAltM(f_sigMDCB, f_sig2D)")
        wspace.factory("PROD::f_sig3D_Alt(f_sigM_Alt, f_sig2D)")
        wspace.factory("PROD::f_sig3DAltM_Alt(f_sigM_DCBG_Alt, f_sig2D)")
        f_sig3D = wspace.pdf("f_sig3D")
        f_sig3D_ts = wspace.pdf("f_sig3D_ts")
        f_sig3D_ce = wspace.pdf("f_sig3D_ce")
        f_sig3DAltM = wspace.pdf("f_sig3DAltM")
        f_sig3D_Alt = wspace.pdf("f_sig3D_Alt")
        f_sig3DAltM_Alt = wspace.pdf("f_sig3DAltM_Alt")

    self.cfg['source']['f_sig2D']    = f_sig2D
    self.cfg['source']['f_sig2D_ts'] = f_sig2D_ts
    self.cfg['source']['f_sig2D_ce'] = f_sig2D_ce
    self.cfg['source']['f_sig3D']    = f_sig3D
    self.cfg['source']['f_sig3D_ts'] = f_sig3D_ts
    self.cfg['source']['f_sig3D_ce'] = f_sig3D_ce
    self.cfg['source']['f_sig3D_Alt'] = f_sig3D_Alt
    self.cfg['source']['f_sig3DAltM_Alt'] = f_sig3DAltM_Alt

#======================================================================================================
setupBuildBkgCombM = {
    'objName': "f_bkgCombM",
    'varNames': ["Bmass", "Phimass"],
    'factoryCmd': [
        "bkgCombM_c1[-0.1,-20,2]",
        "EXPR::f_bkgCombM('exp(bkgCombM_c1*Bmass)', {Bmass,bkgCombM_c1})",
        "EXPR::f_bkgPhiM('exp(bkgPhiM_p1*Phimass)', {Phimass, bkgPhiM_p1[0.1, -200, 200]})",
        #"EXPR::f_bkgPhiM('bkgPhiM_p1*Phimass+bkgPhiM_p2*pow(Phimass, 2)+bkgPhiM_p3*pow(Phimass,3)+bkgPhiM_p4*pow(Phimass,4)', {Phimass, bkgPhiM_p1[0.0, -20, 20], bkgPhiM_p2[0.0, -20, 20], bkgPhiM_p3[0.0, -20, 20], bkgPhiM_p4[0.0, -20, 20]})",
    ],
    'CopyObj': [('JP', 'f_bkgCombM'), ('PP', 'f_bkgCombM')]
}
buildBkgCombM = functools.partial(buildGenericObj, **setupBuildBkgCombM)

#======================================================================================================
setupBuildBkgCombMAltM = {
    'objName': "f_bkgCombMAltM",
    'varNames': ["Bmass"],
    'factoryCmd': [
        "bkgCombMAltM_c1[0.1,1e-5,10]",
        "bkgCombMAltM_c2[-5.6,-20,-4]",
        "EXPR::f_bkgCombMAltM('bkgCombMAltM_c1+pow(Bmass+bkgCombMAltM_c2,2)',{Bmass,bkgCombMAltM_c1,bkgCombMAltM_c2})",
    ],
}
buildBkgCombMAltM = functools.partial(buildGenericObj, **setupBuildBkgCombMAltM)

#======================================================================================================
from BsToPhiMuMuFitter.python.pdfDicts import f_analyticBkgCombA_format
def GetAnalyticBkgAList(self):
    Args=self.process.cfg['args']
    AltRange = Args.AltRange
    if Args.Year==2016:
        f_analyticBkgCombA_format['DEFAULT']        = f_analyticBkgCombA_format['Poly6_Poly6']
        f_analyticBkgCombA_format['belowJpsiA']     = f_analyticBkgCombA_format['Gaus3Poly4_Poly6'] #['Gaus2_Poly6'] #['Gaus3Poly4_Exp']
        f_analyticBkgCombA_format['belowJpsiB']     = f_analyticBkgCombA_format['Gaus2Poly2_Poly6'] 
        f_analyticBkgCombA_format['belowJpsiC']     = f_analyticBkgCombA_format['Poly6_Poly6' if AltRange else 'Gaus2Poly2_Poly6']
        f_analyticBkgCombA_format['betweenPeaks']   = f_analyticBkgCombA_format['Poly6_Poly4']
        f_analyticBkgCombA_format['abovePsi2s']     = f_analyticBkgCombA_format['Poly6_Poly4']
        f_analyticBkgCombA_format['summaryLowQ2']   = f_analyticBkgCombA_format['Gaus3Poly4_Poly6']
        return f_analyticBkgCombA_format.get(self.process.cfg['binKey'], f_analyticBkgCombA_format['DEFAULT'])
    if Args.Year==2017:
        f_analyticBkgCombA_format['DEFAULT']        = f_analyticBkgCombA_format['Poly6_Poly6']
        f_analyticBkgCombA_format['belowJpsiA']     = f_analyticBkgCombA_format['Gaus3_Poly4']
        f_analyticBkgCombA_format['belowJpsiB']     = f_analyticBkgCombA_format['Poly3_Poly3' if AltRange else 'Gaus3Poly4_Poly6']
        f_analyticBkgCombA_format['belowJpsiC']     = f_analyticBkgCombA_format['Poly6_Poly5']
        f_analyticBkgCombA_format['betweenPeaks']   = f_analyticBkgCombA_format['Poly6_Poly6']
        f_analyticBkgCombA_format['summaryLowQ2']   = f_analyticBkgCombA_format['Poly6_Poly4' if AltRange else 'Gaus3_Poly6']
        return f_analyticBkgCombA_format.get(self.process.cfg['binKey'], f_analyticBkgCombA_format['DEFAULT'])
    if Args.Year==2018:
        f_analyticBkgCombA_format['DEFAULT']        = f_analyticBkgCombA_format['Poly6_Poly6']
        f_analyticBkgCombA_format['belowJpsiA']     = f_analyticBkgCombA_format['Gaus2_Poly4'] #['Gaus2Poly4_Poly3']
        f_analyticBkgCombA_format['belowJpsiB']     = f_analyticBkgCombA_format['Gaus3Poly4_Poly6'] #['Gaus2Poly2_Poly6']
        f_analyticBkgCombA_format['belowJpsiC']     = f_analyticBkgCombA_format['Poly6_Poly5']
        f_analyticBkgCombA_format['summaryLowQ2']   = f_analyticBkgCombA_format['Gaus2Poly4_Poly4' if AltRange else 'Gaus3Poly4_Exp']
        return f_analyticBkgCombA_format.get(self.process.cfg['binKey'], f_analyticBkgCombA_format['DEFAULT'])
setupBuildAnalyticBkgCombA = {
    'objName': "f_bkgCombA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'CopyObj': [('Alt', 'f_bkgCombA')],
    'factoryCmd': [  ]
}
#======================================================================================================

f_analyticBkgA_KStar_format = {}
# pdfL: Poly8, pdfK: Poly8
f_analyticBkgA_KStar_format['Poly9_Poly8'] = ["bkgKStarL_c{}[-10,10]".format(i) for i in range(1, 10)] \
        + ["bkgKStarK_c{}[-10,10]".format(i) for i in range(1, 9)] \
        + ["RooPolynomial::pdfL_kst(CosThetaL, {bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarL_c5, bkgKStarL_c6, bkgKStarL_c7, bkgKStarL_c8})"] \
        + ["RooPolynomial::pdfK_kst(CosThetaK, {bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4, bkgKStarK_c5, bkgKStarK_c6, bkgKStarK_c7, bkgKStarK_c8})"] \
        + ["PROD::f_bkgA_KStar(pdfL_kst, pdfK_kst)"]
# pdfL: Poly8, pdfK: Poly8
f_analyticBkgA_KStar_format['Poly8_Poly8'] = ["bkgKStarL_c{}[-10,10]".format(i) for i in range(1, 9)] \
        + ["bkgKStarK_c{}[-10,10]".format(i) for i in range(1, 9)] \
        + ["RooPolynomial::pdfL_kst(CosThetaL, {bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarL_c5, bkgKStarL_c6, bkgKStarL_c7, bkgKStarL_c8})"] \
        + ["RooPolynomial::pdfK_kst(CosThetaK, {bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4, bkgKStarK_c5, bkgKStarK_c6, bkgKStarK_c7, bkgKStarK_c8})"] \
        + ["PROD::f_bkgA_KStar(pdfL_kst, pdfK_kst)"]
f_analyticBkgA_KStar_format['Poly4_Poly4'] = [ # pdfL: Poly4, pdfK: Poly4
    "bkgKStarL_c1[-10.,10.]", "bkgKStarL_c2[-10.,10.]", "bkgKStarL_c3[-10.,10.]", "bkgKStarL_c4[-10.,10.]",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::f_bkgA_KStar('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgKStarL_c1*CosThetaL+bkgKStarL_c2*pow(CosThetaL,2)+bkgKStarL_c3*pow(CosThetaL, 3)+bkgKStarL_c4*pow(CosThetaL,4)",
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}")
]
f_analyticBkgA_KStar_format['Poly6_Poly4'] = [ # pdfL: Poly6, pdfK: Poly4
    "bkgKStarL_c1[-10.,10.]", "bkgKStarL_c2[-10.,10.]", "bkgKStarL_c3[-10.,10.]", "bkgKStarL_c4[-10.,10.]", "bkgKStarL_c5[-10.,10.]", "bkgKStarL_c6[-10.,10.]",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::f_bkgA_KStar('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgKStarL_c1*CosThetaL+bkgKStarL_c2*pow(CosThetaL,2)+bkgKStarL_c3*pow(CosThetaL, 3)+bkgKStarL_c4*pow(CosThetaL,4)+bkgKStarL_c5*pow(CosThetaL,5)+bkgKStarL_c6*pow(CosThetaL,6)",
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarL_c5, bkgKStarL_c6, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}")
]
f_analyticBkgA_KStar_format['QuadGaus_Poly4'] = [ # pdfL: Quad + Gauss, pdfK: Poly4
    "bkgKStarL_c1[0.01,1]", "bkgKStarL_c2[0.1,20]", "bkgKStarL_c3[-1,1]", "bkgKStarL_c4[0.05,1]",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::f_bkgA_KStar('({pdfL})*({pdfK})', {args})".format(
        pdfL="1-pow(pow(CosThetaL,2)-bkgKStarL_c1,2)+bkgKStarL_c2*exp(-0.5*pow((CosThetaL-bkgKStarL_c3)/bkgKStarL_c4,2))",
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}")
]
f_analyticBkgA_KStar_format['Gaus2_Poly4'] = [ # pdfL: Gaus + Gauss, pdfK: Poly4
    "bkgKStarL_c1[-.1,-1,1]", "bkgKStarL_c2[0.18, 0.01, 2.9]", "bkgKStarL_c3[0.1,-1,1]", "bkgKStarL_c4[0.19, 0.01, 5.0]",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::f_bkgA_KStar('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgKStarL_c1*exp(-0.5*pow((CosThetaL-bkgKStarL_c3)/bkgKStarL_c2,2))+exp(-0.5*pow((CosThetaL-bkgKStarL_c3)/bkgKStarL_c4,2))",
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}")
]

f_analyticBkgA_KStar_format['Gaus2_Poly4_DM'] = [ # pdfL: Gaus + Gauss, pdfK: Poly4
    "RooGaussian::Gauss1L(CosThetaL, bkgKStarL_c1[-.5,-.5, .5], bkgKStarL_c2[.02, .0001, 4.])",
    "RooGaussian::Gauss2L(CosThetaL, bkgKStarL_c3[ .2, .0, .8], bkgKStarL_c4[.02, .0001, 4.])",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::pdfK('({pdfK})', {args})".format(
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaK, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}"),
    "SUM::Gauss2(bkgA_frac1_KStar[.1,0.,39.]*Gauss1L, Gauss2L)",
    "PROD::f_bkgA_KStar(Gauss2, pdfK)"
]
f_analyticBkgA_KStar_format['Gaus3_Poly4_DM'] = [ # pdfL: Gaus + Gauss + Gauss, pdfK: Poly4
    "RooGaussian::Gauss1L(CosThetaL, bkgKStarL_c1[ .0,-.5, .5], bkgKStarL_c2[.08, .0001, 4.])",
    "RooGaussian::Gauss2L(CosThetaL, bkgKStarL_c3[ .2,-.5, .8], bkgKStarL_c4[.08, .0001, 4.])",
    "RooGaussian::Gauss3L(CosThetaL, bkgKStarL_c5[-.01,-.7, .2], bkgKStarL_c6[.18, .0001, 4.])",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::pdfK('({pdfK})', {args})".format(
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaK, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}"),
    "SUM::Gauss3(bkgA_frac1_KStar[.1,0.,29.]*Gauss1L, bkgA_frac2_KStar[.5,0.,29.]*Gauss2L, Gauss3L)",
    "PROD::f_bkgA_KStar(Gauss3, pdfK)"
]
def GetAnalyticBkgA_KStarList(self):
    Args=self.process.cfg['args']
    AltRange=Args.AltRange
    if Args.Year==2016:
        f_analyticBkgA_KStar_format['DEFAULT']     = f_analyticBkgA_KStar_format['Gaus2_Poly4']
        f_analyticBkgA_KStar_format['belowJpsiA']  = f_analyticBkgA_KStar_format['Gaus3_Poly4_DM']
        f_analyticBkgA_KStar_format['belowJpsiB']  = f_analyticBkgA_KStar_format['Gaus3_Poly4_DM']
        f_analyticBkgA_KStar_format['belowJpsiC']  = f_analyticBkgA_KStar_format['Gaus3_Poly4_DM']
        f_analyticBkgA_KStar_format['betweenPeaks']= f_analyticBkgA_KStar_format['Poly6_Poly4']
        f_analyticBkgA_KStar_format['abovePsi2s']  = f_analyticBkgA_KStar_format['Poly6_Poly4']
        f_analyticBkgA_KStar_format['summary']     = f_analyticBkgA_KStar_format['Poly6_Poly4']
        f_analyticBkgA_KStar_format['summaryLowQ2']= f_analyticBkgA_KStar_format['Gaus3_Poly4_DM']
        return f_analyticBkgA_KStar_format.get(self.process.cfg['binKey'], f_analyticBkgA_KStar_format['DEFAULT'])
    if Args.Year==2017:
        f_analyticBkgA_KStar_format['DEFAULT']     = f_analyticBkgA_KStar_format['Gaus2_Poly4']
        f_analyticBkgA_KStar_format['belowJpsiA']  = f_analyticBkgA_KStar_format['Gaus2_Poly4_DM']
        f_analyticBkgA_KStar_format['belowJpsiB']  = f_analyticBkgA_KStar_format['Gaus3_Poly4_DM'] #['Gaus2_Poly4_DM']
        f_analyticBkgA_KStar_format['belowJpsiC']  = f_analyticBkgA_KStar_format['Gaus3_Poly4_DM']
        f_analyticBkgA_KStar_format['betweenPeaks']= f_analyticBkgA_KStar_format['Poly6_Poly4' if AltRange else 'Gaus3_Poly4_DM']
        f_analyticBkgA_KStar_format['abovePsi2s']  = f_analyticBkgA_KStar_format['Poly6_Poly4']
        f_analyticBkgA_KStar_format['summary']     = f_analyticBkgA_KStar_format['Poly6_Poly4' if AltRange else 'Gaus2_Poly4_DM']
        f_analyticBkgA_KStar_format['summaryLowQ2']= f_analyticBkgA_KStar_format['Gaus2_Poly4']
        return f_analyticBkgA_KStar_format.get(self.process.cfg['binKey'], f_analyticBkgA_KStar_format['DEFAULT'])
    if Args.Year==2018:
        f_analyticBkgA_KStar_format['DEFAULT']     = f_analyticBkgA_KStar_format['Gaus2_Poly4']
        f_analyticBkgA_KStar_format['belowJpsiA']  = f_analyticBkgA_KStar_format['Gaus2_Poly4']
        f_analyticBkgA_KStar_format['belowJpsiB']  = f_analyticBkgA_KStar_format['Gaus2_Poly4']
        f_analyticBkgA_KStar_format['belowJpsiC']  = f_analyticBkgA_KStar_format['Gaus3_Poly4_DM']
        f_analyticBkgA_KStar_format['betweenPeaks']= f_analyticBkgA_KStar_format['Poly6_Poly4']
        f_analyticBkgA_KStar_format['abovePsi2s']  = f_analyticBkgA_KStar_format['Poly6_Poly4']
        f_analyticBkgA_KStar_format['summary']     = f_analyticBkgA_KStar_format['Gaus2_Poly4_DM']
        f_analyticBkgA_KStar_format['summaryLowQ2']= f_analyticBkgA_KStar_format['Gaus2_Poly4_DM']
        return f_analyticBkgA_KStar_format.get(self.process.cfg['binKey'], f_analyticBkgA_KStar_format['DEFAULT'])

setupBuildAnalyticBkgA_KStar = {
    'objName': "f_bkgA_KStar",
    'varNames': ["CosThetaK", "CosThetaL"],
    'CopyObj': [('Alt', 'f_bkgA_KStar')],
    'factoryCmd': [ ]
}

#"Math::Gaus::f_bkgM_KStar(Bmass, mean_Kstar[5.4, 5.3, 5.5], sigma_KStar[.3, 0, 4])"
f_BkgM_KStar_format = {}
f_BkgM_KStar_format['Gaus'] = [
    "bkgMKStar_c1[0.01,20]", "bkgMKStar_c2[5.4, 5.3,5.5]", "bkgMKStar_c3[0.05,10]",
    "bkgMKStar_c4[0.01,20]", "bkgMKStar_c5[5.35,5.3,5.5]", "bkgMKStar_c6[0.05,10]",
    "EXPR::f_bkgM_KStar('({pdfL})*({pdfK})',{args})".format(
        pdfL="bkgMKStar_c1*exp(-0.5*pow((Bmass-bkgMKStar_c2)/bkgMKStar_c3,2))",
        pdfK="bkgMKStar_c4*exp(-0.5*pow((Bmass-bkgMKStar_c5)/bkgMKStar_c6,2))",
        args="{Bmass, bkgMKStar_c1, bkgMKStar_c2, bkgMKStar_c3, bkgMKStar_c4, bkgMKStar_c5, bkgMKStar_c6}")
]
f_BkgM_KStar_format['Gaus2_Poly5'] = [
    "RooGaussian::gauss1(Bmass, bkgMKStar_c1[5.36, 5.25, 5.45], bkgMKStar_c2[.02, .001, 4.])",
    "RooGaussian::gauss2(Bmass, bkgMKStar_c3[5.4, 5.25, 5.45], bkgMKStar_c4[.02, .001, 4.])",
    "bkgMKStar_c5[-10,10]", "bkgMKStar_c6[-10,10]", "bkgMKStar_c7[-10,10]", "bkgMKStar_c8[-14,14]", "bkgMKStar_c9[-10,10]",
    "EXPR::Poly6_KStar('1+bkgMKStar_c5*Bmass+bkgMKStar_c6*pow(Bmass,2)+bkgMKStar_c7*pow(Bmass, 3)+bkgMKStar_c8*pow(Bmass,4)+bkgMKStar_c9*pow(Bmass,5)', {Bmass, bkgMKStar_c5, bkgMKStar_c6, bkgMKStar_c7, bkgMKStar_c8, bkgMKStar_c9})",
    #"SUM::f_bkgM_KStar(bkgM_frac1_KStar[0.4, 0.0, 1.0]*gauss1, bkgM_frac2_KStar[0.5, 0.0, 1.0]*gauss2, Poly6_KStar)",
    "PROD::f_bkgM_KStar(gauss1, gauss2, Poly6_KStar)",
]
f_BkgM_KStar_format['Gaus2_Poly6'] = [
    "RooGaussian::gauss1(Bmass, bkgMKStar_c1[5.36, 5.25, 5.45], bkgMKStar_c2[.02, .001, 4.])",
    "RooGaussian::gauss2(Bmass, bkgMKStar_c3[5.4, 5.25, 5.45], bkgMKStar_c4[.02, .001, 4.])",
    "bkgMKStar_c5[-10,10]", "bkgMKStar_c6[-10,10]", "bkgMKStar_c7[-10,10]", "bkgMKStar_c8[-14,14]", "bkgMKStar_c9[-10,10]", "bkgMKStar_c10[-10,10]",
    "EXPR::Poly6_KStar('1+bkgMKStar_c5*Bmass+bkgMKStar_c6*pow(Bmass,2)+bkgMKStar_c7*pow(Bmass, 3)+bkgMKStar_c8*pow(Bmass,4)+bkgMKStar_c9*pow(Bmass,5)+bkgMKStar_c10*pow(Bmass,6)', {Bmass, bkgMKStar_c5, bkgMKStar_c6, bkgMKStar_c7, bkgMKStar_c8, bkgMKStar_c9, bkgMKStar_c10})",
    #"SUM::f_bkgM_KStar(bkgM_frac1_KStar[0.4, 0.0, 1.0]*gauss1, bkgM_frac2_KStar[0.5, 0.0, 1.0]*gauss2, Poly6_KStar)",
    "PROD::f_bkgM_KStar(gauss1, gauss2, Poly6_KStar)",
]
f_BkgM_KStar_format['Gaus2'] = [
    "RooGaussian::gauss1(Bmass, bkgMKStar_c1[5.36, 5.25, 5.45], bkgMKStar_c2[.02, .001, 4.])",
    "RooGaussian::gauss2(Bmass, bkgMKStar_c3[5.4, 5.25, 5.45], bkgMKStar_c4[.02, .001, 4.])",
    "SUM::f_bkgM_KStar(bkgM_frac_KStar[0.4, 0.0, 1.0]*gauss1, gauss2)",
]
f_BkgM_KStar_format['Gaus3'] = [
    "RooGaussian::gauss1(Bmass, bkgMKStar_c1[5.36, 5.25, 5.45], bkgMKStar_c2[.02, .001, 4.])",
    "RooGaussian::gauss2(Bmass, bkgMKStar_c3[5.4, 5.25, 5.45], bkgMKStar_c4[.02, .001, 4.])",
    "RooGaussian::gauss3(Bmass, bkgMKStar_c5[5.4, 5.25, 5.45], bkgMKStar_c6[.02, .001, 4.])",
    #"SUM::f_bkgM_KStar(bkgM_frac1_KStar[0.4, 0.0, 1.0]*gauss1, bkgM_frac2_KStar[0.4, 0.0, 1.0]*gauss2, gauss3)",
    "PROD::f_bkgM_KStar(gauss1, gauss2, gauss3)",
]
f_BkgM_KStar_format['Double_Crystal_Ball'] = [ # pdfB: Double Crystal Ball
        "{cbs_mean_KStar}",
        "RooCBShape::cbs_KStar_1(Bmass, cbs_mean_KStar, {cbs1_sigma_KStar}, {cbs1_alpha_KStar}, {cbs1_n_KStar})",
        "RooCBShape::cbs_KStar_2(Bmass, cbs_mean_KStar, {cbs2_sigma_KStar}, {cbs2_alpha_KStar}, {cbs2_n_KStar})",
        "SUM::f_bkgM_KStar({bkgM_frac_KStar}*cbs_KStar_1, cbs_KStar_2)",
]
f_BkgM_KStar_format['DCB_Gaus'] = [ # pdfB: Double Crystal Ball + Gauss
        "{cbs_mean_KStar}",
        "RooCBShape::cbs_KStar_1(Bmass, cbs_mean_KStar, {cbs1_sigma_KStar}, {cbs1_alpha_KStar}, {cbs1_n_KStar})",
        "RooCBShape::cbs_KStar_2(Bmass, cbs_mean_KStar, {cbs2_sigma_KStar}, {cbs2_alpha_KStar}, {cbs2_n_KStar})",
        "RooGaussian::gauss1(Bmass, bkgMKStar_c1[5.40, 5.25, 5.45], bkgMKStar_c2[.009, .00001, 4.])",
        "SUM::f_bkgM_KStar({bkgM_frac_KStar}*cbs_KStar_1, bkgM_frac1_KStar[.1,0.,1.]*gauss1, cbs_KStar_2)",
]

def InitParams_KStar(self):
    """Initializing parameters for each bin and each year"""
    Args=self.process.cfg['args']
    params={
            'cbs_mean_KStar'  : 'cbs_mean_KStar[5.3733, 5.28, 5.5]',    'cbs1_sigma_KStar'  : 'cbs1_sigma_KStar[0.0929, 0.0001, .60]',
            'cbs1_alpha_KStar': 'cbs1_alpha_KStar[1.04, -6.0, 6.0]',    'cbs1_n_KStar'      : 'cbs1_n_KStar[121, 0, 1000]',
            'cbs2_sigma_KStar': 'cbs2_sigma_KStar[0.0406, 0.0001, 0.6]','cbs2_alpha_KStar'  : 'cbs2_alpha_KStar[-0.506,-9.4, 9.6]',
            'cbs2_n_KStar'    : 'cbs2_n_KStar[127, 0, 1000]',           'bkgM_frac_KStar'   : 'bkgM_frac_KStar[0.237, 0.0, 1.0]'
            }
    if Args.Year==2016:
        if self.process.cfg['binKey'] is 'summary':
            return {
            'cbs_mean_KStar': 'cbs_mean_KStar[5.40108, 5.38, 5.43]', 'cbs1_sigma_KStar': 'cbs1_sigma_KStar[0.0671412, 0.0001, 0.60]',
            'cbs1_alpha_KStar': 'cbs1_alpha_KStar[1.32481, -6.0, 6.0]', 'cbs1_n_KStar': 'cbs1_n_KStar[1.98694, 0, 500]',
            'cbs2_sigma_KStar': 'cbs2_sigma_KStar[0.0431308, 0.0001, 0.60]', 'cbs2_alpha_KStar': 'cbs2_alpha_KStar[-.372776,-19.4, 19.6]',
            'cbs2_n_KStar': 'cbs2_n_KStar[122.213, 0, 1000]', 'bkgM_frac_KStar': 'bkgM_frac_KStar[.620647, 0.0, 1.0]'
            }
        elif self.process.cfg['binKey'] is 'belowJpsiC':
            return {                                   
            'cbs_mean_KStar': 'cbs_mean_KStar[5.40108, 5.38, 5.43]', 'cbs1_sigma_KStar': 'cbs1_sigma_KStar[0.0671412, 0.0001, 0.60]',
            'cbs1_alpha_KStar': 'cbs1_alpha_KStar[1.32481, -6.0, 6.0]', 'cbs1_n_KStar': 'cbs1_n_KStar[1.98694, 0, 500]',
            'cbs2_sigma_KStar': 'cbs2_sigma_KStar[0.0431308, 0.0001, 0.60]', 'cbs2_alpha_KStar': 'cbs2_alpha_KStar[-.372776,-19.4, 19.6]',
            'cbs2_n_KStar': 'cbs2_n_KStar[122.213, 0, 1000]', 'bkgM_frac_KStar': 'bkgM_frac_KStar[.620647, 0.0, 1.0]'
            }
        else:
            return params
    elif Args.Year==2017:
        if self.process.cfg['binKey'] is 'belowJpsiA':
            return params
        else:
            return params
    elif Args.Year==2018:
        if self.process.cfg['binKey'] is 'belowJpsiA':
            return params
        else:
            return params
    else:
        return params
    
def GetBkgM_KStarList(self):
    """Return list containing PDF for current bin/year"""
    Args=self.process.cfg['args']
    if Args.Year==2016 or Args.Year==2017:
        f_BkgM_KStar_format['DEFAULT']    = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['DCB_Gaus']]
        f_BkgM_KStar_format['belowJpsiA'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['belowJpsiB'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['belowJpsiC'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['betweenPeaks'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['abovePsi2s'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['summaryLowQ2']=[var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        return f_BkgM_KStar_format.get(self.process.cfg['binKey'], f_BkgM_KStar_format['DEFAULT'])
    if Args.Year==2018:
        f_BkgM_KStar_format['DEFAULT']    = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['DCB_Gaus']]
        f_BkgM_KStar_format['belowJpsiA'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['belowJpsiB'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['belowJpsiC'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['betweenPeaks'] = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['summary']    = [var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        f_BkgM_KStar_format['summaryLowQ2']=[var.format(**InitParams_KStar(self)) for var in f_BkgM_KStar_format['Double_Crystal_Ball']]
        return f_BkgM_KStar_format.get(self.process.cfg['binKey'], f_BkgM_KStar_format['DEFAULT'])

setupBuildBkgM_KStar = {
    'objName': "f_bkgM_KStar",
    'varNames': ["Bmass"],
    'CopyObj': [('Alt', 'f_bkgM_KStar')],
    'factoryCmd': [ ]
}

setupSmoothBkg={'factoryCmd': []}
SmoothBkgCmd={}
SmoothBkgCmd['DEFAULT']=[1.0, 1.0, 1.0, 1.0]
SmoothBkgCmd['belowJpsiA']=[1.1, 1.1, 1.4, 1.4]
SmoothBkgCmd['belowJpsiB']=[1.5, 1.5, 0.9, 0.9]
SmoothBkgCmd['belowJpsiC']=[1.6, 1.6, 1.6, 1.6]
SmoothBkgCmd['betweenPeaks']=[1.6, 1.6, 36, 1]
SmoothBkgCmd['abovePsi2sA']=[1.5, 1.5, 1.5, 1.5]
SmoothBkgCmd['abovePsi2sB']=[1.9, 1.9, 1.4, 1.4]
SmoothBkgCmd['summary']=[3.1, 3.1, 2.0, 2.0]
SmoothBkgCmd['summaryLowQ2']=[2., 2., 2., 2.]
def buildSmoothBkgCombA(self, factoryCmd):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()
    Cmd=factoryCmd
    f_bkgCombAAltA = wspace.pdf("f_bkgCombAAltA")
    frac_bkgCombAAltA = wspace.var("frac_bkgCombAAltA")
    if f_bkgCombAAltA == None:
        f_bkgCombAAltKUp = RooKeysPdf("f_bkgCombAAltKUp",
                                      "f_bkgCombAAltKUp",
                                      CosThetaK,
                                      self.process.sourcemanager.get('dataReader.{0}.USB'.format(self.process.cfg['args'].Year)),
                                      RooKeysPdf.MirrorBoth, Cmd[0])
        f_bkgCombAAltKLo = RooKeysPdf("f_bkgCombAAltKLo",
                                      "f_bkgCombAAltKLo",
                                      CosThetaK,
                                      self.process.sourcemanager.get('dataReader.{0}.LSB'.format(self.process.cfg['args'].Year)),
                                      RooKeysPdf.MirrorBoth, Cmd[1])
        f_bkgCombAAltLUp = RooKeysPdf("f_bkgCombAAltLUp",
                                      "f_bkgCombAAltLUp",
                                      CosThetaL,
                                      self.process.sourcemanager.get('dataReader.{0}.USB'.format(self.process.cfg['args'].Year)),
                                      RooKeysPdf.MirrorBoth, Cmd[2])
        f_bkgCombAAltLLo = RooKeysPdf("f_bkgCombAAltLLo",
                                      "f_bkgCombAAltLLo",
                                      CosThetaL,
                                      self.process.sourcemanager.get('dataReader.{0}.LSB'.format(self.process.cfg['args'].Year)),
                                      RooKeysPdf.MirrorBoth, Cmd[3])
        for f in f_bkgCombAAltKLo, f_bkgCombAAltKUp, f_bkgCombAAltLLo, f_bkgCombAAltLUp:
            getattr(wspace, 'import')(f)
        wspace.factory("PROD::f_bkgCombAAltAUp(f_bkgCombAAltKUp,f_bkgCombAAltLUp)")
        wspace.factory("PROD::f_bkgCombAAltALo(f_bkgCombAAltKLo,f_bkgCombAAltLLo)")
        wspace.factory("SUM::f_bkgCombAAltA(frac_bkgCombAAltA[0.5,0,1]*f_bkgCombAAltALo,f_bkgCombAAltAUp)")
        f_bkgCombAAltA = wspace.pdf("f_bkgCombAAltA")
        frac_bkgCombAAltA = wspace.var("frac_bkgCombAAltA")
        frac_bkgCombAAltA.setVal(self.process.sourcemanager.get('dataReader.{0}.LSB'.format(str(self.process.cfg['args'].Year))).sumEntries() / (self.process.sourcemanager.get('dataReader.{0}.LSB'.format(str(self.process.cfg['args'].Year))).sumEntries() + self.process.sourcemanager.get('dataReader.{0}.USB'.format(str(self.process.cfg['args'].Year))).sumEntries()))
        frac_bkgCombAAltA.setConstant(True)

    self.cfg['source']['frac_bkgCombAAltA'] = frac_bkgCombAAltA
    self.cfg['source']['f_bkgCombAAltA'] = f_bkgCombAAltA

def buildBkgComb(self):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()

    variations = [("f_bkgComb", "f_bkgCombM", "f_bkgCombA"),
                  ("f_bkgComb_Alt", "f_bkgCombM", "f_bkgCombA_Alt"),
                  #("f_bkgCombAltA", "f_bkgCombM", "f_bkgCombAAltA"),
                  ("f_bkgCombAltM", "f_bkgCombMAltM", "f_bkgCombA"),
                  ("f_bkg_KStar", "f_bkgM_KStar", "f_bkgA_KStar"),
                  ("f_bkg_KStar_Alt", "f_bkgM_KStar_Alt", "f_bkgA_KStar_Alt"),
                  #("f_bkgCombAltM_AltA", "f_bkgCombMAltM", "f_bkgCombAAltA"),
                    ]
    for p, pM, pA in variations:
        f_bkgComb = wspace.pdf(p)
        if f_bkgComb == None:
            for k in [pM, pA]:
                locals()[k] = self.cfg['source'][k] if k in self.cfg['source'] else self.process.sourcemanager.get(k)
                if wspace.obj(k) == None:
                    getattr(wspace, 'import')(locals()[k])
            wspace.factory("PROD::{0}({1}, {2})".format(p, pM, pA))
            f_bkgComb = wspace.pdf(p)
        self.cfg['source'][p] = f_bkgComb

def buildFinal(self):
    """Combination of signal and background components."""
    wspace = self.getWspace()

    # Keep also mass spectrum only for prefit
    variations = [("f_final", "f_sig3D", "f_bkgComb"),                                          #3D=nSig(Sig2D*SigM)+nBkg(fBkgM*fBkg)
                  ("f_final_AltM", "f_sig3DAltM", "f_bkgComb"),                                 #3D=nSig(Sig2D*SigMDCB)+nBkg(fBkgM*fBkg)
                  #("f_finalAltBkgCombA", "f_sig3D", "f_bkgCombAltA"),
                  #("f_finalAltMAltBkgCombA", "f_sig3DAltM", "f_bkgCombAltA"),                   #3D=nSig(Sig2D*SigMDCB)+nBkg(fBkgM*fBkgAltA)
                  ("f_finalAltBkgCombM", "f_sig3D", "f_bkgCombAltM"),
                  #("f_finalAltM_AltBkgCombM_AltBkgCombA", "f_sig3DAltM","f_bkgCombAltM_AltA"), #3D=nSig(Sig2D*SigMDCB)+nBkg(fBkgAltM*fBkgAltA)
                  ("f_finalM", "f_sigM", "f_bkgCombM"),                                         #Mass PDF = nSig(SigM)+nBkg(fBkgM)
                  ("f_finalMAltBkgCombM", "f_sigM", "f_bkgCombMAltM"),
                  ("f_finalMDCB", "f_sigMDCB", "f_bkgCombM"),
                  ("f_finalMDCB_AltBkgCombM", "f_sigMDCB", "f_bkgCombMAltM"),                   #Mass PDF = nSig(SigMDCB)+nBkg(fBkgAltM)
                  ("f_finalPhiM", "f_sigPhiM3", "f_bkgPhiM")]                                #Phi Mass PDF = nSig(SigM)+nBkg(fBkgM)
    wspace.factory("nSig[10,1e-2,1e8]")
    wspace.factory("nBkgComb[100,1e-2,1e8]")
    for p, pSig, pBkg in variations:
        f_final = wspace.obj(p)
        if f_final == None:
            for k in [pSig, pBkg]:
                locals()[k] = self.cfg['source'][k] if k in self.cfg['source'] else self.process.sourcemanager.get(k)
                if wspace.obj(k) == None:
                    getattr(wspace, 'import')(locals()[k])
            wspace.factory("SUM::{0}(nSig*{1},nBkgComb*{2})".format(p, pSig, pBkg))
            f_final = wspace.obj(p)
        self.cfg['source'][p] = f_final

    variations2 = [("f_final_WithKStar", "f_sig3D", "f_bkgComb", "f_bkg_KStar"),
                   ("f_final_WithKStar_ts", "f_sig3D_ts", "f_bkgComb", "f_bkg_KStar"),          # Final PDF with 2Step eff
                   ("f_final_WithKStar_Alt", "f_sig3D_Alt", "f_bkgComb_Alt", "f_bkg_KStar_Alt"),
                   ("f_final_AltM_WithKStar", "f_sig3DAltM", "f_bkgComb", "f_bkg_KStar"),
                   ("f_finalM_JP", "f_sigM_DCBG_JP", "f_bkgCombM_JP", "f_sigM_DCBG_JK"),                #Mass PDF = nSig(BkgMDCBG)+nBkg(fBkgM)
                   ("f_finalM_PP", "f_sigM_DCBG_PP", "f_bkgCombM_PP", "f_sigM_DCBG_PK")]                #Mass PDF = nSig(BkgMDCBG)+nBkg(fBkgM)

    from BsToPhiMuMuFitter.python.datainput import GetPeakingFraction
    wspace.factory("PeakFrac[{}]".format(GetPeakingFraction(self)*3.90625*(9.4E-7/(8.2E-7*0.492)) ) ) #Has to be different for each bin
    wspace.obj("PeakFrac").setError(0.0118)
    wspace.factory("prod::nBkgPeak(PeakFrac, nSig)")
    for p, pSig, pBkg, kBkg in variations2:
        f_final2 = wspace.obj(p)
        if f_final2 == None:
            for k in [pSig, pBkg, kBkg]:
                locals()[k] = self.cfg['source'][k] if k in self.cfg['source'] else self.process.sourcemanager.get(k)
                if wspace.obj(k) == None:
                    getattr(wspace, 'import')(locals()[k])
            wspace.factory("SUM::{0}(nSig*{1},nBkgComb*{2}, nBkgPeak*{3})".format(p, pSig, pBkg, kBkg))
            f_final2 = wspace.obj(p)
        self.cfg['source'][p] = f_final2
    wspace.Print()


sharedWspaceTagString = "{binLabel}"
CFG_WspaceReader = copy(WspaceReader.templateConfig())
CFG_WspaceReader.update({
    'obj': OrderedDict([
    ])  # Empty by default loads all Functions and Pdfs
})

def customizeWspaceReader(self):
    self.cfg['fileName'] = "{0}/input/wspace_{2}_{1}.root".format(modulePath, q2bins[self.process.cfg['binKey']]['label'], str(self.process.cfg['args'].Year))
    self.cfg['wspaceTag'] = sharedWspaceTagString.format(binLabel=q2bins[self.process.cfg['binKey']]['label'])

def GetWspaceReader(self):
    stdWspaceReader = WspaceReader(CFG_WspaceReader); stdWspaceReader.name="stdWspaceReader.{0}".format(str(self.cfg['args'].Year))
    stdWspaceReader.customize = types.MethodType(customizeWspaceReader, stdWspaceReader)
    return stdWspaceReader

CFG_PDFBuilder = ObjProvider.templateConfig()
stdPDFBuilder = ObjProvider(copy(CFG_PDFBuilder)); stdPDFBuilder.name="stdPDFBuilder"
def customizePDFBuilder(self):
    """Customize pdf for q2 bins"""

    wspaceTag = sharedWspaceTagString.format(binLabel=q2bins[self.process.cfg['binKey']]['label'])
    wspaceName = "wspace.{0}.{1}".format(self.process.cfg['args'].Year, wspaceTag)
    if wspaceName in self.process.sourcemanager.keys():
        Wspace = self.process.sourcemanager.get(wspaceName)
        if Wspace.allVars().find("CosThetaK"):
            print("INFO: RooWorkspace is already exists. Not building it again") 
            return 0
        else:
            pass

    setupBuildAnalyticBkgCombA['factoryCmd']   = GetAnalyticBkgAList(self) 
    setupBuildAnalyticBkgA_KStar['factoryCmd'] = GetAnalyticBkgA_KStarList(self)
    setupBuildBkgM_KStar['factoryCmd']         = GetBkgM_KStarList(self) 
    setupBuildEffiSigA['factoryCmd']           = GetEffiSigAList(self) 
    setupBuild_accEffiSigA['factoryCmd']       = Get_AccEff_List(self) 
    setupBuild_recEffiSigA['factoryCmd']       = Get_RecEff_List(self) 
    buildAnalyticBkgCombA   = functools.partial(buildGenericObj, **setupBuildAnalyticBkgCombA)
    buildAnalyticBkgA_KStar = functools.partial(buildGenericObj, **setupBuildAnalyticBkgA_KStar)
    buildBkgM_KStar         = functools.partial(buildGenericObj, **setupBuildBkgM_KStar)
    buildEffiSigA           = functools.partial(buildGenericObj, **setupBuildEffiSigA)
    build_accEffiSigA       = functools.partial(buildGenericObj, **setupBuild_accEffiSigA)
    build_recEffiSigA       = functools.partial(buildGenericObj, **setupBuild_recEffiSigA)
    
    setupSmoothBkg['factoryCmd'] = SmoothBkgCmd.get(self.process.cfg['binKey'], SmoothBkgCmd['DEFAULT'])
    buildSmoothBkg = functools.partial(buildSmoothBkgCombA, **setupSmoothBkg)
    # Configure setup
    self.cfg.update({
        'wspaceTag': wspaceTag,
        'obj': OrderedDict([
            ('effi_sigA', [buildEffiSigA]),
            ('acc_effi_sigA', [build_accEffiSigA]),
            ('rec_effi_sigA', [build_recEffiSigA]),
            ('f_sigA', [buildSigA]),
            ('f_sigM', [buildSigM]),
            ('f_sig3D', [buildSig]),  # Include f_sig2D
            ('f_bkgCombA', [buildAnalyticBkgCombA]),
            ('f_bkgM_KStar', [buildBkgM_KStar]),
            ('f_bkgA_KStar', [buildAnalyticBkgA_KStar]),
            #('f_bkgCombAAltA', [buildSmoothBkg]),
            ('f_bkgCombM', [buildBkgCombM]),
            ('f_bkgCombMAltM', [buildBkgCombMAltM]),
            ('f_bkgComb', [buildBkgComb]),  # Include all variations
            ('f_final', [buildFinal]),  # Include all variations
        ])
    })
stdPDFBuilder.customize = types.MethodType(customizePDFBuilder, stdPDFBuilder)

if __name__ == '__main__':
    binKey = [sys.argv[1]]
    for b in binKey:
        p.cfg['binKey'] = b
        p.setSequence([dataCollection.dataReader, stdWspaceReader, stdPDFBuilder])
        p.beginSeq()
        p.runSeq()
        p.endSeq()

        #  p.reset()
        dataCollection.dataReader.reset()
        stdWspaceReader.reset()
        stdPDFBuilder.reset()
