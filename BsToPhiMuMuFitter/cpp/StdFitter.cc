// vim: set sts=4 sw=4 fdm=marker fdn=3 et:

#include "RooAbsPdf.h"
#include "RooDataSet.h"

#include "RooAbsReal.h"
#include "RooDataHist.h"

#include "RooMinuit.h"
#include "RooFitResult.h"
#include "RooLinkedList.h"
#include "RooArgSet.h"


#ifndef STDFITTER_H
#define STDFITTER_H

class StdFitter{
public:
    StdFitter();
    virtual ~StdFitter();

    void addNLLOpt(RooCmdArg*);
    RooMinuit* Init(RooAbsPdf*, RooDataSet*);
    RooMinuit* Init(RooAbsReal*, RooDataHist*);
    RooFitResult* FitMigrad();
    void FitHesse();
    RooFitResult* FitMinos(RooArgSet&);

    RooAbsReal* GetNLL(){return nll;}
    RooMinuit* GetMinuit(){return minuit;}
private:
    RooMinuit *minuit = 0;
    RooAbsReal *nll = 0;
    RooLinkedList createNLLOpt;
};

StdFitter::StdFitter(){}
StdFitter::~StdFitter(){
    delete minuit;
    minuit = 0;
}

void StdFitter::addNLLOpt(RooCmdArg *cmd){
    std::cout<<"This is Pritam5"<<std::endl;
    cmd->Print();
    this->createNLLOpt.Add(cmd);
}

RooMinuit* StdFitter::Init(RooAbsPdf* pdf, RooDataSet* data){
    std::cout<<"This is Pritam2"<<std::endl;
    nll = pdf->createNLL(*data, this->createNLLOpt);
    minuit = new RooMinuit(*nll);
    minuit->setPrintLevel(3); //Pritam
    return minuit;
}

RooMinuit* StdFitter::Init(RooAbsReal* pdf, RooDataHist* data){
    std::cout<<"This is Pritam"<<std::endl;
    nll = pdf->createChi2(*data, this->createNLLOpt);
    minuit = new RooMinuit(*nll);
    return minuit;
}

RooFitResult* StdFitter::FitMigrad(){
    std::cout<<"This is Pritam3"<<std::endl;
    int isMigradConverge{-1};
    RooFitResult *res = 0;
    for (int iL = 0; iL < 10; iL++) {
        std::cout<<"This is Pritam 6i"<<std::endl;
        isMigradConverge = this->minuit->migrad();
        
        std::cout<<"This is Pritam 6f"<<std::endl;
        res = this->minuit->save();
        if (isMigradConverge == 0 && fabs(res->minNll()) < 1e20){
            break;
        }
    }
    return res;
}

void StdFitter::FitHesse(){
    this->minuit->hesse();
}

RooFitResult* StdFitter::FitMinos(RooArgSet& args){
    std::cout<<"This is Pritam4"<<std::endl;
    int isMinosValid{-1};
    RooFitResult *res = 0;
    for (int iL = 0; iL < 3; iL++) {
        isMinosValid = this->minuit->minos(args);
        res = this->minuit->save();
        if (isMinosValid == 0 && fabs(res->minNll()) < 1e20){
            break;
        }
    }
    std::cout<<"This is Pritam4z"<<std::endl;
    return res;
}
#endif
