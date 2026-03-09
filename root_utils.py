"""
root_utils.py
=============
ROOT plotting utilities for physics data analysis.
"""

import ROOT
import numpy as np
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
#  COLOR MAP
# ─────────────────────────────────────────────────────────────────────────────

_COLORS: dict[str, int] = {
    "black":       ROOT.kBlack,
    "white":       ROOT.kWhite,
    "red":         ROOT.kRed,
    "dark_red":    ROOT.kRed + 2,
    "light_red":   ROOT.kRed - 7,
    "blue":        ROOT.kBlue,
    "dark_blue":   ROOT.kBlue + 2,
    "light_blue":  ROOT.kBlue - 7,
    "cyan":        ROOT.kCyan + 1,
    "green":       ROOT.kGreen + 2,
    "dark_green":  ROOT.kGreen + 3,
    "light_green": ROOT.kGreen - 3,
    "orange":      ROOT.kOrange + 7,
    "yellow":      ROOT.kYellow + 1,
    "magenta":     ROOT.kMagenta,
    "violet":      ROOT.kViolet,
    "gray":        ROOT.kGray + 1,
    "dark_gray":   ROOT.kGray + 2,
}

def color(name) -> int:
    """Resolve a color name string or ROOT integer to a ROOT color code."""
    if isinstance(name, int):
        return name
    key = name.lower().replace(" ", "_")
    if key not in _COLORS:
        raise ValueError(f"Unknown color '{name}'. Available: {list(_COLORS)}")
    return _COLORS[key]


# ─────────────────────────────────────────────────────────────────────────────
#  TEXT HELPER
# ─────────────────────────────────────────────────────────────────────────────

def latex(text: str) -> str:
    """
    Pass-through helper applied to every text field in the module.

    Use ROOT TLatex syntax directly: ``#mu``, ``#sigma``, ``#chi^{2}``,
    ``#frac{a}{b}``, ``x^{2}``, ``x_{i}``, etc.

    The only transformation performed is stripping any surrounding ``$...$``
    delimiters, so strings copy-pasted from LaTeX source still work as labels
    as long as the content inside the dollars is already valid ROOT TLatex.

    Examples
    --------
    >>> latex("#mu #pm #sigma")
    '#mu #pm #sigma'
    >>> latex("mass [MeV/c^{2}]")
    'mass [MeV/c^{2}]'
    """
    return text.replace("$", "")


# ─────────────────────────────────────────────────────────────────────────────
#  LINE STYLE MAP
# ─────────────────────────────────────────────────────────────────────────────

_LINE_STYLES: dict[str, int] = {
    "solid":               1,
    "dashed":              2,
    "dotted":              3,
    "dash_dot":            4,
    "dash_dot_dot":        5,
    "long_dashed":         6,
    "long_dash_dot":       7,
    "long_dash_dot_dot":   8,
    "dash":                2,
    "dot":                 3,
    "dot_dash":            4,
    "dotdash":             4,
    "dashdot":             4,
    "dot_dot_dash":        5,
}

def line_style(style) -> int:
    """
    Resolve a line style name or ROOT integer to a ROOT line style code.

    Supported names
    ---------------
    "solid"             → 1   ───────────────
    "dashed" / "dash"   → 2   ─ ─ ─ ─ ─ ─ ─
    "dotted" / "dot"    → 3   · · · · · · · ·
    "dash_dot"          → 4   ─ · ─ · ─ · ─
    "dash_dot_dot"      → 5   ─ · · ─ · · ─
    "long_dashed"       → 6   ── ── ── ──
    "long_dash_dot"     → 7   ── · ── · ──
    "long_dash_dot_dot" → 8   ── · · ── · ·
    """
    if isinstance(style, int):
        return style
    key = style.lower().replace(" ", "_").replace("-", "_")
    if key not in _LINE_STYLES:
        raise ValueError(f"Unknown line style '{style}'. Available: {list(_LINE_STYLES)}")
    return _LINE_STYLES[key]


# ─────────────────────────────────────────────────────────────────────────────
#  MARKER STYLE MAP
# ─────────────────────────────────────────────────────────────────────────────

_MARKERS: dict[str, int] = {
    "circle":             20,
    "square":             21,
    "triangle_up":        22,
    "triangle_down":      23,
    "star":               29,
    "diamond":            33,
    "cross_circle":       34,
    "open_circle":        24,
    "open_square":        25,
    "open_triangle_up":   26,
    "open_triangle_down": 32,
    "open_star":          30,
    "open_diamond":       27,
    "dot":                 1,
    "plus":                2,
    "asterisk":            3,
    "cross":               5,
    "x":                   5,
    "tiny_dot":            6,
    "small_dot":           7,
    "full_circle":        20,
    "full_square":        21,
    "full_triangle":      22,
    "full_star":          29,
    "full_diamond":       33,
    "triangle":           22,
    "open_triangle":      26,
}

