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

---

## Quick start

```python
from root_utils import *
import numpy as np

set_style()

data = np.random.normal(0, 1, 10000)
h = histogram(data, bins=60, range=(-4, 4),
              xlabel="#Delta E [MeV]", ylabel="Counts / 0.1 MeV",
              color="blue")
f = fit(h, "gaus", xmin=-3, xmax=3)
draw([h, f],
     labels=["Simulation", "Gaussian fit"],
     fit_stats=True,
     save="quickstart.pdf")
```

---

## Text and labels — ROOT TLatex syntax

Every text field in the module (axis titles, histogram titles, parameter names,
legend labels) is passed through `latex()`, which only strips `$` characters.
Write ROOT TLatex directly:

| What you want | ROOT TLatex string |
|---|---|
| Greek letter μ | `#mu` |
| Subscript p_T | `p_{T}` |
| Superscript x² | `x^{2}` |
| Fraction a/b | `#frac{a}{b}` |
| Square root | `#sqrt{x}` |
| Plus-minus | `#pm` |
| Chi squared | `#chi^{2}` |
| Italic text | `#it{text}` |
| Bold text | `#bf{text}` |

```python
h = histogram(data,
              xlabel="m_{#pi#pi} [MeV/c^{2}]",
              ylabel="Events / 5 MeV")

f = func("gaus", -5, 5,
         param_names=["A", "#mu", "#sigma"])

draw([h, f],
     labels=["Data #sqrt{s} = 13 TeV", "Gaussian fit #pm 1#sigma"])
```

---

## Global style

```python
set_style()
```

Applies a publication-ready style: Times New Roman font, no statistics box,
no title box, tick marks on all four sides, white background, and clean margins.
Call once at the start of every script.

---

## Colors

Pass a name string or a raw ROOT integer to any `color` parameter.

| Name | Appearance |
|---|---|
| `"black"`, `"white"` | — |
| `"red"`, `"dark_red"`, `"light_red"` | — |
| `"blue"`, `"dark_blue"`, `"light_blue"` | — |
| `"green"`, `"dark_green"`, `"light_green"` | — |
| `"cyan"`, `"orange"`, `"yellow"` | — |
| `"magenta"`, `"violet"` | — |
| `"gray"`, `"dark_gray"` | — |

Raw ROOT integers also work: `color=ROOT.kRed+3`.

---

## Line styles

Pass a name string or a ROOT integer to any `line_style` parameter.

| Name | Aliases | ROOT code |
|---|---|---|
| `"solid"` | — | 1 |
| `"dashed"` | `"dash"` | 2 |
| `"dotted"` | `"dot"` | 3 |
| `"dash_dot"` | `"dashdot"`, `"dot_dash"` | 4 |
| `"dash_dot_dot"` | `"dot_dot_dash"` | 5 |
| `"long_dashed"` | — | 6 |
| `"long_dash_dot"` | — | 7 |
| `"long_dash_dot_dot"` | — | 8 |

---

## Marker styles

Pass a name string or a ROOT integer to any `marker` parameter.

**Filled:** `"circle"`, `"square"`, `"triangle_up"`, `"triangle_down"`,
`"star"`, `"diamond"`, `"cross_circle"`

**Open:** `"open_circle"`, `"open_square"`, `"open_triangle_up"`,
`"open_triangle_down"`, `"open_star"`, `"open_diamond"`

**Simple:** `"dot"`, `"plus"`, `"asterisk"`, `"cross"` / `"x"`

---

## Graphs

### `graph` — TGraphErrors (symmetric errors)

```python
g = graph(x, y,
          ex=None, ey=dy,           # optional error arrays
          xlabel="t [ns]",
          ylabel="V [mV]",
          color="blue",
          marker="circle",          # or any marker name / ROOT integer
          marker_size=1.2,
          line_style="solid",
          line_width=2)
```

### `graph_asymm` — TGraphAsymmErrors (independent low/high errors)

```python
g = graph_asymm(x, y,
                eyl=err_low, eyh=err_high,
                color="dark_green",
                marker="open_square")
```

---

## Functions

### `func` — TF1 (1D)

```python
f = func("[0]*exp(-0.5*((x-[1])/[2])^2)",
         xmin=-5, xmax=5,
         params=[100.0, 0.0, 1.0],
         param_names=["A", "#mu", "#sigma"],
         color="red",
         line_style="dashed",
         npx=2000)           # increase for sharp peaks
```

