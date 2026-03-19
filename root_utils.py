"""
root_utils.py — Pythonic wrappers for PyROOT plotting.

All text fields accept ROOT TLatex syntax (#mu, #sigma, p_{T}, x^{2}, etc.).
Call set_style() once at the top of your script before creating any objects.
"""

import os
import sys

# ── Silence ROOT warnings and info messages ───────────────────────────────────
# Redirect stderr to /dev/null during ROOT import to suppress banner and warnings
_stderr_fd = sys.stderr.fileno()
_devnull = os.open(os.devnull, os.O_WRONLY)
_old_stderr = os.dup(_stderr_fd)
os.dup2(_devnull, _stderr_fd)
os.close(_devnull)

import ROOT

os.dup2(_old_stderr, _stderr_fd)
os.close(_old_stderr)

# Suppress ROOT runtime error/warning messages (kPrint=0, kInfo=1000, kWarning=2000, kError=3000)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")

import numpy as np
import pandas as pd


# ── Colors ────────────────────────────────────────────────────────────────────

_COLORS = {
    "black": ROOT.kBlack, "white": ROOT.kWhite,
    "red": ROOT.kRed, "dark_red": ROOT.kRed+2, "light_red": ROOT.kRed-7,
    "blue": ROOT.kBlue, "dark_blue": ROOT.kBlue+2, "light_blue": ROOT.kBlue-7,
    "cyan": ROOT.kCyan+1, "green": ROOT.kGreen+2, "dark_green": ROOT.kGreen+3,
    "light_green": ROOT.kGreen-3, "orange": ROOT.kOrange+7,
    "yellow": ROOT.kYellow+1, "magenta": ROOT.kMagenta, "violet": ROOT.kViolet,
    "gray": ROOT.kGray+1, "dark_gray": ROOT.kGray+2,
}

def color(name):
    if isinstance(name, int):
        return name
    key = name.lower().replace(" ", "_")
    if key not in _COLORS:
        raise ValueError(f"Unknown color '{name}'. Available: {list(_COLORS)}")
    return _COLORS[key]


# ── Line styles ───────────────────────────────────────────────────────────────

_LINE_STYLES = {
    "solid": 1, "dashed": 2, "dash": 2, "dotted": 3, "dot": 3,
    "dash_dot": 4, "dashdot": 4, "dot_dash": 4, "dotdash": 4,
    "dash_dot_dot": 5, "long_dashed": 6, "long_dash_dot": 7, "long_dash_dot_dot": 8,
}

def line_style(style):
    if isinstance(style, int):
        return style
    key = style.lower().replace(" ", "_").replace("-", "_")
    if key not in _LINE_STYLES:
        raise ValueError(f"Unknown line style '{style}'. Available: {list(_LINE_STYLES)}")
    return _LINE_STYLES[key]


# ── Marker styles ─────────────────────────────────────────────────────────────

_MARKERS = {
    "circle": 20, "full_circle": 20, "square": 21, "full_square": 21,
    "triangle_up": 22, "triangle": 22, "full_triangle": 22, "triangle_down": 23,
    "star": 29, "full_star": 29, "diamond": 33, "full_diamond": 33,
    "cross_circle": 34, "open_circle": 24, "open_square": 25,
    "open_triangle_up": 26, "open_triangle": 26, "open_triangle_down": 32,
    "open_star": 30, "open_diamond": 27,
    "dot": 1, "plus": 2, "asterisk": 3, "cross": 5, "x": 5,
    "tiny_dot": 6, "small_dot": 7,
}

def marker_style(style):
    if isinstance(style, int):
        return style
    key = style.lower().replace(" ", "_").replace("-", "_")
    if key not in _MARKERS:
        raise ValueError(f"Unknown marker style '{style}'. Available: {list(_MARKERS)}")
    return _MARKERS[key]


# ── Text ──────────────────────────────────────────────────────────────────────

def latex(text):
    """Strip $ signs; everything else passes through unchanged."""
    return text.replace("$", "")


# ── Style ─────────────────────────────────────────────────────────────────────

