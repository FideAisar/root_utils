# root_utils

High-level PyROOT plotting utilities for physics data analysis (vibe-coded).

`root_utils` wraps the ROOT C++ library with a clean Python API.  The goal is to
eliminate boilerplate: one import, one style call, then work directly with numpy
arrays and human-readable names for colors, markers, and line styles.

### Requirements
- Python ≥ 3.10
- ROOT (with PyROOT enabled)
- numpy
- pandas


### Setup
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
# filled: "circle"  "square"  "triangle_up"  "triangle_down"  "star"  "diamond"
# open:   "open_circle"  "open_square"  "open_triangle_up"  "open_triangle_down"  "open_star"  "open_diamond"
# simple: "dot"  "plus"  "asterisk"  "cross"
```

### TLatex · `latex(text)`
Pass-through that strips `$` characters — copy-paste LaTeX-wrapped TLatex strings safely.
```python
latex("#mu #pm #sigma")       # '#mu #pm #sigma'
latex("p_{T} [GeV/c^{2}]")   # 'p_{T} [GeV/c^{2}]'
```

---

## Graphs
### `graph()` → `TGraphErrors`
```python
g = graph(x = np.ndarray,
          y = np.ndarray,
          ex = np.ndarray = None,
          ey =  np.ndarray = None,
          title =  "",
          xlabel = "x",
          ylabel = "y",
          color = "blue",
          marker = "circle",
          marker_size = 1.2,
          line_style  = "solid",
          line_width = 2,
         )
```

### `graph_asymm()` → `TGraphAsymmErrors`
Same parameters as `graph()` but with independent low/high error bars.
```python
ga = graph_asymm(x = np.ndarray,
                 y = np.ndarray,
                 exl = np.ndarray,
                 exh = np.ndarray,
                 eyl = np.ndarray,
                 eyh = np.ndarray,
                 title= "",
                 xlabel = "x",
                 ylabel= "y",
                 color = "blue",
                 marker = "circle",
                 marker_size = 1.2,
                 line_style = "solid",
                 line_width = 2,
                ) 
```

## Functions (TF1 / TF2 / TF3)
### `func()` → `TF1`
```python
f =  func(expression = "",
          xmin = 1.0,
          xmax = 2.0,
          params = [],
          param_names = [],
          title = "",
          xlabel = "x",
          ylabel = "f(x)",
          color = "red",
          line_style = "solid",
          line_width = 2,
          npx = 1000,
         )
```

### `func2d()` → `TF2`
```python
f2 = func2d(expression = "",
            xmin = 1.0,
            xmax = 2.0,
            ymin = 1.0,
            ymax = 2.0,
            params = [],
            param_names = [],
            title = "",
            xlabel = "x",
            ylabel = "y",
            zlabel = "f(x,y)",
            color = "red",
            line_style = "solid",
            line_width = 2,
            npx = 1000,
            npy = 1000,
           ) 
```

### `func3d()` → `TF3`
```python
f3 = func3d(expression = "",
            xmin = 1.0,
            xmax = 2.0,
            ymin = 1.0,
            ymax = 2.0,
            zmin = 1.0,
            zmax = 2.0,
            params = [],
            param_names = [],
            title = "",
            xlabel = "x",
            ylabel = "y",
            zlabel = "z",

            # ── surface appearance 
            color = "red",
            fill_color = None,
            fill_alpha = 0.5,
            line_color = None,
            line_style = "solid",
            line_width = 1,

            # ── draw mode ("iso, "gl", "gl_iso", "gl_col", "gl_box", "fb", "bb")
            draw_mode = "iso",

            # ── sampling resolution 
            npx = 30,
            npy = 30,
            npz = 30
           ) 
```

---

## Histograms
### `histogram()` → `TH1D`
```python
h = histogram(data = np.ndarray,
              bins = 50,
              range = [1.0,5.0],
              title = "",
              xlabel = "x",
              ylabel = "Counts",
              color = "blue",
              line_style = "solid",
              line_width = 2,
              fill = True,
              fill_alpha = 0.3,
             ) 
