# root_utils

Pythonic wrappers for PyROOT plotting. Provides a clean API to create styled graphs, histograms, functions, fits and canvases without boilerplate ROOT code.

---

## Requirements

```
Python >= 3.8
ROOT (PyROOT)
numpy
pandas
```

---

## Import

```python
from root_utils import *
```

All functions, color names, marker names and line style names are available directly in the namespace. Call `set_style()` once at the top of every script, before creating any ROOT object.

---

## 1. Style

### `set_style()`

Applies a publication-ready global ROOT style: Times New Roman font, no stat box, no title, tick marks on all sides, standard margins.

```python
set_style()
```

### `color(name)`

Resolves a color name to a ROOT integer. Integers pass through unchanged.

```python
color(name="blue")
color(name="dark_red")
color(name=ROOT.kGreen+2)   # integers pass through
```

Available names: `black`, `white`, `red`, `dark_red`, `light_red`, `blue`, `dark_blue`, `light_blue`, `cyan`, `green`, `dark_green`, `light_green`, `orange`, `yellow`, `magenta`, `violet`, `gray`, `dark_gray`.

### `line_style(style)`

Resolves a style name to a ROOT integer.

Available names: `solid`, `dashed`, `dotted`, `dash_dot`, `dash_dot_dot`, `long_dashed`, `long_dash_dot`, `long_dash_dot_dot`.

### `marker_style(style)`

Resolves a marker name to a ROOT integer.

Available names: `circle`, `square`, `triangle_up`, `triangle_down`, `star`, `diamond`, `open_circle`, `open_square`, `open_triangle_up`, `open_triangle_down`, `open_star`, `open_diamond`, `dot`, `plus`, `asterisk`, `cross`.

### `latex(text)`

Strips `$` signs from a string so both plain TLatex and LaTeX-style notation work transparently. All title and label strings in the library pass through this automatically.

```python
# Both are equivalent everywhere in the library
ylabel = "#frac{dN}{dp_{T}}"
ylabel = "$\\frac{dN}{dp_{T}}$"
```

Common TLatex: `#mu`, `#sigma`, `#chi`, `#pi`, `#sqrt{x}`, `#frac{a}{b}`, `p_{T}`, `x^{2}`.

---

## 2. Func

### `func()`

Creates a styled `TF1`.

```python
f = func(
    expression="gaus",
    range=(-5, 5),
    params=[1000, 0, 1],
    param_names=["N", "#mu", "#sigma"],
    title="",
    xlabel="x",
    ylabel="f(x)",
    color="red",
    line_style="solid",
    line_width=2,
    npx=1000,
)
```

### `func2d()`

Creates a styled `TF2`.

```python
f2 = func2d(
    expression="x*x + y*y",
    range_x=(-3, 3),
    range_y=(-3, 3),
    params=None,
    param_names=None,
    title="",
    xlabel="x",
    ylabel="y",
    zlabel="f(x,y)",
    color="red",
    line_style="solid",
    line_width=2,
    npx=1000,
    npy=1000,
)
```

### `func3d()`

Creates a styled `TF3` isosurface.

```python
f3 = func3d(
    expression="sin(x)*cos(y)*z",
    range_x=(-3, 3),
    range_y=(-3, 3),
    range_z=(-3, 3),
    params=None,
    param_names=None,
    title="",
    xlabel="x",
    ylabel="y",
    zlabel="z",
    color="red",
    fill_color=None,        # defaults to color
    fill_alpha=0.5,
    line_color=None,        # defaults to color
    line_style="solid",
    line_width=1,
    draw_mode="iso",        # iso | iso_fb | iso_bb | fb | bb | gl | gl_iso | gl_col | gl_box
    npx=30,
    npy=30,
    npz=30,
)
```

### `fit()`

Fits a graph or histogram. Accepts either a `TF1` or a ROOT expression string (in that case `range` is required). Returns the fitted `TF1`.

```python
f = fit(
    graph_or_hist=g,
    func_or_expr="gaus",        # or a TF1 object
    range=(-3, 3),              # required when passing a string
    params=[100, 0, 1],
    param_names=["N", "#mu", "#sigma"],
    options="QRS",
    print_results=True,
    units=[None, "GeV", "GeV"],
)
```

