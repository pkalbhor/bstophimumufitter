import os
from argparse import ArgumentParser

def SetParser(add_help=True):
    parser = ArgumentParser(add_help=add_help, conflict_handler='resolve')
    parser.add_argument('-b', '--binKey', dest='binKey', type=str, default='bin1A', help="Select q2 bin with bin label")
    parser.add_argument('-s', '--seq', dest='seqKey', type=str, default='loadData', help="Sequence name to execute")
    parser.add_argument('-f', '--force', help='Mainly for forcefully overwriting dataset files (Default: False)', action='store_true')
    EffGroup=parser.add_mutually_exclusive_group()
    EffGroup.add_argument('--TwoStep', help='Use 2 Step efficiency (Default: False)', action='store_true')
    EffGroup.add_argument('--OneStep', help='Use 1 Step efficiency (Default: False)', action='store_true')
    parser.add_argument("--list", nargs="+", default=["effi"])
    parser.add_argument('-y', '--Year', dest='Year', type=int, default=2016, choices=[2016, 2017, 2018], help="Year of the dataset to process")
    parser.add_argument('--NoImport', help='Import variables from database (Default: False)', action='store_true')
    parser.add_argument('--NoFit', help='If mentioned, only plot distributions without fit (Default: False)', action='store_true')
    parser.add_argument('--NoPull', help='If mentioned, only plot distributions without pull(Default: False)', action='store_true')
    parser.add_argument('--AltRange', help='If mentioned, use alternate Bmass range(Default: False)', action='store_true')
    parser.add_argument('-f', '--force', help='Mainly for forcefully overwriting dataset files (Default: False)', action='store_true')
    Group=parser.add_mutually_exclusive_group()
    Group.add_argument('--SimFit', help='Fitting over 3 year data (Default: False)', action='store_true')
    Group.add_argument('--SimFitPlots', help='Plotting over 3 year data (Default: False)', action='store_true')
    Group.add_argument('--Toy2', help='Use 2nd option for doing toy study (Default: True)', action='store_false')
    parser.add_argument('--debug', action='store_true', help="Print logs to standard output (Default: False)")
    parser.add_argument('--isBatchTask', action='store_true', help="Submit as a batch task (Default: False)")
    parser.add_argument('--pp', dest='plotsPath', type=str, default='/eos/user/p/pkalbhor/www/public/PhimumuAnalysis', help="Provide path where output files will be stored")
    return parser

def GetBatchTaskParser():
    import v2Fitter.Batch.AbsBatchTaskWrapper as AbsBatchTaskWrapper
    parentParser=SetParser(False)
    parser = AbsBatchTaskWrapper.BatchTaskParser
    parser._add_container_actions(parentParser) # Connect with main parser
    parser.add_argument('-t', '--nToy', dest="nSetOfToys", type=int, default=5, help="Number of subsamples to produce"    )
 
    BatchTaskSubparserPostproc = AbsBatchTaskWrapper.BatchTaskSubparsers.add_parser('postproc')
    BatchTaskSubparserPostproc.add_argument('--forceHadd', dest='forceHadd', action='store_true', 
                                            help="Force recreate summary root file."
                                            )
    BatchTaskSubparserPostproc.add_argument(
        '--drawGEN',
        dest='drawGEN',
        action='store_false',
        help="Draw a line for GEN level value"
    )
    BatchTaskSubparserPostproc.add_argument(
        '--forall',
        dest='forall',
        action='store_true',
        help="Draw for all bins in one go"
    )
    BatchTaskSubparserPostproc.set_defaults(func=None) 
    TableParser = AbsBatchTaskWrapper.BatchTaskSubparsers.add_parser('MakeTables')
    TableParser.add_argument(
        "-tseq", "--TSeq",
        nargs="+", default=["effiFitter"],
        help="Sub sequences for making tables"
    )
    subparser_systematics = AbsBatchTaskWrapper.BatchTaskSubparsers.add_parser('systematics')
    subparser_systematics.set_defaults(func=None)
    subparser_systematics.add_argument(
        "-type",
        type=str,
        help="Specify type of systematics you want to derive"
        )
    subparser_systematics.add_argument(
        "--updatePlot",
        action='store_true',
        help='Update/Rewrite existing plots'
        )
    subparser_systematics.add_argument(
        "--updateDB",
        action='store_true',
        help='Update/Rewrite existing DB parameters'
        )
    parser.add_argument('-h', '--help', action='help', default='==SUPPRESS==', help=('show this help message and exit'))
    return parser
 
modulePath=os.path.abspath(os.path.dirname('seqCollection.py'))