def marker_style(style) -> int:
    """
    Resolve a marker style name or ROOT integer to a ROOT marker style code.

    Filled markers
    --------------
    "circle"  / "full_circle"         → 20  ●
    "square"  / "full_square"         → 21  ■
    "triangle_up" / "triangle"        → 22  ▲
    "triangle_down"                   → 23  ▼
    "star"    / "full_star"           → 29  ★
    "diamond" / "full_diamond"        → 33  ◆
    "cross_circle"                    → 34

    Open markers
    ------------
    "open_circle"                     → 24  ○
    "open_square"                     → 25  □
    "open_triangle_up"                → 26  △
    "open_triangle_down"              → 32  ▽
    "open_star"                       → 30  ☆
    "open_diamond"                    → 27  ◇

    Simple marks
    ------------
    "dot"                             →  1  ·
    "plus"                            →  2  +
    "asterisk"                        →  3  *
    "cross" / "x"                     →  5  ×
    """
    if isinstance(style, int):
        return style
    key = style.lower().replace(" ", "_").replace("-", "_")
    if key not in _MARKERS:
        raise ValueError(f"Unknown marker style '{style}'. Available: {list(_MARKERS)}")
    return _MARKERS[key]


# ─────────────────────────────────────────────────────────────────────────────
#  STYLE
# ─────────────────────────────────────────────────────────────────────────────

def set_style() -> None:
    """Apply a clean, LaTeX-compatible ROOT style (Times font, no stat box)."""
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)

    font = 132  # Times New Roman — matches LaTeX default

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

    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetLegendFillColor(0)
    ROOT.gStyle.SetLegendFont(font)
    ROOT.gStyle.SetLegendTextSize(0.04)


# ─────────────────────────────────────────────────────────────────────────────
#  GRAPHS
# ─────────────────────────────────────────────────────────────────────────────

def _apply_graph_style(g, c: int, mkr: int, marker_size: float, line_width: int) -> None:
    g.SetMarkerStyle(mkr)
    g.SetMarkerColor(c)
    g.SetLineColor(c)
    g.SetMarkerSize(marker_size)
    g.SetLineWidth(line_width)


def graph(
    x: np.ndarray,
    y: np.ndarray,
    ex: np.ndarray = None,
    ey: np.ndarray = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    color: str | int = "blue",
    marker: str | int = "circle",
    marker_size: float = 1.2,
    line_style: str | int = "solid",
    line_width: int = 2,
) -> ROOT.TGraphErrors:
    """
    Create a TGraphErrors.

    Parameters
    ----------
    marker : str or int
        Name (e.g. ``"circle"``, ``"open_square"``) or ROOT integer (e.g. ``20``).
        See :func:`marker_style` for the full list.
    line_style : str or int
        Name (e.g. ``"dashed"``, ``"dotted"``) or ROOT integer (e.g. ``2``).
        See :func:`line_style` for the full list.
    """
    n = len(x)
    _ex = np.zeros(n) if ex is None else np.asarray(ex, dtype=np.float64)
    _ey = np.zeros(n) if ey is None else np.asarray(ey, dtype=np.float64)

    g = ROOT.TGraphErrors(
        n,
        np.asarray(x, dtype=np.float64),
        np.asarray(y, dtype=np.float64),
        _ex,
        _ey,
    )
    g.SetTitle(f"{latex(title)};{latex(xlabel)};{latex(ylabel)}")
    c = globals()["color"](color)
    mkr = globals()["marker_style"](marker)
    ls  = globals()["line_style"](line_style)
    _apply_graph_style(g, c, mkr, marker_size, line_width)
    g.SetLineStyle(ls)
    return g


def graph_asymm(
    x: np.ndarray,
    y: np.ndarray,
    exl: np.ndarray = None,
    exh: np.ndarray = None,
    eyl: np.ndarray = None,
    eyh: np.ndarray = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    color: str | int = "blue",
    marker: str | int = "circle",
    marker_size: float = 1.2,
    line_style: str | int = "solid",
    line_width: int = 2,
) -> ROOT.TGraphAsymmErrors:
    """
    Create a TGraphAsymmErrors.

    Parameters
    ----------
    marker : str or int
        Name (e.g. ``"triangle_up"``, ``"open_diamond"``) or ROOT integer.
        See :func:`marker_style` for the full list.
    line_style : str or int
        Name (e.g. ``"dashed"``, ``"dash_dot"``) or ROOT integer.
        See :func:`line_style` for the full list.
    """
    n = len(x)
    zeros = np.zeros(n)

    g = ROOT.TGraphAsymmErrors(
        n,
        np.asarray(x, dtype=np.float64),
        np.asarray(y, dtype=np.float64),
        zeros if exl is None else np.asarray(exl, dtype=np.float64),
        zeros if exh is None else np.asarray(exh, dtype=np.float64),
        zeros if eyl is None else np.asarray(eyl, dtype=np.float64),
        zeros if eyh is None else np.asarray(eyh, dtype=np.float64),
    )
    g.SetTitle(f"{latex(title)};{latex(xlabel)};{latex(ylabel)}")
    c   = globals()["color"](color)
    mkr = globals()["marker_style"](marker)
    ls  = globals()["line_style"](line_style)
    _apply_graph_style(g, c, mkr, marker_size, line_width)
    g.SetLineStyle(ls)
    return g