### `print_params()`

Prints chi2, NDF and all parameter values with errors to stdout.

```python
print_params(
    f=fitted_func,
    units=["", "GeV", "GeV"],
    precision=3,
)
```

---

## 3. Graph

### `graph()`

Creates a styled `TGraphErrors`. `ex`/`ey` default to zero if omitted.

```python
g = graph(
    x=x_array,
    y=y_array,
    ex=None,
    ey=ey_array,
    title="",
    xlabel="x",
    ylabel="y",
    color="light_blue",
    marker="square",
    marker_size=1.2,
    line_style="solid",
    line_width=2,
)
```

### `graph_asymm()`

Creates a styled `TGraphAsymmErrors` with independent low/high error bars.

```python
g = graph_asymm(
    x=x_array,
    y=y_array,
    exl=None,               # x low errors
    exh=None,               # x high errors
    eyl=eyl_array,
    eyh=eyh_array,
    title="",
    xlabel="x",
    ylabel="y",
    color="blue",
    marker="circle",
    marker_size=1.2,
    line_style="solid",
    line_width=2,
)
```

---

## 4. Hist

### `histogram()`

Creates and fills a `TH1D` from a numpy array.

```python
h = histogram(
    data=data_array,
    bins=50,
    range=(-5, 5),          # defaults to (data.min(), data.max())
    title="",
    xlabel="x",
    ylabel="Counts",
    color="blue",
    line_style="solid",
    line_width=2,
    fill=True,
    fill_alpha=0.3,
)
```

### `histogram2d()`

Creates and fills a `TH2D` from two numpy arrays. Palette defaults to `ROOT.kBird`.

```python
h2 = histogram2d(
    x=x_array,
    y=y_array,
    bins_x=40,
    bins_y=40,
    range_x=(-5, 5),        # defaults to (min, max)
    range_y=(-5, 5),
    title="",
    xlabel="x",
    ylabel="y",
    zlabel="Counts",
    palette=None,           # ROOT palette integer, default kBird
)
```

---

## 5. Maps

Build a 2D pixel map (`TH2D`) from column/row/value data, with automatic bin-edge computation.

### `map_from_arrays()`

```python
h = map_from_arrays(
    col=col_array,
    row=row_array,
    values=values_array,
    xlabel="x",
    ylabel="y",
    zlabel="Value",
    palette=None,
)
```

### `map_from_file()`

Reads column/row/value from a delimited text file (whitespace-separated by default).

```python
h = map_from_file(
    filepath="data.txt",
    col_col=0,              # column index (or name) for x
    col_row=1,              # column index (or name) for y
    col_val=2,              # column index (or name) for value
    sep=r"\s+",             # separator, use "," for CSV
    xlabel="col",
    ylabel="row",
    zlabel="Value",
    palette=None,
)
```

---

## 6. Draw

### `draw()`

Draws a list of ROOT objects on a new canvas. Returns `(canvas, legend)`.

