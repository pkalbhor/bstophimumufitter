#!/usr/bin/env python3
# vim: set sts=4 sw=4 fdm=indent fdl=1 fdn=3 et:

import os, pdb, sys, shelve, math, glob
from subprocess import call
from copy import copy, deepcopy

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True # supress ROOT parser options
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath

import BsToPhiMuMuFitter.StdFitter as StdFitter
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection
import BsToPhiMuMuFitter.plotCollection as plotCollection
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

import v2Fitter.Fitter.AbsToyStudier as AbsToyStudier
class SigMCStudier(AbsToyStudier.AbsToyStudier):
    """"""
    def __init__(self, cfg):                    
        super(SigMCStudier, self).__init__(cfg)
        self.plotflag = True                    
        self.DBFlag = True  
        ROOT.gROOT.ProcessLine(
        """struct MyTreeContent {
           Double_t     fl;
           Double_t     afb;
           Double_t     status;
           Double_t     hesse;
           Double_t     minos;
           Double_t     events;
           Double_t     events16;
           Double_t     events17;
           Double_t     events18;
           Double_t     nSig;
           Double_t     nll;
        };""")      

    def getSubDataEntries(self, setIdx, Type, Year=2016):
        try:
            if self.process.cfg['args'].SimFit:
                db = shelve.open(os.path.join(modulePath, "plots_{}".format(Year), self.process.dbplayer.odbfile), "r")
            else:
                db = shelve.open(self.process.dbplayer.odbfile, "r")
            expectedYield = db[Type]['getVal']
        finally:
            db.close()
        yields = ROOT.gRandom.Poisson(expectedYield)
        self.logger.logINFO("SubDataSet has expected yields {0} in set {1}".format(yields, setIdx))
        return yields

    def _preSetsLoop(self):
        self.otree = ROOT.TTree("tree", "")
        self.treeContent = ROOT.MyTreeContent()
        self.otree.Branch("fl", ROOT.addressof(self.treeContent, 'fl'), 'fl/D')
        self.otree.Branch("afb", ROOT.addressof(self.treeContent, 'afb'), 'afb/D')
        self.otree.Branch("status", ROOT.addressof(self.treeContent, 'status'), 'status/D')
        self.otree.Branch("hesse", ROOT.addressof(self.treeContent, 'hesse'), 'hesse/D')
        self.otree.Branch("minos", ROOT.addressof(self.treeContent, 'minos'), 'minos/D')
        self.otree.Branch("nSig", ROOT.addressof(self.treeContent, 'nSig'), 'nSig/D')
        self.otree.Branch("nll", ROOT.addressof(self.treeContent, 'nll'), 'nll/D')
        if self.process.cfg['args'].SimFit:
            self.otree.Branch("events16", ROOT.addressof(self.treeContent, 'events16'), 'events16/D')
            self.otree.Branch("events17", ROOT.addressof(self.treeContent, 'events17'), 'events17/D')
            self.otree.Branch("events18", ROOT.addressof(self.treeContent, 'events18'), 'events18/D')
        else:
            self.otree.Branch("events", ROOT.addressof(self.treeContent, 'events'), 'events/D')
        pass

    def _preRunFitSteps(self, setIdx):
        #self.process.dbplayer.resetDB(False)  # Force same starting point
        import shutil           
        cwd=os.getcwd()         
        workdir = os.path.join(modulePath, "plots_{}".format(self.process.cfg['args'].Year))
        if self.DBFlag:         
            self.DBFlag = False
            shutil.copy(os.path.join(workdir, self.process.dbplayer.odbfile), self.process.dbplayer.odbfile)

    def _postRunFitSteps(self, setIdx):
        if math.fabs(self.fitter._nll.getVal()) < 1e20:
            SimFit = self.process.cfg['args'].SimFit
            unboundAfb = self.fitter.minimizer.getParameters(self.fitter.dataWithCategories).find('unboundAfb').getVal() if SimFit else self.fitter.args.find('unboundAfb').getVal()
            unboundFl  = self.fitter.minimizer.getParameters(self.fitter.dataWithCategories).find('unboundFl').getVal() if SimFit else self.fitter.args.find('unboundFl').getVal()
            self.treeContent.fl = StdFitter.unboundFlToFl(unboundFl) 
            self.treeContent.afb = StdFitter.unboundAfbToAfb(unboundAfb, self.treeContent.fl)
            #self.treeContent.fl = self.process.sourcemanager.get('fl.{}'.format(self.process.cfg['args'].Year)).getVal()
            #self.treeContent.afb = self.process.sourcemanager.get('afb.{}'.format(self.process.cfg['args'].Year)).getVal()
            self.treeContent.status = self.fitter.migradResult if SimFit else self.fitter.fitResult['{}.migrad'.format(self.fitter.name)]['status']
            self.treeContent.hesse = self.fitter.hesseResult if SimFit else self.fitter.fitResult['{}.hesse'.format(self.fitter.name)]['status']                                      
            self.treeContent.minos = self.fitter.minosResult.status() if SimFit else self.fitter.fitResult['{}.minos'.format(self.fitter.name)]['status']
            if self.process.cfg['args'].SimFit:
                self.treeContent.events16 = self.fitter.data[0].sumEntries()
                self.treeContent.events17 = self.fitter.data[1].sumEntries()
                self.treeContent.events18 = self.fitter.data[2].sumEntries()
            else:
                self.treeContent.events = self.fitter.data.numEntries()
            self.treeContent.nSig = 0
            self.treeContent.nll = self.fitter.minosResult.minNll() if SimFit else self.fitter._nll.getVal()
            self.otree.Fill()

    def _postSetsLoop(self):
        SimFit = self.process.cfg['args'].SimFit
        ofile = ROOT.TFile("setSummary_{}_{}.root".format("Simult" if SimFit else self.process.cfg['args'].Year, q2bins[self.process.cfg['binKey']]['label']), 'RECREATE')
        ofile.cd()
        self.otree.Write()
        ofile.Close()

    getSubData = AbsToyStudier.getSubData_random

