#!/usr/bin/env python
# vim: set sts=4 sw=4 fdm=indent fdl=1 fdn=3 et:

import os, pdb, sys, shelve, math, glob
from subprocess import call
from copy import deepcopy

from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
import BsToPhiMuMuFitter.StdFitter as StdFitter
import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper

#from BsToPhiMuMuFitter.StdProcess import p
import ROOT
import BsToPhiMuMuFitter.cpp
import BsToPhiMuMuFitter.dataCollection as dataCollection
import BsToPhiMuMuFitter.toyCollection as toyCollection
import BsToPhiMuMuFitter.pdfCollection as pdfCollection
import BsToPhiMuMuFitter.fitCollection as fitCollection
import BsToPhiMuMuFitter.plotCollection as plotCollection
import v2Fitter.Fitter.AbsToyStudier as AbsToyStudier
from BsToPhiMuMuFitter.FitDBPlayer import FitDBPlayer

# Define
ROOT.gROOT.ProcessLine(
"""struct MyTreeContent {
   Double_t     fl;
   Double_t     afb;
   Double_t     status;
   Double_t     hesse;
   Double_t     minos;
   Double_t     entries;
   Double_t     nSig;
   Double_t     nBkgComb;
   Double_t     nBkgPeak;
   Double_t     nll;
};""")
from ROOT import addressof

