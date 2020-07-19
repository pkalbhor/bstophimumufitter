#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdn=3 ft=python et:

# Description     : Define PDFs
# Author          : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
#                   Pritam Kalbhor (physics.pritam@gmail.com)
# Last Modified   : 19 Apr 2020 12:04 01:26

############
# WARNINGS #
############
# Dont call TObject.Print(), it seems the iterators leads to random crash
# In RooWorkspace.factory(), you MUST replace the calculation between numbers to a single float number, e.g. 2/3 -> 0.666667
#   It is possible that the parser don't designed to handle RooAddition and RooProduct between RooConstVar

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

import ROOT
from ROOT import RooWorkspace
from ROOT import RooEffProd
from ROOT import RooKeysPdf

from BsToPhiMuMuFitter.StdProcess import p

def getWspace(self):
    """Read workspace"""
    wspaceName = "wspace.{0}".format(self.cfg.get('wspaceTag', "DEFAULT"))
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

f_effiSigA_format = {}

pdfL = "1+l1*CosThetaL+l2*pow(CosThetaL,2)+l3*pow(CosThetaL,3)+l4*pow(CosThetaL,4)+l5*pow(CosThetaL,5)+l6*pow(CosThetaL,6)+l7*pow(CosThetaL,7)+l8*pow(CosThetaL,8)"; nLo=9
pdfK = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)"; nK=7
n=25 #Number of x. LP4*Pol4
xTerm = "\
(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)\
+(x20+x21*CosThetaK+x22*(1.5*pow(CosThetaK,2)-0.5)+x23*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x24*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,4)"

f_effiSigA_format['DEFAULT'] = ["l{0}[-10,10]".format(i) for i in range(1, nLo)] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL, args="{CosThetaL, " + ', '.join(["l{0}".format(i) for i in range(1, nLo)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK, " + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL,
        pdfK=pdfK,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLo)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(n)]) + "}")]

xTerm2 = "\
(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)"; n1A=20
#pdfL1A = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2))"; nLc=6
pdfL1A = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2)) + l7*exp(-0.5*pow((CosThetaL-l8)/l9,2))"; nLc=9
pdfK1A = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)"; nK1A=7
f_effiSigA_format['belowJpsiA'] = ["l{0}[.1,0,10]".format(3*i-2) for i in range(1, nLc/3+1)] \
    + ["l{0}[0,-.5,.5]".format(3*i-1) for i in range(1, nLc/3+1)] \
    + ["l{0}[.2,.01,5.]".format(3*i) for i in range(1, nLc/3+1)] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK1A)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1A, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLc+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK1A, args="{CosThetaK,"+', '.join(["k{0}".format(i) for i in range(1, nK1A)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL1A,
        pdfK=pdfK1A,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLc+1)] + ["k{0}".format(i) for i in range(1, nK1A)] + ["x{0}".format(i) for i in range(n)]) + "}")]

f_effiSigA_format['Test1'] = deepcopy(f_effiSigA_format['belowJpsiA'])
#f_effiSigA_format['belowJpsiC'] = deepcopy(f_effiSigA_format['belowJpsiA'])
#f_effiSigA_format['summaryLowQ2'] = deepcopy(f_effiSigA_format['belowJpsiA'])
pdfL1B = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2)) + l7*exp(-0.5*pow((CosThetaL-l8)/l9,2))"; nLB=9
f_effiSigA_format['belowJpsiB'] = ["l1[.1,0,10]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[0.2,0,10]", "l5[.2,-0.5,0.5]", "l6[.2,0.01,5.0]", "l7[0.1,0,10]", "l8[0,-.5,.5]", "l9[.2,.01,5.]"] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1B, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL1B,
        pdfK=pdfK,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(n)]) + "}")]

"""pdfL1C = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2))"; nLC=6
f_effiSigA_format['belowJpsiC'] = ["l1[.1,0,10]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[0.2,0,10]", "l5[.2,-0.5,0.5]", "l6[.2,0.01,5.0]"] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1C, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLC+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL1C,
        pdfK=pdfK,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLC+1)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(n)]) + "}")]"""