Built-in ROOT named functions also work: `"gaus"`, `"pol2"`, `"expo"`, etc.

### `func2d` — TF2 (2D surface)

```python
f = func2d("sin(x)*cos(y)",
           xmin=-3.14, xmax=3.14,
           ymin=-3.14, ymax=3.14,
           xlabel="x [rad]", ylabel="y [rad]", zlabel="Amplitude")
draw([f])
```

### `func3d` — TF3 (3D isosurface)

```python
f = func3d("exp(-(x*x+y*y+z*z)/(2*[0]*[0]))",
           -4, 4, -4, 4, -4, 4,
           params=[1.0], param_names=["#sigma"],
           color="blue",
           fill_alpha=0.4,      # 0 = invisible, 1 = opaque
           draw_mode="iso",     # or "iso_fb", "bb", "gl", ...
           npx=40, npy=40, npz=40)
draw([f], labels=["Gaussian sphere"])
```

**`draw_mode` options:** `"iso"` (default), `"iso_fb"`, `"iso_bb"`, `"fb"`,
`"bb"`, `"gl"`, `"gl_iso"`, `"gl_col"`, `"gl_box"`, `"tf3"`.

---

## Histograms

### `histogram` — TH1D

```python
h = histogram(data,
              bins=80,
              range=(-5, 5),
              xlabel="#Delta p [MeV/c]",
              ylabel="Counts / 0.125 MeV/c",
              color="blue",
              fill=True,
              fill_alpha=0.3)
```

### `histogram2d` — TH2D

```python
h2 = histogram2d(px, py,
                 bins_x=60, bins_y=60,
                 range_x=(-3, 3), range_y=(-3, 3),
                 xlabel="p_{x} [GeV/c]",
                 ylabel="p_{y} [GeV/c]",
                 zlabel="Counts",
                 palette=ROOT.kViridis)   # optional; default is kBird
draw([h2])
```

---

## Fitting

### `fit`

```python
# Fit with a named formula string
f = fit(h, "gaus", xmin=-3, xmax=3)

# Fit with a pre-built TF1
my_f = func("[0]*(1 + [1]*cos(x))", 0, 6.28, params=[1.0, 0.5])
f    = fit(g, my_f, options="RQS", print_results=False)
```

**Common `options` flags:**

| Flag | Effect |
|---|---|
| `"R"` | Use function range |
| `"S"` | Save fit result object |
| `"Q"` | Quiet mode (suppress ROOT output) |
| `"L"` | Log-likelihood fit |
| `"W"` | Ignore point errors |

### `print_params`

```python
print_params(f, units=["", "MeV/c^{2}", "MeV/c^{2}"], precision=4)
```

---

## Drawing

`draw()` is the central function.  It creates a canvas, draws all objects in
the correct order, optionally adds a legend with statistics, and saves the result.

```python
canvas, legend = draw(
    objects,                      # list of ROOT objects
    labels=["label1", "label2"],  # triggers legend creation
    xlabel="x axis title",
    ylabel="y axis title",
    xrange=(0, 10),               # visible x range
    yrange=(0, 500),              # visible y range
    options="AP",                 # global draw option (or list, see below)
    width=900, height=600,
    log_x=False, log_y=False,
    save="output.pdf",
)
```

### Per-object draw options

Pass a list instead of a string to control each object individually:

```python
draw([g1, g2, h2d], options=["AP", "dashed", "COLZ"])
#                              ^      ^         ^
#                              |      |         raw ROOT draw string
#                              |      line-style shorthand (applied in-place)
#                              raw ROOT draw string
```

Each list element can be:
- `None` — auto-detect from object type
- A line-style name (`"dotted"`, `"dashed"`, …) — sets `SetLineStyle` and draws normally
- Any ROOT draw string (`"AP"`, `"HIST"`, `"COLZ"`, …) — used verbatim

### Legend options

```python
draw([h, f], labels=["Data", "Fit"],
     legend_pos="top_right",       # or "top_left", "bottom_right", etc.
     legend_width=0.30,
     legend_row_height=0.050,      # increase for more row spacing
     legend_ncols=1,
     legend_text_size=0.038,
     legend_margin=0.25,
     legend_border=1,              # 0 = no border
     legend_fill_alpha=1.0)        # 0 = transparent, 1 = opaque white

# Or provide exact NDC coordinates
draw([h], labels=["Data"],
     legend_pos=(0.60, 0.70, 0.90, 0.88))
```

### Histogram statistics in legend