# ─────────────────────────────────────────────────────────────────────────────
#  FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def func(
    expression: str,
    xmin: float,
    xmax: float,
    params: list[float] = None,
    param_names: list[str] = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "f(x)",
    color: str | int = "red",
    line_style: str | int = "solid",
    line_width: int = 2,
    npx: int = 1000,
) -> ROOT.TF1:
    """
    Create a TF1.

    Parameters
    ----------
    line_style : str or int
        Name (e.g. ``"dashed"``, ``"dotted"``) or ROOT integer (e.g. ``2``).
        See :func:`line_style` for the full list.
    """
    c  = globals()["color"](color)
    ls = globals()["line_style"](line_style)
    f  = ROOT.TF1(f"f_{np.random.randint(10000)}", expression, xmin, xmax)
    f.SetTitle(f"{latex(title)};{latex(xlabel)};{latex(ylabel)}")
    f.SetLineColor(c)
    f.SetLineWidth(line_width)
    f.SetLineStyle(ls)
    f.SetNpx(npx)

    if params is not None:
        for i, val in enumerate(params):
            f.SetParameter(i, val)

    if param_names is not None:
        for i, name in enumerate(param_names):
            if i < f.GetNpar():
                f.SetParName(i, latex(name))

    return f


def func2d(
    expression: str,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    params: list[float] = None,
    param_names: list[str] = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "f(x,y)",
    color: str | int = "red",
    line_style: str | int = "solid",
    line_width: int = 2,
    npx: int = 1000,
    npy: int = 1000,
) -> ROOT.TF2:
    """
    Create a TF2.

    Parameters
    ----------
    line_style : str or int
        Name (e.g. ``"dashed"``, ``"dotted"``) or ROOT integer (e.g. ``2``).
        See :func:`line_style` for the full list.
    """
    c  = globals()["color"](color)
    ls = globals()["line_style"](line_style)
    f  = ROOT.TF2(f"f2d_{np.random.randint(10000)}", expression, xmin, xmax, ymin, ymax)
    f.SetTitle(f"{latex(title)};{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}")
    f.SetLineColor(c)
    f.SetLineWidth(line_width)
    f.SetLineStyle(ls)
    f.SetNpx(npx)
    f.SetNpy(npy)

    if params is not None:
        for i, val in enumerate(params):
            f.SetParameter(i, val)

    if param_names is not None:
        for i, name in enumerate(param_names):
            if i < f.GetNpar():
                f.SetParName(i, latex(name))

    return f


_TF3_DRAW_MODES: dict[str, str] = {
    # Isosurface modes
    "iso":      "ISO",    # solid isosurface (default)
    "iso_fb":   "ISOFB",  # ISO + front/back face culling
    "iso_bb":   "ISOBB",  # ISO + back-face culling only
    "fb":       "FB",     # front+back faces, no isosurface mesh
    "bb":       "BB",     # back faces only
    # Glowing / smooth (requires OpenGL / GLEW at build time)
    "gl":       "GL",     # OpenGL smooth surface
    "gl_iso":   "GLISO",  # OpenGL isosurface
    "gl_col":   "GLCOL",  # OpenGL colored volume
    "gl_box":   "GLBOX",  # OpenGL box (voxel) rendering
    # Slice / projection
    "tf3":      "TF3",    # same as ISO, explicit ROOT keyword
}


