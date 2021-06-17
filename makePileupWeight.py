import sys
import ROOT as rt

def dumpRootFile(filename):
    f=rt.TFile(filename)
    h=f.Get("pileup")
    out=[]
    for i in range(1,h.GetXaxis().GetNbins()+1):
        out+=[h.GetBinContent(i)]
    f.Close()
    return out

if len(sys.argv)<2:
    print("Usage: python makePileupWeight.py YEAR")
    exit(1)
year=sys.argv[1]
if year=="2016preVFP": from SimGeneral.MixingModule.mix_2016_25ns_UltraLegacy_PoissonOOTPU_cfi import mix
elif year=="2016postVFP": from SimGeneral.MixingModule.mix_2016_25ns_UltraLegacy_PoissonOOTPU_cfi import mix
elif year=="2017": from SimGeneral.MixingModule.mix_2017_25ns_UltraLegacy_PoissonOOTPU_cfi import mix
elif year=="2018": from SimGeneral.MixingModule.mix_2018_25ns_UltraLegacy_PoissonOOTPU_cfi import mix
else:
    print("wrong year.. exit...")
    exit(1)
    
pu_data=dumpRootFile(year+"/"+year+"_DATA_69p2.root")
pu_data_up=dumpRootFile(year+"/"+year+"_DATA_72p4.root")
pu_data_down=dumpRootFile(year+"/"+year+"_DATA_66p0.root")
pu_mc=mix.input.nbPileupEvents.probValue
    
while 0 in pu_mc:
    pu_mc[-2]+=pu_mc[-1]
    pu_mc=pu_mc[:-1]

if len(pu_data)>len(pu_mc):
    while len(pu_data)!=len(pu_mc):
        pu_data[-2]+=pu_data[-1]
        pu_data=pu_data[:-1]
        pu_data_up[-2]+=pu_data_up[-1]
        pu_data_up=pu_data_up[:-1]
        pu_data_down[-2]+=pu_data_down[-1]
        pu_data_down=pu_data_down[:-1]

elif len(pu_data)<len(pu_mc):
    while len(pu_data)!=len(pu_mc):
        pu_data+=[0.]
        pu_data_up+=[0.]
        pu_data_down+=[0.]

pu_data=[i/sum(pu_data) for i in pu_data]
pu_data_up=[i/sum(pu_data_up) for i in pu_data_up]
pu_data_down=[i/sum(pu_data_down) for i in pu_data_down]
pu_mc=[i/sum(pu_mc) for i in pu_mc]
while pu_data[-1]/pu_mc[-1]>3:
    pu_data[-2]+=pu_data[-1]
    pu_data=pu_data[:-1]
    pu_data_up[-2]+=pu_data_up[-1]
    pu_data_up=pu_data_up[:-1]
    pu_data_down[-2]+=pu_data_down[-1]
    pu_data_down=pu_data_down[:-1]
    pu_mc[-2]+=pu_mc[-1]
    pu_mc=pu_mc[:-1]

print("sum pu_mc:"+str(sum(pu_mc)))
print("sum pu_data:"+str(sum(pu_data)))

w=[pu_data[i]/pu_mc[i] for i in range(len(pu_data))]
w_up=[pu_data_up[i]/pu_mc[i] for i in range(len(pu_data_up))]
w_down=[pu_data_down[i]/pu_mc[i] for i in range(len(pu_data_down))]
fout=rt.TFile("PileupWeight"+year+".root","recreate")
h=rt.TH1D("MC_"+year+"_central","MC_"+year+"_central",len(w),0,len(w))
h_up=rt.TH1D("MC_"+year+"_sig_up","MC_"+year+"_sig_up",len(w),0,len(w))
h_down=rt.TH1D("MC_"+year+"_sig_down","MC_"+year+"_sig_down",len(w),0,len(w))
h_data=rt.TH1D("DATA_PU","DATA_PU",len(pu_data),0,len(pu_data))
h_mc=rt.TH1D("MC_PU","MC_PU",len(pu_mc),0,len(pu_mc))
for i in range(len(w)):
    h.SetBinContent(i+1,w[i])
    h_up.SetBinContent(i+1,w_up[i])
    h_down.SetBinContent(i+1,w_down[i])
    h_data.SetBinContent(i+1,pu_data[i])
    h_mc.SetBinContent(i+1,pu_mc[i])
h.Write()
h_up.Write()
h_down.Write()
h_data.Write()
h_mc.Write()
fout.Close()
