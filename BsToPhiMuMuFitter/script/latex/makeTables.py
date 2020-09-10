#!/usr/bin/env python
# vim: set sw=4 sts=4 fdm=indent fdl=0 fdn=3 nopaste et:

from __future__ import print_function

import os
import math
import shelve
from collections import OrderedDict

import ROOT
import BsToPhiMuMuFitter.cpp

from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from BsToPhiMuMuFitter.StdFitter import unboundFlToFl, unboundAfbToAfb
from BsToPhiMuMuFitter.StdProcess import p
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

# For developers:
#   * Input db is forced to be StdProcess.dbplayer.absInputDir
#   * function name for labelled table is table_label1[_label2]

#dbplayer = FitDBPlayer(absInputDir=os.path.join(modulePath, "plots_2018"))
#p.addService("dbplayer", dbplayer)

#db_dir = p.dbplayer.absInputDir

indent = "  "

def table_sysFL_sysAFB():
    baseIndentLevel = 2
    for var in ["fl", "afb"]:
        dbKeyToLine = OrderedDict()
        dbKeyToLine['syst_randEffi'] = [r"Limited MC size"]
        dbKeyToLine['syst_altEffi'] = [r"Eff.\ mapping"]
        dbKeyToLine['syst_simMismodel'] = [r"Simu.\ mismodel"]
        dbKeyToLine['syst_altSP'] = [r"$S$ - $P$ wave interf.\ "]
        dbKeyToLine['syst_altBkgCombA'] = [r"Comb.\ Bkg.\ shape"]
        dbKeyToLine['syst_vetoJpsiX'] = [r"$J/\psi + X$ contrib.\ "]
        dbKeyToLine['syst_altFitRange'] = [r"$B$ mass range"]
        totalErrorLine = ["Total"]
        for binKey in ['belowJpsi', 'betweenPeaks', 'abovePsi2s', 'summary']:
            db = shelve.open("{0}/fitResults_{1}.db".format(db_dir, q2bins[binKey]['label']))
            totalSystErr = 0.
            for systKey, latexLine in dbKeyToLine.items():
                err = db["{0}_{1}".format(systKey, var)]['getError']
                latexLine.append("{0:.03f}".format(err))
                totalSystErr += pow(err, 2)
            db.close()
            totalErrorLine.append("{0:.03f}".format(math.sqrt(totalSystErr)))

        print("[table_sysFL_sysAFB] Printing table of syst. unc. for {0}".format(var))
        print("")
        print(indent * (baseIndentLevel + 0) + r"\begin{tabular}{|l|c|c|c|c|}")
        print(indent * (baseIndentLevel + 1) + r"\hline")
        print(indent * (baseIndentLevel + 1) + r"Syst.\ err.\ $\backslash$ $q^2$ bin & 1 & 3 & 5 & 0 \\")
        print(indent * (baseIndentLevel + 1) + r"\hline")
        print(indent * (baseIndentLevel + 1) + r"\hline")
        print(indent * (baseIndentLevel + 1) + r"\multicolumn{5}{|c|}{Uncorrelated systematic uncertainties} \\")
        print(indent * (baseIndentLevel + 1) + r"\hline")
        for systKey, latexLine in dbKeyToLine.items():
            print(indent * (baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")
        print(indent * (baseIndentLevel + 1) + r"\hline")
        print(indent * (baseIndentLevel + 1) + " & ".join(totalErrorLine) + r" \\")
        print(indent * (baseIndentLevel + 1) + r"\hline")
        print(indent * (baseIndentLevel + 0) + r"\end{tabular}")
        print("")

def table_yields():
    baseIndentLevel = 2
    print("[table_yields] Printing table of yields")
    print("")
    print(indent * (baseIndentLevel + 0) + r"\begin{tabular}{|c|c|c|}")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"$q^2$ bin & $Y_S$ & $Y^C_B$ \\")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"\hline")

    binKeyToLine = OrderedDict()
    for binKey in q2bins.keys():
        if binKey in ['jpsi', 'psi2s', 'peaks', 'abovePsi2sA', 'abovePsi2sB']:
            continue
        binKeyToLine[binKey] = [q2bins[binKey]['label'].strip('bin')]
        #binKeyToLine['betweenPeaks'] = ["3"]
        #binKeyToLine['abovePsi2s'] = ["5"]
        #binKeyToLine['summary'] = ["0"]
    for binKey, latexLine in binKeyToLine.items():
        db = shelve.open("{0}/fitResults_{1}.db".format(db_dir, q2bins[binKey]['label']))
        latexLine.append("${0:.01f} \pm {1:.01f}$".format(db['nSig']['getVal'], db['nSig']['getError']))
        latexLine.append("${0:.01f} \pm {1:.01f}$".format(db['nBkgComb']['getVal'], db['nBkgComb']['getError']))
        db.close()
        print(indent * (baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")

    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 0) + r"\end{tabular}")
    print("")

