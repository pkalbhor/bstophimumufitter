TObjArray *qt = new TObjArray();
qt->SetOwner(kTRUE);
for(Int_t i=0; i<2; i++){
    TH2D *h3=new TH2D("hist"+TString::Itoa(i, 2), "title", 100, -1., 1., 100, 0., 1.);
    TH2D *h2=(TH2D*)h3;
    for(Int_t j=0; j<3000; j++){
        Double_t a6=gRandom->Uniform(-1, 1);
        Double_t fl=gRandom->Uniform(0, 1.-abs(a6));
        //cout<< a6 << "\t" << fl <<endl;
        h2->Fill(a6, fl);
        }
    qt->Add(h2);
    cout<< &h2 << endl;
    //h2->Print();
    //h2->Draw();
    //gPad->SaveAs("hist"+TString::Itoa(i, 10)+".pdf");
    //gPad->Clear();
    //delete h2;
}
qt->Print();
TFile *f=new TFile("save.root", "RECREATE");
qt->Write();
f->Close();
qt->At(0)->Draw();

((2. * (1. - (0.5 + (atan($49) / pi))) * atan($48)) / pi):(0.5 + (atan($49) / pi))

