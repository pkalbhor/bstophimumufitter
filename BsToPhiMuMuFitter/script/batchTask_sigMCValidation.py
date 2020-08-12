#!/usr/bin/env python
# vim: set sts=4 sw=4 fdm=indent fdl=1 fdn=3 et:

import os, pdb, sys, shelve, math, glob
from subprocess import call
from copy import copy, deepcopy

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True # supress ROOT parser options
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
import BsToPhiMuMuFitter.python.ArgParser as ArgParser
parentParser=ArgParser.SetParser(False)      # Mandatory for passing commandline options to other modules
args=parentParser.parse_known_args()[0]

import BsToPhiMuMuFitter.StdFitter as StdFitter
from BsToPhiMuMuFitter.StdProcess import p
from BsToPhiMuMuFitter.python.datainput import allBins
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection
import BsToPhiMuMuFitter.plotCollection as plotCollection
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

ROOT.gROOT.ProcessLine(
"""struct MyTreeContent {
   Double_t     fl;
   Double_t     afb;
   Double_t     fitstatus;
   Double_t     events;
   Double_t     nSig;
   Double_t     nBkgComb;
   Double_t     nll;
};""")

import v2Fitter.Fitter.AbsToyStudier as AbsToyStudier
class SigMCStudier(AbsToyStudier.AbsToyStudier):
    """"""
    def getSubDataEntries(self, setIdx):
        try:
            db = shelve.open(self.process.dbplayer.odbfile)
            expectedYield = db['nSig']['getVal']
        finally:
            db.close()
        yields = ROOT.gRandom.Poisson(expectedYield)
        self.logger.logINFO("SubDataSet has expected yields {0} in set {1}".format(yields, setIdx))
        return yields

    def _preSetsLoop(self):
        self.otree = ROOT.TTree("tree", "")
        self.treeContent = ROOT.MyTreeContent()
        self.otree.Branch("fl", ROOT.AddressOf(self.treeContent, 'fl'), 'fl/D')
        self.otree.Branch("afb", ROOT.AddressOf(self.treeContent, 'afb'), 'afb/D')
        self.otree.Branch("fitstatus", ROOT.AddressOf(self.treeContent, 'fitstatus'), 'fitstatus/D')
        self.otree.Branch("events", ROOT.AddressOf(self.treeContent, 'events'), 'events/D')
        self.otree.Branch("nSig", ROOT.AddressOf(self.treeContent, 'nSig'), 'nSig/D')
        self.otree.Branch("nBkgComb", ROOT.AddressOf(self.treeContent, 'nBkgComb'), 'nBkgComb/D')
        self.otree.Branch("nll", ROOT.AddressOf(self.treeContent, 'nll'), 'nll/D')
        pass

    def _preRunFitSteps(self, setIdx):
        self.process.dbplayer.resetDB(True)  # Force same starting point

    def _postRunFitSteps(self, setIdx):
        if math.fabs(self.fitter._nll.getVal()) < 1e20:
            self.treeContent.fl = self.process.sourcemanager.get('fl').getVal()
            self.treeContent.afb = self.process.sourcemanager.get('afb').getVal()
            self.treeContent.fitstatus = self.fitter.fitResult['sig2DFitter.migrad']['status']
            self.treeContent.events = self.fitter.data.numEntries()
            self.treeContent.nSig = 0
            self.treeContent.nBkgComb = 0
            self.treeContent.nll = self.fitter._nll.getVal()
            self.otree.Fill()

    def _postSetsLoop(self):
        ofile = ROOT.TFile("setSummary_{0}.root".format(q2bins[self.process.cfg['binKey']]['label']), 'RECREATE')
        ofile.cd()
        self.otree.Write()
        ofile.Close()

    getSubData = AbsToyStudier.getSubData_random