def table_coverageAFBFL():
    baseIndentLevel = 2
    print("[table_coverageAFBFL] Printing table of stat error coverage")
    print("")
    print(indent * (baseIndentLevel + 0) + r"\begin{tabular}{|c|c|c|}")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"$q^2$ bin & $A_{FB}$ & $F_{L}$ \\")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"\hline")

    binKeyToLine = OrderedDict()
    binKeyToLine['belowJpsi'] = ["1"]
    binKeyToLine['betweenPeaks'] = ["3"]
    binKeyToLine['abovePsi2s'] = ["5"]
    binKeyToLine['summary'] = ["0"]
    for binKey, latexLine in binKeyToLine.items():
        db = shelve.open("{0}/fitResults_{1}.db".format(db_dir, q2bins[binKey]['label']))
        latexLine.append("{0:.1f}\%".format(db['stat_FC_afb']['coverage'] * 100.))
        latexLine.append("{0:.1f}\%".format(db['stat_FC_fl']['coverage'] * 100.))
        db.close()
        print(indent * (baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")

    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 0) + r"\end{tabular}")
    print("")

def table_dataresAFBFL(self):
    baseIndentLevel = 2

    print("[table_dataresAFBFL] Printing table of final result")
    print("")
    print(indent * (baseIndentLevel + 0) + r"\begin{tabular}{|c|c|c|c|c|}")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"$q^2$ bin index & $q^2$ range (in $GeV^2$) & Signal Yield & $A_{6}$ & $F_{L}$ \\")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"\hline")

    binKeyToLine = OrderedDict()
    binKeyToLine['belowJpsiA'] = ["1A", r"1.00 -- 2.00"]
    binKeyToLine['belowJpsiB'] = ["1B", r"2.00 -- 5.00"]
    binKeyToLine['belowJpsiC'] = ["1C", r"5.00 -- 8.00"]
    binKeyToLine['jpsi'] = ["2", r"8.00 -- 11.00", r"\multicolumn{3}{|c|} {$J/\psi$ resonance region}"]
    binKeyToLine['betweenPeaks'] = ["3", r"11.00 -- 12.5"]
    binKeyToLine['psi2s'] = ["4", r"12.5 -- 15.00", r"\multicolumn{3}{|c|} {$\psi'$ resonance region}"]
    #binKeyToLine['abovePsi2sA'] = ["5A", r"15.00 -- 17.00"]
    #binKeyToLine['abovePsi2sB'] = ["5B", r"17.00 -- 19.00"]
    binKeyToLine['abovePsi2s'] = ["5", r"15.00 -- 19.00"]
    binKeyToLine['summaryLowQ2'] = ["LowQ2", r"1.00 -- 6.00"]
    binKeyToLine['summary'] = ["0", r"$1A$+$1B$+$1C$+$3$+$5$"]

    syst_sources = [
        #'syst_randEffi',
        #'syst_altEffi',
        #'syst_simMismodel',
        #'syst_altSP',
        #'syst_altBkgCombA',
        #'syst_vetoJpsiX',
        #  'syst_altFitRange',
    ]
    for binKey, latexLine in binKeyToLine.items():
        if binKey not in ['jpsi', 'psi2s']:
            db = shelve.open(r"{0}/fitResults_{1}.db".format(self.process.dbplayer.absInputDir, q2bins[binKey]['label']))
            latexLine.append(r"${0:.01f} \pm {1:.01f}$".format(db['nSig']['getVal'], db['nSig']['getError'])) #(0., 0.))
            fl = unboundFlToFl(db['unboundFl']['getVal'])
            afb = unboundAfbToAfb(db['unboundAfb']['getVal'], fl)

            yyFlErrHi = unboundFlToFl(db['unboundFl']['getVal'] + db['unboundFl']['getErrorHi']) - fl
            yyFlErrLo = fl - unboundFlToFl(db['unboundFl']['getVal'] + db['unboundFl']['getErrorLo'])
            yyAfbErrHi = unboundAfbToAfb(db['unboundAfb']['getVal'] + db['unboundAfb']['getErrorHi'], fl) - afb
            yyAfbErrLo = afb - unboundAfbToAfb(db['unboundAfb']['getVal'] + db['unboundAfb']['getErrorLo'], fl)

            latexLine.append("${0:.2f}^{{{1:+.2f}}}_{{-{2:.2f}}}$".format( # \pm {3:.2f}$".format(
                afb, yyAfbErrHi, yyAfbErrLo
                #db['stat_FC_afb']['getErrorHi'],
                #db['stat_FC_afb']['getErrorLo'],
                #math.sqrt(sum([pow(db[v + '_afb']['getError'], 2) for v in syst_sources]))
                ))
            latexLine.append("${0:.2f}^{{{1:+.2f}}}_{{-{2:.2f}}}$".format( # \pm {3:.2f}$".format(
                fl, yyFlErrHi, yyFlErrLo
                #db['stat_FC_fl']['getErrorHi'],
                #db['stat_FC_fl']['getErrorLo'],
                #math.sqrt(sum([pow(db[v + '_fl']['getError'], 2) for v in syst_sources]))
                ))
            db.close()
        print(indent * (baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")
        print(indent * (baseIndentLevel + 1) + r"\hline")

    print(indent * (baseIndentLevel + 0) + r"\end{tabular}")
    print("")

def table_FinalDataresAFBFL(self):
    table_dataresAFBFL(self)

def table_FitResults():
    baseIndentLevel = 2                                                                                                                        
    print("[table_FitResults] Printing table of Fit-Results")
    print("")
    print(indent * (baseIndentLevel + 0) + r"\begin{tabular}{|c|l|l|l|l|l|}")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"$q^2$ bin & SigGEN & Sig2D & SigM & SigMDCB & BkgCombA & Final \\")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"\hline")
 
    binKeyToLine = OrderedDict()
    for binKey in q2bins.keys():
        if binKey in ['jpsi', 'psi2s', 'peaks']:
            continue
        binKeyToLine[binKey] = [q2bins[binKey]['label'].strip('bin')]
    for binKey, latexLine in binKeyToLine.items():
        db = shelve.open("{0}/fitResults_{1}.db".format(db_dir, q2bins[binKey]['label']))
        latexLine.append("${0}$ nll:${1:10.1f}$ ".format(db['sigAFitter.migrad']['status'], db['sigAFitter.migrad']['nll']))
        latexLine.append("${0}$ nll:${1:10.1f}$ ".format(db['sig2DFitter.migrad']['status'], db['sig2DFitter.migrad']['nll']))
        latexLine.append("${0}$ nll:${1:10.1f}$ ".format(db['sigMFitter.migrad']['status'], db['sigMFitter.migrad']['nll']))
        latexLine.append("${0}$ nll:${1:10.1f}$ ".format(db['sigMDCBFitter.migrad']['status'] if 'sigMDCBFitter.migrad' in db.keys() else 8, db['sigMDCBFitter.migrad']['nll'] if 'sigMDCBFitter.migrad' in db.keys() else 8))
        latexLine.append("${0}$ nll:${1:10.1f}$ ".format(db['bkgCombAFitter.migrad']['status'], db['bkgCombAFitter.migrad']['nll']))
        latexLine.append("${0}$ nll:${1:10.1f}$ ".format(db['finalFitter.migrad']['status'], db['finalFitter.migrad']['nll']))
        db.close()
        print(indent * (baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")
             
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 0) + r"\end{tabular}")
    print("")
 
