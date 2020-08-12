import os, sys, shelve, math, glob
from subprocess import call
from copy import copy, deepcopy
import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper
import BsToPhiMuMuFitter.python.ArgParser as ArgParser

class BatchTaskWrapper(AbsBatchTaskWrapper.AbsBatchTaskWrapper):                                                                   
    def createJdl(self, parser_args):                                                                                              
        jdl = self.createJdlBase()
        jdl += """Transfer_Input_Files = {0}/seqCollection.py""".format(ArgParser.modulePath)
        for BinKey in parser_args.binKey:                                                                                          
            jdl += """ 
arguments = -b {binKey} -s {seqKey} --Year {Year} {TwoStep}
queue {nJobs}""" 
            jdl = jdl.format(binKey=BinKey, seqKey=parser_args.seqKey, nJobs=self.cfg['nJobs'], executable=ArgParser.modulePath+"/seqCollection.py", Year=parser_args.Year, TwoStep="--TwoStep" if parser_args.TwoStep else "")
        return jdl    

setupBatchTask = deepcopy(BatchTaskWrapper.templateCfg())
setupBatchTask.update({    
    'nJobs': 1,           
    'queue': "longlunch",  
})


if __name__ == '__main__':                 
    wrappedTask = BatchTaskWrapper(        
        "myBatchTask",                     
        ArgParser.modulePath+"/batchTask_seqCollection",
        cfg=setupBatchTask)                

    parser = AbsBatchTaskWrapper.BatchTaskParser
    parser.set_defaults(wrapper=wrappedTask)    

    seqParser=ArgParser.SetParser(add_help=False)
    parser._add_container_actions(seqParser)
    ArgParser.add_help(parser)
    args = parser.parse_args()
    from BsToPhiMuMuFitter.anaSetup import q2bins
    from BsToPhiMuMuFitter.python.datainput import allBins
    if args.binKey =="all":
        args.binKey = [q2bins[k]['label'] for k in allBins]
    else:
        args.binKey = [args.binKey]
    args.func(args)
    sys.exit()




