/// combining paddle #11 and #12

#include "TCanvas.h"
#include "TString.h"
#include "TFile.h"
#include "TTree.h" 

//void L_add11_12()
void test(){
  
  Double_t tdcTime = 56.23e-12;    // in ns:   F1 TDCs, 56.23 ps / Ch
  
  //Int_t runNUM = 90854;
  // Int_t evtNUM = 10000;
  TH1F *h12=new TH1F("h12","h12 with  +9.975e-10",500,0.10e-6,0.15e-6);
  TString filename;
  for(int irun=100400;irun<100435;irun++) {
    if(irun != 100422 && irun!=100423){
      for (int subrun = 1;subrun<2;subrun++){
	
	//if(irun==100422 || subrun==1) continue;
	//filename = (Form("/adaqfs/home/a-onl/tritium_work/bishnu/Rootfiles/tritium_%d.root",irun));
	
	filename = (Form("/adaqfs/home/a-onl/tritium_work/bishnu/Rootfiles/tritium_%d_%d.root",irun,subrun));
	TFile *data_file = new TFile(filename,"READ"); 
	TTree *T = (TTree*)data_file->Get("T");
	
	/// variables to be used event by event
	Double_t RF_s2_mean;
	Double_t RF_s2_pad11_meanCorr;
	Double_t RF_s2_pad12_meanCorr;
	
	//Define TTree Leaf names that will be used (shoule be exactly as it appears on the TTree)
	TString nLHRS_trig = "DR.evtypebits";
	TString nLs2_pad = "L.s2.t_pads";
	TString nLs2_nthit = "L.s2.nthit";
	TString nLs2_tdchit = "LTDC.F1FirstHit";
	TString nL_trx = "L.tr.x";
	TString nL_trth = "L.tr.th";
	TString nLs2_ladc = "L.s2.la_c";
	
	// Define TTree Leaf  variables to hold the values
	Double_t LHRS_trig;
	Double_t  Ls2_pad[100];
	Double_t Ls2_nthit;
	Double_t Ls2_tdchit[100];
	Double_t L_trx[100];
	Double_t  L_trth[100];
	Double_t Ls2_ladc[100];
	
	// Now set the branch address
	T->SetBranchAddress(nLHRS_trig, &LHRS_trig);
	T->SetBranchAddress(nLs2_pad, &Ls2_pad);
	T->SetBranchAddress(nLs2_nthit, &Ls2_nthit);
	T->SetBranchAddress(nLs2_tdchit, &Ls2_tdchit);
	T->SetBranchAddress(nL_trx, &L_trx);
	T->SetBranchAddress(nL_trth, &L_trth);
	T->SetBranchAddress(nLs2_ladc, &Ls2_ladc);
	
	
	// loop over nentries
	Long64_t nentries = T->GetEntries();
	for(Long64_t i=0;i<nentries;i++){
	  T->GetEntry(i);
	  UInt_t LHRS_trig_bit2 = (static_cast<UInt_t>(LHRS_trig)>>2)&1;
	  
	  // Do not use these variables
	  RF_s2_pad11_meanCorr =(Ls2_tdchit[37] -Ls2_tdchit[47])*tdcTime - (((Ls2_tdchit[30]- Ls2_tdchit[11])*tdcTime + (Ls2_tdchit[37] - Ls2_tdchit[59])*tdcTime )/2.0 + 7.745e-09*L_trx[0]  -3.43925e-08*L_trth[0] -1.816135e-12*Ls2_ladc[11] + 9.985e-10); 
	  
	  RF_s2_pad12_meanCorr = (Ls2_tdchit[37] -Ls2_tdchit[47])*tdcTime - (((Ls2_tdchit[30] - Ls2_tdchit[12])*tdcTime + (Ls2_tdchit[37] - Ls2_tdchit[60])*tdcTime )/2.0 + 5.94972e-09*L_trx[0] -3.05521e-08*L_trth[0] -1.15547e-12*Ls2_ladc[12] +9.975e-10);
	  
	  
	  // Defining cuts
	  if(LHRS_trig_bit2 && Ls2_pad[0]==11 && Ls2_nthit==1) {
	    RF_s2_mean = RF_s2_pad11_meanCorr;
	  }
	  else if( LHRS_trig_bit2 && Ls2_pad[0]==12 && Ls2_nthit==1 ){
	    RF_s2_mean = RF_s2_pad12_meanCorr;
	  }
	  else if( LHRS_trig_bit2 && (Ls2_pad[0]==11 && Ls2_pad[1]==12 )) {
	    RF_s2_mean = (RF_s2_pad11_meanCorr + RF_s2_pad12_meanCorr)/2.0;
	  }
	  
	  else {
	    RF_s2_mean = 0;
	  }
	  
	  if (RF_s2_mean !=0) {
	    h12->Fill(RF_s2_mean);
	  } 
	  
	} // end Entry loop
	
      }// end of subrun
    } // end run loop
  } 
  TCanvas *c1 = new TCanvas("c1","c1",600,600);
  c1->cd();
  h12->Draw();
  
  
}