```python
c, leg = draw(
    objects=[h, f],
    labels=["Signal", "Gaussian fit"],  # None = no legend
    xlabel="E [GeV]",
    ylabel="Counts",
    xrange=(0, 10),
    yrange=(0, 500),
    options="AP",               # ROOT draw option for graphs; auto-set for TH1/TH2
    width=900,
    height=600,
    log_x=False,
    log_y=False,
    # ── Grid ──────────────────────────────────────────────────────
    grid_x=False,               # vertical grid lines
    grid_y=False,               # horizontal grid lines
    grid_color="gray",
    grid_style="dashed",
    grid_width=1,
    # ── X axis ────────────────────────────────────────────────────
    x_title=None,               # overrides xlabel if set
    x_title_size=None,          # NDC, e.g. 0.05
    x_title_offset=None,        # distance axis–title
    x_title_color=None,
    x_label_size=None,
    x_label_color=None,
    x_label_offset=None,
    x_tick_length=None,
    x_ndivisions=None,          # e.g. 510 = 10 primary + 5 secondary
    x_invert=False,
    # ── Y axis ────────────────────────────────────────────────────
    y_title=None,
    y_title_size=None,
    y_title_offset=None,
    y_title_color=None,
    y_label_size=None,
    y_label_color=None,
    y_label_offset=None,
    y_tick_length=None,
    y_ndivisions=None,
    y_invert=False,
    # ── Legend ────────────────────────────────────────────────────
    legend_pos="top_right",     # top_right | top_left | bottom_right | bottom_left | top_center | (x1,y1,x2,y2)
    legend_width=0.25,
    legend_row_height=0.045,
    legend_ncols=1,
    legend_text_size=0.038,
    legend_margin=0.25,
    legend_border=1,
    legend_fill_alpha=1.0,      # 0.0 = transparent background
    # ── Histogram stats in legend ─────────────────────────────────
    hist_stats=False,
    hist_stats_precision=3,
    hist_stats_show_mean=True,
    hist_stats_show_std=True,
    hist_stats_show_counts=True,
    hist_stats_mean_label="Mean",
    hist_stats_std_label="Std Dev",
    hist_stats_counts_label="Counts",
    # ── Fit stats in legend ───────────────────────────────────────
    fit_stats=True,             # shown only for TF1 with NDF > 0
    fit_stats_precision=2,
    fit_stats_show_chi2=True,
    fit_stats_show_params=True,
    fit_stats_show_errors=True,
    fit_stats_chi2_label="#chi^{2} / NDF",
    fit_stats_param_names=None, # override parameter names in legend
    fit_stats_units=None,       # e.g. [None, "GeV", "GeV"]
    # ── Output ────────────────────────────────────────────────────
    save=None,                  # e.g. "plot.pdf" or "plot.png"
)
```

> **`fit_stats`:** statistics are appended to the legend only for `TF1` objects with `NDF > 0`, i.e. that have actually been fitted. Unfitted functions are silently skipped even if `fit_stats=True`.

### `make_legend()`

Creates a `TLegend` independently from `draw`, useful for multi-pad canvases.

```python
leg = make_legend(
    objects=[g1, g2, f],
    labels=["Run A", "Run B", "Fit"],
    pos="top_right",
    ncols=1,
    text_size=0.038,
    width=0.25,
    row_height=0.045,
    margin=0.30,
    border=1,
    fill_alpha=1.0,
)
```

---

## I/O

All functions read delimited text files. Default separator is whitespace; pass `sep=","` for CSV.

```python
x      = load_column(filepath="data.txt",  column=0)           # by index
x      = load_column(filepath="data.txt",  column="energy")     # by header name
x, y   = load_columns(filepath="data.txt", columns=[0, 1])
row    = load_row(filepath="data.txt",     row=0)
rows   = load_rows(filepath="data.txt",    rows=[0, 1, 2])
```

---

## ROOT macros

```python
run_macro(path="my_macro.C")                 # interpreted
run_macro(path="my_macro.C+",  100, 200)     # compiled, with arguments
run_macro(path="my_macro.C++")               # force recompile
```

---

## Full example

```python
from root_utils import *
import numpy as np

set_style()

rng  = np.random.default_rng(42)
data = rng.normal(loc=2.0, scale=0.5, size=2000)

h = histogram(
    data=data,
    bins=60,
    range=(0, 4),
    xlabel="E [GeV]",
    ylabel="Counts",
    color="light_blue",
    fill=True,
    fill_alpha=0.4,
)

f = func(
    expression="gaus",
    range=(0, 4),
    params=[200, 2.0, 0.5],
    param_names=["N", "#mu", "#sigma"],
    color="red",
    line_width=2,
)

fit(graph_or_hist=h, func_or_expr=f, options="QRS")

c, leg = draw(
    objects=[h, f],
    labels=["MC signal", "Gaussian fit"],
    xlabel="E [GeV]",
    ylabel="Counts / 0.067 GeV",
    grid_y=True,
    legend_pos="top_right",
    fit_stats=True,
    fit_stats_units=[None, "GeV", "GeV"],
    save="signal.pdf",
)
```
