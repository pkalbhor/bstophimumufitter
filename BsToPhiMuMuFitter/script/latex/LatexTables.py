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

    @classmethod
    def templateConfig(cls):
        cfg = {
            "name": "TableMaker",
            "Titles" : [],
            "DbNames" : [],
            "DbValue" : [],
            "ExcludeBins" : ["abovePsi2s", "abovePsi2sA", "abovePsi2sB"],
        }
        return cfg

    def _runPath(self):
        """Main methoMain methodd"""
        self.BinKeyList()
        self.CompileTable()

    def BinKeyList(self):
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
        
        for xbin in self.cfg["ExcludeBins"]:
            self.binKeyToLine.pop(xbin)

    def CompileTable(self):
        print(self.indent * (self.baseIndentLevel + 0) + r"\begin{{tabular}}{{|{}|}}".format("|".join(["c" for a in range(2+len(self.cfg['Titles']))])))
        print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        if self.process.cfg['args'].TSeq =="effiFitter":
            print(self.indent * (self.baseIndentLevel + 1) + r"\multicolumn{2}{|c|}{%d} & \multicolumn{5}{|c|}{cos$\theta_K$} & \multicolumn{5}{|c|} {cos$\theta_L$} & \multicolumn{5}{|c|} {Corr. Term} \\"%(self.process.cfg['args'].Year))
            print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        print(self.indent * (self.baseIndentLevel + 1) + r"$q^2$ bin index & $q^2$ range (in $GeV^2$) & {} \\".format(" & ".join(self.cfg['Titles'])))
        print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        print(self.indent * (self.baseIndentLevel + 1) + r"\hline")
        import shelve
        for binKey, latexLine in self.binKeyToLine.items():
            if binKey in ['jpsi', 'psi2s']: continue
            db = shelve.open(r"{0}/fitResults_{1}.db".format(self.process.dbplayer.absInputDir, q2bins[binKey]['label']))
            for dbname, dbvalue in zip(self.cfg['DbNames'], self.cfg['DbValue']):
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