# Define Process
def GetToyObject(self):
    Year = self.cfg['args'].Year
    if self.cfg['args'].SimFit:
        from BsToPhiMuMuFitter.fitCollection import SimultaneousFitter_sigMCValidation
        setupSigMCStudier = deepcopy(AbsToyStudier.AbsToyStudier.templateConfig())
        setupSigMCStudier.update({
            'name': "sigMCStudier",
            'data': ["sigMCReader.{}.Fit"],
            'Type': [(0, 'nSig','Sim')],
            'fitter': SimultaneousFitter_sigMCValidation,
            'nSetOfToys': 1,
        })
        sigMCStudier = SigMCStudier(setupSigMCStudier)
        return sigMCStudier
    else:
        setupSigMCStudier = deepcopy(AbsToyStudier.AbsToyStudier.templateConfig())
        setupSigMCStudier.update({
            'name': "sigMCStudier.{0}".format(self.cfg['args'].Year),
            'data': ["sigMCReader.{}.Fit".format(Year)],
            'Type': [(0, 'nSig', 'Sim')], 
            'fitter': fitCollection.GetFitterObjects(self, 'sig3DFitter'),
            'nSetOfToys': 1,
        })
        sigMCStudier = SigMCStudier(setupSigMCStudier)
        sigMCStudier.cfg['fitter'].cfg['data'] = "sigMCValidation.{0}.Fit".format(Year)
        return sigMCStudier

# Customize batch task
import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper
class BatchTaskWrapper(AbsBatchTaskWrapper.AbsBatchTaskWrapper):
    def createJdl(self, parser_args):
        jdl = self.createJdlBase()
        jdl += """Transfer_Input_Files = {0}/seqCollection.py""".format(modulePath)
        jdl += """
arguments = -b {binKey} -s {seqKey} -y {Year} -t {nSetOfToys}{SimFit} run $(Process)
queue {nJobs}
"""
        jdl = jdl.format(binKey = q2bins[parser_args.process.cfg['binKey']]['label'], 
                        nSetOfToys=parser_args.nSetOfToys, nJobs=self.cfg['nJobs'], 
                        seqKey  = parser_args.process.cfg['args'].seqKey,
                        Year    = parser_args.process.cfg['args'].Year,
                        SimFit  = " --SimFit" if parser_args.process.cfg['args'].SimFit else "",
                        executable=os.path.join(modulePath,"seqCollection.py"),)
        return jdl

setupBatchTask = deepcopy(BatchTaskWrapper.templateCfg())
setupBatchTask.update({
    'nJobs': 1,
    'queue': "tomorrow",
})

