"""
root_utils.py
=============
High-level ROOT plotting utilities for physics data analysis.

This module wraps PyROOT with a clean, Pythonic API so that producing
publication-quality plots requires minimal boilerplate.  All text fields
(axis titles, labels, parameter names, legend entries) accept ROOT TLatex
syntax directly — see :func:`latex` for details.

Typical usage
-------------
    from root_utils import *

    set_style()                          # apply Times-font, no-stat-box style

    h = histogram(data, xlabel="#mu [GeV]", ylabel="Counts / 0.5 GeV")
    f = fit(h, "gaus", -3, 3)
    draw([h, f], labels=["Data", "Gaussian fit"], fit_stats=True, save="plot.pdf")
"""

import ROOT
import numpy as np
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
#  COLOR MAP
# ─────────────────────────────────────────────────────────────────────────────

# Human-readable color names mapped to ROOT color codes.
# Pass any key to the ``color`` parameter of graph(), histogram(), func(), etc.
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


def color(name: str | int) -> int:
    """
    Resolve a color name string or a raw ROOT integer to a ROOT color code.

    Parameters
    ----------
    name : str or int
        A key from ``_COLORS`` (e.g. ``"red"``, ``"dark_blue"``) or a raw
        ROOT integer (e.g. ``ROOT.kRed + 3``).  Integers are returned as-is.

    Returns
    -------
    int
        ROOT color code suitable for ``SetLineColor``, ``SetMarkerColor``, etc.

    Raises
    ------
    ValueError
        If ``name`` is a string not present in ``_COLORS``.
    """
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
    Pass-through helper applied automatically to every text field in the module.

    Write ROOT TLatex syntax directly everywhere: axis titles, histogram
    titles, function labels, parameter names, legend entries, etc.

    ROOT TLatex quick reference
    ---------------------------
    Greek letters   ``#mu``  ``#sigma``  ``#chi``  ``#pi``  ``#alpha`` ...
    Superscript     ``x^{2}``  ``E^{*}``
    Subscript       ``x_{i}``  ``p_{T}``
    Fractions       ``#frac{a}{b}``
    Square root     ``#sqrt{x}``  ``#sqrt[3]{x}``
    Math symbols    ``#pm``  ``#mp``  ``#times``  ``#cdot``  ``#leq``  ``#geq``
                    ``#infty``  ``#partial``  ``#int``  ``#sum``  ``#prod``
    Arrows          ``#rightarrow``  ``#leftarrow``  ``#Rightarrow``
    Font style      ``#it{text}``  ``#bf{text}``  ``#rm{text}``

    The only transformation performed by this function is stripping ``$``
    characters, which lets you copy-paste ROOT TLatex strings wrapped in
    dollar signs without errors.

    Parameters
    ----------
    text : str
        Any string; ``$`` characters are removed, everything else is unchanged.

    Returns
    -------
    str
        The same string with all ``$`` characters stripped.

    Examples
    --------
    >>> latex("#mu #pm #sigma")
    '#mu #pm #sigma'
    >>> latex("p_{T} [GeV/c^{2}]")
    'p_{T} [GeV/c^{2}]'
    """
    return text.replace("$", "")


# ─────────────────────────────────────────────────────────────────────────────
#  LINE STYLE MAP
# ─────────────────────────────────────────────────────────────────────────────

# Human-readable line style names mapped to ROOT line style integers.
# Aliases (dash, dot, dashdot, ...) are included for convenience.
_LINE_STYLES: dict[str, int] = {
    "solid":               1,
    "dashed":              2,
    "dotted":              3,
    "dash_dot":            4,
    "dash_dot_dot":        5,
    "long_dashed":         6,
    "long_dash_dot":       7,
    "long_dash_dot_dot":   8,
    # common aliases
    "dash":                2,
    "dot":                 3,
    "dot_dash":            4,
    "dotdash":             4,
    "dashdot":             4,
    "dot_dot_dash":        5,
}


def line_style(style: str | int) -> int:
    """
    Resolve a line style name or ROOT integer to a ROOT line style code.

    Parameters
    ----------
    style : str or int
        A key from ``_LINE_STYLES`` or a raw ROOT integer.  Integers are
        returned as-is.

    Returns
    -------
    int
        ROOT line style code suitable for ``SetLineStyle``.

    Supported names
    ---------------
    ``"solid"``               -> 1   ───────────────
    ``"dashed"`` / ``"dash"`` -> 2   - - - - - - - -
    ``"dotted"`` / ``"dot"``  -> 3   . . . . . . . .
    ``"dash_dot"``            -> 4   - . - . - . - .
    ``"dash_dot_dot"``        -> 5   - . . - . . - .
    ``"long_dashed"``         -> 6   -- -- -- --
    ``"long_dash_dot"``       -> 7   -- . -- . --
    ``"long_dash_dot_dot"``   -> 8   -- . . -- . .
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

# Human-readable marker names mapped to ROOT marker style integers.
_MARKERS: dict[str, int] = {
    # filled markers
    "circle":             20,
    "square":             21,
    "triangle_up":        22,
    "triangle_down":      23,
    "star":               29,
    "diamond":            33,
    "cross_circle":       34,
    # open markers
    "open_circle":        24,
    "open_square":        25,
    "open_triangle_up":   26,
    "open_triangle_down": 32,
    "open_star":          30,
    "open_diamond":       27,
    # simple point-like marks
    "dot":                 1,
    "plus":                2,
    "asterisk":            3,
    "cross":               5,
    "x":                   5,
    "tiny_dot":            6,
    "small_dot":           7,
    # aliases for filled markers
    "full_circle":        20,
    "full_square":        21,
    "full_triangle":      22,
    "full_star":          29,
    "full_diamond":       33,
    "triangle":           22,
    "open_triangle":      26,
}


