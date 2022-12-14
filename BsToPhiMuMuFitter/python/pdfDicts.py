
f_effiSigA_format = {}

pdfL = "1+l1*CosThetaL+l2*pow(CosThetaL,2)+l3*pow(CosThetaL,3)+l4*pow(CosThetaL,4)+l5*pow(CosThetaL,5)+l6*pow(CosThetaL,6)+l7*pow(CosThetaL,7)+l8*pow(CosThetaL,8)"; nLo=9
pdfK = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)"; nK=7
n=25 #Number of x. LP4*Pol4
xTerm = "(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)\
+(x20+x21*CosThetaK+x22*(1.5*pow(CosThetaK,2)-0.5)+x23*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x24*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,4)"

# LP4*Pol3
xTerm2 = "(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)"; n1A=20

# LP3*Pol3
xTerm3 = "(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))\
+(x4+x5*CosThetaK+x6*(1.5*pow(CosThetaK,2)-0.5)+x7*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*CosThetaL\
+(x8+x9*CosThetaK+x10*(1.5*pow(CosThetaK,2)-0.5)+x11*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*pow(CosThetaL,2)\
+(x12+x13*CosThetaK+x14*(1.5*pow(CosThetaK,2)-0.5)+x15*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*pow(CosThetaL,3)"; Nx3=16

# LP3*Pol4
xTerm4 = "(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))\
+(x4+x5*CosThetaK+x6*(1.5*pow(CosThetaK,2)-0.5)+x7*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*CosThetaL\
+(x8+x9*CosThetaK+x10*(1.5*pow(CosThetaK,2)-0.5)+x11*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*pow(CosThetaL,2)\
+(x12+x13*CosThetaK+x14*(1.5*pow(CosThetaK,2)-0.5)+x15*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*pow(CosThetaL,3)\
+(x16+x17*CosThetaK+x18*(1.5*pow(CosThetaK,2)-0.5)+x19*(2.5*pow(CosThetaK,3)-1.5*CosThetaK))*pow(CosThetaL,4)"; Nx4=20

# LP4*Pol5
xTerm5 = "(x0+x1*CosThetaK+x2*(1.5*pow(CosThetaK,2)-0.5)+x3*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x4*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))\
+(x5+x6*CosThetaK+x7*(1.5*pow(CosThetaK,2)-0.5)+x8*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x9*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*CosThetaL\
+(x10+x11*CosThetaK+x12*(1.5*pow(CosThetaK,2)-0.5)+x13*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x14*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,2)\
+(x15+x16*CosThetaK+x17*(1.5*pow(CosThetaK,2)-0.5)+x18*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x19*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,3)\
+(x20+x21*CosThetaK+x22*(1.5*pow(CosThetaK,2)-0.5)+x23*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x24*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,4)\
+(x25+x26*CosThetaK+x27*(1.5*pow(CosThetaK,2)-0.5)+x28*(2.5*pow(CosThetaK,3)-1.5*CosThetaK)+x29*(4.375*pow(CosThetaK, 4)-3.75*pow(CosThetaK, 2)+0.375))*pow(CosThetaL,4)"; Nx5=30

pdfL1A = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2)) + exp(-0.5*pow((CosThetaL-l4)/l5,2)) + exp(-0.5*pow((CosThetaL-l6)/l7,2))"; nLc=7
pdfK1A = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)"; nK1A=7
f_effiSigA_format['Gaus3_Poly6_XTerm_v11'] = ["l{0}[.1,0,10]".format(3*i-2) for i in range(1, nLc//3 + 1)] \
    + ["l{0}[0,-.5,.5]".format(3*i-1) for i in range(1, nLc//3+1)] \
    + ["l{0}[.2,.01,5.]".format(3*i) for i in range(1, nLc//3+1)] \
    + ["k{0}[-10,10]".format(i) for i in range(1, nK1A)] \
    + ["effi_norm[0.5,0,1]", "hasXTerm[0]"] + ["x{0}[-20,20]".format(i) for i in range(n)] \
    + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1A, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLc+1)]) + "}")] \
    + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK1A, args="{CosThetaK,"+', '.join(["k{0}".format(i) for i in range(1, nK1A)]) + "}")] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=xTerm, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}".format(i) for i in range(n)]) + "}")] \
    + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
        pdfL=pdfL1A,
        pdfK=pdfK1A,
        xTerm=xTerm,
        args="{CosThetaL,CosThetaK,hasXTerm,effi_norm," + ','.join(["l{0}".format(i) for i in range(1, nLc+1)] + ["k{0}".format(i) for i in range(1, nK1A)] + ["x{0}".format(i) for i in range(n)]) + "}")]

pdfL1B = "l1*exp(-0.5*pow((CosThetaL-l2)/l3,2)) + exp(-0.5*pow((CosThetaL-l4)/l5,2)) + exp(-0.5*pow((CosThetaL-l6)/l7,2))"; nLB=7

