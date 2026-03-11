# root_utils

High-level PyROOT plotting utilities for physics data analysis (vibe-coded).

`root_utils` wraps the ROOT C++ library with a clean Python API.  The goal is to
eliminate boilerplate: one import, one style call, then work directly with numpy
arrays and human-readable names for colors, markers, and line styles.

---

## Requirements

- Python ≥ 3.10
- ROOT (with PyROOT enabled)
- numpy
- pandas


## Setup

```python
from root_utils import *
set_style()  # apply Times font, no stat box, clean margins
```

---

## Style

### `set_style()`
Apply global publication-ready style (Times New Roman, no stat/title box, tick marks on all sides).


### Colors · `color(name)`
Resolve a name to a ROOT color code. Pass anywhere a `color=` parameter is accepted.

```
"black"  "white"  "red"  "dark_red"  "light_red"
"blue"   "dark_blue"  "light_blue"  "cyan"
"green"  "dark_green"  "light_green"
"orange"  "yellow"  "magenta"  "violet"  "gray"  "dark_gray"
```

Raw ROOT integers (e.g. `ROOT.kRed + 3`) are always accepted too.


### Line styles · `line_style(style)`

```
"solid"  "dashed"  "dotted"  "dash_dot"  "dash_dot_dot"
"long_dashed"  "long_dash_dot"  "long_dash_dot_dot"
```

### Marker styles · `marker_style(style)`

```
# filled
"circle"  "square"  "triangle_up"  "triangle_down"  "star"  "diamond"
# open
"open_circle"  "open_square"  "open_triangle_up"  "open_triangle_down"  "open_star"  "open_diamond"
# simple
"dot"  "plus"  "asterisk"  "cross"
```

### TLatex · `latex(text)`
Pass-through that strips `$` characters — copy-paste LaTeX-wrapped TLatex strings safely.

```python
latex("#mu #pm #sigma")       # '#mu #pm #sigma'
latex("p_{T} [GeV/c^{2}]")   # 'p_{T} [GeV/c^{2}]'
```
```
"black"  "white"  "red"  "dark_red"  "light_red"
"blue"   "dark_blue"  "light_blue"  "cyan"
"green"  "dark_green"  "light_green"
"orange"  "yellow"  "magenta"  "violet"  "gray"  "dark_gray"
```

Raw ROOT integers (e.g. `ROOT.kRed + 3`) are always accepted too.


### Line styles · `line_style(style)`

```
"solid"  "dashed"  "dotted"  "dash_dot"  "dash_dot_dot"
"long_dashed"  "long_dash_dot"  "long_dash_dot_dot"
```

### Marker styles · `marker_style(style)`

```
# filled
"circle"  "square"  "triangle_up"  "triangle_down"  "star"  "diamond"
# open
"open_circle"  "open_square"  "open_triangle_up"  "open_triangle_down"  "open_star"  "open_diamond"
# simple
"dot"  "plus"  "asterisk"  "cross"
```


### TLatex · `latex(text)`
Pass-through that strips `$` characters — copy-paste LaTeX-wrapped TLatex strings safely.

```python
latex("#mu #pm #sigma")       # '#mu #pm #sigma'
latex("p_{T} [GeV/c^{2}]")   # 'p_{T} [GeV/c^{2}]'
```

---

## Graphs

### `graph(x, y, ex, ey, ...)` → `TGraphErrors`
```python
g = graph(x=x, 
          y=y, ey=dy,
          xlabel="t [ns]", ylabel="V [mV]",
          color="red", marker="circle")
```

| Parameter | Default |
|-----------|---------|
| `color` | `"blue"` |
| `marker` | `"circle"` |
| `marker_size` | `1.2` |
| `line_style` | `"solid"` |
| `line_width` | `2` |

### `graph_asymm(x, y, exl, exh, eyl, eyh, ...)` → `TGraphAsymmErrors`
Same parameters as `graph()` but with independent low/high error bars.

---

## Functions (TF1 / TF2 / TF3)

### `func(expression, xmin, xmax, ...)` → `TF1`
```python
f = func("[0]*exp(-0.5*((x-[1])/[2])^2)",
         xmin=-5, xmax=5,
         params=[1.0, 0.0, 1.0],
         param_names=["A", "#mu", "#sigma"],
         color="red", 
         line_style="dashed")
```

### `func2d(expression, xmin, xmax, ymin, ymax, ...)` → `TF2`
Same interface extended with `ymin/ymax`, `ylabel`, `zlabel`, `npy`.

### `func3d(expression, xmin, xmax, ymin, ymax, zmin, zmax, ...)` → `TF3`
Renders as an isosurface. Extra parameters:

| Parameter | Default | Notes |
|-----------|---------|-------|
| `fill_color` | same as `color` | isosurface fill |
| `fill_alpha` | `0.5` | transparency [0–1] |
| `line_color` | same as `color` | wireframe edge |
| `draw_mode` | `"iso"` | `"iso"` `"gl"` `"gl_iso"` `"gl_col"` `"gl_box"` `"fb"` `"bb"` … |
| `npx/npy/npz` | `30` | sampling resolution |

---

## Histograms

### `histogram(data, bins, range, ...)` → `TH1D`
```python
h = histogram(data, bins=80, range=(-5, 5),
              xlabel="#Delta E [MeV]", color="blue",
              fill=True, fill_alpha=0.3)
```

### `histogram2d(x, y, bins_x, bins_y, ...)` → `TH2D`
```python
h2 = histogram2d(px, py, bins_x=60, bins_y=60,
                 xlabel="p_{x} [GeV/c]", ylabel="p_{y} [GeV/c]",
                 palette=ROOT.kViridis)
```

