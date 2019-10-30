#include "TFile.h"

void RooWorkspaceReader(){
TFile f("./input/wspace_bin1A.root", "READ");
f.Print();
f.ls();
RooWorkspace *w=(RooWorkspace*)f.Get("wspace.bin1A");
w->Print();
}