for ver, numb, term in [('', n, xTerm), ('2', n1A, xTerm2), ('3', Nx3, xTerm3), ('4', Nx4, xTerm4), ('5', Nx5, xTerm5)]:
    f_effiSigA_format['Poly6_Poly6_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Gaus3_Poly6_XTerm_{}'.format(ver)] = ["l1[.1,0,1.]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[.2,-1.,1.]", "l5[.2,0.01,5.0]", "l6[0,-1.,1.]", "l7[.2,.001,5.]", "l8[.1,0,1.]", "l9[.3, 0, 1]"] \
        + ["k{0}[-10,10]".format(i) for i in range(1, 7)] \
        + ["RooGaussian::G1(CosThetaL, l2, l3)", "RooGaussian::G2(CosThetaL, l4, l5)", "RooGaussian::G3(CosThetaL, l6, l7)"] \
        + ["sum::G12(l1*G1, l8*G2)"] + ["sum::effi_cosl(G12, G3)"]\
        + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6})"] + ["hasXTerm[0]"] \
        + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
        + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    pdfK7 = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)+k6*pow(CosThetaK,6)+k7*pow(CosThetaK,7)"
    f_effiSigA_format['Gaus3_Poly7_XTerm{}'.format(ver)] = ["l1[.1,0,10]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[.2,0.,1.]", "l5[.2,0.001,5.0]", "l6[-.3,-.5,.5]", "l7[.2,.001,5.]"] + ["k{0}[-10,10]".format(i) for i in range(1, 8)] \
        + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1B, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
        + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK7, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, 8)]) + "}")] \
        + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm[0]," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
        + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
            pdfL=pdfL1B,
            pdfK=pdfK7,
            xTerm=term,
            args="{CosThetaL,CosThetaK,hasXTerm,effi_norm[.5,0,1]," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, 8)] + ["x{0}".format(i) for i in range(numb)]) + "}")]

    f_effiSigA_format['Gaus3_Poly6_XTerm{}'.format(ver)] = ["l1[.1,0,10]", "l2[0,-0.02,0.02]", "l3[0.9,.0001,5.]", "l4[.2,0, .9.]", "l5[.2,0.0001,5.0]", "l6[-.2,-1.,0.]", "l7[.2,.001,5.]"] + ["k{0}[-10,10]".format(i) for i in range(1, nK)] \
        + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1B, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
        + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, nK)]) + "}")] \
        + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm[0]," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
        + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
            pdfL=pdfL1B,
            pdfK=pdfK,
            xTerm=term,
            args="{CosThetaL,CosThetaK,hasXTerm,effi_norm[.5,0,1]," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, nK)] + ["x{0}".format(i) for i in range(numb)]) + "}")]

    pdfK5 = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)+k5*pow(CosThetaK,5)"
    f_effiSigA_format['Gaus3_Poly5_XTerm{}'.format(ver)] = ["l1[.1,0,10]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[.2,-1.0,1.0]", "l5[.2,0.001,5.0]", "l6[0,-1.,1.]", "l7[.2,.001,5.]"] + ["k{0}[-10,10]".format(i) for i in range(1, 6)] \
        + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1B, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
        + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK5, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, 6)]) + "}")] \
        + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm[0]," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
        + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
            pdfL=pdfL1B,
            pdfK=pdfK5,
            xTerm=term,
            args="{CosThetaL,CosThetaK,hasXTerm,effi_norm[.5,0,1]," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, 6)] + ["x{0}".format(i) for i in range(numb)]) + "}")]

    pdfK4 = "1+k1*CosThetaK+k2*pow(CosThetaK,2)+k3*pow(CosThetaK,3)+k4*pow(CosThetaK,4)"
    f_effiSigA_format['Gaus3_Poly4_XTerm{}'.format(ver)] = ["l1[.1,0,10]", "l2[0,-0.5,0.5]", "l3[0.2,.01,5.]", "l4[.2,-1.0,1.0]", "l5[.2,0.001,5.0]", "l6[0,-1.,1.]", "l7[.2,.001,5.]"] + ["k{0}[-10,10]".format(i) for i in range(1, 5)] \
        + ["EXPR::effi_cosl('{pdf}',{args})".format(pdf=pdfL1B, args="{CosThetaL,"+', '.join(["l{0}".format(i) for i in range(1, nLB+1)]) + "}")] \
        + ["EXPR::effi_cosK('{pdf}',{args})".format(pdf=pdfK4, args="{CosThetaK," + ', '.join(["k{0}".format(i) for i in range(1, 5)]) + "}")] \
        + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm[0]," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
        + ["expr::effi_sigA('effi_norm*({pdfL})*({pdfK})*(1+hasXTerm*({xTerm}))', {args})".format(
            pdfL=pdfL1B,
            pdfK=pdfK4,
            xTerm=term,
            args="{CosThetaL,CosThetaK,hasXTerm,effi_norm[.5,0,1]," + ','.join(["l{0}".format(i) for i in range(1, nLB+1)] + ["k{0}".format(i) for i in range(1, 5)] + ["x{0}".format(i) for i in range(numb)]) + "}")]

    f_effiSigA_format['Gaus3_Poly8_XTerm{}'.format(ver)] = ["l1[.1,0,10]", "l2[0,-1.5,1.5]", "l3[0.2,.01,5.]", "l4[.2,-2.5,2.5]", "l5[.2,0.01,5.0]", "l6[0,-1.5,1.5]", "l7[.2,.001,5.]", "l8[.1,0,10]"] \
        + ["k{0}[-20,20]".format(i) for i in range(1, 9)] \
        + ["RooGaussian::G1(CosThetaL, l2, l3)", "RooGaussian::G2(CosThetaL, l4, l5)", "RooGaussian::G3(CosThetaL, l6, l7)"] \
        + ["RSUM::effi_cosl(l1*G1, l8*G2, G3)"]\
        + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6, k7, k8})"] + ["hasXTerm[0]"] \
        + ["EXPR::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
        + ["PROD::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    #Polynomials
    f_effiSigA_format['Poly9_Poly8_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 10)]\
                    + ["k{}[-10,10]".format(i) for i in range(1, 9)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8, l9})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6, k7, k8})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly7_Poly4_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 8)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 5)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly7_Poly5_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 8)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 6)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly7_Poly6_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 8)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly7_Poly7_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 8)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 8)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6, k7})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly8_Poly8_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 9)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 9)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6, k7, k8})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly8_Poly4_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 9)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly8_Poly6_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 9)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly8_Poly7_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 9)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 8)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6, k7})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly9_Poly4_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 10)]\
                    + ["k{}[-10,10]".format(i) for i in range(1, 5)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8, l9})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly9_Poly5_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 10)]\
                    + ["k{}[-10,10]".format(i) for i in range(1, 6)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8, l9})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly9_Poly6_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 10)]\
                    + ["k{}[-10,10]".format(i) for i in range(1, 7)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8, l9})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly9_Poly7_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 10)]\
                    + ["k{}[-10,10]".format(i) for i in range(1, 8)]\
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6, l7, l8, l9})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6, k7})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Cheb6_Cheb6_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["RooChebychev::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6})"] \
                    + ["RooChebychev::effi_cosK(CosThetaK, {k1, k2, k3, k4, k5, k6})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly6_Poly4_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 7)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 5)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5, l6})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly5_Poly4_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 6)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 5)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4, l5})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

    f_effiSigA_format['Poly4_Poly4_XTerm{}'.format(ver)] = ["l{}[-10,10]".format(i) for i in range(1, 5)] \
                    + ["k{}[-10,10]".format(i) for i in range(1, 5)] \
                    + ["RooPolynomial::effi_cosl(CosThetaL, {l1, l2, l3, l4})"] \
                    + ["RooPolynomial::effi_cosK(CosThetaK, {k1, k2, k3, k4})"] + ["hasXTerm[0]"] \
    + ["expr::effi_xTerm('1+hasXTerm*({xTerm})',{args})".format(xTerm=term, args="{CosThetaL,CosThetaK,hasXTerm," + ','.join(["x{0}[-30,30]".format(i) for i in range(numb)]) + "}")] \
                    + ["prod::effi_sigA(effi_norm[0.5,0,1], effi_cosl, effi_cosK, effi_xTerm)"]

# Conditional PDFs
for m, n in ((a, b) for a in range(1, 10) for b in range(1, 10)):
        f_effiSigA_format['GausXY{}_Cbv{}'.format(m, n)] = \
            ["RooPolyVar::FofK(CosThetaK, {} )".format("{"+", ".join(['k{}[-10,10]'.format(i) for i in range(1,m+1)])+"}")] \
            + ["RooGaussian::effi_cosl(CosThetaL, FofK, l1[0.3, 0.001, 5] )"] \
            + ["RooChebychev::effi_cosK(CosThetaK, {} )".format("{"+", ".join(['k{}[-10,10]'.format(i) for i in range(m+1,m+n+1)])+"}")] \
            + ["PROD::effi_sigA(effi_cosl|CosThetaK, effi_cosK)"]

######################################################################################################
# Analytical Functions for Combinatorial Background Shapes of Angular Variables

f_analyticBkgCombA_format = {}
f_analyticBkgCombA_format['Poly2_Poly2'] = [ # pdfL: Poly2, pdfK: Poly2
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombK_c1, bkgCombK_c2}")
]
f_analyticBkgCombA_format['Poly3_Poly3'] = [ # pdfL: Poly3, pdfK: Poly3
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly3_Poly5'] = [ # pdfL: Poly3, pdfK: Poly5
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5}")
]
f_analyticBkgCombA_format['Poly4_Poly4'] = [ # pdfL: Poly4, pdfK: Poly4
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Poly5_Poly5'] = [ # pdfL: Poly5, pdfK: Poly5
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5}")
]
f_analyticBkgCombA_format['Poly6_Poly6'] = [ # pdfL: Poly6, pdfK: Poly6
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]", "bkgCombL_c6[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-14,14]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)+bkgCombL_c6*pow(CosThetaL,6)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
]
f_analyticBkgCombA_format['Poly7_Poly7'] = [ # pdfL: Poly7, pdfK: Poly7
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]", "bkgCombL_c6[-10.,10.]", "bkgCombL_c7[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]", "bkgCombK_c7[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)+bkgCombL_c6*pow(CosThetaL,6)+bkgCombL_c7*pow(CosThetaL,7)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)+bkgCombK_c7*pow(CosThetaK,7)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6, bkgCombK_c7}")
]
f_analyticBkgCombA_format['Poly8_Poly8'] = [ # pdfL: Poly8, pdfK: Poly8
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]", "bkgCombL_c6[-10.,10.]", "bkgCombL_c7[-10.,10.]", "bkgCombL_c8[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]", "bkgCombK_c7[-10,10]", "bkgCombK_c8[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)+bkgCombL_c6*pow(CosThetaL,6)+bkgCombL_c7*pow(CosThetaL,7)+bkgCombL_c8*pow(CosThetaL,8)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)+bkgCombK_c7*pow(CosThetaK,7)+bkgCombK_c8*pow(CosThetaK,8)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6, bkgCombK_c7, bkgCombK_c8}")
]
f_analyticBkgCombA_format['Poly6_Poly5'] = [ # pdfL: Poly6, pdfK: Poly5
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]", "bkgCombL_c6[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)+bkgCombL_c6*pow(CosThetaL,6)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5}")
]
f_analyticBkgCombA_format['Poly6_Poly4'] = [ # pdfL: Poly6, pdfK: Poly4
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-20.,20.]", "bkgCombL_c5[-10.,10.]", "bkgCombL_c6[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)+bkgCombL_c6*pow(CosThetaL,6)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Poly6_Poly3'] = [ # pdfL: Poly6, pdfK: Poly3
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]", "bkgCombL_c6[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL,5)+bkgCombL_c6*pow(CosThetaL,6)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly4_Poly3'] = [ # pdfL: Poly4, pdfK: Poly3
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly5_Poly3'] = [ # pdfL: Poly5, pdfK: Poly3
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]", "bkgCombL_c5[-10.,10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)+bkgCombL_c5*pow(CosThetaL, 5)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Poly4_Exp'] = [ # pdfL: Poly4, pdfK: exp()+exp()
    "bkgCombL_c1[-10.,10.]", "bkgCombL_c2[-10.,10.]", "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10.,10.]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="1.+bkgCombL_c1*CosThetaL+bkgCombL_c2*pow(CosThetaL,2)+bkgCombL_c3*pow(CosThetaL, 3)+bkgCombL_c4*pow(CosThetaL,4)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus3Poly2_Poly6'] = [ #pdfL: Gaus+Gaus+Gaus+Poly4, pdfK: Poly6
    "bkgCombL_c0[1,0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[1, 0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombL_c8[-10,10]", "bkgCombL_c9[-10,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))+bkgCombL_c8*CosThetaL+bkgCombL_c9*pow(CosThetaL, 2)",
        pdfK="bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
]
f_analyticBkgCombA_format['Gaus3Poly2_Poly6_v2'] = [ #pdfL: Gaus+Gaus+Gaus+Poly2, pdfK: Poly6
    "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0.0,-1., 1.]", "bkgCombL_c6[0.4, 0.001, 1.0]",
    "bkgCombL_c7[-10,10]", "bkgCombL_c8[-10,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]",
    "bkgCombL_c9[1,0,10]", "bkgCombL_c10[1,0,10]", "bkgCombL_c11[1,0,10]",
    "RooGaussian::BkgAG1(CosThetaL, bkgCombL_c1, bkgCombL_c2)", "RooGaussian::BkgAG2(CosThetaL, bkgCombL_c3, bkgCombL_c4)", "RooGaussian::BkgAG3(CosThetaL, bkgCombL_c5, bkgCombL_c6)", 
    "RooPolynomial::BkgAPolyL(CosThetaL, {bkgCombL_c7, bkgCombL_c8})",
    "RooPolynomial::BkgAPolyK(CosThetaK, {bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6})",
    "SUM::BkgApdfL(bkgCombL_c9*BkgAG1, bkgCombL_c10*BkgAG2, bkgCombL_c11*BkgAG3, BkgAPolyL)",
    "PROD::f_bkgCombA(BkgApdfL, BkgAPolyK)"
]
f_analyticBkgCombA_format['Gaus3Poly4_Poly4'] = [ #pdfL: Gaus+Gaus+Gaus+Poly4, pdfK: Poly4
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombL_c8[-10,10]", "bkgCombL_c9[-10,10]", "bkgCombL_c10[-10,10]", "bkgCombL_c11[-10,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))+1.+bkgCombL_c8*CosThetaL+bkgCombL_c9*pow(CosThetaL, 2)+bkgCombL_c10*pow(CosThetaL,3)+bkgCombL_c11*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombL_c11, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus3Poly4_Poly6'] = [ #pdfL: Gaus+Gaus+Gaus+Poly4, pdfK: Poly6
    "bkgCombL_c0[1, 0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[1, 0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombL_c8[-10,10]", "bkgCombL_c9[-10,10]", "bkgCombL_c10[-10,10]", "bkgCombL_c11[-10,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]",  "bkgCombK_c3[-10,10]", "bkgCombK_c4[-20,20]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-20,20]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))+1.+bkgCombL_c8*CosThetaL+bkgCombL_c9*pow(CosThetaL, 2)+bkgCombL_c10*pow(CosThetaL,3)+bkgCombL_c11*pow(CosThetaL,4)",
        pdfK="1.+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombL_c11, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
]
f_analyticBkgCombA_format['Gaus3Poly4_Exp'] = [ #pdfL: Gaus+Gaus+Gaus+Poly4, pdfK: exp()+expt()
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombL_c8[-10,10]", "bkgCombL_c9[-10,10]", "bkgCombL_c10[-10,10]", "bkgCombL_c11[-10,10]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))+1.+bkgCombL_c8*CosThetaL+bkgCombL_c9*pow(CosThetaL, 2)+bkgCombL_c10*pow(CosThetaL,3)+bkgCombL_c11*pow(CosThetaL,4)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombL_c11, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus3_Poly4'] = [ #pdfL: Gaus+Gaus+Gaus, pdfK: Poly4
    "bkgCombL_c0[1,0,10]", "bkgCombL_c1[0.6, -1., 1.]", "bkgCombL_c2[0.15, 0.001, 1.0]", "bkgCombL_c3[-0.6,-1., 1.]",
    "bkgCombL_c4[0.4, 0.001, 1.0]", "bkgCombL_c5[1,0,10]", "bkgCombL_c6[-0.2,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus3_Poly6'] = [ #pdfL: Gaus+Gaus+Gaus, pdfK: Poly6
    "bkgCombL_c0[1,0,10]", "bkgCombL_c1[0.6, -1., 1.]", "bkgCombL_c2[0.15, 0.001, 1.0]", "bkgCombL_c3[-0.6,-1., 1.]",
    "bkgCombL_c4[0.4, 0.001, 1.0]", "bkgCombL_c5[1,0,10]", "bkgCombL_c6[-0.2,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
]
f_analyticBkgCombA_format['Gaus3_Exp'] = [ #pdfL: Gaus+Gaus+Gaus, pdfK: exp()+expt()
    "bkgCombL_c0[1,0,10]", "bkgCombL_c1[0.65, -1., 1.]", "bkgCombL_c2[0.1, 0.001, 1.0]", "bkgCombL_c3[-0.62,-1., 1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[1,0,10]", "bkgCombL_c6[0.0,-1., 1.]", "bkgCombL_c7[0.4, 0.001, 1.0]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c6)/bkgCombL_c7,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus2Poly2_Exp'] = [ #pdfL: Gaus+Gaus+Poly2, pdfK: exp()+exp()
    "bkgCombL_c0[1,0,10]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.1,0.001,1.]", "bkgCombL_c3[-0.62,-1.,1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[1,0,10]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]", "bkgCombL_c8[-10., 10.]",
    "bkgCombK_c1[-5,10]", "bkgCombK_c2[-10,10]",  "bkgCombK_c3[-3,5]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c8+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)",
        pdfK="exp(bkgCombK_c1*CosThetaK)+exp(bkgCombK_c3*CosThetaK+bkgCombK_c2)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus2Poly2_Poly4'] = [ #pdfL: Gaus+Gaus+Poly2, pdfK: Poly4
    "bkgCombL_c0[1,0,10]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.1,0.001,1.]", "bkgCombL_c3[-0.62,-1.,1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]", "bkgCombL_c8[-10., 10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]",  "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c8+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK, 4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus2Poly2_Poly6'] = [ #pdfL: Gaus+Gaus+Poly2, pdfK: Poly6
    "bkgCombL_c0[1,0,50]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.05,0.001,1.]", "bkgCombL_c3[-0.62,-1.,1.]",
    "bkgCombL_c4[0.01, 0.001, 1.0]", "bkgCombL_c6[-30., 30.]", "bkgCombL_c7[-30.,30.]", "bkgCombL_c8[-30., 30.]",
    "bkgCombK_c1[-30,30]", "bkgCombK_c2[-30,30]",  "bkgCombK_c3[-30,30]", "bkgCombK_c4[-30,30]", "bkgCombK_c5[-30,30]", "bkgCombK_c6[-30,30]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c8+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
]
f_analyticBkgCombA_format['Gaus2Poly6_Poly4'] = [ #pdfL: Gaus+Gaus+Poly6, pdfK: Poly4
    "bkgCombL_c0[0.5,0,25]", "bkgCombL_c1[-0.7,-1.,1.]", "bkgCombL_c2[0.05,0.001,1.]", "bkgCombL_c3[0.7,-1.,1.]",
    "bkgCombL_c4[0.05, 0.001, 1.0]", "bkgCombL_c5[-10., 10.]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]", "bkgCombL_c8[-10., 10.]", "bkgCombL_c9[-10., 10.]", "bkgCombL_c10[-10., 10.]", "bkgCombL_c11[-10., 10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c5+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)+bkgCombL_c8*pow(CosThetaL, 3)+bkgCombL_c9*pow(CosThetaL,4)+bkgCombL_c10*pow(CosThetaL,5)+bkgCombL_c11*pow(CosThetaL,6)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK, 4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombL_c11, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus2Poly5_Poly4'] = [ #pdfL: Gaus+Gaus+Poly5, pdfK: Poly4
    "bkgCombL_c0[0,25]", "bkgCombL_c1[-0.7,-1.,1.]", "bkgCombL_c2[0.05,0.001,1.]", "bkgCombL_c3[0.7,-1.,1.]",
    "bkgCombL_c4[0.05, 0.001, 1.0]", "bkgCombL_c5[-10., 10.]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]", "bkgCombL_c8[-10., 10.]", "bkgCombL_c9[-10., 10.]", "bkgCombL_c10[-10., 100.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c5+bkgCombL_c6*CosThetaL+bkgCombL_c7*pow(CosThetaL, 2)+bkgCombL_c8*pow(CosThetaL, 3)+bkgCombL_c9*pow(CosThetaL,4)+bkgCombL_c10*pow(CosThetaL,5)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK, 4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus2Poly4_Poly6'] = [ #pdfL: Gaus+Gaus+Poly4, pdfK: Poly6
    "bkgCombL_c0[.5,0,10]", "bkgCombL_c1[0.7,-1.,1.]", "bkgCombL_c2[0.05,0.001,2.]", "bkgCombL_c3[-0.7,-1.,1.]",
    "bkgCombL_c4[0.05, 0.001, 5.0]", "bkgCombL_c6[-20., 20.]", "bkgCombL_c7[-20., 20.]", "bkgCombL_c8[-20., 20.]", "bkgCombL_c9[-20., 20.]", "bkgCombL_c10[-40., 40.]",
    "bkgCombK_c1[-20,20]", "bkgCombK_c2[-20,20]", "bkgCombK_c3[-20,20]", "bkgCombK_c4[-20,20]", "bkgCombK_c5[-20,20]", "bkgCombK_c6[-20,20]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c6+bkgCombL_c7*CosThetaL+bkgCombL_c8*pow(CosThetaL, 2)+bkgCombL_c9*pow(CosThetaL, 3)+bkgCombL_c10*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
]
f_analyticBkgCombA_format['Gaus2Poly4_Poly4'] = [ #pdfL: Gaus+Gaus+Poly4, pdfK: Poly4
    "bkgCombL_c0[0,25]", "bkgCombL_c1[-0.7,-1.,1.]", "bkgCombL_c2[0.05,0.001,1.]", "bkgCombL_c3[0.7,-1.,1.]",
    "bkgCombL_c4[0.05, 0.001, 1.0]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]", "bkgCombL_c8[-10., 10.]", "bkgCombL_c9[-10., 10.]", "bkgCombL_c10[-10., 10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c6+bkgCombL_c7*CosThetaL+bkgCombL_c8*pow(CosThetaL, 2)+bkgCombL_c9*pow(CosThetaL, 3)+bkgCombL_c10*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK, 4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus2Poly4_Poly3'] = [ #pdfL: Gaus+Gaus+Poly4, pdfK: Poly3
    "bkgCombL_c0[1, 0,10]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.1,0.001,1.]", "bkgCombL_c3[-0.62,-1.,1.]",
    "bkgCombL_c4[0.1, 0.001, 1.0]", "bkgCombL_c5[1, 0,10]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]", "bkgCombL_c8[-10., 10.]", "bkgCombL_c9[-10., 10.]", "bkgCombL_c10[-10., 10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]",  "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))+bkgCombL_c6+bkgCombL_c7*CosThetaL+bkgCombL_c8*pow(CosThetaL, 2)+bkgCombL_c9*pow(CosThetaL, 3)+bkgCombL_c10*pow(CosThetaL,4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombL_c8, bkgCombL_c9, bkgCombL_c10, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['GausPoly4_Poly3'] = [ #pdfL: Gaus1+Poly4, pdfK: Poly3
    "bkgCombL_c0[0,10]", "bkgCombL_c1[0.65,-1,1]", "bkgCombL_c2[0.1,0.001,1.]", 
    "bkgCombL_c3[-10.,10.]", "bkgCombL_c4[-10,10]", "bkgCombL_c5[-10,10]", "bkgCombL_c6[-10., 10.]", "bkgCombL_c7[-10., 10.]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="bkgCombL_c0*exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c7+bkgCombL_c3*CosThetaL+bkgCombL_c4*pow(CosThetaL, 2)+bkgCombL_c5*pow(CosThetaL, 3)+bkgCombL_c6*pow(CosThetaL, 4)",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)",
        args="{CosThetaL, CosThetaK, bkgCombL_c0, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6, bkgCombL_c7, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3}")
]
f_analyticBkgCombA_format['Gaus2_Poly4'] = [ # pdfL: Gauss+Gauss, pdfK: Poly4
    "bkgCombL_c1[1,-3,3]", "bkgCombL_c2[0.7, 0.01, 0.5]", "bkgCombL_c3[-0.48,-1,1]", "bkgCombL_c4[0.15, 0.01, 1.0]", "bkgCombL_c5[1,0,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4}")
]
f_analyticBkgCombA_format['Gaus2_Poly6'] = [ # pdfL: Gauss+Gauss, pdfK: Poly6
    "bkgCombL_c1[1,-3,3]", "bkgCombL_c2[0.2, 0.01, 0.5]", "bkgCombL_c3[-0.48,-1,1]", "bkgCombL_c4[0.15, 0.01, 1.0]", "bkgCombL_c5[1,0,10]",
    "bkgCombK_c1[-10,10]", "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]", "bkgCombK_c6[-10,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})', {args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="1+bkgCombK_c1*CosThetaK+bkgCombK_c2*pow(CosThetaK,2)+bkgCombK_c3*pow(CosThetaK, 3)+bkgCombK_c4*pow(CosThetaK,4)+bkgCombK_c5*pow(CosThetaK,5)+bkgCombK_c6*pow(CosThetaK,6)",
        args="{CosThetaL, CosThetaK, bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5, bkgCombK_c6}")
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
    "bkgCombL_c1[0.01,1]", "bkgCombL_c2[0.1,20]", "bkgCombL_c3[-1,1]", "bkgCombL_c4[0.05,1]", "bkgCombL_c5[0.,10]",
    "bkgCombK_c1[-10,0]",  "bkgCombK_c2[0,20]",   "bkgCombK_c3[0,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})',{args})".format(
        pdfL="exp(-0.5*pow((CosThetaL-bkgCombL_c1)/bkgCombL_c2,2))+bkgCombL_c5*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+bkgCombK_c2*exp(bkgCombK_c3*CosThetaK)",
        args="{CosThetaL,CosThetaK,bkgCombL_c1,bkgCombL_c2,bkgCombL_c3,bkgCombL_c4, bkgCombL_c5, bkgCombK_c1,bkgCombK_c2,bkgCombK_c3}")
]
f_analyticBkgCombA_format['New'] = [ # pdfL: Gauss, pdfK: exp()+exp()
    "bkgCombL_c2[0.1,20]", "bkgCombL_c3[-1,1]", "bkgCombL_c4[0.05,1]",
    "bkgCombK_c1[-10,0]",  "bkgCombK_c2[0,20]",   "bkgCombK_c3[0,10]",
    "EXPR::f_bkgCombA('({pdfL})*({pdfK})',{args})".format(
        pdfL="bkgCombL_c2*exp(-0.5*pow((CosThetaL-bkgCombL_c3)/bkgCombL_c4,2))",
        pdfK="exp(bkgCombK_c1*CosThetaK)+bkgCombK_c2*exp(bkgCombK_c3*CosThetaK)",
        args="{CosThetaL,CosThetaK,bkgCombL_c2,bkgCombL_c3,bkgCombL_c4,bkgCombK_c1,bkgCombK_c2,bkgCombK_c3}")
]

