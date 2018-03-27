/*
* hole_fit.C
* Author: Tyler Hague
* Fits the Carbon Hole in order to calibrate the raster
* 
* Changelog:
* 23 March 2018 - Created
*/

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

  if(!gSystem->AccessPathName(TString::Format("/chafs1/work1/tritium/tmp_data/tritium_%d.root",run),kFileExists)){
    rootfile->Add(TString::Format("/chafs1/work1/tritium/tmp_data/tritium_%d.root",run));
    cout << "Added file: tritium_" << run << ".root" << endl;
  }else{
    cout << "Requested run has not been replayed. Exiting." << endl << endl;
    return;
  }

  while(!gSystem->AccessPathName(TString::Format("/chafs1/work1/tritium/tmp_data/tritium_%d_%d.root",run,i),kFileExists)){
    rootfile->Add(TString::Format("/chafs1/work1/tritium/tmp_data/tritium_%d_%d.root",run,i));
    cout << "Added file: tritium_" << run << "_" << i << ".root" << endl;
    i=i+1;
  }                      
 
  TString arm;
  if(RIGHT_ARM_CONDITION){
    arm="Rrb";
  }else if(LEFT_ARM_CONDITION){
    arm="Lrb";
  }

  //Define the fits and the plots

  TF2 *ell_fit = new TF2("ell_fit","[0]*((([1]*([2]-x))^2 + ([3]*([4]-y))^2) > 2 ? 0 : 1 )",45000,95000,20000,120000);

  Double_t param[5] = {40,0.00008,72500,0.00003,80000};
  ell_fit->SetParameters(param);
  
  TF2 *ell_fit2 = new TF2("ell_fit2","[0]*((([1]*([2]-x))^2 + ([3]*([4]-y))^2) > 2 ? 0 : 1 )",45000,95000,20000,120000);

  Double_t param2[5] = {40,0.00008,72500,0.00003,80000};
  ell_fit2->SetParameters(param2);

  TH2F *R1 = new TH2F("R1","Raster 1 Carbon Hole",5000,45000,95000,10000,20000,120000);
  TH2F *R2 = new TH2F("R2","Raster 2 Carbon Hole",5000,45000,95000,10000,20000,120000);

  TCanvas *c1 = new TCanvas();
  TCanvas *c2 = new TCanvas();
  c1->cd(0);
  T->Draw(arm + ".Raster.rawcur.y:" + arm + ".Raster.rawcur.x>>R1",cut,"colz");
  R1->Fit(ell_fit);
  ell_fit->Draw("cont1 same");
  c2->cd(0);
  T->Draw(arm + ".Raster2.rawcur.y:" + arm + ".Raster2.rawcur.x>>R2",cut,"colz");
  R2->Fit(ell_fit2);
  ell_fit2->Draw("cont1 same");
}