class MixedToyStudier(AbsToyStudier.AbsToyStudier):
    """"""
    def __init__(self, cfg):
        super(MixedToyStudier, self).__init__(cfg)
        self.plotflag = True
        self.DBFlag = True

    def getSubDataEntries(self, setIdx, Type):
        expectedYield = 0
        try:
            db = shelve.open(self.process.dbplayer.odbfile)
            expectedYield += db['PeakFrac']['getVal']*db['nSig']['getVal'] if Type=='nBkgPeak' else db[Type]['getVal']
        finally:
            db.close()
        yields = ROOT.gRandom.Poisson(expectedYield)
        self.logger.logINFO("SubDataSet has expected yields {0} in set {1}".format(yields, setIdx))
        return yields

    def _preSetsLoop(self):
        self.otree = ROOT.TTree("tree", "")
        self.treeContent = ROOT.MyTreeContent()
        self.otree.Branch("fl", addressof(self.treeContent, 'fl'), 'fl/D')
        self.otree.Branch("afb", addressof(self.treeContent, 'afb'), 'afb/D')
        self.otree.Branch("status", addressof(self.treeContent, 'status'), 'status/D')
        self.otree.Branch("hesse", addressof(self.treeContent, 'hesse'), 'hesse/D')
        self.otree.Branch("minos", addressof(self.treeContent, 'minos'), 'minos/D')
        self.otree.Branch("entries", addressof(self.treeContent, 'entries'), 'entries/D')
        self.otree.Branch("nSig", addressof(self.treeContent, 'nSig'), 'nSig/D')
        self.otree.Branch("nBkgComb", addressof(self.treeContent, 'nBkgComb'), 'nBkgComb/D')
        self.otree.Branch("nBkgPeak", addressof(self.treeContent, 'nBkgPeak'), 'nBkgPeak/D')
        self.otree.Branch("nll", addressof(self.treeContent, 'nll'), 'nll/D')
        pass

    def _preRunFitSteps(self, setIdx):
        #self.process.dbplayer.resetDB(True)  # Force same starting point
        import shutil
        cwd=os.getcwd()
        workdir = os.path.join(modulePath, "plots_{}".format(self.process.cfg['args'].Year))
        if self.DBFlag:
            self.DBFlag = False
            shutil.copy(os.path.join(workdir, self.process.dbplayer.odbfile), self.process.dbplayer.odbfile)

    def _runToyCreater(self, Type):                                                                                                            
        from BsToPhiMuMuFitter.toyCollection import GetToyObject
        if Type=='nBkgComb':
            obj = GetToyObject(self.process, 'bkgCombToyGenerator')
            obj.cfg['mixWith'] = "bkgCombToy.{}.Fit".format(self.process.cfg['args'].Year)
            obj.cfg['scale'] = 1.
        if Type=='nBkgPeak':
            obj = GetToyObject(self.process, 'bkgPeakToyGenerator')
            obj.cfg['mixWith'] = "bkgPeakToy.{}.Fit".format(self.process.cfg['args'].Year)
            obj.cfg['scale'] = 1.
        obj.hookProcess(self.process)
        setattr(obj, "logger", self.process.logger)
        obj.customize()
        obj._runPath()
        return obj.data

    def _postRunFitPlotter(self, idx):
        self.plotflag = False
        from BsToPhiMuMuFitter.Plotter import Plotter, defaultPlotRegion, plotterCfg_styles
        import BsToPhiMuMuFitter.plotCollection as plotCollection

        Year = self.process.cfg['args'].Year
        self.process.cfg['args'].list = ['plot_final_WithKStar']
        plotter = plotCollection.GetPlotterObject(self.process)
        plotter.cfg['plots']['plot_final_WithKStar']['kwargs']['pltName'] = "plot_final_{}.{}".format(idx, Year)
        plotter.cfg['plots']['plot_final_WithKStar']['kwargs']['dataReader'] = "SubSampleData.{}".format(Year)

        self.process.cfg['args'].NoImport = True
        self.process.sourcemanager.update("SubSampleData.{}.Fit".format(Year), self.fitter.data)
        self.process.sourcemanager.update("f_final_WithKStar.{}".format(Year), self.fitter.pdf)
        plotter.hookProcess(self.process)
        setattr(plotter, "logger", self.process.logger)
        plotter._runPath()

    def _postRunFitSteps(self, setIdx):
        if math.fabs(self.fitter._nll.getVal()) < 1e20:
            unboundAfb = self.fitter.args.find('unboundAfb').getVal()
            unboundFl  = self.fitter.args.find('unboundFl').getVal()
            self.treeContent.fl = StdFitter.unboundFlToFl(unboundFl)
            self.treeContent.afb = StdFitter.unboundAfbToAfb(unboundAfb, self.treeContent.fl)
            self.treeContent.status = self.fitter.fitResult['{}.migrad'.format(self.fitter.name)]['status']
            self.treeContent.hesse = self.fitter.fitResult['{}.hesse'.format(self.fitter.name)]['status']
            self.treeContent.minos = self.fitter.fitResult['{}.minos'.format(self.fitter.name)]['status']
            self.treeContent.entries = self.fitter.data.numEntries()
            self.treeContent.nSig = self.fitter.args.find('nSig').getVal()
            self.treeContent.nBkgComb = self.fitter.args.find('nBkgComb').getVal()
            self.treeContent.nBkgPeak = self.fitter.pdf.servers().findByName("nBkgPeak").getVal()
            self.treeContent.nll = self.fitter._nll.getVal()
            self.otree.Fill()
            if (unboundFl > 0.95 and abs(unboundAfb) < 0.05 and self.plotflag): self._postRunFitPlotter(setIdx)

    def _postSetsLoop(self):
        ofile = ROOT.TFile("setSummary_{}_{}.root".format(self.process.cfg['args'].Year, q2bins[self.process.cfg['binKey']]['label']), 'RECREATE')
        ofile.cd()
        self.otree.Write()
        ofile.Close()

    getSubData = AbsToyStudier.getSubData_random

# Define Process
def GetMixedToyObject(self):
    Year = self.cfg['args'].Year
    setupMixedToyStudier = deepcopy(AbsToyStudier.AbsToyStudier.templateConfig())
    setupMixedToyStudier.update({
        'name': "mixedToyStudier.{}".format(Year),
        'data': ["sigMCReader.{}.Fit".format(Year), "f_bkgComb.{}".format(Year), "f_bkg_KStar.{}".format(Year)],
        'Type': [(0, 'nSig', 'Sim'), (1, 'nBkgComb', 'Toy'), (2, 'nBkgPeak', 'Toy')],
        'fitter': fitCollection.GetFitterObjects(self, 'finalFitter_WithKStar'),
        'nSetOfToys': 1,
    })
    mixedToyStudier = MixedToyStudier(setupMixedToyStudier)
    mixedToyStudier.cfg['fitter'].cfg['data'] = "sigMCReader.{}.Fit".format(Year)
    mixedToyStudier.cfg['fitter'].cfg['FitMinos'] = [True, ('unboundAfb', 'unboundFl')]
    return mixedToyStudier

