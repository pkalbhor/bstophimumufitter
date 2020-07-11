import os, sys, shelve, math, glob
from subprocess import call
from copy import copy, deepcopy
from BsToPhiMuMuFitter.python.datainput import allBins
from BsToPhiMuMuFitter.anaSetup import q2bins, modulePath
import BsToPhiMuMuFitter.StdFitter as StdFitter
import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper


class BatchTaskWrapper(AbsBatchTaskWrapper.AbsBatchTaskWrapper):                                                                   
    def createJdl(self, parser_args):                                                                                              
        jdl = self.createJdlBase()
        jdl += """Transfer_Input_Files = {0}/seqCollection.py""".format(modulePath)
        for BinKey in parser_args.binKey:                                                                                          
            jdl += """ 
arguments = -b {binKey} -s {seqKey}
queue {nJobs}""" 
            jdl = jdl.format(binKey=BinKey, seqKey=parser_args.seqKey, nJobs=self.cfg['nJobs'], executable=modulePath+"/seqCollection.py",) 
        return jdl    

setupBatchTask = deepcopy(BatchTaskWrapper.templateCfg())
setupBatchTask.update({    
    'nJobs': 20,           
    'queue': "longlunch",  
})          

if __name__ == '__main__':                 
    wrappedTask = BatchTaskWrapper(        
        "myBatchTask",                     
        modulePath+"/batchTask_seqCollection",
        cfg=setupBatchTask)                

    parser = AbsBatchTaskWrapper.BatchTaskParser
    parser.add_argument(                   
        '-b', '--binKey',                  
        dest="binKey",                                                                                                                         
        default="summary",                 
        help="Select q2 bin with binKey"    )
                      
    parser.add_argument(
        '-s', '--seqKey',
        dest="seqKey",
        type=str,      
        default="buildPdfs",     
        help="Sequence name to execute")
    args = parser.parse_args()
    parser.set_defaults(
        wrapper=wrappedTask
    )    
    args = parser.parse_args()
    if args.binKey =="all":
        args.binKey = [q2bins[k]['label'] for k in allBins]
        #p.cfg['bins'] = args.binKey
    else:
        #p.cfg['bins'] = [args.binKey]
        args.binKey = [args.binKey] #[key for key in q2bins.keys() if q2bins[key]['label']==args.binKey]
    args.func(args)
    sys.exit()