pdfL = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2))+l7*exp(-0.5*pow((CosThetaL-l8)/l9,2))"; nLB=9
f_effiSigA_format['summaryLowQ2'] = ["l{0}[.1,0,10]".format(3*i-2) for i in range(1, nLB/3+1)] \
    + ["l{0}[0,-.5,.5]".format(3*i-1) for i in range(1, nLB/3+1)] \
    + ["l{0}[.2,.1,2.]".format(3*i) for i in range(1, nLB/3+1)] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL, args="{CosThetaL," + ', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL,
        pdfK=pdfK,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(n)]) + "}")]

setupBuildEffiSigA = {
    'objName': "effi_sigA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [
    ]
}

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



def buildSigA(self):
    """Build with RooWorkspace.factory. See also RooFactoryWSTool.factory"""
    wspace = self.getWspace()

    f_sigA = wspace.pdf("f_sigA")
    if f_sigA == None:
        # wspace.factory("fs[0.00001,0.00001,0.2]")
        wspace.factory("unboundFl[0.6978,-3e3,3e3]")
        wspace.factory("unboundAfb[-0.01,-3e3,3e3]")
        # wspace.factory("transAs[0,-1e5,1e5]")
        wspace.factory("expr::fl('0.5+TMath::ATan(unboundFl)/TMath::Pi()',{unboundFl})")
        wspace.factory("expr::afb('2.*(1-fl)*TMath::ATan(unboundAfb)/TMath::Pi()',{unboundAfb,fl})")
        # wspace.factory("expr::as('1.78*TMath::Sqrt(3*fs*(1-fs)*fl)*transAs',{fs,fl,transAs})")
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

setupBuildBkgCombM = {
    'objName': "f_bkgCombM",
    'varNames': ["Bmass"],
    'factoryCmd': [
        "bkgCombM_c1[-5,-40,2]",
        "EXPR::f_bkgCombM('exp(bkgCombM_c1*Bmass)',{Bmass,bkgCombM_c1})",
    ],
}
buildBkgCombM = functools.partial(buildGenericObj, **setupBuildBkgCombM)

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

f_analyticBkgCombA_format = {}

f_analyticBkgCombA_format['Poly4_Exp'] = [ # pdfL: Poly4, pdfK: exp()+exp()
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly4_Poly4'] = [ # pdfL: Poly4, pdfK: Poly4
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus3_Exp'] = [ #pdfL: Gaus+Gaus+Gaus, pdfK: exp()+expt()
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]", "bkgCombL_c8[0,10]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c8*exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['GausPoly_Exp'] = [ #pdfL: Gaus+Gaus+Poly2, pdfK: exp()+exp()
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.1,0.001,1.]", "bkgCombL_c3[-0.62,-1.,1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0,10]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]",  "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+1.+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus2_Poly4'] = [ # pdfL: Gauss+Gauss, pdfK: Poly4
    "bkgCombL_c1[-3,3]", "bkgCombL_c2[0.1, 0.01, 0.5]", "bkgCombL_c3[-3,3]", "bkgCombL_c4[0.1, 0.01, 1.0]", "bkgCombL_c5[0,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Lin_Poly3'] = [ # pdfL: Linear, pdfK: Poly3
    "bkgCombL_c1[-3,3]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL",
        pdfK="1.+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly2_Poly3'] = [ # pdfL: Poly2, pdfK: Poly3
    "bkgCombL_c1[-3,3]",   "bkgCombL_c2[-3,3]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL, 2)",
        pdfK="1.+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['QuadGaus_Exp'] = [ # pdfL: Quadratic+Gauss, pdfK: exp()+exp()
    "bkgCombL_c1[0.01,1]", "bkgCombL_c2[0.1,20]", "bkgCombL_c3[-1,1]", "bkgCombL_c4[0.05,1]",
    "bkgCombK_c1[-10,0]",  "bkgCombK_c2[0,20]",   "bkgCombK_c3[0,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})',{args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+bkgCombK_c2*exp(bkgCombK_c3*CosThetaK)",
        args="{CosThetaL,CosThetaK,bkgCombL_c1,bkgCombL_c2,bkgCombL_c3,bkgCombL_c4,bkgCombK_c1,bkgCombK_c2,bkgCombK_c3}")
]
f_analyticBkgCombA_format['New'] = [ # pdfL: Gauss, pdfK: exp()+exp()
    "bkgCombL_c2[0.1,20]", "bkgCombL_c3[-1,1]", "bkgCombL_c4[0.05,1]",
    "bkgCombK_c1[-10,0]",  "bkgCombK_c2[0,20]",   "bkgCombK_c3[0,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})',{args})".format(
        pdfL="bkgCombL_c2*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+bkgCombK_c2*exp(bkgCombK_c3*CosThetaK)",
        args="{CosThetaL,CosThetaK,bkgCombL_c2,bkgCombL_c3,bkgCombL_c4,bkgCombK_c1,bkgCombK_c2,bkgCombK_c3}")
]