for i, j in ((a, b) for a in range(1, 10) for b in range(1, 10)):
    f_analyticBkgCombA_format['Cbv{}_Cbv{}'.format(i, j)] = [ # 
        "RooChebychev::fL(CosThetaL, {} )".format("{"+", ".join(['bkgCombL_c{}[-10,10]'.format(i) for i in range(1,i+1)])+"}"),
        "RooChebychev::fK(CosThetaK, {} )".format("{"+", ".join(['bkgCombK_c{}[-10,10]'.format(i) for i in range(1,j+1)])+"}"),
        "PROD::f_bkgCombA(fL, fK)"
    ]
f_analyticBkgCombA_format['RooCbv62_Cbv5'] = [ # 
    "bkgCombL_c1[-10,10]", "bkgCombL_c2[-10,10]", "bkgCombL_c3[-10,10]", "bkgCombL_c4[-10,10]", "bkgCombL_c5[-10,10]", "bkgCombL_c6[-10,10]", 
    "bkgCombL_c7[-10,10]", "bkgCombL_c8[-10,10]", "bkgCombL_c9[-10,10]",
    "bkgCombL_c10[-10,10]", "bkgCombL_c11[-10,10]", "bkgCombL_c12[-10,10]", "bkgCombL_c13[-10,10]", "bkgCombL_c14[-10,10]", "bkgCombL_c15[-10,10]", 
    "bkgCombK_c1[-10,10]",  "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "RooChebychev::fL1(CosThetaL, {bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5, bkgCombL_c6} )",
    "RooChebychev::fL2(CosThetaL, {bkgCombL_c7, bkgCombL_c8} )",
    "RooChebychev::fL3(CosThetaL, {bkgCombL_c10, bkgCombL_c11, bkgCombL_c12, bkgCombL_c13, bkgCombL_c14, bkgCombL_c15} )",
    "SUM::fL(bkgCombL_c9*fL1, fL2)",
    "RooChebychev::fK(CosThetaK, {bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5} )",
    "PROD::f_bkgCombA(fL1, fL3, fK)"
]
f_analyticBkgCombA_format['RooLeg23_Cbv5'] = [ #
    "bkgCombL_c1[-10,10]", "bkgCombL_c2[-10,10]",
    "bkgCombK_c1[-10,10]",  "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "RooLegendre::fL1(CosThetaL, 2, 0)",
    "RooLegendre::fL2(CosThetaL, 3, 0)",
    "RooRealSumPdf::fL({0.5, fL1, fL2}, {1, bkgCombL_c1, bkgCombL_c2}, 1)",
    "RooChebychev::fK(CosThetaK, {bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5} )",
    "PROD::f_bkgCombA(fL, fK)"
]
f_analyticBkgCombA_format['Leg67G2_Cbv5'] = [ #
    "bkgCombL_c1[-10,10]", "bkgCombL_c2[-10,10]", "bkgCombL_c3[-10,10]", "bkgCombL_c4[-10,10]",
    "bkgCombK_c1[-10,10]",  "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "RooLegendre::fL1(CosThetaL, 6, 1)",
    "RooLegendre::fL2(CosThetaL, 0, 0)",
    "RooGaussian::fL3(CosThetaL, bkgCombL_c5[0.7, 0.6, 0.9], bkgCombL_c6[0.08, 0, 5])",
    "RooGaussian::fL4(CosThetaL, bkgCombL_c7[-0.75, -0.9, -0.6], bkgCombL_c8[0.1, 0, 5])",
    "RooRealSumPdf::fL5({0.5, fL1, fL2}, {1, bkgCombL_c1, bkgCombL_c2}, 1)",
    "SUM::fL(bkgCombL_c3*fL3, bkgCombL_c4*fL4, fL5)",
    "RooChebychev::fK(CosThetaK, {bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5} )",
    "PROD::f_bkgCombA(fL, fK)"
]