# Customize batch task
class BatchTaskWrapper(AbsBatchTaskWrapper.AbsBatchTaskWrapper):
    def createJdl(self, parser_args):
        jdl = self.createJdlBase()
        jdl += """Transfer_Input_Files = {0}/seqCollection.py""".format(modulePath)
        jdl += """
arguments = -b {binKey} -s {seqKey} -y {Year} -t {nSetOfToys} run $(Process)
queue {nJobs}"""
        jdl = jdl.format(binKey = q2bins[parser_args.process.cfg['binKey']]['label'],
                        nSetOfToys=parser_args.nSetOfToys, nJobs=self.cfg['nJobs'],
                        seqKey  = parser_args.process.cfg['args'].seqKey,       
                        Year    = parser_args.process.cfg['args'].Year,         
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
        ifilename = "setSummary_{}_{}.root".format(args.Year, q2bins[binKey]['label'])
        if not os.path.exists(ifilename) or args.forceHadd:
            call(["hadd", "-f", ifilename] + glob.glob('*/setSummary_{}_{}.root'.format(args.Year, q2bins[binKey]['label'])))
        ifile = ROOT.TFile(ifilename)
        tree = ifile.Get("tree")

        binWidth = 0.01
        h_setSummary_afb = ROOT.TH1F("h_setSummary_afb", "", int(1.5 / binWidth), -0.75, 0.75)
        h_setSummary_fl = ROOT.TH1F("h_setSummary_fl", "", int(1. / binWidth), 0., 1.)

        tree.Draw("afb>>h_setSummary_afb", "status==0")
        tree.Draw("fl>>h_setSummary_fl", "status==0")

        f_setSummary_afb = ROOT.TF1("f_setSummary_afb", "gaus", -0.75 + binWidth, 0.75 - binWidth)
        h_setSummary_afb.Fit("f_setSummary_afb")
        h_setSummary_afb.GetFunction("f_setSummary_afb").SetLineColor(4)

        f_setSummary_fl = ROOT.TF1("f_setSummary_fl", "gaus", binWidth, 1 - binWidth)
        h_setSummary_fl.Fit("f_setSummary_fl")
        h_setSummary_fl.GetFunction("f_setSummary_fl").SetLineColor(4)

        # Draw
        db = shelve.open(os.path.join(args.process.dbplayer.absInputDir, "fitResults_{0}.db".format(q2bins[binKey]['label'])))
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
        plotCollection.Plotter.latexDataMarks(['mix'])
        plotCollection.Plotter.canvas.Print("h_setSummary_mixedToyValidation_a6_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))

        h_setSummary_fl.SetXTitle("F_{L}")
        h_setSummary_fl.SetYTitle("Number of test samples")
        h_setSummary_fl.SetFillColor(ROOT.kGreen-10)
        h_setSummary_fl.GetYaxis().SetRangeUser(0., 1.5 * h_setSummary_fl.GetMaximum())
        h_setSummary_fl.Draw()
        GetParams(f_setSummary_fl, h_setSummary_fl, binKey, fl_GEN, "fl")
        if args.drawGEN:
            line.DrawLine(fl_GEN, 0, fl_GEN, h_setSummary_fl.GetMaximum())
        plotCollection.Plotter.latexDataMarks(['mix'])
        plotCollection.Plotter.canvas.Print("h_setSummary_mixedToyValidation_fl_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))

        from copy import deepcopy
        tree.Draw("nSig", "status==0")
        nSigHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))
        tree.Draw("nBkgComb", "status==0")
        nBkgCombHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))
        tree.Draw("nBkgPeak", "status==0")
        nBkgPeakHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))
        tree.Draw("entries", "status==0")
        nTotalHist = deepcopy(ROOT.gPad.GetPrimitive("htemp"))

        # Signal Event Distributions
        nSigHist.Draw()
        nSigHist.SetFillColor(ROOT.kBlue-10)
        #nSigHist.SetLineColor(ROOT.kBlue)
        ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[4]{{Mean}}   : {param}}}".format(param=round(nSigHist.GetMean(), 5)) )
        ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nSigHist.GetEntries(), 0)) )
        ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nSig}} : {param}}}".format(param=round(db['nSig']['getVal'], 0)) )
        plotCollection.Plotter.canvas.Update(); line.DrawLine(db['nSig']['getVal'], 0, db['nSig']['getVal'], ROOT.gPad.GetUymax())
        ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        plotCollection.Plotter.canvas.Print("h_nSig_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))

        #Bkg yield distribution
        nBkgCombHist.Draw()
        nBkgCombHist.SetFillColor(ROOT.kRed-10)
        #nBkgCombHist.SetLineColor(ROOT.kRed)
        ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[2]{{Mean}}   : {param}}}".format(param=round(nBkgCombHist.GetMean(), 5)) )
        ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nBkgCombHist.GetEntries(), 0)) )
        ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nBkg}} : {param}}}".format(param=round(db['nBkgComb']['getVal'], 0)) )
        plotCollection.Plotter.canvas.Update(); line.DrawLine(db['nBkgComb']['getVal'], 0, db['nBkgComb']['getVal'], ROOT.gPad.GetUymax())
        ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        plotCollection.Plotter.canvas.Print("h_nBkgComb_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))
    
        #Peaking Bkg yield distribution
        nBkgPeakHist.Draw()
        nBkgPeakHist.SetFillColor(ROOT.kGreen-10)
        #nBkgPeakHist.SetLineColor(ROOT.kGreen)
        ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[3]{{Mean}}   : {param}}}".format(param=round(nBkgPeakHist.GetMean(), 5)) )
        ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nBkgPeakHist.GetEntries(), 0)) )
        nPeak = db['PeakFrac']['getVal']*db['nSig']['getVal']
        ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nPeak}} : {param}}}".format(param=round(nPeak, 0)) )
        plotCollection.Plotter.canvas.Update(); line.DrawLine(nPeak, 0, nPeak, ROOT.gPad.GetUymax())
        ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        plotCollection.Plotter.canvas.Print("h_nBkgPeak_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))
        
        # Total yield distributions 
        nTotalHist.Draw()
        nTotalHist.SetFillColor(ROOT.kBlue-10)
        #nTotalHist.SetLineColor(ROOT.kBlue)
        ROOT.TLatex().DrawLatexNDC(.73,.77,r"#scale[0.7]{{#color[4]{{Mean}}   : {param}}}".format(param=round(nTotalHist.GetMean(), 5)) )
        ROOT.TLatex().DrawLatexNDC(.73,.73,r"#scale[0.7]{{#color[1]{{Samples}} : {param}}}".format(param=round(nTotalHist.GetEntries(), 0)) )
        nTotal = db['nBkgComb']['getVal']+db['nSig']['getVal']+nPeak
        ROOT.TLatex().DrawLatexNDC(.73,.82,r"#scale[0.7]{{#color[2]{{nTotal}} : {param}}}".format(param=round(nTotal, 0)) )
        plotCollection.Plotter.canvas.Update(); line.DrawLine(nTotal, 0, nTotal, ROOT.gPad.GetUymax())
        ROOT.TLatex().DrawLatexNDC(.45, .89, r"#scale[0.8]{{{latexLabel}}}".format(latexLabel=q2bins[binKey]['latexLabel']))
        plotCollection.Plotter.canvas.Print("h_nTotal_{}_{}.pdf".format(args.Year, q2bins[binKey]['label']))

        db.close()

if __name__ == '__main__': # Not supported anymore
    wrappedTask = BatchTaskWrapper(
        "myBatchTask",
        modulePath+"/batchTask_mixedToyValidation",
        cfg=setupBatchTask)

    parser = AbsBatchTaskWrapper.BatchTaskParser
    parser.add_argument(
        '-b', '--binKey',
        dest="binKey",
        default="summary",
        help="Select q2 bin with binKey"
    )
    parser.add_argument(
        '-t', '--nToy',
        dest="nSetOfToys",
        type=int,
        default=5,
        help="Number of subsamples to produce"    
    )
    parser.set_defaults(
        wrapper=wrappedTask,
        process=p
    )

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

    args = parser.parse_args()
    args.process._sequence[3].cfg['nSetOfToys']=args.nSetOfToys
    #p.cfg['binKey'] = args.binKey
    if args.binKey =="all":
        args.binKey = allBins
        p.cfg['bins'] = args.binKey
    else:
        p.cfg['bins'] = [key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
        args.binKey = p.cfg['bins']   
    args.func(args)

    sys.exit()

