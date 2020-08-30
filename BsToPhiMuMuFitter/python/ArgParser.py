import os
from argparse import ArgumentParser

def SetParser(add_help=True):
    parser = ArgumentParser(add_help=add_help, conflict_handler='resolve')
    parser.add_argument('-b', '--binKey', dest='binKey', type=str, default='bin0', help="Select q2 bin with bin label")
    parser.add_argument('-s', '--seq', dest='seqKey', type=str, default='loadData', help="Sequence name to execute")
    parser.add_argument('--TwoStep', help='Use 2 Step efficiency (Default: False)', action='store_true')
    parser.add_argument("--list", nargs="+", default=["effi"])
    parser.add_argument('-y', '--Year', dest='Year', type=int, default=2016, choices=[2016, 2017, 2018], help="Year of the dataset to process")
    parser.add_argument('--NoImport', help='Import variables from database (Default: False)', action='store_true')
    Group=parser.add_mutually_exclusive_group()
    Group.add_argument('--SimFit', help='Fitting over 3 year data (Default: False)', action='store_true')
    Group.add_argument('--SimFitPlots', help='Plotting over 3 year data (Default: False)', action='store_true')
    return parser

def add_help(parser):
    parser.add_argument('-h', '--help', action='help', default='==SUPPRESS==', help=('show this help message and exit'))

def GetBatchTaskParser():
    import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper
    import BsToPhiMuMuFitter.script.batchTask_sigMCValidation as batchTask_sigMCValidation
    parentParser=SetParser(False)
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
    BatchTaskSubparserPostproc.set_defaults(func=batchTask_sigMCValidation.func_postproc, )
    add_help(parser)
    return parser
 
modulePath=os.path.abspath(os.path.dirname('seqCollection.py'))