def func3d(
    expression: str,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    zmin: float,
    zmax: float,
    params: list[float] = None,
    param_names: list[str] = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "z",
    # ── surface appearance ───────────────────────────────────────────────────
    color: str | int = "red",
    fill_color: str | int = None,
    fill_alpha: float = 0.5,
    line_color: str | int = None,
    line_style: str | int = "solid",
    line_width: int = 1,
    # ── draw mode ────────────────────────────────────────────────────────────
    draw_mode: str = "iso",
    # ── sampling resolution ──────────────────────────────────────────────────
    npx: int = 30,
    npy: int = 30,
    npz: int = 30,
) -> ROOT.TF3:
    """
    Create a styled TF3 (three-dimensional function / isosurface).

    The expression is a ROOT TFormula string in three variables ``x``, ``y``,
    and ``z``.  Parameters are referenced as ``[0]``, ``[1]``, etc.

    Parameters
    ----------
    expression : str
        ROOT TFormula expression, e.g. ``"x*x + y*y + z*z"`` or
        ``"[0]*exp(-([1]*x*x + [2]*y*y + [3]*z*z))"``.
    xmin, xmax : float
        x-axis domain.
    ymin, ymax : float
        y-axis domain.
    zmin, zmax : float
        z-axis domain.
    params : list[float], optional
        Initial parameter values (``[0]``, ``[1]``, …).
    param_names : list[str], optional
        Display names for the parameters.

    Surface appearance
    ------------------
    color : str or int
        Shorthand that sets *both* fill and line colour in one go.
        Overridden individually by ``fill_color`` / ``line_color``.
        See :func:`color` for the full list.
    fill_color : str or int, optional
        Colour of the isosurface fill.  Defaults to ``color``.
    fill_alpha : float
        Opacity of the isosurface fill, in [0, 1] (default 1.0 = opaque).
        Values below 1 produce a semi-transparent surface.
    line_color : str or int, optional
        Colour of the isosurface wireframe/edges.  Defaults to ``color``.
    line_style : str or int
        Wireframe line style name or ROOT integer (default ``"solid"``).
        See :func:`line_style` for the full list.
    line_width : int
        Wireframe line width (default 1).

    Draw mode
    ---------
    draw_mode : str
        How the isosurface is rendered when passed to :func:`draw`.
        Supported values:

        ============  =====================================================
        ``"iso"``     Solid filled isosurface (default).
        ``"iso_fb"``  ISO with front+back face culling (``ISOFB``).
        ``"iso_bb"``  ISO with back-face culling only (``ISOBB``).
        ``"fb"``      Front+back faces without the iso mesh (``FB``).
        ``"bb"``      Back faces only (``BB``).
        ``"gl"``      OpenGL smooth surface (requires GL build).
        ``"gl_iso"``  OpenGL isosurface (``GLISO``).
        ``"gl_col"``  OpenGL colored volume (``GLCOL``).
        ``"gl_box"``  OpenGL voxel/box rendering (``GLBOX``).
        ``"tf3"``     Explicit ROOT ``TF3`` keyword (same as ``"iso"``).
        ============  =====================================================

    Sampling resolution
    -------------------
    npx, npy, npz : int
        Number of evaluation points along each axis (default 30).
        Higher values give a smoother isosurface but are slower.

    Returns
    -------
    ROOT.TF3
        The TF3 object with a ``_draw_mode`` attribute consumed by
        :func:`draw` to select the correct ROOT draw option.

    Examples
    --------
    Semi-transparent Gaussian ball::

        f = func3d(
            "exp(-(x*x + y*y + z*z) / (2*[0]*[0]))",
            -5, 5, -5, 5, -5, 5,
            params=[1.0], param_names=["sigma"],
            color="blue", fill_alpha=0.4,
            draw_mode="iso",
        )
        draw([f], labels=[r"$e^{-r^{2}/2\\sigma^{2}}$"])

    Wireframe-only torus (no fill)::

        f = func3d(
            "(sqrt(x*x+y*y)-[0])*(sqrt(x*x+y*y)-[0]) + z*z - [1]*[1]",
            -4, 4, -4, 4, -2, 2,
            params=[2.5, 0.8], param_names=["R","r"],
            fill_alpha=0.0, line_color="dark_blue", line_width=2,
        )
    """
    if draw_mode not in _TF3_DRAW_MODES:
        raise ValueError(
            f"Unknown draw_mode '{draw_mode}'. "
            f"Available: {list(_TF3_DRAW_MODES)}"
        )

    _color     = globals()["color"]
    _ls        = globals()["line_style"]

    base_c     = _color(color)
    fc         = _color(fill_color)  if fill_color  is not None else base_c
    lc         = _color(line_color)  if line_color  is not None else base_c
    ls         = _ls(line_style)

    f = ROOT.TF3(
        f"f3d_{np.random.randint(10000)}",
        expression,
        xmin, xmax,
        ymin, ymax,
        zmin, zmax,
    )
    f.SetTitle(f"{latex(title)};{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}")

    # Surface fill
    if fill_alpha >= 1.0:
        f.SetFillColor(fc)
    else:
        f.SetFillColorAlpha(fc, max(0.0, fill_alpha))

    # Wireframe / edges
    f.SetLineColor(lc)
    f.SetLineStyle(ls)
    f.SetLineWidth(line_width)

    # Resolution
    f.SetNpx(npx)
    f.SetNpy(npy)
    f.SetNpz(npz)

    # Store the chosen ROOT draw keyword as a private attribute so that
    # _draw_option() can retrieve it without needing extra state.
    f._draw_mode = _TF3_DRAW_MODES[draw_mode]

    if params is not None:
        for i, val in enumerate(params):
            f.SetParameter(i, val)

    if param_names is not None:
        for i, name in enumerate(param_names):
            if i < f.GetNpar():
                f.SetParName(i, latex(name))

    return f


# ─────────────────────────────────────────────────────────────────────────────
#  FITTING
# ─────────────────────────────────────────────────────────────────────────────

def fit(
    graph_or_hist,
    func_or_expr: ROOT.TF1 | str,
    xmin: float = None,
    xmax: float = None,
    params: list[float] = None,
    param_names: list[str] = None,
    options: str = "RS",
    print_results: bool = True,
    units: list[str] = None,
) -> ROOT.TF1:
    if isinstance(func_or_expr, str):
        if xmin is None or xmax is None:
            raise ValueError("xmin and xmax are required when fitting with a string expression.")
        f = func(func_or_expr, xmin, xmax, params=params, param_names=param_names)
    else:
        f = func_or_expr

    graph_or_hist.Fit(f, options)

    if print_results:
        print_params(f, units=units)

    return f


def print_params(f: ROOT.TF1, units: list[str] = None, precision: int = 6) -> None:
    """Print fitted parameters with errors to stdout."""
    fmt = f"{{:.{precision}f}}"
    print("\n" + "=" * 60)
    print("FIT PARAMETERS")
    print("=" * 60)
    for i in range(f.GetNpar()):
        name  = f.GetParName(i)
        val   = f.GetParameter(i)
        err   = f.GetParError(i)
        unit  = f" [{units[i]}]" if units and i < len(units) else ""
        print(f"  {name}{unit} = {fmt.format(val)} ± {fmt.format(err)}")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
#  HISTOGRAMS
# ─────────────────────────────────────────────────────────────────────────────