f_analyticBkgCombA_format['DEFAULT']    = f_analyticBkgCombA_format['QuadGaus_Exp']
f_analyticBkgCombA_format['belowJpsiA'] = f_analyticBkgCombA_format['New']
f_analyticBkgCombA_format['belowJpsiB'] = f_analyticBkgCombA_format['Poly4_Poly4']
f_analyticBkgCombA_format['belowJpsiC'] = f_analyticBkgCombA_format['Poly4_Poly4']
f_analyticBkgCombA_format['betweenPeaks'] = f_analyticBkgCombA_format['Gaus2_Poly4']
f_analyticBkgCombA_format['abovePsi2sA'] = f_analyticBkgCombA_format['Lin_Poly3']
f_analyticBkgCombA_format['abovePsi2sB'] = f_analyticBkgCombA_format['Poly2_Poly3']
f_analyticBkgCombA_format['summaryLowQ2'] = f_analyticBkgCombA_format['Poly4_Poly4']
f_analyticBkgCombA_format['summary']    = f_analyticBkgCombA_format['Poly4_Poly4'] #['Poly2_Poly3']
f_analyticBkgCombA_format['Test3']      = f_analyticBkgCombA_format['Poly2_Poly3']

setupBuildAnalyticBkgCombA = {
    'objName': "f_bkgCombA",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [
    ]
}


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