for i, j, k, l, m in ((a,b,c,d,e) for a in range(10) for b in range(10) for c in range(a+1) for d in range(b+1) for e in range(8)):
    f_analyticBkgCombA_format['Leg{}{}G2_Cbv{}_v{}{}'.format(i,j,m,k,l)] = [ #
        "RooLegendre::fL1(CosThetaL, {}, {})".format(i, k),
        "RooLegendre::fL2(CosThetaL, {}, {})".format(j, l),
        "RooRealSumPdf::fL3({0.5, fL1, fL2}, {1, bkgCombL_c1[-10,10], bkgCombL_c2[-10,10]}, 1)",
        "RooGaussian::fL4(CosThetaL, bkgCombL_c3[0.78, 0.5, 0.9], bkgCombL_c5[0.08, 0, 5])",
        "RooGaussian::fL5(CosThetaL, bkgCombL_c4[-0.75, -0.9, -0.6], bkgCombL_c6[0.1, 0, 5])",
        "SUM::fL(bkgCombL_c7[0.2,0,1]*fL3, bkgCombL_c8[0.5,0,1]*fL4, fL5)",
        "RooChebychev::fK(CosThetaK, {} )".format("{"+", ".join(['bkgCombK_c{}[-10,10]'.format(i) for i in range(1,m+1)])+"}"),
        "PROD::f_bkgCombA(fL, fK)"
    ]
