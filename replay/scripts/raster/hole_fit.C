/*
* hole_fit.C
* Author: Tyler Hague
* Fits the Carbon Hole in order to calibrate the raster
* 
* Changelog:
* 23 March 2018 - Created
*/


#define RIGHT_ARM_CONDITION run>=90000
#define LEFT_ARM_CONDITION run<90000

#include "TString.h"

void hole_fit(){
  Int_t run = 0;
  cout << "What run number would you like to calibrate with?    ";
  cin >> run;
  cout << endl << endl;
  if(run<=0){
    cout << "Invalid run number. Exiting." << endl << endl;
    return;
  }

  Double_t kx = 1.;
  Double_t ky = -1.;

  //Open Root File

  TChain *rootfile = new TChain("T");

  int i = 1;

  if(!gSystem->AccessPathName(TString::Format("/cache/halla/triton/prod/marathon/pass1_calibration/kin1/tritium_%d.root",run),kFileExists)){
    rootfile->Add(TString::Format("/cache/halla/triton/prod/marathon/pass1_calibration/kin1/tritium_%d.root",run));
    cout << "Added file: tritium_" << run << ".root" << endl;
  }else{
    cout << "Requested run has not been replayed. Exiting." << endl << endl;
    return;
  }

  while(!gSystem->AccessPathName(TString::Format("/cache/halla/triton/prod/marathon/pass1_calibration/kin1/tritium_%d_%d.root",run,i),kFileExists)){
    rootfile->Add(TString::Format("/cache/halla/triton/prod/marathon/pass1_calibration/kin1/tritium_%d_%d.root",run,i));
    cout << "Added file: tritium_" << run << "_" << i << ".root" << endl;
    i=i+1;
  }                      
 
  TString arm;
  if(RIGHT_ARM_CONDITION){
    arm="Rrb";
  }else if(LEFT_ARM_CONDITION){
    arm="Lrb";
  }
  //Define cuts

  TString cut = "(TMath::Abs(" + arm + ".BPMA.x)<100)&&((ev";
  if(RIGHT_ARM_CONDITION){
    cut += "Right";
  }else if(LEFT_ARM_CONDITION){
    cut += "Left";
  }
  cut += "dnew_r*0.0003299)>4.5)";
  cut += "&&(";
  if(RIGHT_ARM_CONDITION){
    cut += "R";
  }else if(LEFT_ARM_CONDITION){
    cut += "L";
  }
  cut += ".tr.n==1)";
  /*cut += "&&(";
  if(RIGHT_ARM_CONDITION){
    cut += "R";
  }else if(LEFT_ARM_CONDITION){
    cut += "L";
  }
  cut += ".cer.asum_c)>2000";*/
  cut += "&&(abs(";
  if(RIGHT_ARM_CONDITION){
    cut += "R";
  }else if(LEFT_ARM_CONDITION){
    cut += "L";
  }
  cut += ".tr.vz)<0.02)";

  //Define the fits and the plots

  TF2 *ell_fit = new TF2("ell_fit","[0]/(1. + exp(-1. * [5] * ((([1]*([2]-x))^2 + ([3]*([4]-y))^2)-1.)))",60000,87000,40000,114000);

  Double_t param[6] = {25,0.00008,72500,0.00003,80000, 1.};
  ell_fit->SetParameters(param);
  ell_fit->SetParLimits(0,10,50);
  ell_fit->SetParLimits(1,.00006,.0001);
  ell_fit->SetParLimits(2,65000,75000);
  ell_fit->SetParLimits(3,.00001,.00005);
  ell_fit->SetParLimits(4,70000,85000);
  ell_fit->SetParLimits(5,.5,10);
  
  TF2 *ell_fit2 = new TF2("ell_fit2","[0]/(1. + exp(-1. * [5] * ((([1]*([2]-x))^2 + ([3]*([4]-y))^2)-1.)))",45000,95000,20000,120000);

  Double_t param2[6] = {25,0.00008,72500,0.00003,80000, 1.};
  ell_fit2->SetParameters(param2);
  ell_fit2->SetParLimits(0,10,50);
  ell_fit2->SetParLimits(1,.00006,.0001);
  ell_fit2->SetParLimits(2,65000,75000);
  ell_fit2->SetParLimits(3,.00001,.00005);
  ell_fit2->SetParLimits(4,70000,85000);
  ell_fit2->SetParLimits(5,.5,10);

  TH2F *R1 = new TH2F("R1","Raster 1 Carbon Hole",25,45000,95000,50,20000,120000);
  TH2F *R2 = new TH2F("R2","Raster 2 Carbon Hole",25,45000,95000,50,20000,120000);

  TCanvas *c1 = new TCanvas();
  TCanvas *c2 = new TCanvas();
  c1->cd(0);
  rootfile->Draw(arm + ".Raster.rawcur.y:" + arm + ".Raster.rawcur.x>>R1",TCut(cut),"colz");
  R1->Fit(ell_fit);
  //ell_fit->Draw("cont1 same");
  c2->cd(0);
  rootfile->Draw(arm + ".Raster2.rawcur.y:" + arm + ".Raster2.rawcur.x>>R2",TCut(cut),"colz");
  R2->Fit(ell_fit2);
  //ell_fit2->Draw("cont1 same");
  
  cout << arm << ".Raster.raw2posT = " << ell_fit->GetParameter(2)*-1.*kx*ell_fit->GetParameter(1)/1000. << " " << ell_fit->GetParameter(4)*-1.*ky*ell_fit->GetParameter(3)/1000. << " " << ell_fit->GetParameter(1)*kx/1000. << " " << ell_fit->GetParameter(3)*ky/1000. << " 0.0 0.0" << endl;

  cout << arm << ".Raster2.raw2posT = " << ell_fit2->GetParameter(2)*-1.*kx*ell_fit2->GetParameter(1)/1000. << " " << ell_fit2->GetParameter(4)*-1.*ky*ell_fit2->GetParameter(3)/1000. << " " << ell_fit2->GetParameter(1)*kx/1000. << " " << ell_fit2->GetParameter(3)*ky/1000. << " 0.0 0.0" << endl;
}