f_analyticBkgA_KStar_format['DEFAULT']  = f_analyticBkgA_KStar_format['Gaus2_Poly4']
f_analyticBkgA_KStar_format['belowJpsiA']  = f_analyticBkgA_KStar_format['QuadGaus_Poly4']
#f_analyticBkgA_KStar_format['belowJpsiB']  = f_analyticBkgA_KStar_format['QuadGaus_Poly4']
setupBuildAnalyticBkgA_KStar = {
    'objName': "f_bkgA_KStar",
    'varNames': ["CosThetaK", "CosThetaL"],
    'factoryCmd': [
    ]
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

f_BkgM_KStar_format['DEFAULT'] = f_BkgM_KStar_format['Double_Crystal_Ball']
f_BkgM_KStar_format['belowJpsiA'] = f_BkgM_KStar_format['Gaus']
f_BkgM_KStar_format['belowJpsiB'] = f_BkgM_KStar_format['Gaus']
f_BkgM_KStar_format['belowJpsiC'] = f_BkgM_KStar_format['Gaus2']
setupBuildBkgM_KStar = {
    'objName': "f_bkgM_KStar",
    'varNames': ["Bmass"],
    'factoryCmd': [
    ]
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
    if f_bkgCombAAltA == None:
        f_bkgCombAAltKUp = RooKeysPdf("f_bkgCombAAltKUp",
                                      "f_bkgCombAAltKUp",
                                      CosThetaK,
                                      self.process.sourcemanager.get('dataReader.USB'),
                                      RooKeysPdf.MirrorBoth, Cmd[0])
        f_bkgCombAAltKLo = RooKeysPdf("f_bkgCombAAltKLo",
                                      "f_bkgCombAAltKLo",
                                      CosThetaK,
                                      self.process.sourcemanager.get('dataReader.LSB'),
                                      RooKeysPdf.MirrorBoth, Cmd[1])
        f_bkgCombAAltLUp = RooKeysPdf("f_bkgCombAAltLUp",
                                      "f_bkgCombAAltLUp",
                                      CosThetaL,
                                      self.process.sourcemanager.get('dataReader.USB'),
                                      RooKeysPdf.MirrorBoth, Cmd[2])
        f_bkgCombAAltLLo = RooKeysPdf("f_bkgCombAAltLLo",
                                      "f_bkgCombAAltLLo",
                                      CosThetaL,
                                      self.process.sourcemanager.get('dataReader.LSB'),
                                      RooKeysPdf.MirrorBoth, Cmd[3])
        for f in f_bkgCombAAltKLo, f_bkgCombAAltKUp, f_bkgCombAAltLLo, f_bkgCombAAltLUp:
            getattr(wspace, 'import')(f)
        wspace.factory("PROD::f_bkgCombAAltAUp(f_bkgCombAAltKUp,f_bkgCombAAltLUp)")
        wspace.factory("PROD::f_bkgCombAAltALo(f_bkgCombAAltKLo,f_bkgCombAAltLLo)")
        wspace.factory("SUM::f_bkgCombAAltA(frac_bkgCombAAltA[0.5,0,1]*f_bkgCombAAltALo,f_bkgCombAAltAUp)")
        f_bkgCombAAltA = wspace.pdf("f_bkgCombAAltA")
        frac_bkgCombAAltA = wspace.var("frac_bkgCombAAltA")
        frac_bkgCombAAltA.setVal(self.process.sourcemanager.get('dataReader.LSB').sumEntries() / (self.process.sourcemanager.get('dataReader.LSB').sumEntries() + self.process.sourcemanager.get('dataReader.USB').sumEntries()))
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
    wspace.factory("nBkgKStar[{0}, 0, 1000]".format(self.process.sourcemanager.get('KsigMCReader.Fit').sumEntries()*35.9/2765.2853))
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
stdWspaceReader = WspaceReader(CFG_WspaceReader); stdWspaceReader.name="stdWspaceReader"
def customizeWspaceReader(self):
    self.cfg['fileName'] = "{0}/input/wspace_{1}.root".format(modulePath, q2bins[self.process.cfg['binKey']]['label'])
    self.cfg['wspaceTag'] = sharedWspaceTagString.format(binLabel=q2bins[self.process.cfg['binKey']]['label'])
stdWspaceReader.customize = types.MethodType(customizeWspaceReader, stdWspaceReader)

CFG_PDFBuilder = ObjProvider.templateConfig()
stdPDFBuilder = ObjProvider(copy(CFG_PDFBuilder)); stdPDFBuilder.name="stdPDFBuilder"
def customizePDFBuilder(self):
    """Customize pdf for q2 bins"""
    setupBuildAnalyticBkgCombA['factoryCmd'] = f_analyticBkgCombA_format.get(self.process.cfg['binKey'], f_analyticBkgCombA_format['DEFAULT'])
    setupBuildAnalyticBkgA_KStar['factoryCmd'] = f_analyticBkgA_KStar_format.get(self.process.cfg['binKey'], f_analyticBkgA_KStar_format['DEFAULT'])
    setupBuildBkgM_KStar['factoryCmd'] = f_BkgM_KStar_format.get(self.process.cfg['binKey'], f_BkgM_KStar_format['DEFAULT'])
    setupBuildEffiSigA['factoryCmd'] = f_effiSigA_format.get(self.process.cfg['binKey'], f_effiSigA_format['DEFAULT'])
    buildAnalyticBkgCombA = functools.partial(buildGenericObj, **setupBuildAnalyticBkgCombA)
    buildAnalyticBkgA_KStar = functools.partial(buildGenericObj, **setupBuildAnalyticBkgA_KStar)
    buildBkgM_KStar = functools.partial(buildGenericObj, **setupBuildBkgM_KStar)
    buildEffiSigA = functools.partial(buildGenericObj, **setupBuildEffiSigA)
    
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