```python
draw([h], labels=["MC"],
     hist_stats=True,
     hist_stats_show_mean=True,
     hist_stats_show_std=True,
     hist_stats_show_counts=True,
     hist_stats_precision=3)
```

### Fit statistics in legend

```python
draw([h, f], labels=["Data", "Gaussian"],
     fit_stats=True,
     fit_stats_show_chi2=True,
     fit_stats_show_params=True,
     fit_stats_show_errors=True,
     fit_stats_precision=3,
     fit_stats_units=["", "MeV", "MeV"])
```

---

## Legend (standalone)

Use `make_legend` when you need a legend outside a `draw()` call, e.g. on a
multi-pad canvas:

```python
leg = make_legend([g1, g2, h],
                  ["Signal", "Background", "Data"],
                  pos="top_right",
                  width=0.30,
                  row_height=0.05,
                  fill_alpha=0.8,
                  border=1)
leg.Draw()
```

---

## Detector / pixel maps

### `map_from_arrays`

```python
h = map_from_arrays(col, row, charge,
                    xlabel="Column",
                    ylabel="Row",
                    zlabel="Charge [e^{-}]",
                    palette=ROOT.kViridis)
draw([h])
```

Bin edges are computed automatically from the unique coordinate values, so
non-uniform pixel spacing is handled correctly.

### `map_from_file`

```python
h = map_from_file("scan.txt",
                  col_col=0, col_row=1, col_val=2,
                  xlabel="Strip",
                  ylabel="Channel",
                  zlabel="Efficiency")
draw([h])
```

---

## I/O utilities

```python
# Single column by index or name
x  = load_column("data.txt", 0)
vy = load_column("data.csv", "voltage", sep=",")

# Multiple columns at once
x, y, ey = load_columns("data.txt", [0, 1, 2])

# Single row (useful when each line is a spectrum)
spectrum = load_row("spectra.txt", row=3)

# Multiple rows
row0, row5 = load_rows("matrix.txt", [0, 5])
```

Default separator is `r"\s+"` (any whitespace).  Pass `sep=","` for CSV files.

---

## Full example — mass spectrum fit

```python
from root_utils import *
import numpy as np

set_style()

# Simulated invariant mass distribution: signal + background
rng  = np.random.default_rng(42)
sig  = rng.normal(775, 25, 5000)      # rho(770) peak
bkg  = rng.uniform(600, 1000, 20000)  # combinatorial background
data = np.concatenate([sig, bkg])

# Histogram
h = histogram(data,
              bins=80, range=(600, 1000),
              xlabel="m_{#pi#pi} [MeV/c^{2}]",
              ylabel="Events / 5 MeV/c^{2}",
              color="blue")

# Fit: Gaussian signal + linear background
f = func("[0]*exp(-0.5*((x-[1])/[2])^2) + [3] + [4]*x",
         xmin=650, xmax=950,
         params=[500, 775, 25, 100, -0.1],
         param_names=["A", "#mu", "#sigma", "p_{0}", "p_{1}"],
         color="red")

fit(h, f, options="RS")

draw([h, f],
     labels=["Data", "Signal + background"],
     fit_stats=True,
     fit_stats_units=["", "MeV/c^{2}", "MeV/c^{2}", "", ""],
     legend_pos="top_right",
     legend_width=0.38,
     save="mass_spectrum.pdf")
```

---

## Full example — 2D correlation plot

```python
from root_utils import *
import numpy as np

set_style()

rng = np.random.default_rng(0)
px  = rng.normal(0, 1, 50000)
py  = 0.6 * px + rng.normal(0, 0.8, 50000)

h2 = histogram2d(px, py,
                 bins_x=80, bins_y=80,
                 range_x=(-4, 4), range_y=(-4, 4),
                 xlabel="p_{x} [GeV/c]",
                 ylabel="p_{y} [GeV/c]",
                 zlabel="Counts",
                 palette=ROOT.kBird)
draw([h2], save="correlation.pdf")
```

---

## Full example — 3D isosurface

```python
from root_utils import *

set_style()

f = func3d("exp(-(x*x + y*y + z*z) / (2*[0]*[0]))",
           -4, 4, -4, 4, -4, 4,
           params=[1.5],
           param_names=["#sigma"],
           color="cyan",
           fill_alpha=0.5,
           draw_mode="iso",
           npx=35, npy=35, npz=35)

draw([f],
     labels=["Gaussian #sigma = 1.5"],
     legend_pos="top_right",
     save="gaussian_3d.pdf")
```