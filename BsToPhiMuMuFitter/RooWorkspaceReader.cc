#include "TFile.h"

void RooWorkspaceReader(){
Option_t *t = "./input/wspace_bin1A.root";
Option_t *m = "wspace.bin1A";
TFile f(t, "READ");
f.Print();
f.ls();
RooWorkspace *w=(RooWorkspace*)f.Get(m);
w->Print();
}

