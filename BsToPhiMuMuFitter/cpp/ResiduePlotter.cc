//  ////////////////////////////////////////////////////////////////////////////////////////////
//  Description : Input given as two frames. It divides Canvas into two Pads and Plots two graph
//  Author      : Pritam Kalbhor
//  Email       : physics.pritam@gmail.com
//
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#include "RooArgSet.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooPlot.h"
#include "TAxis.h"
#include "TPad.h"
#include "TStyle.h"
#include "TRatioPlot.h"

class NewResPlot{
private:
	void SetgStyles();
	void SetupPads();
	void Init(RooPlot *f1, RooPlot *f2);
	double fInsetWidth= 0.0025; 
	double fSplitFraction=0.3;
   Float_t fUpTopMargin = 0.1; ///< Stores the top margin of the upper pad
   Float_t fUpBottomMargin = 0.02; ///< Stores the bottom margin of the upper pad
   Float_t fLowTopMargin = 0.05; ///< Stores the top margin of the lower pad
   Float_t fLowBottomMargin = 0.3; ///< Stores the bottom margin of the lower pad
   Float_t fFontSize = 18.;

public:
	NewResPlot(RooPlot *f1, RooPlot *f2);
	~NewResPlot();
	TPad *fUpperPad = 0;
	TPad *fLowerPad = 0;
    RooPlot *frame1 = 0;
    RooPlot *frame2 = 0;

    void SetPadMargins();
	void PostDrawDecoration();
	void Draw();
};

NewResPlot::NewResPlot(RooPlot *f1, RooPlot *f2){
 Init(f1, f2); 	
}//Default Constructer

NewResPlot::~NewResPlot(){}

void NewResPlot::SetupPads(){
	double pm =fInsetWidth;
   double width = gPad->GetWNDC();
   double height = gPad->GetHNDC();
   double f = height/width;
	
   if (!gPad) {
      std::cout<<"SetupPads: need to create a canvas first"<<std::endl;
      return;
	}
	fUpperPad = new TPad("upper_pad", "", pm*f, fSplitFraction, 1.-pm*f, 1.-pm);
    fLowerPad = new TPad("lower_pad", "", pm*f, pm, 1.-pm*f, fSplitFraction); 
}

void NewResPlot::SetgStyles(){
   gStyle->SetFrameBorderMode(0);
   gStyle->SetFrameBorderSize(1);
   gStyle->SetFrameFillColor(0);
   gStyle->SetFrameFillStyle(0);
   gStyle->SetFrameLineColor(1);
   gStyle->SetFrameLineStyle(1);
   gStyle->SetFrameLineWidth(1);
   gStyle->SetPadTickX(1); //For Ticks on Opposide side of Axis
   gStyle->SetPadTickY(1);
  
   gStyle->SetPadTopMargin(0.05);
   gStyle->SetPadBottomMargin(0.13);
   gStyle->SetPadLeftMargin(0.12);
   gStyle->SetPadRightMargin(0.02);

	gStyle->SetTitleFont(42);
	gStyle->SetTitleSize(0.06, "XYZ");

}

void NewResPlot::SetPadMargins(){
   //fUpperPad->SetTopMargin(fUpTopMargin);
   fUpperPad->SetBottomMargin(fUpBottomMargin);
   fLowerPad->SetTopMargin(fLowTopMargin);
   fLowerPad->SetBottomMargin(fLowBottomMargin);
}



void NewResPlot::Init(RooPlot *f1, RooPlot *f2){
	frame1=f1; frame2=f2;
	SetgStyles();
	SetupPads();
	SetPadMargins();
}

void NewResPlot::PostDrawDecoration(){
	float textsize = fFontSize/(fLowerPad->GetWh()*fLowerPad->GetAbsHNDC());
	frame2->GetXaxis()->SetLabelSize(textsize);
	frame2->GetYaxis()->SetLabelSize(textsize);
	frame2->GetXaxis()->SetTitle("Cos#theta_{l}");
	frame2->GetXaxis()->SetTitleSize(textsize);
	frame2->GetXaxis()->SetTickLength(0.08); 
	frame2->GetYaxis()->SetNdivisions(505);
	frame2->GetYaxis()->SetTitleSize(textsize);
	frame2->GetYaxis()->SetTitleOffset(0.52);
	frame2->GetYaxis()->SetTitle("Residual");
	frame2->SetTitle("");
	
	textsize = fFontSize/(fUpperPad->GetWh()*fUpperPad->GetAbsHNDC());
	frame1->SetTitle("");
	frame1->GetYaxis()->SetLabelSize(textsize);
	frame1->GetYaxis()->SetTitleSize(textsize);
	frame1->GetXaxis()->SetLabelOffset(999);
	frame1->GetXaxis()->SetTitle("");
}

void NewResPlot::Draw(){
 	fUpperPad->Draw();
   fLowerPad->Draw();

	fUpperPad->cd();
	frame1->Draw();
	
	fLowerPad->cd();
	frame2->Draw();
	
   PostDrawDecoration();
}


