def histogram(
    data: np.ndarray,
    bins: int = 50,
    range: tuple[float, float] = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "Counts",
    color: str | int = "blue",
    line_style: str | int = "solid",
    line_width: int = 2,
    fill: bool = True,
    fill_alpha: float = 0.3,
) -> ROOT.TH1D:
    """
    Create and fill a TH1D.

    Parameters
    ----------
    line_style : str or int
        Name (e.g. ``"dashed"``, ``"dotted"``) or ROOT integer (e.g. ``2``).
        See :func:`line_style` for the full list.
    """
    c  = globals()["color"](color)
    ls = globals()["line_style"](line_style)
    xmin = range[0] if range else float(np.min(data))
    xmax = range[1] if range else float(np.max(data))

    h = ROOT.TH1D(f"h1_{np.random.randint(10000)}", f"{latex(title)};{latex(xlabel)};{latex(ylabel)}", bins, xmin, xmax)

    data_64 = np.asarray(data, dtype=np.float64)
    h.FillN(len(data_64), data_64, np.ones(len(data_64)))

    h.SetLineColor(c)
    h.SetLineStyle(ls)
    h.SetLineWidth(line_width)
    h.SetStats(0)
    h.SetTitle(latex(title))
    if fill:
        h.SetFillColorAlpha(c, fill_alpha)
    return h


def histogram2d(
    x: np.ndarray,
    y: np.ndarray,
    bins_x: int = 40,
    bins_y: int = 40,
    range_x: tuple[float, float] = None,
    range_y: tuple[float, float] = None,
    title: str = "",
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "Counts",
    palette: int = None,
) -> ROOT.TH2D:
    xmin = range_x[0] if range_x else float(np.min(x))
    xmax = range_x[1] if range_x else float(np.max(x))
    ymin = range_y[0] if range_y else float(np.min(y))
    ymax = range_y[1] if range_y else float(np.max(y))

    h = ROOT.TH2D(
        f"h2_{np.random.randint(10000)}", f"{latex(title)};{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}",
        bins_x, xmin, xmax, bins_y, ymin, ymax,
    )
    for xi, yi in zip(x, y):
        h.Fill(xi, yi)

    ROOT.gStyle.SetPalette(palette if palette is not None else ROOT.kBird)
    return h


# ─────────────────────────────────────────────────────────────────────────────
#  HISTOGRAM STATS HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def hist_stats_entries(
    h: ROOT.TH1,
    show_mean: bool = True,
    show_std: bool = True,
    show_counts: bool = True,
    precision: int = 3,
    mean_label: str = "Mean",
    std_label: str = "Std Dev",
    counts_label: str = "Counts",
) -> list[tuple]:
    """
    Return a list of (dummy_obj, label, option) tuples carrying histogram
    statistics, ready to be fed into a TLegend via ``AddEntry``.
    """
    fmt = f"{{:.{precision}f}}"
    entries = []

    if show_mean:
        dummy = ROOT.TBox(0, 0, 0, 0)
        dummy.SetFillStyle(0)
        dummy.SetLineStyle(0)
        entries.append((dummy, f"{mean_label} = {fmt.format(h.GetMean())}", ""))

    if show_std:
        dummy = ROOT.TBox(0, 0, 0, 0)
        dummy.SetFillStyle(0)
        dummy.SetLineStyle(0)
        entries.append((dummy, f"{std_label} = {fmt.format(h.GetStdDev())}", ""))

    if show_counts:
        dummy = ROOT.TBox(0, 0, 0, 0)
        dummy.SetFillStyle(0)
        dummy.SetLineStyle(0)
        entries.append((dummy, f"{counts_label} = {int(h.GetEntries())}", ""))

    return entries


def fit_stats_entries(
    f: ROOT.TF1,
    show_chi2: bool = True,
    show_params: bool = True,
    show_errors: bool = True,
    precision: int = 3,
    chi2_label: str = "#chi^{2} / NDF",
    param_names_override: list[str] = None,
    units: list[str] = None,
) -> list[tuple]:
    """
    Return a list of (dummy_obj, label, option) tuples carrying fit results,
    ready for ``TLegend.AddEntry``.
    """
    fmt = f"{{:.{precision}f}}"
    entries = []

    def _dummy():
        b = ROOT.TBox(0, 0, 0, 0)
        b.SetFillStyle(0)
        b.SetLineStyle(0)
        return b

    if show_chi2:
        ndf    = f.GetNDF()
        chi2   = f.GetChisquare()
        ratio  = chi2 / ndf if ndf > 0 else float("nan")
        label  = f"{chi2_label} = {fmt.format(chi2)} / {ndf} = {fmt.format(ratio)}"
        entries.append((_dummy(), label, ""))

    if show_params:
        npar = f.GetNpar()
        for i in range(npar):
            name  = (latex(param_names_override[i])
                     if param_names_override and i < len(param_names_override)
                     else f.GetParName(i))
            val   = f.GetParameter(i)
            err   = f.GetParError(i)
            unit  = f" [{units[i]}]" if units and i < len(units) else ""
            if show_errors:
                label = f"{name}{unit} = {fmt.format(val)} #pm {fmt.format(err)}"
            else:
                label = f"{name}{unit} = {fmt.format(val)}"
            entries.append((_dummy(), label, ""))

    return entries


# ─────────────────────────────────────────────────────────────────────────────
#  LEGEND HELPERS
# ─────────────────────────────────────────────────────────────────────────────