def set_style():
    """Apply clean, publication-ready ROOT global style (Times font, no stat box)."""
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    font = 132  # Times New Roman
    for axis in ("X", "Y", "Z"):
        ROOT.gStyle.SetLabelFont(font, axis)
        ROOT.gStyle.SetTitleFont(font, axis)
        ROOT.gStyle.SetLabelSize(0.045, axis)
        ROOT.gStyle.SetTitleSize(0.050, axis)
        ROOT.gStyle.SetTitleOffset(1.2, axis)
        ROOT.gStyle.SetNdivisions(510, axis)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetPadColor(0)
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasBorderMode(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetPadLeftMargin(0.15)
    ROOT.gStyle.SetPadBottomMargin(0.15)
    ROOT.gStyle.SetPadRightMargin(0.05)
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetLegendBorderSize(1)
    ROOT.gStyle.SetLegendFillColor(ROOT.kWhite)
    ROOT.gStyle.SetLegendFont(font)
    ROOT.gStyle.SetLegendTextSize(0.04)


# ── Macro execution ───────────────────────────────────────────────────────────

def run_macro(path, *args):
    """
    Execute a ROOT macro (.C file) via gROOT.

    Parameters
    ----------
    path : str
        Path to the .C macro file (e.g. "my_macro.C").
    *args : str or numeric
        Optional arguments forwarded to the macro entry point.
        They are stringified and passed as: MyMacro(arg0, arg1, ...).

    Returns
    -------
    int
        Return value of ROOT.gROOT.ProcessLine (0 on success).

    Examples
    --------
    run_macro("draw_signal.C")                     # no arguments
    run_macro("fit_peak.C", 100, 200)              # with arguments
    run_macro("my_macro.C+")                       # compiled mode (+)
    run_macro("my_macro.C++")                      # force recompile (++)
    """
    path = str(path)

    # Separate compilation flags (+/++) from the filename
    flags = ""
    if path.endswith("++"):
        flags = "++"
        path = path[:-2]
    elif path.endswith("+"):
        flags = "+"
        path = path[:-1]

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Macro not found: '{path}'")

    if args:
        # Build "path+flags(arg0, arg1, ...)"
        arg_str = ", ".join(
            f'"{a}"' if isinstance(a, str) else str(a) for a in args
        )
        cmd = f'.x {path}{flags}({arg_str})'
    else:
        cmd = f'.x {path}{flags}'

    ret = ROOT.gROOT.ProcessLine(cmd)
    return ret


# ── Internal helpers ──────────────────────────────────────────────────────────

def _title(title, xlabel, ylabel, zlabel=None):
    parts = [latex(title), latex(xlabel), latex(ylabel)]
    if zlabel is not None:
        parts.append(latex(zlabel))
    return ";".join(parts)

def _apply_line(obj, c, ls, lw):
    obj.SetLineColor(c); obj.SetLineStyle(ls); obj.SetLineWidth(lw)

def _apply_marker(obj, c, mkr, ms):
    obj.SetMarkerColor(c); obj.SetMarkerStyle(mkr); obj.SetMarkerSize(ms)

def _uid():
    return np.random.randint(100_000)


# ── Graphs ────────────────────────────────────────────────────────────────────

def graph(x, y, ex=None, ey=None, 
          title="", 
          xlabel="x", 
          ylabel="y",
          color="light_blue", 
          marker="square", 
          marker_size=1.2,
          line_style="solid", 
          line_width=2):
    
    """Create a styled TGraphErrors. ex/ey default to zero."""
    n = len(x)
    _ex = np.zeros(n) if ex is None else np.asarray(ex, float)
    _ey = np.zeros(n) if ey is None else np.asarray(ey, float)
    
    g = ROOT.TGraphErrors(n, np.asarray(x, float), np.asarray(y, float), _ex, _ey)
    g.SetTitle(_title(title, xlabel, ylabel))
    
    _apply_marker(g, globals()["color"](color), globals()["marker_style"](marker), marker_size)
    _apply_line(g, globals()["color"](color), globals()["line_style"](line_style), line_width)
    return g


def graph_asymm(x, y, exl=None, exh=None, eyl=None, eyh=None,
                title="", xlabel="x", ylabel="y",
                color="blue", marker="circle", marker_size=1.2,
                line_style="solid", line_width=2):
    
    """Create a styled TGraphAsymmErrors with independent low/high error bars."""
    n = len(x)
    z = np.zeros(n)
    
    g = ROOT.TGraphAsymmErrors(
        n, np.asarray(x, float), np.asarray(y, float),
        z if exl is None else np.asarray(exl, float),
        z if exh is None else np.asarray(exh, float),
        z if eyl is None else np.asarray(eyl, float),
        z if eyh is None else np.asarray(eyh, float),
    )
    g.SetTitle(_title(title, xlabel, ylabel))
    
    _apply_marker(g, globals()["color"](color), globals()["marker_style"](marker), marker_size)
    _apply_line(g, globals()["color"](color), globals()["line_style"](line_style), line_width)
    return g


# ── Functions ─────────────────────────────────────────────────────────────────

def _set_params(f, params, param_names):
    if params:
        for i, v in enumerate(params): f.SetParameter(i, v)
    if param_names:
        for i, n in enumerate(param_names):
            if i < f.GetNpar(): f.SetParName(i, latex(n))

def func(expression, range, params=None, param_names=None,
         title="", xlabel="x", ylabel="f(x)",
         color="red", line_style="solid", line_width=2, npx=1000):
    
    """Create a styled TF1."""
    f = ROOT.TF1(f"f_{_uid()}", expression, *range)
    f.SetTitle(_title(title, xlabel, ylabel))
    
    _apply_line(f, globals()["color"](color), globals()["line_style"](line_style), line_width)
    f.SetNpx(npx)
    _set_params(f, params, param_names)
    return f


def func2d(expression, range_x, range_y, params=None, param_names=None,
           title="", xlabel="x", ylabel="y", zlabel="f(x,y)",
           color="red", line_style="solid", line_width=2, npx=1000, npy=1000):
    
    """Create a styled TF2."""
    f = ROOT.TF2(f"f2d_{_uid()}", expression, *range_x, *range_y)
    f.SetTitle(_title(title, xlabel, ylabel, zlabel))
    
    _apply_line(f, globals()["color"](color), globals()["line_style"](line_style), line_width)
    f.SetNpx(npx); f.SetNpy(npy)
    _set_params(f, params, param_names)
    return f

_TF3_DRAW_MODES = {
    "iso": "ISO", "iso_fb": "ISOFB", "iso_bb": "ISOBB",
    "fb": "FB", "bb": "BB", "tf3": "TF3",
    "gl": "GL", "gl_iso": "GLISO", "gl_col": "GLCOL", "gl_box": "GLBOX",
}

def func3d(expression, range_x, range_y, range_z,
           params=None, param_names=None,
           title="", xlabel="x", ylabel="y", zlabel="z",
           color="red", fill_color=None, fill_alpha=0.5,
           line_color=None, line_style="solid", line_width=1,
           draw_mode="iso", npx=30, npy=30, npz=30):
    
    """Create a styled TF3 isosurface."""
    if draw_mode not in _TF3_DRAW_MODES:
        raise ValueError(f"Unknown draw_mode '{draw_mode}'. Available: {list(_TF3_DRAW_MODES)}")

    base = globals()["color"](color)
    fc = globals()["color"](fill_color) if fill_color is not None else base
    lc = globals()["color"](line_color) if line_color is not None else base
    f = ROOT.TF3(f"f3d_{_uid()}", expression, *range_x, *range_y, *range_z)
    f.SetTitle(_title(title, xlabel, ylabel, zlabel))
    f.SetFillColor(fc) if fill_alpha >= 1.0 else f.SetFillColorAlpha(fc, max(0.0, fill_alpha))
    _apply_line(f, lc, globals()["line_style"](line_style), line_width)
    f.SetNpx(npx); f.SetNpy(npy); f.SetNpz(npz)
    f._draw_mode = _TF3_DRAW_MODES[draw_mode]
    _set_params(f, params, param_names)
    return f


# ── Fitting ───────────────────────────────────────────────────────────────────

def fit(graph_or_hist, 
        func_or_expr, 
        range=None, 
        params=None, param_names=None,
        options="QRS", 
        print_results=True, 
        units=None):
    
    """Fit a histogram or graph; optionally print a parameter table."""
    if isinstance(func_or_expr, str):
        if range is None:
            raise ValueError("range is required when fitting with a string expression.")
        f = globals()["func"](func_or_expr, range=range, params=params, param_names=param_names)
    else:
        f = func_or_expr
        
    graph_or_hist.Fit(f, options)
    if print_results:
        print_params(f, units=units)
    return f


def print_params(f, units=None, precision=3):
    """Print fitted TF1 parameters and chi2/NDF to stdout."""
    fmt = f"{{:.{precision}f}}"
    ndf = f.GetNDF()
    chi2 = f.GetChisquare()
    chi2_over_ndf = (chi2 / ndf) if ndf > 0 else float("nan")

    print("\n" + "=" * 50 + "\nFIT PARAMETERS\n" + "=" * 50)
    print(f"  chi2         = {fmt.format(chi2)}")
    print(f"  NDF          = {ndf}")
    print(f"  chi2 / NDF   = {fmt.format(chi2_over_ndf)}")
    print("-" * 50)
    for i in range(f.GetNpar()):
        unit = f" [{units[i]}]" if units and i < len(units) else ""
        print(f"  {f.GetParName(i)}{unit} = {fmt.format(f.GetParameter(i))} "
              f"+/- {fmt.format(f.GetParError(i))}")
    print("=" * 50 + "\n")


# ── Histograms ────────────────────────────────────────────────────────────────

def histogram(data, bins=50, range=None, title="", xlabel="x", ylabel="Counts",
              color="blue", line_style="solid", line_width=2,
              fill=True, fill_alpha=0.3):
    
    """Create and fill a TH1D from a numpy array."""
    data = np.asarray(data, float)
    xmin, xmax = (range[0], range[1]) if range else (data.min(), data.max())
    
    h = ROOT.TH1D(f"h1_{_uid()}", _title(title, xlabel, ylabel), bins, xmin, xmax)
    h.FillN(len(data), data, np.ones(len(data)))
    _apply_line(h, globals()["color"](color), globals()["line_style"](line_style), line_width)
    h.SetStats(0)
    if fill:
        h.SetFillColorAlpha(globals()["color"](color), fill_alpha)
    return h


def histogram2d(x, y, bins_x=40, bins_y=40, range_x=None, range_y=None,
                title="", xlabel="x", ylabel="y", zlabel="Counts", palette=None):
    
    """Create and fill a TH2D from two numpy arrays."""
    xmin = range_x[0] if range_x else float(np.min(x))
    xmax = range_x[1] if range_x else float(np.max(x))
    ymin = range_y[0] if range_y else float(np.min(y))
    ymax = range_y[1] if range_y else float(np.max(y))
    
    h = ROOT.TH2D(f"h2_{_uid()}", _title(title, xlabel, ylabel, zlabel),
                  bins_x, xmin, xmax, bins_y, ymin, ymax)
    for xi, yi in zip(x, y):
        h.Fill(xi, yi)
    ROOT.gStyle.SetPalette(palette if palette is not None else ROOT.kBird)
    return h


# ── Legend stats helpers ──────────────────────────────────────────────────────

def _dummy_box():
    b = ROOT.TBox(0, 0, 0, 0); 
    b.SetFillStyle(0); 
    b.SetLineStyle(0); 
    return b

def hist_stats_entries(h, show_mean=True, show_std=True, show_counts=True,
                       precision=3, mean_label="Mean", std_label="Std Dev",
                       counts_label="Counts"):
    
    """Return legend entries with histogram statistics (mean, std dev, counts)."""
    fmt = f"{{:.{precision}f}}"
    entries = []
    if show_mean:   entries.append((_dummy_box(), f"{mean_label} = {fmt.format(h.GetMean())}", ""))
    if show_std:    entries.append((_dummy_box(), f"{std_label} = {fmt.format(h.GetStdDev())}", ""))
    if show_counts: entries.append((_dummy_box(), f"{counts_label} = {int(h.GetEntries())}", ""))
    return entries


def fit_stats_entries(f, show_chi2=True, show_params=True, show_errors=True,
                      precision=3, chi2_label="#chi^{2} / NDF",
                      param_names_override=None, units=None):
    
    """Return legend entries with fit results (chi2, parameters, errors)."""
    fmt = f"{{:.{precision}f}}"
    entries = []
    
    if show_chi2:
        ndf = f.GetNDF()
        entries.append((_dummy_box(), f"{chi2_label} = {fmt.format(f.GetChisquare())} / {ndf}", ""))
    if show_params:
        for i in range(f.GetNpar()):
            name = (latex(param_names_override[i])
                    if param_names_override and i < len(param_names_override)
                    else f.GetParName(i))
            unit = f" [{units[i]}]" if units and i < len(units) else ""
            val_str = f"{fmt.format(f.GetParameter(i))}"
            if show_errors:
                val_str += f" #pm {fmt.format(f.GetParError(i))}"
            entries.append((_dummy_box(), f"{name}{unit} = {val_str}", ""))
    return entries


# ── Legend ────────────────────────────────────────────────────────────────────

_LEGEND_ANCHORS = {
    "top_right":    (0.92, 0.92, "TR"),
    "top_left":     (0.20, 0.92, "TL"),
    "bottom_right": (0.92, 0.15, "BR"),
    "bottom_left":  (0.15, 0.15, "BL"),
    "top_center":   (0.535, 0.92, "TC"),
}

def _legend_option(obj):
    if isinstance(obj, ROOT.TF1): return "l"
    if isinstance(obj, ROOT.TH1): return "lf"
    return "lep"

def _legend_coords(pos, total_w, total_h):
    if isinstance(pos, tuple):
        return pos
    if pos not in _LEGEND_ANCHORS:
        raise ValueError(f"Unknown legend position '{pos}'")
    
    ax, ay, corner = _LEGEND_ANCHORS[pos]
    y2 = ay if "T" in corner else ay + total_h
    y1 = y2 - total_h
    
    if "R" in corner:   x2, x1 = ax, ax - total_w
    elif "L" in corner: x1, x2 = ax, ax + total_w
    else:               x1, x2 = ax - total_w/2, ax + total_w/2
    return x1, y1, x2, y2

def make_legend(objects, labels, pos="top_right", ncols=1, text_size=0.038,
                width=0.25, row_height=0.045, margin=0.30,
                border=1, fill_alpha=1.0):
    
    """Create a TLegend from a list of ROOT objects and labels."""
    n_rows = int(np.ceil(len(objects) / ncols))
    x1, y1, x2, y2 = _legend_coords(pos, width, n_rows * row_height)
    
    leg = ROOT.TLegend(x1, y1, x2, y2)
    leg.SetNColumns(ncols); leg.SetTextSize(text_size); leg.SetMargin(margin)
    leg.SetBorderSize(border)
    leg.SetFillStyle(0 if fill_alpha == 0.0 else 1001)
    
    if fill_alpha > 0: leg.SetFillColorAlpha(ROOT.kWhite, fill_alpha)
    for obj, label in zip(objects, labels):
        leg.AddEntry(obj, label, _legend_option(obj))
    return leg


# ── Drawing ───────────────────────────────────────────────────────────────────

_LINE_STYLE_NAMES = frozenset(_LINE_STYLES)

def _auto_draw_option(obj, first, base):
    if isinstance(obj, ROOT.TF3):
        mode = getattr(obj, "_draw_mode", "ISO")
        return mode if first else f"{mode} SAME"
    if isinstance(obj, ROOT.TF1):
        return "" if first else "SAME"
    if isinstance(obj, (ROOT.TH1D, ROOT.TH1F)):
        return "HIST" if first else "HIST SAME"
    if isinstance(obj, (ROOT.TH2D, ROOT.TH2F)):
        return "COLZ"
    return base if first else base.replace("A", "") + " SAME"

def _resolve_draw_option(obj, per_item, first, base):
    if per_item is None:
        return _auto_draw_option(obj, first, base)
    key = per_item.strip().lower().replace(" ", "_").replace("-", "_")
    if key in _LINE_STYLE_NAMES:
        obj.SetLineStyle(_LINE_STYLES[key])
        return _auto_draw_option(obj, first, base)
    opt = per_item.strip()
    if not first and "SAME" not in opt.upper():
        opt = (opt.replace("A", "").replace("a", "").strip() + " SAME").strip()
    return opt


def draw(objects, 
         labels=None, xlabel=None, ylabel=None,
         xrange=None, yrange=None, options="AP",
         width=900, height=600, 
         log_x=False, log_y=False,
         legend_pos="top_right", 
         legend_width=0.25, 
         legend_row_height=0.045,
         legend_ncols=1, 
         legend_text_size=0.038, 
         legend_margin=0.25,
         legend_border=1, 
         legend_fill_alpha=1.0,
         hist_stats=False, 
         hist_stats_precision=3,
         hist_stats_show_mean=True, 
         hist_stats_show_std=True,
         hist_stats_show_counts=True,
         hist_stats_mean_label="Mean", 
         hist_stats_std_label="Std Dev",
         hist_stats_counts_label="Counts",
         fit_stats=True, fit_stats_precision=2,
         fit_stats_show_chi2=True, 
         fit_stats_show_params=True,
         fit_stats_show_errors=True,
         fit_stats_chi2_label="#chi^{2} / NDF",
         fit_stats_param_names=None, fit_stats_units=None,
         save=None):
    
    """Draw ROOT objects on a canvas with optional legend, stats, and file save."""
    canvas = ROOT.TCanvas(f"c_{_uid()}", "", width, height)
    if log_x: canvas.SetLogx()
    if log_y: canvas.SetLogy()

    if isinstance(options, list):
        global_base = "AP"
        per_obj_opts = list(options) + [None] * (len(objects) - len(options))
    else:
        global_base = options
        per_obj_opts = [None] * len(objects)

    first_idx = next((i for i, o in enumerate(objects) if not isinstance(o, ROOT.TF1)), None)
    draw_order = (
        [first_idx] + [i for i in range(len(objects)) if i != first_idx]
        if first_idx is not None else list(range(len(objects)))
    )
    for pos, i in enumerate(draw_order):
        obj = objects[i]
        opt = _resolve_draw_option(obj, per_obj_opts[i], pos == 0, global_base)
        obj.Draw(opt)

    primary = objects[first_idx] if first_idx is not None else objects[0]
    if xlabel: primary.GetXaxis().SetTitle(latex(xlabel))
    if ylabel: primary.GetYaxis().SetTitle(latex(ylabel))
    if xrange: primary.GetXaxis().SetRangeUser(*xrange)
    if yrange: primary.GetYaxis().SetRangeUser(*yrange)

    legend = None
    if labels:
        stat_map = {}
        n_stat_rows = 0

        if hist_stats:
            for obj in objects:
                if isinstance(obj, ROOT.TH1):
                    entries = hist_stats_entries(obj,
                        show_mean=hist_stats_show_mean,
                        show_std=hist_stats_show_std,
                        show_counts=hist_stats_show_counts,
                        precision=hist_stats_precision,
                        mean_label=hist_stats_mean_label,
                        std_label=hist_stats_std_label,
                        counts_label=hist_stats_counts_label)
                    stat_map[id(obj)] = entries
                    n_stat_rows += len(entries)

        if fit_stats:
            for obj in objects:
                if isinstance(obj, ROOT.TF1):
                    entries = fit_stats_entries(obj,
                        show_chi2=fit_stats_show_chi2,
                        show_params=fit_stats_show_params,
                        show_errors=fit_stats_show_errors,
                        precision=fit_stats_precision,
                        chi2_label=fit_stats_chi2_label,
                        param_names_override=fit_stats_param_names,
                        units=fit_stats_units)
                    stat_map[id(obj)] = entries
                    n_stat_rows += len(entries)

        n_rows = int(np.ceil((len(objects) + n_stat_rows) / legend_ncols))
        x1, y1, x2, y2 = _legend_coords(legend_pos, legend_width, n_rows * legend_row_height)
        
        legend = ROOT.TLegend(x1, y1, x2, y2)
        legend.SetNColumns(legend_ncols)
        legend.SetTextSize(legend_text_size)
        legend.SetMargin(legend_margin)
        legend.SetBorderSize(legend_border)
        legend.SetFillStyle(0 if legend_fill_alpha == 0.0 else 1001)
        
        if legend_fill_alpha > 0:
            legend.SetFillColorAlpha(ROOT.kWhite, legend_fill_alpha)

        for obj, label in zip(objects, [latex(l) for l in labels]):
            legend.AddEntry(obj, label, _legend_option(obj))
            for dummy, lbl, opt in stat_map.get(id(obj), []):
                legend.AddEntry(dummy, lbl, opt)
        legend.Draw()

    canvas.Update()
    if save:
        canvas.SaveAs(save)
        print(f"[draw] Saved: {save}")
    return canvas, legend


# ── I/O ───────────────────────────────────────────────────────────────────────

def _read_csv(filepath, sep=r"\s+"):
    return pd.read_csv(filepath, sep=sep, engine="python")

def load_column(filepath, column, sep=r"\s+"):
    """Load a single column from a delimited text file."""
    df = _read_csv(filepath, sep)
    return df.iloc[:, column].to_numpy() if isinstance(column, int) else df[column].to_numpy()

def load_columns(filepath, columns, sep=r"\s+"):
    """Load multiple columns from a delimited text file."""
    return [load_column(filepath, c, sep) for c in columns]

def load_row(filepath, row=0, sep=r"\s+"):
    """Load a single row from a delimited text file."""
    with open(filepath) as fh:
        lines = [l.rstrip("\n") for l in fh if l.strip()]
    if len(lines) == 1:
        return np.array(lines[0].split(), dtype=float)
    return _read_csv(filepath, sep).iloc[row].to_numpy(dtype=float)

def load_rows(filepath, rows, sep=r"\s+"):
    """Load multiple rows from a delimited text file."""
    df = pd.read_csv(filepath, sep=sep, engine="python", header=None)
    return [df.iloc[r].to_numpy(dtype=float) for r in rows]


# ── 2D maps ───────────────────────────────────────────────────────────────────

def map_from_arrays(col, row, values, xlabel="x", ylabel="y",
                    zlabel="Value", palette=None):
    """Build a TH2D pixel map from (col, row, value) arrays."""
    col, row, values = map(lambda a: np.asarray(a, float), (col, row, values))
    ucol, urow = np.unique(col), np.unique(row)

    def _edges(u):
        if len(u) == 1: return np.array([u[0]-0.5, u[0]+0.5])
        d = np.diff(u)
        left = np.concatenate([[u[0]-d[0]/2], u[:-1]+d/2])
        return np.concatenate([left, [left[-1]+d[-1]/2]])

    h = ROOT.TH2D(f"map_{_uid()}", f";{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}",
                  len(ucol), _edges(ucol), len(urow), _edges(urow))
    for c, r, v in zip(col, row, values):
        h.Fill(c, r, v)
    ROOT.gStyle.SetPalette(palette if palette is not None else ROOT.kBird)
    ROOT.gStyle.SetOptStat(0)
    return h


def map_from_file(filepath, col_col=0, col_row=1, col_val=2, sep=r"\s+",
                  xlabel="x", ylabel="y", zlabel="Value", palette=None):
    """Build a TH2D pixel map from a delimited text file."""
    df = _read_csv(filepath, sep)
    def _get(k): return df.iloc[:, k].to_numpy() if isinstance(k, int) else df[k].to_numpy()
    return map_from_arrays(_get(col_col), _get(col_row), _get(col_val),
                           xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, palette=palette)