---

## Fitting

### `fit(graph_or_hist, func_or_expr, xmin, xmax, ...)` → `TF1`
```python
f = fit(h, "gaus", xmin=-3, xmax=3)
f = fit(g, my_tf1, options="RQS", print_results=False)
```

| Parameter | Default |
|-----------|---------|
| `options` | `"RS"` |
| `print_results` | `True` |
| `units` | `None` |

### `print_params(f, units, precision)`
Print a formatted parameter table for any fitted `TF1`.

---

## Drawing

### `draw(objects, labels, ...)` → `(TCanvas, TLegend)`

```python
c, leg = draw([h, f],
              labels=["Data", "Gaussian fit"],
              xlabel="m_{#pi#pi} [MeV/c^{2}]",
              ylabel="Events / 10 MeV",
              fit_stats=True,
              save="mass_fit.pdf")
```

**Canvas**

| Parameter | Default |
|-----------|---------|
| `width / height` | `900 / 600` |
| `log_x / log_y` | `False` |
| `xrange / yrange` | `None` |

**Draw options** — pass a single string (global) or a list (per-object):
- `None` → auto-detect from object type
- Line-style name (`"dotted"`) → apply in-place
- Any ROOT string (`"AP"`, `"HIST"`, `"COLZ"`) → verbatim; `SAME` appended automatically

**Legend**

| Parameter | Default |
|-----------|---------|
| `legend_pos` | `"top_right"` |
| `legend_width` | `0.25` |
| `legend_ncols` | `1` |
| `legend_text_size` | `0.038` |
| `legend_fill_alpha` | `0.0` |

`legend_pos` accepts `"top_right"` `"top_left"` `"bottom_right"` `"bottom_left"` `"top_center"` or explicit `(x1, y1, x2, y2)` NDC.

**Histogram stats in legend** (`hist_stats=True`)
Shows mean, std dev, entry count for each `TH1` — toggle individually with `hist_stats_show_mean/std/counts`.

**Fit stats in legend** (`fit_stats=True`)
Shows χ²/NDF and all parameters ± errors for each `TF1` — toggle with `fit_stats_show_chi2/params/errors`.

---

## Legend (manual)

### `make_legend(objects, labels, pos, ...)` → `TLegend`
Lower-level helper for legends outside a `draw()` call.

---

## I/O

```python
load_column(filepath, column, sep)          # → np.ndarray
load_columns(filepath, [col1, col2, ...])   # → list[np.ndarray]
load_row(filepath, row, sep)                # → np.ndarray
load_rows(filepath, [row1, row2, ...])      # → list[np.ndarray]
```

`column` / `row` accept zero-based integer indices or string column names. Default separator: whitespace.

---

## Detector Maps

### `map_from_arrays(col, row, values, ...)` → `TH2D`
Build a pixel/detector map from three equal-length arrays. Bin edges computed automatically from unique coordinate values.

### `map_from_file(filepath, col_col, col_row, col_val, ...)` → `TH2D`
Convenience wrapper — reads col/row/value arrays from a delimited file and calls `map_from_arrays`.

```python
h = map_from_file("scan.txt", col_col=0, col_row=1, col_val=2,
                  xlabel="Strip", ylabel="Channel",
                  zlabel="Efficiency")
draw([h])
```

---

# Examples
In c++

```c++
#include <iostream>
#include <fstream>
#include "TH1D.h"
#include "TApplication.h"
#include "TCanvas.h"
#include "TF1.h"        
#include "TF2.h"        
#include "TLegend.h"   
using namespace std;

int main() {
  TApplication app("app",0,0);

  // setup histogram
  TH1D *hist = new TH1D("hist","Invariant mass distribution",100,1.3,5);
  
  // read from file
  double readvalue;
  ifstream infile("jpsimass.txt");
  while(infile >> readvalue){
      hist->Fill(readvalue);
  }
  
  // fit
  TF1 *modelfit = new TF1("modelfit","gaus(0)+gaus(3)+pol1(6)",1,5);
  modelfit->SetNpx(5000);
  modelfit->SetParameters(6000,3.1,0.14,1500,3.6,0.1,48200,-1621);
  modelfit->SetParLimits(4,3.4,3.7);

  for(int i=0; i<8; i++){
    hist->Fit(modelfit,"0");
  }

  // canvas
  TCanvas *can = new TCanvas("can","can",600,400);
  can->SetMargin(0.15,0.05,0.1,0.1);
  can->cd();
  hist->GetXaxis()->SetTitle("m_{#mu^{+}#mu^{-}}");
  hist->GetYaxis()->SetTitle("counts");

  // draw
  hist->Draw("E");
  modelfit->Draw("same");



  app.Run();
  return 0;
}
```

In Python + root_utils:
```python
from root_utils import *

# Style per latex
#set_style()

data = load_row("jpsimass.txt")
h = histogram(data,bins=100,title="Conteggi")


f = func(expression="gaus(0)+pol1(3)",
         params=[50000,3.1,1,50000,-2000],
         param_names=["A","#mu","#sigma","q","m"],
         xmin=1,xmax=5)

fit_f = fit(h,f)


c, leg = draw(objects=[h,fit_f], 
     labels=["Counts", "Fit"],
     options=["hist","dashed"],
     hist_stats=True,
     #fit_stats=True,
     save="interpolazione.pdf",
     legend_border=2,
     legend_width=0.3,
     legend_fill_alpha=1,)
```
![interpolazione](/esempi/interpolazione/interpolazione.png)