for i in range(10):
    for j in range(10):
        for k in range(i+1):
            for l in range(j+1):
                f_analyticBkgCombA_format['Leg{}{}_Cbv5_v{}{}'.format(i,j,k,l)] = [ #
                    "bkgCombL_c1[-10,10]", "bkgCombL_c2[-10,10]",
                    "bkgCombK_c1[-10,10]",  "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
                    "RooLegendre::fL1(CosThetaL, {}, {})".format(i, k),
                    "RooLegendre::fL2(CosThetaL, {}, {})".format(j, l),
                    "RooRealSumPdf::fL({0.5, fL1, fL2}, {1, bkgCombL_c1, bkgCombL_c2}, 1)",
                    "RooChebychev::fK(CosThetaK, {bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5} )",
                    "PROD::f_bkgCombA(fL, fK)"
                ]

for i, j, k in ((a, b, c) for a in range(10) for b in range(a+1) for c in range(1,8)):
        f_analyticBkgCombA_format['Leg{}G2_Cbv{}_v{}'.format(i, k, j)] = [ #
            "RooLegendre::fL1(CosThetaL, {}, {})".format(i, j),
            "RooGaussian::fL2(CosThetaL, bkgCombL_c4[0.7, 0.6, 0.9], bkgCombL_c6[0.08, 0, 5])",
            "RooGaussian::fL3(CosThetaL, bkgCombL_c5[-0.75, -0.9, -0.6], bkgCombL_c7[0.1, 0, 5])",
            "RooRealSumPdf::fL4({0.5, fL1}, {1, bkgCombL_c1[-10,10]}, 1)",
            "SUM::fL(bkgCombL_c2[-10,10]*fL2, bkgCombL_c3[-10,10]*fL3, fL4)",
            "RooChebychev::fK(CosThetaK, {} )".format("{"+", ".join(['bkgCombK_c{}[-10,10]'.format(i) for i in range(1,k+1)])+"}"),
            "PROD::f_bkgCombA(fL, fK)"
        ]