# Customize taskSubmitter and jobRunner if needed
def GetParams(f, h, binKey, GEN, name):
    plotCollection.Plotter.canvas.cd()
    ROOT.TLatex().DrawLatexNDC(.73, .89, r"#scale[0.7]{{#chi^{{2}} / NDF: {chi2}/{ndf}}}".format(chi2=round(f.GetChisquare(), 0),ndf=f.GetNDF()) )
    ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
    plotCollection.Plotter.latexDataMarks(['sim'])
    #plotCollection.Plotter.latexLumi()
    
    ROOT.TLatex().DrawLatexNDC(.73,.85,r"#scale[0.7]{{#color[2]{{Gen {Name}}}: {param}}}".format(Name="F_{L}" if name=="fl" else "A_{6}", param=round(GEN, 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.81,r"#scale[0.7]{{#color[4]{{Fit {Name}}}   : {param}}}".format(Name="F_{L}" if name=="fl" else "A_{6}", param=round(f.GetParameter(1), 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[3]{{Mean}}   : {param}}}".format(param=round(h.GetMean(), 5)) )
    ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(h.GetEntries(), 0)) )
    

# Postproc fit results.
def func_postproc(args):
    """ Fit to fit result and make plots """
    os.chdir(args.wrapper.task_dir)
    args.process.addService("dbplayer", FitDBPlayer(absInputDir=os.path.join(modulePath, "plots_{}".format(args.Year))))
    for binKey in args.process.cfg['bins']:
        ifilename = "setSummary_{}_{}.root".format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label'])
        if not os.path.exists(ifilename) or args.forceHadd:
            call(["hadd", "-f", ifilename] + glob.glob('*/setSummary_{}_{}.root'.format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label'])))
        ifile = ROOT.TFile(ifilename)
        tree = ifile.Get("tree")

        binWidth = 0.01
        h_setSummary_afb = ROOT.TH1F("h_setSummary_afb", "", int(1.5 / binWidth), -0.75, 0.75)
        h_setSummary_fl = ROOT.TH1F("h_setSummary_fl", "", int(1. / binWidth), 0., 1.)
        
        tree.Draw("afb>>h_setSummary_afb", "status==0")
        tree.Draw("fl>>h_setSummary_fl", "status==0")

        f_setSummary_afb = ROOT.TF1("f_setSummary_afb", "gaus", -0.75 + binWidth, 0.75 - binWidth)
        #f_setSummary_afb.SetLineColor(ROOT.kBlue)
        h_setSummary_afb.Fit("f_setSummary_afb")
        h_setSummary_afb.GetFunction("f_setSummary_afb").SetLineColor(4)

        f_setSummary_fl = ROOT.TF1("f_setSummary_fl", "gaus", binWidth, 1 - binWidth)
        #f_setSummary_fl.SetLineColor(ROOT.kBlue)
        h_setSummary_fl.Fit("f_setSummary_fl")
        h_setSummary_fl.GetFunction("f_setSummary_fl").SetLineColor(4)

        # Draw
        db = shelve.open(os.path.join(args.process.dbplayer.absInputDir, "fitResults_{0}.db".format(q2bins[binKey]['label'])), 'r')
        fl_GEN = StdFitter.unboundFlToFl(db['unboundFl_GEN']['getVal'])
        afb_GEN = StdFitter.unboundAfbToAfb(db['unboundAfb_GEN']['getVal'], fl_GEN)
        line = ROOT.TLine()
        line.SetLineWidth(2)
        line.SetLineColor(2)
        line.SetLineStyle(9)
        plotCollection.Plotter.canvas.cd()

        h_setSummary_afb.SetXTitle("A_{6}")
        h_setSummary_afb.SetYTitle("Number of test samples")
        h_setSummary_afb.SetFillColor(ROOT.kGreen-10)
        h_setSummary_afb.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_afb.GetMaximum())
        h_setSummary_afb.Draw()
        GetParams(f_setSummary_afb, h_setSummary_afb, binKey, afb_GEN, "a6")
        if args.drawGEN:
            line.DrawLine(afb_GEN, 0, afb_GEN, h_setSummary_afb.GetMaximum())
        plotCollection.Plotter.latexDataMarks(['sim'])
        plotCollection.Plotter.canvas.Print("h_setSummary_sigMCValidation_a6_{}_{}.pdf".format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label']))

        h_setSummary_fl.SetXTitle("F_{L}")
        h_setSummary_fl.SetYTitle("Number of test samples")
        h_setSummary_fl.SetFillColor(ROOT.kGreen-10)
        h_setSummary_fl.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_fl.GetMaximum())
        h_setSummary_fl.Draw()
        GetParams(f_setSummary_fl, h_setSummary_fl, binKey, fl_GEN, "fl")
        if args.drawGEN:
            line.DrawLine(fl_GEN, 0, fl_GEN, h_setSummary_fl.GetMaximum())
        plotCollection.Plotter.latexDataMarks(['sim'])
        plotCollection.Plotter.canvas.Print("h_setSummary_sigMCValidation_fl_{}_{}.pdf".format("Simult" if args.SimFit else args.Year, q2bins[binKey]['label']))
        db.close()

if __name__ == '__main__': # Unsupported! This module should be accessible from seqCollection.py
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
            os.path.join(modulePath, "batchTask_sigMCValidation"),
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


