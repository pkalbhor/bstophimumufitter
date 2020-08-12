#include "TFile.h"
//#include "Rooworkspace.h"
#include <typeinfo>

void RooWorkspaceReader(){
std::string a[]={"0"};//, "1B", "1C", "3", "5A", "5B", "0"};
int n=sizeof(a)/sizeof(a[0]);

RooWorkspace *w;
std::string b[n];
for(int i=0; i<n;i++){
    std::string c="wspace";             
    c.append("_2016_bin"); c.append(a[i]);   //Makes string as 'wspace_bin'
    char *arr=new char[c.length()+1];   //Allocates size to the array
    strcpy(arr, c.c_str());             //copies string to array
    Option_t *t=arr;

    std::string m="./input/";
    m.append(c); m.append(".root");
    arr =new char[m.length()+1];
    strcpy(arr,m.c_str());
    Option_t *M=arr;
    
    TFile f(M, "READ");
    f.ls();

    std::string k; k.append("wspace.bin"); k.append(a[i]);
    arr=new char[k.length()+1];
    strcpy(arr, k.c_str());
    Option_t *K=arr;
    std::cout<<K<<std::endl;
    w=(RooWorkspace*)f.Get(K);
    w->ls();
    w->Print();
}
exit(0);
}
