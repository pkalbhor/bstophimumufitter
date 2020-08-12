
f_effiSigA_format = {}

pdfL = "1+l1*CosThetaL+l2*pow(CosThetaL,2)+l3*pow(CosThetaL,3)+l4*pow(CosThetaL,4)+l5*pow(CosThetaL,5)+l6*pow(CosThetaL,6)+l7*pow(CosThetaL,7)+l8*pow(CosThetaL,8)"; nLo=9
pdfK = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)"; nK=7
n=25 #Number of x. LP4*Pol4
xTerm = "\
(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)\
+(x20+x21*CosThetaK+x22*(1.5*pow(CosThetaK,2)-0.5)+x23*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x24*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,4)"

f_effiSigA_format['Poly8_Poly6_XTerm'] = ["l{0}[-10,10]".format(i) for i in range(1, nLo)] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL, args="{CosThetaL, " + ', '.join(["l{0}".format(i) for i in range(1, nLo)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK, " + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL,
        pdfK=pdfK,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLo)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(n)]) + "}")]

xTerm2 = "\
(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)"; n1A=20

pdfL1A = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2)) + l7*exp(-0.5*pow((CosThetaL-l8)/l9,2))"; nLc=9
pdfK1A = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)"; nK1A=7
f_effiSigA_format['Gaus3_Poly6_XTerm'] = ["l{0}[.1,0,10]".format(3*i-2) for i in range(1, nLc/3+1)] \
    + ["l{0}[0,-.5,.5]".format(3*i-1) for i in range(1, nLc/3+1)] \
    + ["l{0}[.2,.01,5.]".format(3*i) for i in range(1, nLc/3+1)] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK1A)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1A, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLc+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK1A, args="{CosThetaK,"+', '.join(["k{0}".format(i) for i in range(1, nK1A)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL1A,
        pdfK=pdfK1A,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLc+1)] + ["k{0}".format(i) for i in range(1, nK1A)] + ["x{0}".format(i) for i in range(n)]) + "}")]

pdfL1B = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2))+l4*exp(-0.5*pow((CosThetaL-l5)/l6,2)) + l7*exp(-0.5*pow((CosThetaL-l8)/l9,2))"; nLB=9
f_effiSigA_format['Gaus3_Poly6_XTerm_v2'] = ["l1[.1,0,10]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[0.2,0,10]", "l5[.2,-0.5,0.5]", "l6[.2,0.01,5.0]", "l7[0.1,0,10]", "l8[0,-.5,.5]", "l9[.2,.01,5.]"] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
    + ["effi_norm[1,0,1000]", "hasXTerm[0]"] + ["x{0}[-2,2]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1B, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL1B,
        pdfK=pdfK,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(n)]) + "}")]



######################################################################################################
f_analyticBkgCombA_format = {}

f_analyticBkgCombA_format['Poly4_Exp'] = [ # pdfL: Poly4, pdfK: exp()+exp()
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly4_Poly4'] = [ # pdfL: Poly4, pdfK: Poly4
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus3_Exp'] = [ #pdfL: Gaus+Gaus+Gaus, pdfK: exp()+expt()
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]", "bkgCombL_c8[0,10]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c8*exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['GausPoly_Exp'] = [ #pdfL: Gaus+Gaus+Poly2, pdfK: exp()+exp()
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.1,0.001,1.]", "bkgCombL_c3[-0.62,-1.,1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0,10]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]",  "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+1.+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus2_Poly4'] = [ # pdfL: Gauss+Gauss, pdfK: Poly4
    "bkgCombL_c1[-3,3]", "bkgCombL_c2[0.1, 0.01, 0.5]", "bkgCombL_c3[-3,3]", "bkgCombL_c4[0.1, 0.01, 1.0]", "bkgCombL_c5[0,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Lin_Poly3'] = [ # pdfL: Linear, pdfK: Poly3
    "bkgCombL_c1[-3,3]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL",
        pdfK="1.+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly2_Poly3'] = [ # pdfL: Poly2, pdfK: Poly3
    "bkgCombL_c1[-3,3]",   "bkgCombL_c2[-3,3]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL, 2)",
        pdfK="1.+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['QuadGaus_Exp'] = [ # pdfL: Quadratic+Gauss, pdfK: exp()+exp()
    "bkgCombL_c1[0.01,1]", "bkgCombL_c2[0.1,20]", "bkgCombL_c3[-1,1]", "bkgCombL_c4[0.05,1]",
    "bkgCombK_c1[-10,0]",  "bkgCombK_c2[0,20]",   "bkgCombK_c3[0,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})',{args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+bkgCombK_c2*exp(bkgCombK_c3*CosThetaK)",
        args="{CosThetaL,CosThetaK,bkgCombL_c1,bkgCombL_c2,bkgCombL_c3,bkgCombL_c4,bkgCombK_c1,bkgCombK_c2,bkgCombK_c3}")
]
f_analyticBkgCombA_format['New'] = [ # pdfL: Gauss, pdfK: exp()+exp()
    "bkgCombL_c2[0.1,20]", "bkgCombL_c3[-1,1]", "bkgCombL_c4[0.05,1]",
    "bkgCombK_c1[-10,0]",  "bkgCombK_c2[0,20]",   "bkgCombK_c3[0,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})',{args})".format(
        pdfL="bkgCombL_c2*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+bkgCombK_c2*exp(bkgCombK_c3*CosThetaK)",
        args="{CosThetaL,CosThetaK,bkgCombL_c2,bkgCombL_c3,bkgCombL_c4,bkgCombK_c1,bkgCombK_c2,bkgCombK_c3}")
]
