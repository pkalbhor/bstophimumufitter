#include "TFile.h"

void RooWorkspaceReader(){
TFile f("./input/wspace_bin3.root", "READ");
f.Print();
f.ls();
RooWorkspace *w=(RooWorkspace*)f.Get("wspace.bin3");
w->Print();
}