# Define Process
setupSigMCStudier = deepcopy(AbsToyStudier.AbsToyStudier.templateConfig())
setupSigMCStudier.update({
    'name': "sigMCStudier",
    'data': "sigMCReader.Fit",
    'fitter': fitCollection.sig2DFitter,
    'nSetOfToys': 5,
})
sigMCStudier = SigMCStudier(setupSigMCStudier)
fitCollection.sig2DFitter.cfg['data'] = "sigMCValidation.Fit"

# Customize batch task
import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper
class BatchTaskWrapper(AbsBatchTaskWrapper.AbsBatchTaskWrapper):
    def createJdl(self, parser_args):
        jdl = self.createJdlBase()
        for BinKey in parser_args.binKey:
            jdl += """
arguments = -b {binKey} -t {nSetOfToys} run $(Process)
queue {nJobs}
"""
            jdl = jdl.format(binKey=q2bins[BinKey]['label'], nSetOfToys=parser_args.nSetOfToys, nJobs=self.cfg['nJobs'], executable=os.path.abspath(__file__),)
        return jdl

setupBatchTask = deepcopy(BatchTaskWrapper.templateCfg())
setupBatchTask.update({
    'nJobs': 20,
    'queue': "longlunch",
})

# Customize taskSubmitter and jobRunner if needed
def GetParams(f, h, binKey, GEN, name):
    plotCollection.Plotter.canvas.cd()
    ROOT.TLatex().DrawLatexNDC(.73, .89, r"#scale[0.7]{{#chi^{{2}} / NDF: {chi2}/{ndf}}}".format(chi2=round(f.GetChisquare(), 0),ndf=f.GetNDF()) )
    ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
    plotCollection.Plotter.latexDataMarks(['sim'])
    plotCollection.Plotter.latexLumi()
    
    ROOT.TLatex().DrawLatexNDC(.73,.85,r"#scale[0.7]{{#color[2]{{Gen {Name}}}: {param}}}".format(Name="F_{L}" if name=="fl" else "A_{6}", param=round(GEN, 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.81,r"#scale[0.7]{{#color[4]{{Fit {Name}}}   : {param}}}".format(Name="F_{L}" if name=="fl" else "A_{6}", param=round(f.GetParameter(1), 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[3]{{Mean}}   : {param}}}".format(param=round(h.GetMean(), 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(h.GetEntries(), 0)) )
    

# Postproc fit results.
def func_postproc(args):
    """ Fit to fit result and make plots """
    os.chdir(args.wrapper.task_dir)
    p.addService("dbplayer", FitDBPlayer(absInputDir=os.path.join(modulePath, "input", "selected")))
    for binKey in args.binKey:
        ifilename = "setSummary_{0}.root".format(q2bins[binKey]['label'])
        if not os.path.exists(ifilename) or args.forceHadd:
            call(["hadd", "-f", ifilename] + glob.glob('*/setSummary_{0}.root'.format(q2bins[binKey]['label'])))
        ifile = ROOT.TFile(ifilename)
        tree = ifile.Get("tree")

        binWidth = 0.01
        h_setSummary_afb = ROOT.TH1F("h_setSummary_afb", "", int(1.5 / binWidth), -0.75, 0.75)
        h_setSummary_fl = ROOT.TH1F("h_setSummary_fl", "", int(1. / binWidth), 0., 1.)
        
        tree.Draw("afb>>h_setSummary_afb")
        tree.Draw("fl>>h_setSummary_fl")

        f_setSummary_afb = ROOT.TF1("f_setSummary_afb", "gaus", -0.75 + binWidth, 0.75 - binWidth)
        f_setSummary_afb.SetLineColor(ROOT.kBlue)
        h_setSummary_afb.Fit("f_setSummary_afb", "RL")
        
        f_setSummary_fl = ROOT.TF1("f_setSummary_fl", "gaus", binWidth, 1 - binWidth)
        f_setSummary_fl.SetLineColor(ROOT.kBlue)
        h_setSummary_fl.Fit("f_setSummary_fl", "RL")

        # Draw
        db = shelve.open(os.path.join(p.dbplayer.absInputDir, "fitResults_{0}.db".format(q2bins[binKey]['label'])))
        fl_GEN = StdFitter.unboundFlToFl(db['unboundFl_GEN']['getVal'])
        afb_GEN = StdFitter.unboundAfbToAfb(db['unboundAfb_GEN']['getVal'], fl_GEN)
        line = ROOT.TLine()
        line.SetLineWidth(2)
        line.SetLineColor(2)
        line.SetLineStyle(10)
        plotCollection.Plotter.canvas.cd()

        h_setSummary_afb.SetXTitle("A_{6}")
        h_setSummary_afb.SetYTitle("Number of test samples")
        h_setSummary_afb.SetFillColor(3)
        h_setSummary_afb.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_afb.GetMaximum())
        h_setSummary_afb.Draw()
        GetParams(f_setSummary_afb, h_setSummary_afb, binKey, afb_GEN, "a6")
        if args.drawGEN:
            line.DrawLine(afb_GEN, 0, afb_GEN, h_setSummary_afb.GetMaximum())
        plotCollection.Plotter.canvas.Print("h_setSummary_sigMCValidation_a6_{0}.pdf".format(q2bins[binKey]['label']))

        h_setSummary_fl.SetXTitle("F_{L}")
        h_setSummary_fl.SetYTitle("Number of test samples")
        h_setSummary_fl.SetFillColor(3)
        h_setSummary_fl.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_fl.GetMaximum())
        h_setSummary_fl.Draw()
        GetParams(f_setSummary_fl, h_setSummary_fl, binKey, fl_GEN, "fl")
        if args.drawGEN:
            line.DrawLine(fl_GEN, 0, fl_GEN, h_setSummary_fl.GetMaximum())
        plotCollection.Plotter.canvas.Print("h_setSummary_sigMCValidation_fl_{0}.pdf".format(q2bins[binKey]['label']))

        db.close()

if __name__ == '__main__':
    parser = AbsBatchTaskWrapper.BatchTaskParser
    parser._add_container_actions(parentParser) # Connect with main parser
    parser.add_argument(
        '-t', '--nToy',
        dest="nSetOfToys",
        type=int,
        default=5,
        help="Number of subsamples to produce"    )

    BatchTaskSubparserPostproc = AbsBatchTaskWrapper.BatchTaskSubparsers.add_parser('postproc')
    BatchTaskSubparserPostproc.add_argument(
        '--forceHadd',
        dest='forceHadd',
        action='store_true',
        help="Force recreate summary root file."
    )
    BatchTaskSubparserPostproc.add_argument(
        '--drawGEN',
        dest='drawGEN',
        action='store_false',
        help="Draw a line for GEN level value"
    )
    BatchTaskSubparserPostproc.set_defaults(
        func=func_postproc,
    )
    ArgParser.add_help(parser)
    args = parser.parse_args()

    if args.Function_name in ['run', 'submit']:
        p.name="sigMCValidationProcess"
        sigMCStudier.cfg['nSetOfToys']=args.nSetOfToys
        p.setSequence([
            pdfCollection.stdWspaceReader,
            dataCollection.sigMCReader,
            sigMCStudier,
        ])
        p.cfg['args'] = args
        wrappedTask = BatchTaskWrapper(
            "myBatchTask",
            modulePath+"/batchTask_sigMCValidation",
            cfg=setupBatchTask)
    else:
        wrapper = None
    parser.set_defaults(
        wrapper=wrappedTask,
        process=p
    )
    args = parser.parse_args()
    if args.binKey =="all": 
        args.binKey = allBins
        p.cfg['bins'] = args.binKey
    else: 
        p.cfg['bins'] = [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
        args.binKey = p.cfg['bins']
    args.func(args)

    #sys.exit()
"""
from v2Fitter.Fitter.ObjProvider import ObjProvider
BatchJob = ObjProvider({
    'name': "BatchJob",
    'obj': {
        'BatchJob.test': [__main__, ],
    }
})   
"""
