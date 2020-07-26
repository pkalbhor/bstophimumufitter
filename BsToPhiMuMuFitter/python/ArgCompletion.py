from BsToPhiMuMuFitter.plotCollection import plotterCfg
import BsToPhiMuMuFitter.seqCollection as seqCollection
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
import os, re

seqCollection.SetSequences()

seqKey  = seqCollection.predefined_sequence.keys()
binKey  = [q2bins[k]['label'] for k in q2bins.keys()]
plotList= plotterCfg['plots'].keys()

dirlist = re.findall(r"\w*.py\b",  " ".join(os.listdir(modulePath)))

print dirlist
print binKey
print seqKey
print plotList
print " ".join(dirlist+binKey+seqKey+plotList)
#os.system("""complete -W \"{0}\" python""".format(List))