f_analyticBkgCombA_format['G3Cbv4_Cbv5'] = [ #
    "RooGaussian::fL1(CosThetaL, bkgCombL_c1[0.7, 0.6, 0.9], bkgCombL_c4[0.1, 0, 5])",
    "RooGaussian::fL2(CosThetaL, bkgCombL_c2[-0.7, -0.9, -0.6], bkgCombL_c5[0.1, 0, 5])",
    "RooGaussian::fL3(CosThetaL, bkgCombL_c3[0., -0.3, 0.3], bkgCombL_c6[0.1, 0, 5])",
    "RooChebychev::fL4(CosThetaL, {} )".format("{"+", ".join(['bkgCombL_c{}[-10,10]'.format(i) for i in range(7,11)])+"}"),
    "SUM::fL(bkgCombK_c16[-10,10]*fL1, bkgCombK_c17[-10,10]*fL2, bkgCombK_c18[-10,10]*fL3, fL4)",
    "RooChebychev::fK(CosThetaK, {} )".format("{"+", ".join(['bkgCombK_c{}[-10,10]'.format(i) for i in range(11,16)])+"}"),
    "PROD::f_bkgCombA(fL, fK)"
]
f_analyticBkgCombA_format['Cbv5G2_Cbv5'] = [ #
    "bkgCombL_c1[-10,10]", "bkgCombL_c2[-10,10]", "bkgCombL_c3[-10,10]", "bkgCombL_c4[-10,10]", "bkgCombL_c5[-10,10]",
    "bkgCombK_c1[-10,10]",  "bkgCombK_c2[-10,10]", "bkgCombK_c3[-10,10]", "bkgCombK_c4[-10,10]", "bkgCombK_c5[-10,10]",
    "RooChebychev::fL1(CosThetaL, {bkgCombL_c1, bkgCombL_c2, bkgCombL_c3, bkgCombL_c4, bkgCombL_c5} )",
    "RooGaussian::fL2(CosThetaL, bkgCombL_c6[0.7, 0.6, 0.9], bkgCombL_c7[0.12, 0, 5])",
    "RooGaussian::fL3(CosThetaL, bkgCombL_c8[-0.75, -0.9, -0.6], bkgCombL_c9[0.1, 0, 5])",
    "SUM::fL(bkgCombL_c10[-10,10]*fL2, bkgCombL_c11[-10,10]*fL3, fL1)",
    "RooChebychev::fK(CosThetaK, {bkgCombK_c1, bkgCombK_c2, bkgCombK_c3, bkgCombK_c4, bkgCombK_c5} )",
    "PROD::f_bkgCombA(fL, RooChebychev::fL4(CosThetaL, {bkgCombL_c12[-10,10], bkgCombL_c13[-10,10]}), fK)"
]