def marker_style(style: str | int) -> int:
    """
    Resolve a marker style name or ROOT integer to a ROOT marker style code.

    Parameters
    ----------
    style : str or int
        A key from ``_MARKERS`` or a raw ROOT integer.  Integers are
        returned as-is.

    Returns
    -------
    int
        ROOT marker style code suitable for ``SetMarkerStyle``.

    Filled markers
    --------------
    ``"circle"``  / ``"full_circle"``    -> 20
    ``"square"``  / ``"full_square"``    -> 21
    ``"triangle_up"`` / ``"triangle"``   -> 22
    ``"triangle_down"``                  -> 23
    ``"star"``    / ``"full_star"``      -> 29
    ``"diamond"`` / ``"full_diamond"``   -> 33
    ``"cross_circle"``                   -> 34

    Open markers
    ------------
    ``"open_circle"``                    -> 24
    ``"open_square"``                    -> 25
    ``"open_triangle_up"``               -> 26
    ``"open_triangle_down"``             -> 32
    ``"open_star"``                      -> 30
    ``"open_diamond"``                   -> 27

    Simple marks
    ------------
    ``"dot"``                            ->  1
    ``"plus"``                           ->  2
    ``"asterisk"``                       ->  3
    ``"cross"`` / ``"x"``               ->  5
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
    """
    Apply a clean, publication-ready ROOT global style.

    Settings applied
    ----------------
    - Statistics box and title box hidden (``OptStat=0``, ``OptTitle=0``).
    - Times New Roman font (ROOT font code 132) on all axes and legends,
      consistent with the LaTeX default used in most HEP papers.
    - Axis label size 0.045, title size 0.050, offset 1.2.
    - Tick marks on all four sides of the frame (``PadTickX/Y=1``).
    - Canvas and pad backgrounds set to white (color 0).
    - Pad margins: left 0.15, bottom 0.15, right 0.05, top 0.05.
    - Legend border hidden, fill transparent.

    Call this once at the top of your script, before creating any objects.

    Examples
    --------
    >>> set_style()
    >>> h = histogram(data, xlabel="x [mm]", ylabel="Counts")
    """
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
    """Internal helper: apply marker/line style attributes to a TGraph-like object."""
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
    Create a styled ``TGraphErrors``.

    Symmetric x and y error bars are optional.  Pass ``None`` (the default)
    to draw a graph with zero-length error bars.

    Parameters
    ----------
    x, y : array-like
        Data point coordinates.
    ex, ey : array-like or None
        Symmetric uncertainties on x and y.  ``None`` -> all zeros.
    title : str
        Graph title (ROOT TLatex syntax).
    xlabel, ylabel : str
        Axis labels (ROOT TLatex syntax).
    color : str or int
        Marker and line color.  See :func:`color` for the name list.
    marker : str or int
        Marker style name or ROOT integer.  See :func:`marker_style`.
    marker_size : float
        Marker size multiplier (default 1.2).
    line_style : str or int
        Line style name or ROOT integer.  See :func:`line_style`.
    line_width : int
        Line width in pixels (default 2).

    Returns
    -------
    ROOT.TGraphErrors

    Examples
    --------
    >>> g = graph(x, y, ey=dy, xlabel="t [ns]", ylabel="V [mV]", color="red")
    >>> draw([g], labels=["Signal"])
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
    c   = globals()["color"](color)
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
    Create a styled ``TGraphAsymmErrors`` with independent low/high error bars.

    Parameters
    ----------
    x, y : array-like
        Data point coordinates.
    exl, exh : array-like or None
        Low and high x uncertainties.  ``None`` -> all zeros.
    eyl, eyh : array-like or None
        Low and high y uncertainties.  ``None`` -> all zeros.
    title : str
        Graph title (ROOT TLatex syntax).
    xlabel, ylabel : str
        Axis labels (ROOT TLatex syntax).
    color : str or int
        See :func:`color`.
    marker : str or int
        See :func:`marker_style`.
    marker_size : float
        Marker size multiplier (default 1.2).
    line_style : str or int
        See :func:`line_style`.
    line_width : int
        Line width in pixels (default 2).

    Returns
    -------
    ROOT.TGraphAsymmErrors

    Examples
    --------
    >>> g = graph_asymm(x, y, eyl=err_low, eyh=err_high, color="dark_green")
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
    Create a styled ``TF1`` (one-dimensional function).

    The expression uses ROOT TFormula syntax: standard C math functions
    (``sin``, ``exp``, ``sqrt``, ...), the variable ``x``, and parameters
    referenced as ``[0]``, ``[1]``, etc.

    Parameters
    ----------
    expression : str
        ROOT TFormula string, e.g. ``"gaus"``, ``"[0]*exp(-[1]*x)"``,
        ``"pol2"``.
    xmin, xmax : float
        Function domain.
    params : list[float], optional
        Initial parameter values for ``[0]``, ``[1]``, ...
    param_names : list[str], optional
        Display names for parameters (ROOT TLatex syntax).
    title : str
        Function title (ROOT TLatex syntax).
    xlabel, ylabel : str
        Axis labels (ROOT TLatex syntax).
    color : str or int
        Line color.  See :func:`color`.
    line_style : str or int
        See :func:`line_style`.
    line_width : int
        Line width in pixels (default 2).
    npx : int
        Number of evaluation points (default 1000; increase for sharp peaks).

    Returns
    -------
    ROOT.TF1

    Examples
    --------
    >>> f = func("[0]*exp(-0.5*((x-[1])/[2])^2)",
    ...          xmin=-5, xmax=5,
    ...          params=[1.0, 0.0, 1.0],
    ...          param_names=["A", "#mu", "#sigma"],
    ...          color="red", line_style="dashed")
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
    Create a styled ``TF2`` (two-dimensional function / surface).

    The expression uses ROOT TFormula syntax with variables ``x`` and ``y``
    and parameters ``[0]``, ``[1]``, etc.

    Parameters
    ----------
    expression : str
        ROOT TFormula string, e.g. ``"sin(x)*cos(y)"``.
    xmin, xmax : float
        x-axis domain.
    ymin, ymax : float
        y-axis domain.
    params : list[float], optional
        Initial parameter values.
    param_names : list[str], optional
        Display names for parameters (ROOT TLatex syntax).
    title : str
        Function title.
    xlabel, ylabel, zlabel : str
        Axis labels (ROOT TLatex syntax).
    color : str or int
        See :func:`color`.
    line_style : str or int
        See :func:`line_style`.
    line_width : int
        Line width (default 2).
    npx, npy : int
        Sampling resolution along each axis (default 1000).

    Returns
    -------
    ROOT.TF2

    Examples
    --------
    >>> f = func2d("sin(x)*cos(y)", -3.14, 3.14, -3.14, 3.14,
    ...            xlabel="x [rad]", ylabel="y [rad]", zlabel="Amplitude")
    >>> draw([f])
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


# Valid ROOT draw keywords for TF3 isosurface rendering.
_TF3_DRAW_MODES: dict[str, str] = {
    # ── isosurface modes ────────────────────────────────────────────────────
    "iso":      "ISO",    # solid filled isosurface (default)
    "iso_fb":   "ISOFB",  # ISO + front/back face culling
    "iso_bb":   "ISOBB",  # ISO + back-face culling only
    "fb":       "FB",     # front+back faces, no isosurface mesh
    "bb":       "BB",     # back faces only
    # ── OpenGL modes (requires ROOT built with GL/GLEW) ─────────────────────
    "gl":       "GL",     # smooth OpenGL surface
    "gl_iso":   "GLISO",  # OpenGL isosurface
    "gl_col":   "GLCOL",  # OpenGL colored volume rendering
    "gl_box":   "GLBOX",  # OpenGL voxel/box rendering
    # ── explicit TF3 keyword ────────────────────────────────────────────────
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
    Create a styled ``TF3`` (three-dimensional function / isosurface).

    The expression uses ROOT TFormula syntax with variables ``x``, ``y``,
    ``z`` and parameters ``[0]``, ``[1]``, etc.  The function is rendered as
    an isosurface when drawn.

    Parameters
    ----------
    expression : str
        ROOT TFormula string, e.g. ``"x*x + y*y + z*z"`` or
        ``"[0]*exp(-[1]*(x*x+y*y+z*z))"``.
    xmin, xmax : float
        x-axis domain.
    ymin, ymax : float
        y-axis domain.
    zmin, zmax : float
        z-axis domain.
    params : list[float], optional
        Initial parameter values for ``[0]``, ``[1]``, ...
    param_names : list[str], optional
        Display names for parameters (ROOT TLatex syntax).
    title : str
        Function title.
    xlabel, ylabel, zlabel : str
        Axis labels (ROOT TLatex syntax).
    color : str or int
        Shorthand that sets both fill and line color.  Overridden individually
        by ``fill_color`` / ``line_color``.
    fill_color : str or int, optional
        Isosurface fill color (defaults to ``color``).
    fill_alpha : float
        Isosurface opacity in [0, 1].  0 = invisible, 1 = fully opaque.
        Default 0.5.
    line_color : str or int, optional
        Wireframe edge color (defaults to ``color``).
    line_style : str or int
        Wireframe line style.  See :func:`line_style`.
    line_width : int
        Wireframe line width (default 1).
    draw_mode : str
        Isosurface rendering mode.  One of: ``"iso"`` (default), ``"iso_fb"``,
        ``"iso_bb"``, ``"fb"``, ``"bb"``, ``"gl"``, ``"gl_iso"``,
        ``"gl_col"``, ``"gl_box"``, ``"tf3"``.
    npx, npy, npz : int
        Sampling resolution along each axis (default 30).  Higher values give
        smoother surfaces at the cost of speed.

    Returns
    -------
    ROOT.TF3
        The object also carries a ``_draw_mode`` attribute consumed by
        :func:`draw` to select the correct ROOT draw keyword.

    Examples
    --------
    Semi-transparent Gaussian sphere::

        f = func3d("exp(-(x*x+y*y+z*z)/(2*[0]*[0]))",
                   -4, 4, -4, 4, -4, 4,
                   params=[1.0], param_names=["#sigma"],
                   color="blue", fill_alpha=0.4)
        draw([f], labels=["Gaussian"])

    Wireframe torus::

        f = func3d(
            "(sqrt(x*x+y*y)-[0])^2 + z*z - [1]^2",
            -4, 4, -4, 4, -2, 2,
            params=[2.5, 0.8], param_names=["R", "r"],
            fill_alpha=0.0, line_color="dark_blue", line_width=2,
        )
    """
    if draw_mode not in _TF3_DRAW_MODES:
        raise ValueError(
            f"Unknown draw_mode '{draw_mode}'. "
            f"Available: {list(_TF3_DRAW_MODES)}"
        )

    _color = globals()["color"]
    _ls    = globals()["line_style"]

    base_c = _color(color)
    fc     = _color(fill_color) if fill_color is not None else base_c
    lc     = _color(line_color) if line_color is not None else base_c
    ls     = _ls(line_style)

    f = ROOT.TF3(
        f"f3d_{np.random.randint(10000)}",
        expression,
        xmin, xmax,
        ymin, ymax,
        zmin, zmax,
    )
    f.SetTitle(f"{latex(title)};{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}")

    # Surface fill — use alpha channel when transparency is requested
    if fill_alpha >= 1.0:
        f.SetFillColor(fc)
    else:
        f.SetFillColorAlpha(fc, max(0.0, fill_alpha))

    # Wireframe / edge style
    f.SetLineColor(lc)
    f.SetLineStyle(ls)
    f.SetLineWidth(line_width)

    # Sampling resolution
    f.SetNpx(npx)
    f.SetNpy(npy)
    f.SetNpz(npz)

    # Store the ROOT draw keyword as a private attribute so that
    # _resolve_draw_option() in draw() can retrieve it without extra state.
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
    """
    Fit a histogram or graph with a function and optionally print the results.

    Parameters
    ----------
    graph_or_hist : ROOT.TH1 or ROOT.TGraph-like
        The object to fit.
    func_or_expr : ROOT.TF1 or str
        Either a pre-built ``TF1`` (see :func:`func`) or a ROOT TFormula
        string such as ``"gaus"``, ``"pol2"``, ``"[0]*exp(-[1]*x)"``.
        If a string is given, ``xmin`` and ``xmax`` are required.
    xmin, xmax : float, optional
        Fit range.  Required when ``func_or_expr`` is a string.
    params : list[float], optional
        Initial parameter values (only used when ``func_or_expr`` is a string).
    param_names : list[str], optional
        Parameter display names (only used when ``func_or_expr`` is a string).
    options : str
        ROOT fit options string (default ``"RS"``).
        Common flags: ``"R"`` use function range, ``"S"`` save result,
        ``"Q"`` quiet, ``"L"`` log-likelihood, ``"W"`` ignore errors.
    print_results : bool
        If ``True`` (default), print a formatted parameter table to stdout.
    units : list[str], optional
        Physical units for each parameter, shown in the printed table.

    Returns
    -------
    ROOT.TF1
        The fitted function object (parameters updated in-place).

    Examples
    --------
    >>> f = fit(h, "gaus", xmin=-3, xmax=3)
    >>> f = fit(g, my_tf1, options="RQS", print_results=False)
    """
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
    """
    Print the fitted parameters of a ``TF1`` to stdout in a formatted table.

    Parameters
    ----------
    f : ROOT.TF1
        A function that has already been fitted to data.
    units : list[str], optional
        Physical units for each parameter, e.g. ``["GeV", "GeV", ""]``.
    precision : int
        Number of decimal places (default 6).

    Examples
    --------
    >>> print_params(f, units=["", "GeV/c^{2}", "GeV/c^{2}"])
    """
    fmt = f"{{:.{precision}f}}"
    print("\n" + "=" * 60)
    print("FIT PARAMETERS")
    print("=" * 60)
    for i in range(f.GetNpar()):
        name = f.GetParName(i)
        val  = f.GetParameter(i)
        err  = f.GetParError(i)
        unit = f" [{units[i]}]" if units and i < len(units) else ""
        print(f"  {name}{unit} = {fmt.format(val)} +/- {fmt.format(err)}")
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
    Create and fill a ``TH1D`` from a numpy array.

    Parameters
    ----------
    data : array-like
        One-dimensional array of values to histogram.
    bins : int
        Number of bins (default 50).
    range : (float, float) or None
        Histogram axis range ``(xmin, xmax)``.  If ``None``, the data
        min/max are used.
    title : str
        Histogram title (ROOT TLatex syntax).
    xlabel, ylabel : str
        Axis labels (ROOT TLatex syntax).
    color : str or int
        Line and fill color.  See :func:`color`.
    line_style : str or int
        See :func:`line_style`.
    line_width : int
        Line width in pixels (default 2).
    fill : bool
        If ``True`` (default), fill with a semi-transparent color.
    fill_alpha : float
        Fill opacity in [0, 1] (default 0.3).

    Returns
    -------
    ROOT.TH1D

    Examples
    --------
    >>> h = histogram(data, bins=80, range=(-5, 5),
    ...               xlabel="#Delta E [MeV]", color="blue")
    >>> draw([h], labels=["Run 1"])
    """
    c  = globals()["color"](color)
    ls = globals()["line_style"](line_style)
    xmin = range[0] if range else float(np.min(data))
    xmax = range[1] if range else float(np.max(data))

    h = ROOT.TH1D(
        f"h1_{np.random.randint(10000)}",
        f"{latex(title)};{latex(xlabel)};{latex(ylabel)}",
        bins, xmin, xmax,
    )

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
    """
    Create and fill a ``TH2D`` from two numpy arrays.

    Parameters
    ----------
    x, y : array-like
        Arrays of equal length with the x and y coordinates of each entry.
    bins_x, bins_y : int
        Number of bins along each axis (default 40).
    range_x, range_y : (float, float) or None
        Axis ranges.  If ``None``, data min/max are used.
    title : str
        Histogram title (ROOT TLatex syntax).
    xlabel, ylabel, zlabel : str
        Axis labels (ROOT TLatex syntax).
    palette : int or None
        ROOT color palette code (e.g. ``ROOT.kViridis``).  Defaults to
        ``ROOT.kBird``.

    Returns
    -------
    ROOT.TH2D

    Examples
    --------
    >>> h2 = histogram2d(px, py, bins_x=60, bins_y=60,
    ...                  xlabel="p_{x} [GeV/c]", ylabel="p_{y} [GeV/c]")
    >>> draw([h2])
    """
    xmin = range_x[0] if range_x else float(np.min(x))
    xmax = range_x[1] if range_x else float(np.max(x))
    ymin = range_y[0] if range_y else float(np.min(y))
    ymax = range_y[1] if range_y else float(np.max(y))

    h = ROOT.TH2D(
        f"h2_{np.random.randint(10000)}",
        f"{latex(title)};{latex(xlabel)};{latex(ylabel)};{latex(zlabel)}",
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
    Build legend entries carrying histogram statistics (mean, std dev, counts).

    Used internally by :func:`draw` when ``hist_stats=True``, but can also be
    called manually to build a custom legend via :func:`make_legend`.

    Parameters
    ----------
    h : ROOT.TH1
        The histogram whose statistics are extracted.
    show_mean, show_std, show_counts : bool
        Toggle each statistic (all ``True`` by default).
    precision : int
        Decimal places for the numeric values (default 3).
    mean_label, std_label, counts_label : str
        Label prefixes shown before the ``=`` sign.

    Returns
    -------
    list of (ROOT.TBox, str, str)
        Each tuple is ``(invisible_dummy, label_string, legend_option)`` ready
        for ``TLegend.AddEntry``.
    """
    fmt = f"{{:.{precision}f}}"
    entries = []

    # Invisible dummy object: TLegend.AddEntry requires a TObject even for
    # text-only entries.  A TBox with zero size and no fill/line is invisible.
    def _dummy():
        b = ROOT.TBox(0, 0, 0, 0)
        b.SetFillStyle(0)
        b.SetLineStyle(0)
        return b

    if show_mean:
        entries.append((_dummy(), f"{mean_label} = {fmt.format(h.GetMean())}", ""))
    if show_std:
        entries.append((_dummy(), f"{std_label} = {fmt.format(h.GetStdDev())}", ""))
    if show_counts:
        entries.append((_dummy(), f"{counts_label} = {int(h.GetEntries())}", ""))

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
    Build legend entries carrying fit results (chi², parameters, errors).

    Used internally by :func:`draw` when ``fit_stats=True``, but can also be
    called manually to build a custom legend via :func:`make_legend`.

    Parameters
    ----------
    f : ROOT.TF1
        A function that has already been fitted to data.
    show_chi2 : bool
        Show the chi²/NDF line (default ``True``).
    show_params : bool
        Show one line per parameter (default ``True``).
    show_errors : bool
        Append ``± error`` to each parameter line (default ``True``).
    precision : int
        Decimal places (default 3).
    chi2_label : str
        Label for the chi² line (ROOT TLatex syntax).
    param_names_override : list[str], optional
        Override the parameter names stored in the TF1 (ROOT TLatex syntax).
    units : list[str], optional
        Physical units appended to each parameter line.

    Returns
    -------
    list of (ROOT.TBox, str, str)
        Same format as :func:`hist_stats_entries`.
    """
    fmt = f"{{:.{precision}f}}"
    entries = []

    def _dummy():
        b = ROOT.TBox(0, 0, 0, 0)
        b.SetFillStyle(0)
        b.SetLineStyle(0)
        return b

    if show_chi2:
        ndf   = f.GetNDF()
        chi2  = f.GetChisquare()
        ratio = chi2 / ndf if ndf > 0 else float("nan")
        entries.append((_dummy(),
                        f"{chi2_label} = {fmt.format(chi2)} / {ndf} = {fmt.format(ratio)}",
                        ""))

    if show_params:
        for i in range(f.GetNpar()):
            name = (latex(param_names_override[i])
                    if param_names_override and i < len(param_names_override)
                    else f.GetParName(i))
            val  = f.GetParameter(i)
            err  = f.GetParError(i)
            unit = f" [{units[i]}]" if units and i < len(units) else ""
            label = (f"{name}{unit} = {fmt.format(val)} #pm {fmt.format(err)}"
                     if show_errors
                     else f"{name}{unit} = {fmt.format(val)}")
            entries.append((_dummy(), label, ""))

    return entries


# ─────────────────────────────────────────────────────────────────────────────
#  LEGEND HELPERS
# ─────────────────────────────────────────────────────────────────────────────

# Named anchor positions: (pad_x, pad_y, corner_code).
# Corner code letters: T=top, B=bottom, L=left, R=right, C=center.
_LEGEND_ANCHORS = {
    "top_right":    (0.92,  0.92,  "TR"),
    "top_left":     (0.15,  0.92,  "TL"),
    "bottom_right": (0.92,  0.15,  "BR"),
    "bottom_left":  (0.15,  0.15,  "BL"),
    "top_center":   (0.535, 0.92,  "TC"),
}


def _legend_option(obj) -> str:
    """Return the TLegend entry option string appropriate for the object type."""
    if isinstance(obj, ROOT.TF1):
        return "l"   # line only
    if isinstance(obj, ROOT.TH1):
        return "lf"  # line + fill box
    return "lep"     # line + error bars + point (graphs)


def make_legend(
    objects: list,
    labels: list[str],
    pos: str | tuple = "top_right",
    ncols: int = 1,
    text_size: float = 0.038,
    width: float = 0.25,
    row_height: float = 0.045,
    margin: float = 0.30,
    border: int = 0,
    fill_alpha: float = 0.0,
) -> ROOT.TLegend:
    """
    Create a ``TLegend`` from a list of ROOT objects and label strings.

    This is a lower-level helper; :func:`draw` creates the legend automatically
    when ``labels`` is provided.  Use ``make_legend`` when you need full manual
    control over a legend that lives outside a :func:`draw` call.

    Parameters
    ----------
    objects : list
        ROOT objects (TGraph, TH1, TF1, ...) to register in the legend.
    labels : list[str]
        Label string for each object (ROOT TLatex syntax).
    pos : str or (x1, y1, x2, y2)
        Named position (``"top_right"``, ``"top_left"``, ``"bottom_right"``,
        ``"bottom_left"``, ``"top_center"``) or explicit NDC coordinates.
    ncols : int
        Number of legend columns (default 1).
    text_size : float
        Text size in NDC units (default 0.038).
    width : float
        Legend box width in NDC units (default 0.25).
    row_height : float
        Height of each legend row in NDC units (default 0.045).
    margin : float
        Fraction of the entry width reserved for the symbol (default 0.30).
    border : int
        Border size in pixels (default 0 = no border).
    fill_alpha : float
        Background opacity in [0, 1] (default 0 = transparent).

    Returns
    -------
    ROOT.TLegend

    Examples
    --------
    >>> leg = make_legend([g1, g2], ["Signal", "Background"],
    ...                   pos="top_right", width=0.30)
    >>> leg.Draw()
    """
    n_entries = len(objects)
    n_rows    = int(np.ceil(n_entries / ncols))
    total_w   = width
    total_h   = n_rows * row_height

    if isinstance(pos, tuple):
        x1, y1, x2, y2 = pos
    elif pos in _LEGEND_ANCHORS:
        ax, ay, corner = _LEGEND_ANCHORS[pos]
        y2 = ay if "T" in corner else ay + total_h
        y1 = y2 - total_h
        if "R" in corner:
            x2, x1 = ax, ax - total_w
        elif "L" in corner:
            x1, x2 = ax, ax + total_w
        else:
            x1, x2 = ax - total_w / 2, ax + total_w / 2
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

# Frozenset of all recognized line-style names.  Used in _resolve_draw_option
# to detect when a per-object option string is a style shorthand rather than
# a raw ROOT draw keyword.
_LINE_STYLE_NAMES: frozenset[str] = frozenset(_LINE_STYLES.keys())


def _auto_draw_option(obj, first: bool, base: str) -> str:
    """
    Return the automatic ROOT draw option string for *obj*.

    The option depends on the object type and whether it is the first object
    drawn (which is responsible for creating the canvas axes).

    Parameters
    ----------
    obj   : ROOT object.
    first : True if this is the first object drawn on the canvas.
    base  : Global fallback option string (e.g. ``"AP"``), used for graphs.
    """
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

    Merges the per-object override (if any) from the ``options`` list with
    the automatic fallback from :func:`_auto_draw_option`.

    Parameters
    ----------
    obj      : ROOT object being drawn.
    per_item : Per-object option from the ``options`` list, or ``None``.
    first    : True if this is the first object drawn.
    base     : Global fallback draw string (e.g. ``"AP"``).

    Resolution rules
    ----------------
    ``None``
        Delegate entirely to :func:`_auto_draw_option`.
    Line-style name (e.g. ``"dotted"``, ``"dashed"``)
        Apply the style to the object via ``SetLineStyle``, then delegate to
        :func:`_auto_draw_option`.  This lets you change a line style at draw
        time without re-creating the object.
    Any other string (e.g. ``"AP"``, ``"HIST"``, ``"COLZ"``)
        Use verbatim as the ROOT draw option.  ``"SAME"`` is appended
        automatically for non-first objects; ``"A"`` is stripped from graph
        options so axes are not re-drawn.
    """
    if per_item is None:
        return _auto_draw_option(obj, first, base)

    key = per_item.strip().lower().replace(" ", "_").replace("-", "_")

    # Line-style shorthand: apply in-place, then fall back to auto option
    if key in _LINE_STYLE_NAMES:
        obj.SetLineStyle(_LINE_STYLES[key])
        return _auto_draw_option(obj, first, base)

    # Raw ROOT draw string
    opt = per_item.strip()
    if not first and "SAME" not in opt.upper():
        # Strip "A" so the axis frame is not redrawn by subsequent objects
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

    This is the main entry point for producing plots.  It handles draw order,
    axis labelling, log scales, legend creation, optional statistics display,
    and saving to file — all in one call.

    Parameters
    ----------
    objects : list
        ROOT objects to draw (TGraphErrors, TH1D, TF1, TH2D, TF3, ...).
        Mixed types are supported.
    labels : list[str] or None
        One label per object (ROOT TLatex syntax).  Providing ``labels``
        automatically creates and draws a legend.  Pass ``None`` to suppress.
    xlabel, ylabel : str or None
        Override the axis titles on the primary (first non-TF1) object.
        Useful when the title was not set at object creation time.
    xrange, yrange : (float, float) or None
        Visible axis range, e.g. ``xrange=(0, 10)``.
    options : str or list[str or None]
        Draw options.  A single string is used as global fallback for all
        graph-like objects.  A list allows per-object control:

        - ``None`` -- auto-detect from object type (default behaviour).
        - Line-style name (``"dotted"``, ``"dashed"``, ...) -- apply in-place
          and draw normally.
        - Any ROOT draw string (``"AP"``, ``"HIST"``, ``"COLZ"``, ...) --
          used verbatim; ``"SAME"`` appended automatically when needed.

    width, height : int
        Canvas dimensions in pixels (default 900 x 600).
    log_x, log_y : bool
        Logarithmic scale on x or y axis.

    Legend parameters
    -----------------
    legend_pos : str or (x1, y1, x2, y2)
        Named anchor (``"top_right"``, ``"top_left"``, ``"bottom_right"``,
        ``"bottom_left"``, ``"top_center"``) or explicit NDC coordinates.
    legend_width : float
        Legend box width in NDC units (default 0.25).
    legend_row_height : float
        Height of each legend row in NDC units (default 0.045).  Increase for
        more row spacing; decrease to compact a tall legend.
    legend_ncols : int
        Number of columns in the legend (default 1).
    legend_text_size : float
        Legend text size in NDC units (default 0.038).
    legend_margin : float
        Fraction of each entry width reserved for the symbol (default 0.25).
    legend_border : int
        Legend border size in pixels (default 0 = no border).
    legend_fill_alpha : float
        Legend background opacity in [0, 1] (default 0 = transparent).

    Histogram statistics in legend
    --------------------------------
    hist_stats : bool
        Append mean, std dev, and entry count for each TH1 (default ``False``).
    hist_stats_precision : int
        Decimal places for stat values (default 3).
    hist_stats_show_mean, hist_stats_show_std, hist_stats_show_counts : bool
        Toggle individual statistics independently.
    hist_stats_mean_label, hist_stats_std_label, hist_stats_counts_label : str
        Customisable label prefixes for each statistic.

    Fit statistics in legend
    -------------------------
    fit_stats : bool
        Append chi², NDF, and parameter values for each TF1 (default ``False``).
    fit_stats_precision : int
        Decimal places (default 3).
    fit_stats_show_chi2, fit_stats_show_params, fit_stats_show_errors : bool
        Toggle chi², parameter values, and error display independently.
    fit_stats_chi2_label : str
        Label for the chi²/NDF legend line (ROOT TLatex syntax).
    fit_stats_param_names : list[str], optional
        Override parameter names shown in the legend (ROOT TLatex syntax).
    fit_stats_units : list[str], optional
        Physical units for each parameter in the legend.

    Output
    ------
    save : str or None
        If provided, save the canvas to this path.  The format is inferred
        from the extension (e.g. ``".pdf"``, ``".png"``, ``".root"``).

    Returns
    -------
    canvas : ROOT.TCanvas
    legend : ROOT.TLegend or None

    Examples
    --------
    Graph + Gaussian fit with statistics in legend::

        c, leg = draw([g, f],
                      labels=["Data", "Gaussian fit"],
                      xlabel="m_{#pi#pi} [MeV/c^{2}]",
                      ylabel="Events / 10 MeV",
                      fit_stats=True,
                      save="mass_fit.pdf")

    Mixed object types with per-object draw options::

        draw([g1, g2, h2d], options=["AP", "dashed", "COLZ"])

    Two-column legend with opaque white background::

        draw([h1, h2, h3, h4], labels=[...],
             legend_ncols=2, legend_fill_alpha=1.0, legend_border=1)
    """
    canvas = ROOT.TCanvas(f"c_{np.random.randint(10000)}", "", width, height)
    if log_x:
        canvas.SetLogx()
    if log_y:
        canvas.SetLogy()

    # ── normalise options to a per-object list ────────────────────────────
    if isinstance(options, list):
        # When a list is supplied, use "AP" as the internal global base for
        # any graph-like object that has no explicit per-object override.
        global_base = "AP"
        per_obj_opts: list[str | None] = list(options)
        # Pad with None so indexing never raises IndexError
        while len(per_obj_opts) < len(objects):
            per_obj_opts.append(None)
    else:
        global_base = options
        per_obj_opts = [None] * len(objects)

    # ── draw order: non-TF1 first so the frame/axes are created early ─────
    # A bare TF1 cannot create axes on its own; drawing it first would
    # produce a blank frame.  We find the first non-TF1 object and promote
    # it to the front of the draw queue.
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

    # ── axis title overrides ──────────────────────────────────────────────
    # The "primary" object owns the axes; all overrides are applied to it.
    primary = objects[first_graph_idx] if first_graph_idx is not None else objects[0]
    if xlabel is not None:
        primary.GetXaxis().SetTitle(latex(xlabel))
    if ylabel is not None:
        primary.GetYaxis().SetTitle(latex(ylabel))

    if xrange is not None:
        primary.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    if yrange is not None:
        primary.GetYaxis().SetRangeUser(yrange[0], yrange[1])

    # ── legend ────────────────────────────────────────────────────────────
    legend = None
    if labels:
        converted_labels = [latex(lbl) for lbl in labels]

        # Pre-collect optional stat entries so their count is known before the
        # legend box dimensions are computed.
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

        # Compute legend box height from total number of rows
        n_total_entries = len(objects) + n_stat_rows
        total_h = int(np.ceil(n_total_entries / legend_ncols)) * legend_row_height
        total_w = legend_width

        # Resolve NDC coordinates from the position argument
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

        # Add main entries, then any stat sub-entries immediately after each object
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
    """
    Load a single column from a delimited text file into a numpy array.

    Parameters
    ----------
    filepath : str
        Path to the file.
    column : str or int
        Column name (requires a header row) or zero-based integer index.
    sep : str
        Column separator regex (default ``r"\\s+"`` for whitespace-delimited).

    Returns
    -------
    np.ndarray

    Examples
    --------
    >>> x = load_column("data.txt", 0)                        # by index
    >>> y = load_column("data.csv", "voltage", sep=",")       # by name
    """
    df = pd.read_csv(filepath, sep=sep, engine="python")
    return df.iloc[:, column].to_numpy() if isinstance(column, int) else df[column].to_numpy()


def load_columns(
    filepath: str,
    columns: list[str | int],
    sep: str = r"\s+",
) -> list[np.ndarray]:
    """
    Load multiple columns from a delimited text file.

    Parameters
    ----------
    filepath : str
        Path to the file.
    columns : list of str or int
        Column names or zero-based indices, in the desired order.
    sep : str
        Column separator regex (default whitespace).

    Returns
    -------
    list of np.ndarray
        One array per requested column, in the same order as ``columns``.

    Examples
    --------
    >>> x, y, ey = load_columns("data.txt", [0, 1, 2])
    """
    return [load_column(filepath, col, sep) for col in columns]


def load_row(
    filepath: str,
    row: int = 0,
    sep: str = r"\s+",
) -> np.ndarray:
    """
    Load a single row from a delimited text file into a numpy array.

    Useful when each line of the file is a spectrum or a set of measurements.
    If the file has exactly one non-empty line (no header), that line is split
    directly without pandas.

    Parameters
    ----------
    filepath : str
        Path to the file.
    row : int
        Zero-based row index (default 0).
    sep : str
        Column separator regex (default whitespace).

    Returns
    -------
    np.ndarray

    Examples
    --------
    >>> spectrum = load_row("spectrum.txt", row=0)
    """
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
    """
    Load multiple rows from a delimited text file.

    Parameters
    ----------
    filepath : str
        Path to the file.
    rows : list of int
        Zero-based row indices.
    sep : str
        Column separator regex (default whitespace).

    Returns
    -------
    list of np.ndarray
        One array per requested row, in the same order as ``rows``.

    Examples
    --------
    >>> row0, row5 = load_rows("matrix.txt", [0, 5])
    """
    df = pd.read_csv(filepath, sep=sep, engine="python", header=None)
    return [df.iloc[r].to_numpy(dtype=float) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
#  MAPS  (2D pixel / detector maps)
# ─────────────────────────────────────────────────────────────────────────────

def map_from_arrays(
    col,
    row,
    values,
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "Value",
    palette: int = None,
) -> ROOT.TH2D:
    """
    Build a ``TH2D`` pixel/detector map from three equal-length arrays.

    Bin edges are computed automatically from the unique values of ``col``
    and ``row``, so the map works correctly even for non-uniform pitch.

    Parameters
    ----------
    col, row : array-like
        Integer or float pixel/strip coordinates for each measurement.
    values : array-like
        Measurement value for each (col, row) pair.
    xlabel, ylabel, zlabel : str
        Axis labels (ROOT TLatex syntax).
    palette : int or None
        ROOT color palette (e.g. ``ROOT.kViridis``).  Defaults to
        ``ROOT.kBird``.

    Returns
    -------
    ROOT.TH2D

    Examples
    --------
    >>> h = map_from_arrays(col, row, charge,
    ...                     xlabel="Column", ylabel="Row",
    ...                     zlabel="Charge [e^{-}]")
    >>> draw([h])
    """
    if palette is None:
        palette = ROOT.kBird

    col    = np.asarray(col,    dtype=float)
    row    = np.asarray(row,    dtype=float)
    values = np.asarray(values, dtype=float)

    ucol = np.unique(col)
    urow = np.unique(row)
    nx, ny = len(ucol), len(urow)

    def _edges(u):
        """Compute bin edges centered on the unique coordinate values in *u*."""
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
    filepath: str,
    col_col: str | int = 0,
    col_row: str | int = 1,
    col_val: str | int = 2,
    sep: str = r"\s+",
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "Value",
    palette: int = None,
) -> ROOT.TH2D:
    """
    Build a ``TH2D`` pixel/detector map directly from a delimited text file.

    A convenience wrapper around :func:`map_from_arrays` that reads the
    column, row, and value arrays from a file.

    Parameters
    ----------
    filepath : str
        Path to the delimited file.
    col_col, col_row, col_val : str or int
        Column names or zero-based indices for the column coordinate, row
        coordinate, and measurement value respectively.
    sep : str
        Column separator regex (default whitespace).
    xlabel, ylabel, zlabel : str
        Axis labels (ROOT TLatex syntax).
    palette : int or None
        ROOT color palette.  Defaults to ``ROOT.kBird``.

    Returns
    -------
    ROOT.TH2D

    Examples
    --------
    >>> h = map_from_file("scan.txt",
    ...                   col_col=0, col_row=1, col_val=2,
    ...                   xlabel="Strip", ylabel="Channel",
    ...                   zlabel="Efficiency")
    >>> draw([h])
    """
    df = pd.read_csv(filepath, sep=sep, engine="python")

    def _get(key):
        return df.iloc[:, key].to_numpy() if isinstance(key, int) else df[key].to_numpy()

    return map_from_arrays(
        _get(col_col), _get(col_row), _get(col_val),
        xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, palette=palette,
    )