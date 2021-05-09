#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set sw=4 ts=4 fdm=indent fdl=2 ft=python et:

# Author          : Po-Hsun Chen (pohsun.chen.hep@gmail.com)
#                 : Pritam Kalbhor (physics.pritam@gmail.com)

from __future__ import print_function, division
import os
from math import sqrt

# Shared global settings
modulePath = os.path.abspath(os.path.dirname(__file__))

# q2 bins
q2bins = {}
def createBinTemplate(name, lowerBd, upperBd):
    template = {
        'q2range': (lowerBd, upperBd),
        'cutString': "Q2 > {0} && Q2 < {1}".format(lowerBd, upperBd),
        'label': "{0}".format(name),
        'latexLabel': "{lowerBd:.2f} < q^{{2}} < {upperBd:.2f}".format(upperBd=upperBd, lowerBd=lowerBd),
    }
    return template

q2bins['belowJpsiA']   = createBinTemplate("bin1A", 1.00, 2.00)
q2bins['belowJpsiB']   = createBinTemplate("bin1B", 2.00, 5.00)
q2bins['belowJpsiC']   = createBinTemplate("bin1C", 5.00, 8.00)
q2bins['jpsi']         = createBinTemplate("bin2", 8.00, 11.0)
q2bins['betweenPeaks'] = createBinTemplate("bin3", 11.0, 12.5)
q2bins['psi2s']        = createBinTemplate("bin4", 12.5, 15.0)
q2bins['abovePsi2sA']  = createBinTemplate("bin5A", 15.0, 17.0)
q2bins['abovePsi2sB']  = createBinTemplate("bin5B", 17.0, 19.0)
q2bins['abovePsi2s']   = createBinTemplate("bin5", 15., 19.)
q2bins['summaryLowQ2'] = createBinTemplate("summaryLowQ2", 1., 6.)
q2bins['summary']      = createBinTemplate("bin0", 1.00, 19.0)
q2bins['summaryA']     = createBinTemplate("bin0A", 1.00, 12.5)
q2bins['summaryA']['cutString'] = "({0}) && !({1})".format(q2bins['summaryA']['cutString'], q2bins['jpsi']['cutString'])
q2bins['Test1']        = createBinTemplate("binA", 1.00, 3.00)
q2bins['Test2']        = createBinTemplate("binB", 3.00, 5.00)
q2bins['summary']['cutString'] = "(Q2 > 1. && Q2 < 19.) && !(Q2 > 8. && Q2 < 11.) && !(Q2 > 12.5 && Q2 <15.)"

q2bins['peaks']        = createBinTemplate("peaks", 1., 19.)
q2bins['peaks']['cutString'] = "(Q2 > 8. && Q2 < 11.) || (Q2 > 12.5 && Q2 < 15.)"
q2bins['full'] = createBinTemplate("full", 1., 19.)

# SM prediction
q2bins['belowJpsiA']['sm'] = {
    'afb': {
        'getVal': -0.6,
        'getError': 0.097,
    },
    'fl': {
        'getVal': 0.453,
        'getError': 0.306,
    }
}
q2bins['belowJpsiB']['sm'] = {
    'afb': {
        'getVal': 0.037,
        'getError': 0.097,
    },
    'fl': {
        'getVal': 0.673,
        'getError': 0.306,
    }
}
q2bins['belowJpsiC']['sm'] = {
    'afb': {
        'getVal': 0.077,
        'getError': 0.097,
    },
    'fl': {
        'getVal': 0.83,
        'getError': 0.306,
    }
}
q2bins['abovePsi2sA']['sm'] = {
    'afb': {
        'getVal': -0.206,
        'getError': 0.030,
    },
    'fl': {
        'getVal': 0.206,
        'getError': 0.035,
    }
}
q2bins['abovePsi2sB']['sm'] = {
    'afb': {
        'getVal': -0.406,
        'getError': 0.030,
    },
    'fl': {
        'getVal': 0.246,
        'getError': 0.035,
    }
}

#q2bins['summary']['sm']     = q2bins['abovePsi2sB']['sm']
#q2bins['betweenPeaks']['sm'] = q2bins['abovePsi2sB']['sm']
#q2bins['summaryLowQ2']['sm'] = q2bins['abovePsi2sB']['sm']

# B mass regions
bMassRegions = {}
def createBmassTemplate(name, lowerBd, upperBd):
    template = {
        'range': (lowerBd, upperBd),
        'cutString': "Bmass > {0} && Bmass < {1}".format(lowerBd, upperBd),
        'label': "{0}".format(name),
    }
    return template

bMassRegions['Full'] = createBmassTemplate("Full", 4.7, 6.0) # Cut off below 4.68
bMassRegions['Fit']  = createBmassTemplate("Fit",  5.25, 5.65)
bMassRegions['SR']   = createBmassTemplate("SR",   5.25, 5.45) #Signal Region
bMassRegions['LSB']  = createBmassTemplate("LSB",  4.9, 5.25) #("LSB", 5.143, 5.223)
bMassRegions['USB']  = createBmassTemplate("USB",  5.65, 6.0) #("USB", 5.511, 5.591)
bMassRegions['SB']   = createBmassTemplate("SB",   4.9, 5.95)
bMassRegions['NSB']   = createBmassTemplate("NSB", 5.20, 5.65)
bMassRegions['SB']['cutString'] = "({0}) && !({1})".format(bMassRegions['SB']['cutString'], bMassRegions['NSB']['cutString'])

# systematics
bMassRegions['altFit'] = createBmassTemplate("altFit", 5.1, 5.60)
bMassRegions['altSR']  = createBmassTemplate("altSR", 5.25, 5.45)
bMassRegions['altLSB'] = createBmassTemplate("altLSB", 5.1, 5.25)
bMassRegions['altUSB'] = createBmassTemplate("altUSB", 5.45, 5.60)
bMassRegions['altSB']  = createBmassTemplate("altSB", 5.10, 5.60)
bMassRegions['altSB']['cutString'] = "({0}) && !({1})".format(bMassRegions['altSB']['cutString'], bMassRegions['altSR']['cutString'])

bMassRegions['altFit_vetoJpsiX'] = createBmassTemplate("altFit_vetoJpsiX", 5.18, 5.80)
bMassRegions['altSR_vetoJpsiX']  = createBmassTemplate("altSR_vetoJpsiX", 5.18, 5.38)
bMassRegions['altLSB_vetoJpsiX'] = createBmassTemplate("altLSB_vetoJpsiX", 5.18, 5.18)
bMassRegions['altUSB_vetoJpsiX'] = createBmassTemplate("altUSB_vetoJpsiX", 5.38, 5.80)
bMassRegions['altSB_vetoJpsiX']  = createBmassTemplate("altSB_vetoJpsiX", 4.76, 5.80)
bMassRegions['altSB_vetoJpsiX']['cutString'] = "({0}) && !({1})".format(bMassRegions['altSB_vetoJpsiX']['cutString'], bMassRegions['altSR_vetoJpsiX']['cutString'])

