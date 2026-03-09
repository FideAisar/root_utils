from root_utils import *

#set_style()

f = func3d(expression="sin(2*x)+sin(3*y)-z",
           xmin=-3,xmax=3,
           ymin=-3,ymax=3,
           zmin=-3,zmax=3,
           color="light_blue")

draw([f], 
     labels=[r"z = sin(2x)$+ sin(3y) + e^{#sigma}"],
     legend_border=1,
     legend_fill_alpha=1,
     legend_width=0.4,
     legend_row_height=0.06,
     save="func_3d.pdf")