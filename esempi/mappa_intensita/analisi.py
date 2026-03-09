from root_utils import *

#set_style()


col, row, i_zero, i = load_columns("data.txt", ["x", "y","i_1","i_2"])

mappa = map_from_arrays(col, row, i_zero - i,)

draw([mappa], 
     labels=["Intensita"],
     options=["LEGO"],
     xrange=[20,90], yrange=[20,80],
     legend_border=2,
     legend_width=0.15,
     legend_fill_alpha=1,
     legend_text_size= 0.032,
     width=1000,
     save="map.pdf")


