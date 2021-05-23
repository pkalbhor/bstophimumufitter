from v2Fitter.FlowControl.Path import Path
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
from collections import OrderedDict

class StdTableMaker(Path):
    """Standard Latex table maker"""
    def __init__(self, cfg):
        super(StdTableMaker, self).__init__(cfg)
        self.reset()

    def reset(self):
        super(StdTableMaker, self).reset()
        self.binKeyToLine = OrderedDict()
        self.baseIndentLevel = 2
        self.indent = "  "
        self.ccfg = {}

    @classmethod
    def templateConfig(cls):
        cfg = {"name": "TableMaker",
                "Titles" : [],
                "DbNames" : [],
                "DbValue" : [],
                "ExcludeBins" : ["abovePsi2s", "abovePsi2sA", "abovePsi2sB"],}
        return cfg

    def _runPath(self):
        """Main method"""
        self.BeginDoc()
        for TSeq in self.process.cfg['args'].TSeq:
            for Year in [2016, 2017, 2018]:
                self.process.cfg['args'].Year = Year
                self.BinKeyList(TSeq)
                self.CompileTable(TSeq)
        self.EndDoc()

    def BeginDoc(self):
        print(r"\documentclass[a4paper, 11pt, table]{article}")
        print(r"\usepackage[showframe=false, margin=0cm, left=1.5cm, right=1.5cm, top=0.5cm,bottom=1.5cm, ignorehead ]{geometry}")
        print(r"\usepackage{graphicx, amsmath, xcolor, adjustbox}")
        print(r"\begin{document}")

    def EndDoc(self):
        print(r"\end{document}")

    def BinKeyList(self, TSeq):
        self.binKeyToLine['summaryLowQ2'] = ["LowQ2", r"1.00 -- 6.00"]
        self.binKeyToLine['belowJpsiA']   = ["1A", r"1.00 -- 2.00"]
        self.binKeyToLine['belowJpsiB']   = ["1B", r"2.00 -- 5.00"]
        self.binKeyToLine['belowJpsiC']   = ["1C", r"5.00 -- 8.00"]
        self.binKeyToLine['jpsi']         = ["2", r"8.00 -- 11.0", r"\multicolumn{3}{|c|} {$J/\psi$ resonance region}"]
        self.binKeyToLine['betweenPeaks'] = ["3", r"11.0 -- 12.5"]
        self.binKeyToLine['psi2s']       =  ["4", r"12.5 -- 15.00", r"\multicolumn{3}{|c|} {$\psi'$ resonance region}"]
        self.binKeyToLine['abovePsi2s']  =  ["5", r"15.00 -- 19.00"]
        self.binKeyToLine['abovePsi2sA'] =  ["5A", r"15.00 -- 17.00"]
        self.binKeyToLine['abovePsi2sB'] =  ["5B", r"17.00 -- 19.00"]
        
        for xbin in self.ccfg[str(self.process.cfg['args'].Year)][TSeq]["ExcludeBins"]:
            self.binKeyToLine.pop(xbin)

    def CompileTable(self, TSeq):
        Year = self.process.cfg['args'].Year
        #import pdb; pdb.set_trace()
        seq = self.ccfg[str(Year)][TSeq]
        print(r"\begin{table}[!htbp]")
        print(r"\centering")
        if TSeq=='effiFitter': print(r"\begin{adjustbox}{width=1.1\textwidth,center=\textwidth}")
        print(self.indent * (self.baseIndentLevel + 0) + r"\begin{{tabular}}{{|{}|}}".format("|".join(["c" for a in range(2+len(seq['Titles']))])))
        print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        if TSeq =="effiFitter":
            print(self.indent * (self.baseIndentLevel + 1) + r"\multicolumn{2}{|c|}{%d} & \multicolumn{5}{|c|}{cos$\theta_K$} & \multicolumn{5}{|c|} {cos$\theta_L$} & \multicolumn{5}{|c|} {Corr. Term} \\"%(Year))
            print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        print(self.indent * (self.baseIndentLevel + 1) + r"$q^2$ bin index & $q^2$ range (in $GeV^2$) & {} \\".format(" & ".join(seq['Titles'])))
        print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        import shelve
        for binKey, latexLine in self.binKeyToLine.items():
            if binKey in ['jpsi', 'psi2s']: continue
            db = shelve.open(r"{0}/fitResults_{1}.db".format("../plots_%d"%(Year), q2bins[binKey]['label']))
            for dbname, dbvalue in zip(seq['DbNames'], seq['DbValue']):
                try:
                    dtype = type(db[dbname][dbvalue])
                    text = r"${}$".format(db[dbname][dbvalue]) if dtype==int else r"${0:.01f}$".format(db[dbname][dbvalue])
                    if (dbvalue=='covQual'and db[dbname][dbvalue]<3): text = r"\cellcolor{yellow}%s"%(text)
                    latexLine.append(text)
                except KeyError:
                    latexLine.append(r"$-$")
            print(self.indent * (self.baseIndentLevel + 1) + " & ".join(latexLine) + r" \\")
            print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        print(self.indent * (self.baseIndentLevel + 1) + r"\end{tabular}")
        if TSeq=='effiFitter': print(r"\end{adjustbox}")
        print(r"\caption{Status of %s. Year %d}"%(TSeq.replace('_', ' '), Year))
        print(r"\end{table}")
        db.close()