_LEGEND_ANCHORS = {
    "top_right":    (0.92,  0.92,  "TR"),
    "top_left":     (0.15,  0.92,  "TL"),
    "bottom_right": (0.92,  0.15,  "BR"),
    "bottom_left":  (0.15,  0.15,  "BL"),
    "top_center":   (0.535, 0.92,  "TC"),
}


def _legend_option(obj) -> str:
    if isinstance(obj, ROOT.TF1):
        return "l"
    if isinstance(obj, ROOT.TH1):
        return "lf"
    return "lep"


def make_legend(
    objects,
    labels,
    pos="top_right",
    ncols: int = 1,
    text_size: float = 0.038,
    width: float = 0.25,
    row_height: float = 0.045,
    margin: float = 0.30,
    border: int = 0,
    fill_alpha: float = 0.0,
) -> ROOT.TLegend:

    n_entries = len(objects)
    n_rows = int(np.ceil(n_entries / ncols))

    total_w = width
    total_h = n_rows * row_height

    if isinstance(pos, tuple):
        x1, y1, x2, y2 = pos
    elif pos in _LEGEND_ANCHORS:
        ax, ay, corner = _LEGEND_ANCHORS[pos]
        y2 = ay if "T" in corner else ay + total_h
        y1 = y2 - total_h

        if "R" in corner:
            x2 = ax
            x1 = ax - total_w
        elif "L" in corner:
            x1 = ax
            x2 = ax + total_w
        else:
            x1 = ax - total_w/2
            x2 = ax + total_w/2
    else:
        raise ValueError(f"Unknown legend position '{pos}'")

    leg = ROOT.TLegend(x1, y1, x2, y2)
    leg.SetNColumns(ncols)
    leg.SetTextSize(text_size)
    leg.SetMargin(margin)
    leg.SetBorderSize(border)
    leg.SetFillStyle(0 if fill_alpha == 0.0 else 1001)

    if fill_alpha > 0:
        leg.SetFillColorAlpha(ROOT.kWhite, fill_alpha)

    for obj, label in zip(objects, labels):
        leg.AddEntry(obj, label, _legend_option(obj))

    return leg


# ─────────────────────────────────────────────────────────────────────────────
#  DRAWING
# ─────────────────────────────────────────────────────────────────────────────

# Line-style names that are valid as per-object draw options in draw().
# When a user passes one of these as an element of the options list, it is
# interpreted as a line-style override rather than a raw ROOT draw string.
_LINE_STYLE_NAMES: frozenset[str] = frozenset(_LINE_STYLES.keys())


def _auto_draw_option(obj, first: bool, base: str) -> str:
    """Return the automatic ROOT draw option for *obj* (no per-item override)."""
    if isinstance(obj, ROOT.TF3):
        mode = getattr(obj, "_draw_mode", "ISO")
        return mode if first else f"{mode} SAME"
    if isinstance(obj, ROOT.TF1):
        return "" if first else "SAME"
    if isinstance(obj, (ROOT.TH1D, ROOT.TH1F)):
        return "HIST" if first else "HIST SAME"
    if isinstance(obj, (ROOT.TH2D, ROOT.TH2F)):
        return "COLZ"
    # TGraph / TGraphErrors / TGraphAsymmErrors
    return base if first else base.replace("A", "") + " SAME"


def _resolve_draw_option(obj, per_item: str | None, first: bool, base: str) -> str:
    """
    Resolve the final ROOT draw option string for a single object.

    Rules
    -----
    * ``None``        → fall back to :func:`_auto_draw_option` (unchanged behaviour).
    * line-style name  → apply the style to *obj* in-place and then fall back to
                         the auto option (e.g. ``"dotted"`` sets ``SetLineStyle(3)``
                         on the object and draws it normally).
    * any other str   → use it verbatim, appending ``" SAME"`` for non-first objects
                         when the string does not already contain ``"SAME"``.

    Parameters
    ----------
    obj       : ROOT object being drawn.
    per_item  : the per-object option string (or ``None``).
    first     : whether this is the first object drawn on the canvas.
    base      : the global fallback draw string (e.g. ``"AP"``).
    """
    if per_item is None:
        return _auto_draw_option(obj, first, base)

    key = per_item.strip().lower().replace(" ", "_").replace("-", "_")

    # ── line-style shorthand ──────────────────────────────────────────────
    if key in _LINE_STYLE_NAMES:
        obj.SetLineStyle(_LINE_STYLES[key])
        return _auto_draw_option(obj, first, base)

    # ── raw ROOT draw string ──────────────────────────────────────────────
    opt = per_item.strip()
    if not first and "SAME" not in opt.upper():
        # Strip "A" from graph options (axis is drawn by the first object)
        opt = opt.replace("A", "").replace("a", "").strip()
        opt = (opt + " SAME").strip()
    return opt


