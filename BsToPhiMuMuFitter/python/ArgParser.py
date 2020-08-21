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
    parser.add_argument('--SimFit', help='Fitting over 3 year data (Default: False)', action='store_true')
    return parser

def add_help(parser):
    parser.add_argument('-h', '--help', action='help', default='==SUPPRESS==', help=('show this help message and exit'))

modulePath=os.path.abspath(os.path.dirname('seqCollection.py'))