def EffiTable(self):
    baseIndentLevel = 2                                                                                                                        
    print("[table_FitResults] Printing table of Efficiency Numbers")
    print("")
    print(indent * (baseIndentLevel + 0) + r"\begin{tabular}{|c|c|l|l|l|}")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"$q^2$ bin & Range & After Final Cuts & With No Cuts & Efficiency \\")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 1) + r"\hline")
    binKeyToLine = OrderedDict()
    for binKey in q2bins.keys():
        if binKey in ['jpsi', 'psi2s', 'peaks', 'abovePsi2sA', 'abovePsi2sB', 'Test1', 'Test2']:
            continue
        binKeyToLine[binKey] = [q2bins[binKey]['label'].strip('bin')]
    for binKey, latexLine in binKeyToLine.items():
        EFile = ROOT.TFile.Open("../data/TotalEffHists_{0}_{1}.root".format(self.process.cfg['args'].Year, q2bins[binKey]['label']), "READ")
        effi = EFile.Get('h2Eff_accXrec_{}'.format(binKey))
        latexLine.append("${}$".format(q2bins[binKey]['latexLabel']))
        latexLine.append("${:.0f}$".format(effi.GetPassedHistogram().GetEntries()))
        latexLine.append("${:.0f}$".format(effi.GetTotalHistogram().GetEntries()))
        latexLine.append("${:.5f}$".format(effi.GetPassedHistogram().GetEntries()/effi.GetTotalHistogram().GetEntries()))
        EFile.Close()
        print(indent * (baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")     
    print(indent * (baseIndentLevel + 1) + r"\hline")
    print(indent * (baseIndentLevel + 0) + r"\end{tabular}")
    print("")


if __name__ == '__main__':
    #  table_sysFL_sysAFB()
    #table_yields()
    #  table_coverageAFBFL()
    #  table_dataresAFBFL()
    table_FinalDataresAFBFL(p)
    #table_FitResults()
