from root_utils import *

#set_style()

data = load_row("jpsimass.txt")
h = histogram(data,bins=100,title="Conteggi")


f = func(expression="gaus(0)+pol1(3)",
         params=[50000,3.1,1,50000,-2000],
         param_names=["A","#mu","#sigma","q","m"],
         range=[1,5])

fit_f = fit(h,f)


c, leg = draw(objects=[h,fit_f], 
     labels=["Counts", "Fit"],
     options=["hist","dashed"],
     hist_stats=True,
     save="interpolazione.pdf",)