```

### `histogram2d()` → `TH2D`
```python
h2 =  histogram2d(x = np.ndarray,
                  y = np.ndarray,
                  bins_x = 40,
                  bins_y = 40,
                  range_x = [1.0,5.0],
                  range_y = [1.0,5.0],
                  title = "",
                  xlabel = "x",
                  ylabel = "y",
                  zlabel = "Counts",
                  palette = 1, # todo: explicit names for palette
                 ) 
```

### `map_from_arrays()` → `TH2D`
Build a pixel/detector map from three equal-length arrays. Bin edges computed automatically from unique coordinate values.
```python
m =  map_from_arrays(col = x,
                     row = y,
                     values = z,
                     xlabel = "x",
                     ylabel = "y",
                     zlabel = "Value",
                     palette = None,
                    )
```

### `map_from_file()` → `TH2D`
Convenience wrapper — reads col/row/value arrays from a delimited file and calls `map_from_arrays`.
```python
m = map_from_file(
    filepath = "",
    col_col = 0, # also header of column as string
    col_row = 1, # also header of column as string
    col_val = 2, # also header of column as string
    sep = r"\s+",
    xlabel = "x",
    ylabel = "y",
    zlabel = "Value",
    palette = None,
) 
```

## Fitting
### `fit()` → `TF1`
```python
gf_fit = fit(graph = g, 
             func = f,
             xmin = 1.0,
             xmax = 2.0,
             params = [],
             param_names = [],
             options = "RS",
             print_results = True,
             units = None,
            )
  
hf_fit = fit(hist = h, 
             func = f,
             xmin = 1.0,
             xmax = 2.0,
             params = [],
             param_names = [],
             options = "RS",
             print_results = True,
             units = None,
            )
```

### `print_params(f, units, precision)`
Print a formatted parameter table for any fitted `TF1`.

---

## Drawing
### `draw()` → `(TCanvas, TLegend)`

```python
c, leg = draw(objects = [h,f,g,...],
              labels = [],
              xlabel = None,
              ylabel = None,
              xrange = [1.0,5.0],
              yrange = [1.0,5.0],
              options = ["HIST", "dotted", "AP",...],
              width = 900,
              height = 600,
              log_x = False,
              log_y = False,

              # ── legend ──── accept "top_right", "top_left", "bottom_right", "bottom_left", "top_center" and coord.
              legend_pos = "top_right", 
              legend_width = 0.25,
              legend_row_height = 0.045,
              legend_ncols = 1,
              legend_text_size = 0.038,
              legend_margin = 0.25,
              legend_border = 0,
              legend_fill_alpha = 0.0,

              # ── stats 
              hist_stats = False,
              hist_stats_precision = 3,
              hist_stats_show_mean = True,
              hist_stats_show_std = True,
              hist_stats_show_counts = True,
              hist_stats_mean_label = "Mean",
              hist_stats_std_label = "Std Dev",
              hist_stats_counts_label = "Counts",
              fit_stats = False,
              fit_stats_precision = 3,
              fit_stats_show_chi2 = True,
              fit_stats_show_params = True,
              fit_stats_show_errors = True,
              fit_stats_chi2_label = "#chi^{2} / NDF",
              fit_stats_param_names = [],
              fit_stats_units = [],
              save = "canvas.pdf",
             )
```

### `make_legend()` → `TLegend`
Lower-level helper for legends outside a `draw()` call.
```python
leg = make_legend(objects = [h,f,g,...],
                  labels = [],
                  pos = "top_right",
                  ncols = 1,
                  text_size = 0.038,
                  width = 0.25,
                  row_height = 0.045,
                  margin = 0.30,
                  border = 0,
                  fill_alpha = 0.0,
                 ) 
```

## I/O
```python
load_column(filepath, column, sep)          # → np.ndarray
load_columns(filepath, [col1, col2, ...])   # → list[np.ndarray]
load_row(filepath, row, sep)                # → np.ndarray
load_rows(filepath, [row1, row2, ...])      # → list[np.ndarray]
```

`column` / `row` accept zero-based integer indices or string column names. Default separator: whitespace.