def draw(
    objects: list,
    labels: list[str] = None,
    xlabel: str = None,
    ylabel: str = None,
    xrange: tuple[float, float] = None,
    yrange: tuple[float, float] = None,
    options: str | list[str | None] = "AP",
    width: int = 900,
    height: int = 600,
    log_x: bool = False,
    log_y: bool = False,
    legend_pos: str | tuple[float, float, float, float] = "top_right",
    legend_width: float = 0.25,
    legend_row_height: float = 0.045,
    legend_ncols: int = 1,
    legend_text_size: float = 0.038,
    legend_margin: float = 0.25,
    legend_border: int = 0,
    legend_fill_alpha: float = 0.0,
    hist_stats: bool = False,
    hist_stats_precision: int = 3,
    hist_stats_show_mean: bool = True,
    hist_stats_show_std: bool = True,
    hist_stats_show_counts: bool = True,
    hist_stats_mean_label: str = "Mean",
    hist_stats_std_label: str = "Std Dev",
    hist_stats_counts_label: str = "Counts",
    fit_stats: bool = False,
    fit_stats_precision: int = 3,
    fit_stats_show_chi2: bool = True,
    fit_stats_show_params: bool = True,
    fit_stats_show_errors: bool = True,
    fit_stats_chi2_label: str = "#chi^{2} / NDF",
    fit_stats_param_names: list[str] = None,
    fit_stats_units: list[str] = None,
    save: str = None,
) -> tuple[ROOT.TCanvas, ROOT.TLegend | None]:
    """
    Draw a list of ROOT objects on a single canvas with an optional legend.

    Labels support both ROOT TLatex syntax (``#mu``, ``#chi^{2}``) and standard
    LaTeX math syntax (``$\\mu$``, ``$\\chi^{2}$``) via the :func:`latex` helper,
    which is applied automatically to every label string.

    Per-object draw options
    -----------------------
    ``options`` can be either a single string (applied as the global fallback for
    all graph-like objects, same as before) **or a list** with one entry per
    object in ``objects``.  Each list element can be:

    ``None``
        Use the automatic draw option for that object type (default behaviour).

    A line-style name (``"solid"``, ``"dashed"``, ``"dotted"``, ``"dash_dot"``,
    ``"dash_dot_dot"``, ``"long_dashed"``, ``"long_dash_dot"``,
    ``"long_dash_dot_dot"``)
        Apply that line style to the object in-place, then draw it with the
        automatic option.  This is the quickest way to override the line style
        at draw time without re-creating the object.

    Any other string (``"AP"``, ``"HIST"``, ``"COLZ"``, ``"P"``, …)
        Use it as a raw ROOT draw option.  ``"SAME"`` is appended automatically
        for non-first objects when not already present.

    Examples
    --------
    Mixed per-object options::

        draw([g1, g2, h], options=["AP", "dotted", "HIST"])

    Only override one object, let the rest use defaults::

        draw([g1, g2, h2d], options=[None, "dashed", "COLZ"])

    Axis ranges
    -----------
    xrange : tuple(float, float) or None
        If provided, sets the visible x-axis range, e.g. ``xrange=(0, 10)``.
    yrange : tuple(float, float) or None
        If provided, sets the visible y-axis range, e.g. ``yrange=(0, 500)``.
    """
    canvas = ROOT.TCanvas(f"c_{np.random.randint(10000)}", "", width, height)
    if log_x:
        canvas.SetLogx()
    if log_y:
        canvas.SetLogy()

    # ── normalise options to a per-object list ────────────────────────────
    # global_base is used by _resolve_draw_option for graph auto-detection
    if isinstance(options, list):
        global_base = "AP"   # sensible default when a list is supplied
        per_obj_opts: list[str | None] = list(options)
        # pad with None so indexing is always safe
        while len(per_obj_opts) < len(objects):
            per_obj_opts.append(None)
    else:
        global_base = options
        per_obj_opts = [None] * len(objects)

    # ── determine draw order (non-TF1 first so axes are created early) ───
    first_graph_idx = next(
        (i for i, o in enumerate(objects) if not isinstance(o, ROOT.TF1)), None
    )
    draw_order = (
        [first_graph_idx] + [i for i in range(len(objects)) if i != first_graph_idx]
        if first_graph_idx is not None
        else list(range(len(objects)))
    )

    for pos, i in enumerate(draw_order):
        obj = objects[i]
        opt = _resolve_draw_option(
            obj,
            per_item=per_obj_opts[i],
            first=(pos == 0),
            base=global_base,
        )
        obj.Draw(opt)

    primary = objects[first_graph_idx] if first_graph_idx is not None else objects[0]
    if xlabel is not None:
        primary.GetXaxis().SetTitle(latex(xlabel))
    if ylabel is not None:
        primary.GetYaxis().SetTitle(latex(ylabel))

    if xrange is not None:
        primary.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    if yrange is not None:
        primary.GetYaxis().SetRangeUser(yrange[0], yrange[1])

    legend = None
    if labels:
        # Apply latex() conversion to every label automatically
        converted_labels = [latex(lbl) for lbl in labels]

        hist_stat_map: dict[int, list] = {}
        fit_stat_map:  dict[int, list] = {}
        n_stat_rows = 0
        if hist_stats:
            for obj in objects:
                if isinstance(obj, ROOT.TH1):
                    entries = hist_stats_entries(
                        obj,
                        show_mean=hist_stats_show_mean,
                        show_std=hist_stats_show_std,
                        show_counts=hist_stats_show_counts,
                        precision=hist_stats_precision,
                        mean_label=hist_stats_mean_label,
                        std_label=hist_stats_std_label,
                        counts_label=hist_stats_counts_label,
                    )
                    hist_stat_map[id(obj)] = entries
                    n_stat_rows += len(entries)
        if fit_stats:
            for obj in objects:
                if isinstance(obj, ROOT.TF1):
                    entries = fit_stats_entries(
                        obj,
                        show_chi2=fit_stats_show_chi2,
                        show_params=fit_stats_show_params,
                        show_errors=fit_stats_show_errors,
                        precision=fit_stats_precision,
                        chi2_label=fit_stats_chi2_label,
                        param_names_override=fit_stats_param_names,
                        units=fit_stats_units,
                    )
                    fit_stat_map[id(obj)] = entries
                    n_stat_rows += len(entries)

        n_total_entries = len(objects) + n_stat_rows
        total_h = int(np.ceil(n_total_entries / legend_ncols)) * legend_row_height
        total_w = legend_width

        if isinstance(legend_pos, tuple):
            x1, y1, x2, y2 = legend_pos
        elif legend_pos in _LEGEND_ANCHORS:
            ax, ay, corner = _LEGEND_ANCHORS[legend_pos]
            y2 = ay if "T" in corner else ay + total_h
            y1 = y2 - total_h
            if "R" in corner:
                x2, x1 = ax, ax - total_w
            elif "L" in corner:
                x1, x2 = ax, ax + total_w
            else:
                x1, x2 = ax - total_w / 2, ax + total_w / 2
        else:
            raise ValueError(f"Unknown legend position '{legend_pos}'")

        legend = ROOT.TLegend(x1, y1, x2, y2)
        legend.SetNColumns(legend_ncols)
        legend.SetTextSize(legend_text_size)
        legend.SetMargin(legend_margin)
        legend.SetBorderSize(legend_border)
        legend.SetFillStyle(0 if legend_fill_alpha == 0.0 else 1001)
        if legend_fill_alpha > 0:
            legend.SetFillColorAlpha(ROOT.kWhite, legend_fill_alpha)

        for obj, label in zip(objects, converted_labels):
            legend.AddEntry(obj, label, _legend_option(obj))
            if id(obj) in hist_stat_map:
                for dummy, lbl, opt in hist_stat_map[id(obj)]:
                    legend.AddEntry(dummy, lbl, opt)
            if id(obj) in fit_stat_map:
                for dummy, lbl, opt in fit_stat_map[id(obj)]:
                    legend.AddEntry(dummy, lbl, opt)

        legend.Draw()

    canvas.Update()

    if save:
        canvas.SaveAs(save)
        print(f"[draw] Saved: {save}")

    return canvas, legend


