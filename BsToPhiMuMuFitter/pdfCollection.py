#!/usr/bin/env python
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
from BsToPhiMuMuFitter.varCollection import Bmass, CosThetaK, CosThetaL
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
#from __main__ import args as Args
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import RooWorkspace, RooEffProd, RooKeysPdf

#from BsToPhiMuMuFitter.StdProcess import p

def getWspace(self):
    """Read workspace"""
    wspaceName = "wspace.{0}.{1}".format(str(self.process.cfg['args'].Year), self.cfg.get('wspaceTag', "DEFAULT"))
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


ObjProvider.getWspace = types.MethodType(getWspace, None, ObjProvider)

#########################
# Now start define PDFs #
#########################


def buildGenericObj(self, objName, factoryCmd, varNames):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()
    obj = wspace.obj(objName)
    if obj == None:
        self.logger.logINFO("Build {0} from scratch.".format(objName))
        for v in varNames:
            if wspace.obj(v) == None:
                getattr(wspace, 'import')(globals()[v])  #Import CosThetaK and CosThetaL 
        for cmdIdx, cmd in enumerate(factoryCmd):
            wspace.factory(cmd)
        obj = wspace.obj(objName)
    self.cfg['source'][objName] = obj

#======================================================================================================
from BsToPhiMuMuFitter.python.pdfDicts import f_effiSigA_format
def GetEffiSigAList(self):
    Args=self.process.cfg['args']
    if Args.Year==2016:
        f_effiSigA_format['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_format['belowJpsiA']   = f_effiSigA_format['Gaus3_Poly6_XTerm']
        f_effiSigA_format['belowJpsiB']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['Test1']        = f_effiSigA_format['Gaus3_Poly6_XTerm']
        f_effiSigA_format['summaryLowQ2'] = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']

    if Args.Year==2017:
        f_effiSigA_format['DEFAULT']    = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_format['belowJpsiA'] = f_effiSigA_format['Gaus3_Poly6_XTerm']
        f_effiSigA_format['belowJpsiB'] = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['Test1']      = f_effiSigA_format['Gaus3_Poly6_XTerm'] 

    if Args.Year==2018:
        f_effiSigA_format['DEFAULT']      = f_effiSigA_format['Poly8_Poly6_XTerm']
        f_effiSigA_format['belowJpsiA']   = f_effiSigA_format['Gaus3_Poly6_XTerm']
        f_effiSigA_format['belowJpsiB']   = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
        f_effiSigA_format['Test1']        = f_effiSigA_format['Gaus3_Poly6_XTerm']
        f_effiSigA_format['summaryLowQ2'] = f_effiSigA_format['Gaus3_Poly6_XTerm_v2']
    return f_effiSigA_format.get(self.process.cfg['binKey'], f_effiSigA_format['DEFAULT'])

setupBuildEffiSigA = {
    'objName': "effi_sigA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [  ]
}

#======================================================================================================
setupBuildSigM = {
    'objName': "f_sigM",
    'varNames': ["Bmass"],
    'factoryCmd': [
        "sigMGauss_mean[5.36, 5.30, 5.5]",
        "RooGaussian::f_sigMGauss1(Bmass, sigMGauss_mean, sigMGauss1_sigma[0.0284, 0.0001, 0.05])",
        "RooGaussian::f_sigMGauss2(Bmass, sigMGauss_mean, sigMGauss2_sigma[0.0667, 0.0005, 0.40])",
        "SUM::f_sigM(sigM_frac[0.7, 0.,1.]*f_sigMGauss1, f_sigMGauss2)",
        "cbs_mean[5.369, 5.28, 5.4]",
        "RooCBShape::cbs_1(Bmass, cbs_mean, cbs1_sigma[0.0268, 0.0001, 0.60], cbs1_alpha[0.89, -6.0, 6.0], cbs1_n[4, 0, 1000])",
        "RooCBShape::cbs_2(Bmass, cbs_mean, cbs2_sigma[0.0296, 0.0001, 0.60], cbs2_alpha[-0.87, -9.4, 9.6], cbs2_n[133, 0, 1000])",
        "SUM::f_sigMDCB(sigMDCB_frac[0.4, 0.0, 1.0]*cbs_1, cbs_2)",
    ],
}
buildSigM = functools.partial(buildGenericObj, **setupBuildSigM)

#======================================================================================================
def buildSigA(self):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()

    f_sigA = wspace.pdf("f_sigA")
    if f_sigA == None:
        wspace.factory("unboundFl[0.6978,-3e3,3e3]")
        wspace.factory("unboundAfb[-0.01,-3e3,3e3]")
        wspace.factory("expr::fl('0.5+TMath::ATan(unboundFl)/TMath::Pi()',{unboundFl})")
        wspace.factory("expr::afb('2.*(1-fl)*TMath::ATan(unboundAfb)/TMath::Pi()',{unboundAfb,fl})")
        wspace.factory("EXPR::f_sigA_original('(9.0/16.0)*((0.5*(1.0-fl)*(1.0-CosThetaK*CosThetaK)*(1.0+CosThetaL*CosThetaL)) + (2.0*fl*CosThetaK*CosThetaK*(1.0-CosThetaL*CosThetaL)) + (afb*(1.0-CosThetaK*CosThetaK)*CosThetaL))', {CosThetaK, CosThetaL, fl, afb})")
        f_sigA = ROOT.RooBtosllModel("f_sigA", "", CosThetaL, CosThetaK, wspace.var('unboundAfb'), wspace.var('unboundFl'))
        getattr(wspace, 'import')(f_sigA)
        wspace.importClassCode(ROOT.RooBtosllModel.Class())

    self.cfg['source']['f_sigA'] = f_sigA

def buildSig(self):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()

    f_sig2D = wspace.obj("f_sig2D")
    f_sig3D = wspace.obj("f_sig3D")
    f_sig3DAltM = wspace.obj("f_sig3DAltM")
    if f_sig3D == None or f_sig3DAltM == None:
        for k in ['effi_sigA', 'f_sigA', 'f_sigM', 'f_sigMDCB']:
            locals()[k] = self.cfg['source'][k] if k in self.cfg['source'] else self.process.sourcemanager.get(k)
        f_sig2D = RooEffProd("f_sig2D", "", locals()['f_sigA'], locals()['effi_sigA'])
        getattr(wspace, 'import')(f_sig2D, ROOT.RooFit.RecycleConflictNodes())
        if wspace.obj("f_sigM") == None:
            getattr(wspace, 'import')(locals()['f_sigM'])
        if wspace.obj("f_sigMDCB") == None:
            getattr(wspace, 'import')(locals()['f_sigMDCB'])
        wspace.factory("PROD::f_sig3D(f_sigM, f_sig2D)")
        wspace.factory("PROD::f_sig3DAltM(f_sigMDCB, f_sig2D)")
        f_sig3D = wspace.pdf("f_sig3D")
        f_sig3DAltM = wspace.pdf("f_sig3DAltM")

    self.cfg['source']['f_sig2D'] = f_sig2D
    self.cfg['source']['f_sig3D'] = f_sig3D
    self.cfg['source']['f_sig3DAltM'] = f_sig3DAltM

#======================================================================================================
setupBuildBkgCombM = {
    'objName': "f_bkgCombM",
    'varNames': ["Bmass"],
    'factoryCmd': [
        "bkgCombM_c1[-5,-40,2]",
        "EXPR::f_bkgCombM('exp(bkgCombM_c1*Bmass)',{Bmass,bkgCombM_c1})",
    ],
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
    if Args.Year==2016 or Args.Year==2017 or Args.Year==2018:
        f_analyticBkgCombA_format['DEFAULT']        = f_analyticBkgCombA_format['Poly6_Poly6']
        f_analyticBkgCombA_format['belowJpsiA']     = f_analyticBkgCombA_format['Poly6_Poly6']
        #f_analyticBkgCombA_format['betweenPeaks']   = f_analyticBkgCombA_format['Gaus2_Poly4']
        #f_analyticBkgCombA_format['abovePsi2sA']    = f_analyticBkgCombA_format['Lin_Poly3']
        #f_analyticBkgCombA_format['abovePsi2sB']    = f_analyticBkgCombA_format['Poly2_Poly3']
        #f_analyticBkgCombA_format['Test3']          = f_analyticBkgCombA_format['Poly2_Poly3']
        f_analyticBkgCombA_format['summaryLowQ2']    = f_analyticBkgCombA_format['Poly8_Poly8']
    return f_analyticBkgCombA_format.get(self.process.cfg['binKey'], f_analyticBkgCombA_format['DEFAULT'])
setupBuildAnalyticBkgCombA = {
    'objName': "f_bkgCombA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [  ]
}
#======================================================================================================

f_analyticBkgA_KStar_format = {}
f_analyticBkgA_KStar_format['Poly4_Poly4'] = [ # pdfL: Poly4, pdfK: Poly4
    "bkgKStarL_c1[-10.,10.]", "bkgKStarL_c2[-10.,10.]", "bkgKStarL_c3[-10.,10.]", "bkgKStarL_c4[-10.,10.]",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::f_bkgA_KStar('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgKStarL_c1*CosThetaL+bkgKStarL_c2*pow(CosThetaL,2)+bkgKStarL_c3*pow(CosThetaL, 3)+bkgKStarL_c4*pow(CosThetaL,4)",
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}")
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
    "bkgKStarL_c1[-3,3]", "bkgKStarL_c2[0.1, 0.01, 0.5]", "bkgKStarL_c3[-3,3]", "bkgKStarL_c4[0.1, 0.01, 1.0]", "bkgKStarL_c5[0,10]",
    "bkgKStarK_c1[-10,10]", "bkgKStarK_c2[-10,10]", "bkgKStarK_c3[-10,10]", "bkgKStarK_c4[-10,10]",
    "EXPR::f_bkgA_KStar('({pdfL})*({pdfK})', {args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgKStarL_c1)/bkgKStarL_c2,2))+bkgKStarL_c5*exp(-0.5*pow((CosThetaL-bkgKStarL_c3)/bkgKStarL_c4,2))",
        pdfK="1+bkgKStarK_c1*CosThetaK+bkgKStarK_c2*pow(CosThetaK,2)+bkgKStarK_c3*pow(CosThetaK, 3)+bkgKStarK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgKStarL_c1, bkgKStarL_c2, bkgKStarL_c3, bkgKStarL_c4, bkgKStarL_c5, bkgKStarK_c1, bkgKStarK_c2, bkgKStarK_c3, bkgKStarK_c4}")
]

def GetAnalyticBkgA_KStarList(self):
    Args=self.process.cfg['args']
    if Args.Year==2016 or Args.Year==2017 or Args.Year==2018:
        f_analyticBkgA_KStar_format['DEFAULT']  = f_analyticBkgA_KStar_format['Gaus2_Poly4']
        f_analyticBkgA_KStar_format['belowJpsiA']  = f_analyticBkgA_KStar_format['QuadGaus_Poly4']
        #f_analyticBkgA_KStar_format['belowJpsiB']  = f_analyticBkgA_KStar_format['QuadGaus_Poly4']
    return f_analyticBkgA_KStar_format.get(self.process.cfg['binKey'], f_analyticBkgA_KStar_format['DEFAULT'])

setupBuildAnalyticBkgA_KStar = {
    'objName': "f_bkgA_KStar",
    'varNames': ["CosThetaK", "CosThetaL"],
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
f_BkgM_KStar_format['Gaus2'] = [
    "RooGaussian::gauss1(Bmass, bkgMKStar_c1[5.36, 5.25, 5.45], bkgMKStar_c2[.02, .001, 4.])",
    "RooGaussian::gauss2(Bmass, bkgMKStar_c3[5.4, 5.25, 5.45], bkgMKStar_c4[.02, .001, 4.])",
    "SUM::f_bkgM_KStar(bkgM_frac_KStar[0.4, 0.0, 1.0]*gauss1, gauss2)",
]
f_BkgM_KStar_format['Double_Crystal_Ball'] = [ # pdfB: Double Crystal Ball
        "cbs_mean_KStar[5.4, 5.28, 5.5]",
        "RooCBShape::cbs_KStar_1(Bmass, cbs_mean_KStar, cbs1_sigma_KStar[0.0268, 0.0001, 0.60], cbs1_alpha_KStar[0.89, -6.0, 6.0], cbs1_n_KStar[4, 0, 1000])",
        "RooCBShape::cbs_KStar_2(Bmass, cbs_mean_KStar, cbs2_sigma_KStar[0.0296, 0.0001, 0.60], cbs2_alpha_KStar[-0.87,-9.4, 9.6], cbs2_n_KStar[133, 0, 1000])",
        "SUM::f_bkgM_KStar(bkgM_frac_KStar[0.4, 0.0, 1.0]*cbs_KStar_1, cbs_KStar_2)",
]

def GetBkgM_KStarList(self):
    Args=self.process.cfg['args']
    if Args.Year==2016 or Args.Year==2017 or Args.Year==2018:
        f_BkgM_KStar_format['DEFAULT'] = f_BkgM_KStar_format['Double_Crystal_Ball']
        f_BkgM_KStar_format['belowJpsiA'] = f_BkgM_KStar_format['Gaus']
        f_BkgM_KStar_format['belowJpsiB'] = f_BkgM_KStar_format['Gaus']
        f_BkgM_KStar_format['belowJpsiC'] = f_BkgM_KStar_format['Gaus2']
    return f_BkgM_KStar_format.get(self.process.cfg['binKey'], f_BkgM_KStar_format['DEFAULT'])

setupBuildBkgM_KStar = {
    'objName': "f_bkgM_KStar",
    'varNames': ["Bmass"],
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
                                      self.process.sourcemanager.get('dataReader.{0}.USB'.format(str(self.process.cfg['args'].Year))),
                                      RooKeysPdf.MirrorBoth, Cmd[0])
        f_bkgCombAAltKLo = RooKeysPdf("f_bkgCombAAltKLo",
                                      "f_bkgCombAAltKLo",
                                      CosThetaK,
                                      self.process.sourcemanager.get('dataReader.{0}.LSB'.format(str(self.process.cfg['args'].Year))),
                                      RooKeysPdf.MirrorBoth, Cmd[1])
        f_bkgCombAAltLUp = RooKeysPdf("f_bkgCombAAltLUp",
                                      "f_bkgCombAAltLUp",
                                      CosThetaL,
                                      self.process.sourcemanager.get('dataReader.{0}.USB'.format(str(self.process.cfg['args'].Year))),
                                      RooKeysPdf.MirrorBoth, Cmd[2])
        f_bkgCombAAltLLo = RooKeysPdf("f_bkgCombAAltLLo",
                                      "f_bkgCombAAltLLo",
                                      CosThetaL,
                                      self.process.sourcemanager.get('dataReader.{0}.LSB'.format(str(self.process.cfg['args'].Year))),
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
                  ("f_bkgCombAltA", "f_bkgCombM", "f_bkgCombAAltA"),
                  ("f_bkgCombAltM", "f_bkgCombMAltM", "f_bkgCombA"),
                  ("f_bkg_KStar", "f_bkgM_KStar", "f_bkgA_KStar"),
                  ("f_bkgCombAltM_AltA", "f_bkgCombMAltM", "f_bkgCombAAltA")]
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
                  ("f_finalAltBkgCombA", "f_sig3D", "f_bkgCombAltA"),
                  ("f_finalAltMAltBkgCombA", "f_sig3DAltM", "f_bkgCombAltA"),                   #3D=nSig(Sig2D*SigMDCB)+nBkg(fBkgM*fBkgAltA)
                  ("f_finalAltBkgCombM", "f_sig3D", "f_bkgCombAltM"),
                  ("f_finalAltM_AltBkgCombM_AltBkgCombA", "f_sig3DAltM", "f_bkgCombAltM_AltA"), #3D=nSig(Sig2D*SigMDCB)+nBkg(fBkgAltM*fBkgAltA)
                  ("f_finalM", "f_sigM", "f_bkgCombM"),                                         #Mass PDF = nSig(SigM)+nBkg(fBkgM)
                  ("f_finalMAltBkgCombM", "f_sigM", "f_bkgCombMAltM"),
                  ("f_finalMDCB", "f_sigMDCB", "f_bkgCombM"),
                  ("f_finalMDCB_AltBkgCombM", "f_sigMDCB", "f_bkgCombMAltM")]                   #Mass PDF = nSig(SigMDCB)+nBkg(fBkgAltM)
    wspace.factory("nSig[10,1e-2,1e5]")
    wspace.factory("nBkgComb[100,1e-2,1e5]")
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

    variations2 = [("f_final_WithKStar", "f_sig3D", "f_bkgComb", "f_bkg_KStar")]
    wspace.factory("nBkgKStar[{0}, 0, 1000]".format(20)) #(self.process.sourcemanager.get('KsigMCReader.Fit').sumEntries()*35.9/2765.2853))
    for p, pSig, pBkg, kBkg in variations2:
        f_final2 = wspace.obj(p)
        if f_final2 == None:
            for k in [pSig, pBkg, kBkg]:
                locals()[k] = self.cfg['source'][k] if k in self.cfg['source'] else self.process.sourcemanager.get(k)
                if wspace.obj(k) == None:
                    getattr(wspace, 'import')(locals()[k])
            wspace.factory("SUM::{0}(nSig*{1},nBkgComb*{2}, nBkgKStar*{3})".format(p, pSig, pBkg, kBkg))
            f_final2 = wspace.obj(p)
        self.cfg['source'][p] = f_final2


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
    setupBuildAnalyticBkgCombA['factoryCmd']   = GetAnalyticBkgAList(self) 
    setupBuildAnalyticBkgA_KStar['factoryCmd'] = GetAnalyticBkgA_KStarList(self)
    setupBuildBkgM_KStar['factoryCmd']         = GetBkgM_KStarList(self) 
    setupBuildEffiSigA['factoryCmd']           = GetEffiSigAList(self) 
    buildAnalyticBkgCombA   = functools.partial(buildGenericObj, **setupBuildAnalyticBkgCombA)
    buildAnalyticBkgA_KStar = functools.partial(buildGenericObj, **setupBuildAnalyticBkgA_KStar)
    buildBkgM_KStar         = functools.partial(buildGenericObj, **setupBuildBkgM_KStar)
    buildEffiSigA           = functools.partial(buildGenericObj, **setupBuildEffiSigA)
    
    setupSmoothBkg['factoryCmd'] = SmoothBkgCmd.get(self.process.cfg['binKey'], SmoothBkgCmd['DEFAULT'])
    buildSmoothBkg = functools.partial(buildSmoothBkgCombA, **setupSmoothBkg)
    # Configure setup
    self.cfg.update({
        'wspaceTag': sharedWspaceTagString.format(binLabel=q2bins[self.process.cfg['binKey']]['label']),
        'obj': OrderedDict([
            ('effi_sigA', [buildEffiSigA]),
            ('f_sigA', [buildSigA]),
            ('f_sigM', [buildSigM]),
            ('f_sig3D', [buildSig]),  # Include f_sig2D
            ('f_bkgCombA', [buildAnalyticBkgCombA]),
            ('f_bkgM_KStar', [buildBkgM_KStar]),
            ('f_bkgA_KStar', [buildAnalyticBkgA_KStar]),
            ('f_bkgCombAAltA', [buildSmoothBkg]),
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
