#!/usr/bin/env python
# vim: set sts=4 sw=4 fdm=indent fdl=1 fdn=3 ft=python et:

import os, time, pdb
import abc, random
import tempfile
from copy import copy
from subprocess import call

import v2Fitter.Batch.batchConfig as batchConfig
from v2Fitter.FlowControl.Logger import Logger

from argparse import ArgumentParser, RawTextHelpFormatter

# NOTE:
#   Two steps to keep in mind:
#       * Job submission (with generator), on Host (lxplus)
#       * Processing, on computing nodes.
#   The two steps should completely separated.

class AbsBatchTaskWrapper:
    """"""
    def __init__(self, name="myBatchTask", task_dir=None, cfg=None):
        """Create process from """
        self.name = name
        if os.path.isabs(task_dir):
            # Since relative path differs on local and cluster.
            # Ensure absolute or there will be no output.
            self.task_dir = task_dir
        else:
            raise ValueError("ERROR: task_dir must be an absolute path")
        if not os.path.exists(self.task_dir + "/log"):
            os.makedirs(self.task_dir + "/log")
        self.cfg = cfg if cfg is not None else self.templateCfg()

        self.logger = Logger("task.log")
        self.logger.setAbsLogfileDir(self.task_dir)

    @classmethod
    def templateCfg(cls):
        cfg = {
            'nJobs': 1,
            'queue': batchConfig.BATCH_QUEUE,
            'work_dir': None,
        }
        return cfg

    def createJdlBase(self):
        """ Base of jdl script to be futher decorated in createJdl """
        """"""
        #transfer_output_files = job$(Process),job$(Process).tar.gz
        templateJdl = """
getenv      = True
log         = log/{time}_{seqKey}_{binKey}_$(Process).log
output      = log/{time}_{seqKey}_{binKey}_$(Process).out
error       = log/{time}_{seqKey}_{binKey}_$(Process).err
+JobFlavour = "{JobFlavour}"

initialdir  = {initialdir}
executable  = {executable}
Notify_user = physics.pritam@gmail.com
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
""".format(
        time=str(time.localtime().tm_yday)+'_'+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec),
        seqKey="{seqKey}",
        initialdir=self.task_dir,
        JobFlavour=self.cfg['queue'],
        executable="{executable}",
        binKey="{binKey}")
        return templateJdl

    @abc.abstractmethod
    def createJdl(self, parser_args):
        """ To be customized by users. Start from createJdlBase. """
        raise NotImplementedError

    def getWrappedProcess(self, process, jobId, **kwargs):
        """ To be customized by users. """
        return process

    def runWrappedProcess(self, process, jobId, wrapper_kwargs=None):
        """ Serve as 'main' to be called on computing nodes """
        if wrapper_kwargs is None:
            wrapper_kwargs = {}
        p = self.getWrappedProcess(process, jobId, **wrapper_kwargs)
        if self.cfg['work_dir'] is None:
            label = "SimFit" if p.cfg['args'].SimFit else p.cfg['args'].Year
            p.work_dir = os.path.join(self.task_dir, "{0}_{1}_{jobId:04d}".format(label, p.cfg['args'].binKey, jobId=jobId))
        elif isinstance(self.cfg['work_dir'], str):
            p.work_dir = os.path.join(self.task_dir, self.cfg['work_dir'])
        else:
            p.work_dir = os.path.join(self.task_dir, self.cfg['work_dir'][jobId])
        
        p.setSequence(p._sequence) ## ALERT
        try:
            p.beginSeq()
            p.runSeq()
        finally:
            p.endSeq()
            p.reset()
            for obj in p._sequence: obj.reset()

            # HTCondor does not transfer output directory but only file
            os.chdir(self.task_dir)

# Followings are pre-defined procedure to reduce routine

BatchTaskParser = ArgumentParser(add_help=False, conflict_handler='resolve',
    description="""
Routine to run a batch task on HTCondor.""", epilog="""
When running batch tasks, users must complete following step(s):
    * Set the task wrapper with
        BatchTaskParser.set_defaults(
            wrapper=YOUR_WRAPPER_INSTANCE,
            process=YOUR_PROCESS_INSTANCE
            )
Optional customization:
    * Customize and hook a submit function with BatchTaskSubparserSubmit.set_defaults(func=?)
    * Customize and hook a run function with BatchTaskSubparserRun.set_defaults(func=?)
""", formatter_class=RawTextHelpFormatter)

BatchTaskSubparsers = BatchTaskParser.add_subparsers(help='Functions', dest='Function_name')
BatchTaskSubparserSubmit = BatchTaskSubparsers.add_parser('submit')
BatchTaskSubparserSubmit.add_argument(
    "-q", "--queue",
    dest="queue",
    type=str,
    help="JobFlavour of HTCondor.")
BatchTaskSubparserSubmit.add_argument(
    "-n", "--nJobs",
    dest="nJobs",
    type=int,
    help="Number of jobs.")
BatchTaskSubparserSubmit.add_argument(
    "-s", "--submit",
    dest="doSubmit",
    action="store_true", # Default: false
    help="Submit the jobs. By default only show submit script to stdout.")

def submitTask(args):
    if args.queue:
        args.wrapper.cfg['queue'] = args.queue
    if args.nJobs:
        args.wrapper.cfg['nJobs'] = args.nJobs
    jdl = args.wrapper.createJdl(parser_args=args)

    if args.doSubmit:
        with tempfile.NamedTemporaryFile(mode='w') as tmp:
            tmp.write(jdl)
            tmp.flush()
            print(jdl)
            call("condor_submit {0}".format(tmp.name), shell=True)
    else:
        print(jdl)

BatchTaskSubparserSubmit.set_defaults(func=submitTask)

BatchTaskSubparserRun = BatchTaskSubparsers.add_parser('run')
BatchTaskSubparserRun.add_argument(
    dest="jobId",
    type=int,
    help="JobId is used to specify which work_dir to go."
)

def runJob(args):
    args.wrapper.runWrappedProcess(process=args.process, jobId=args.jobId)
    pass

BatchTaskSubparserRun.set_defaults(func=runJob)

def copyAndRegSubparser(subparsers, origSubcmdName, copiedSubcmdName):
    subparsers.choices[copiedSubcmdName] = copy(subparsers.choices[origSubcmdName])
    return subparsers.choices[copiedSubcmdName]