# ─────────────────────────────────────────────────────────────────────────────
#  I/O UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def load_column(
    filepath: str,
    column: str | int,
    sep: str = r"\s+",
) -> np.ndarray:
    df = pd.read_csv(filepath, sep=sep, engine="python")
    return df.iloc[:, column].to_numpy() if isinstance(column, int) else df[column].to_numpy()


def load_columns(
    filepath: str,
    columns: list[str | int],
    sep: str = r"\s+",
) -> list[np.ndarray]:
    return [load_column(filepath, col, sep) for col in columns]

def load_row(
    filepath: str,
    row: int = 0,
    sep: str = r"\s+",
) -> np.ndarray:

    with open(filepath, "r") as fh:
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]

    if len(lines) == 1:
        return np.array(lines[0].split(), dtype=np.float64)

    df = pd.read_csv(filepath, sep=sep, engine="python", header=None)
    return df.iloc[row].to_numpy(dtype=float)

def load_rows(
    filepath: str,
    rows: list[int],
    sep: str = r"\s+",
) -> list[np.ndarray]:
    df = pd.read_csv(filepath, sep=sep, engine="python", header=None)
    return [df.iloc[r].to_numpy(dtype=float) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
#  MAPS  (2D pixel / detector maps)
# ─────────────────────────────────────────────────────────────────────────────

def map_from_arrays(
    col, row, values,
    xlabel="x", ylabel="y", zlabel="Value",
    palette=None,
):
    if palette is None:
        palette = ROOT.kBird

    col    = np.asarray(col,    dtype=float)
    row    = np.asarray(row,    dtype=float)
    values = np.asarray(values, dtype=float)

    ucol = np.unique(col)
    urow = np.unique(row)
    nx, ny = len(ucol), len(urow)

    def _edges(u):
        if len(u) == 1:
            return np.array([u[0] - 0.5, u[0] + 0.5])
        d = np.diff(u)
        left  = np.concatenate([[u[0] - d[0] / 2], u[:-1] + d / 2])
        right = np.array([left[-1] + d[-1] / 2])
        return np.concatenate([left, right])

    xedges = _edges(ucol)
    yedges = _edges(urow)

    h = ROOT.TH2D(
        f"map_{np.random.randint(10000)}",
        f";{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}",
        nx, xedges, ny, yedges,
    )

    for c, r, v in zip(col, row, values):
        h.Fill(c, r, v)

    ROOT.gStyle.SetPalette(palette)
    ROOT.gStyle.SetOptStat(0)
    return h


def map_from_file(
    filepath,
    col_col=0, col_row=1, col_val=2,
    sep=r"\s+",
    xlabel="x", ylabel="y", zlabel="Value",
    palette=None,
):
    df = pd.read_csv(filepath, sep=sep, engine="python")

    def _get(key):
        return df.iloc[:, key].to_numpy() if isinstance(key, int) else df[key].to_numpy()

    return map_from_arrays(
        _get(col_col), _get(col_row), _get(col_val),
        xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, palette=palette,
    )