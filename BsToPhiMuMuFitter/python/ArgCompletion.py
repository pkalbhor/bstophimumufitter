from BsToPhiMuMuFitter.python.ArgParser import SetParser, GetBatchTaskParser
parser=GetBatchTaskParser()        
args = parser.parse_known_args()[0]
from   BsToPhiMuMuFitter.StdProcess import p
p.work_dir="plots_{}".format(args.Year)
p.cfg['args'] = args           

from BsToPhiMuMuFitter.plotCollection import GetPlotterObject
import BsToPhiMuMuFitter.seqCollection as seqCollection
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
import os, re

seqKey  = list(seqCollection.predefined_sequence.keys())
binKeys = [q2bins[k]['label'] for k in q2bins.keys()]
plotList= list(GetPlotterObject(p).cfg['plots'].keys())

dirlist = re.findall(r"\w*.py\b",  " ".join(os.listdir(modulePath)))

print(dirlist)
print(binKeys)
print(seqKey)
print(plotList)
List=" ".join(binKeys+seqKey+plotList)
os.system("""complete -W \"{0}\" seqCollection.py """.format(List))
