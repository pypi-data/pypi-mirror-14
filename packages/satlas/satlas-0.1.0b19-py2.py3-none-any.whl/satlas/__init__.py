from .version import __version__, __release__
import matplotlib as mpl
from . import hfsmodel
from .hfsmodel import *
from . import transformmodel
from .transformmodel import *
from . import models
from .models import *
from . import linkedmodel
from .linkedmodel import *
from . import summodel
from .summodel import *
from . import utilities
from .utilities import *
from . import fitting
from .fitting import *
from . import loglikelihood
from .loglikelihood import *

from . import combinedmodel
from .combinedmodel import *
from . import multimodel
from .multimodel import *

__all__ = []

__all__.extend(hfsmodel.__all__)
__all__.extend(transformmodel.__all__)
__all__.extend(models.__all__)
__all__.extend(linkedmodel.__all__)
__all__.extend(summodel.__all__)
__all__.extend(utilities.__all__)
__all__.extend(fitting.__all__)
__all__.extend(combinedmodel.__all__)
__all__.extend(summodel.__all__)

style = {'backend': 'qt4agg',
         'lines.linewidth': 3,
         'lines.linestyle': '-',
         'lines.marker': None,
         'lines.markeredgewidth': 0,
         'lines.markersize': 6,
         'lines.dash_joinstyle': 'miter',
         'lines.dash_capstyle': 'butt',
         'lines.solid_joinstyle': 'miter',
         'lines.solid_capstyle': 'projecting',
         'lines.antialiased': True,
         'font.family': 'serif',
         'font.style': 'normal',
         'font.variant': 'normal',
         'font.weight': 'medium',
         'font.stretch': 'normal',
         'font.size': 12.0,
         'font.serif': ['Palatino Linotype', 'New Century Schoolbook', 'Century Schoolbook L', 'Utopia', 'ITC Bookman', 'Bookman', 'Nimbus Roman No9 L', 'Times New Roman', 'Times', 'Palatino', 'Charter', 'serif'],
         'font.sans-serif': ['Arial', 'Bitstream Vera Sans', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif'],
         'font.cursive': ['Apple Chancery', 'Textile', 'Zapf Chancery', 'Sand', 'Script MT', 'Felipa', 'cursive'],
         'font.fantasy': ['Comic Sans MS', 'Chicago', 'Charcoal', 'Impact', 'Western', 'Humor Sans', 'fantasy'],
         'font.monospace': ['Bitstream Vera Sans Mono', 'Andale Mono', 'Nimbus Mono L', 'Courier New', 'Courier', 'Fixed', 'Terminal', 'monospace'],
         'text.color': 'k',
         'text.usetex': False,
         'text.latex.unicode': True,
         'text.dvipnghack': None,
         'text.hinting': 'auto',
         'text.hinting_factor': 8,
         'text.antialiased': True,
         'axes.hold': True,
         'axes.facecolor': 'w',
         'axes.edgecolor': 'k',
         'axes.linewidth': 1.0,
         'axes.grid': True,
         'axes.titlesize': 18,
         'axes.labelsize': 14,
         'axes.labelweight': 'normal',
         'axes.labelcolor': 'k',
         'axes.axisbelow': False,
         'axes.formatter.limits': (-3, 4),
         'axes.formatter.use_locale': False,
         'axes.formatter.use_mathtext': True,
         'axes.formatter.useoffset': False,
         'axes.unicode_minus': True,
         'axes.color_cycle': ['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#F0E442', '#56B4E9'],
         'axes.xmargin': 0,
         'axes.ymargin': 0,
         'polaraxes.grid': True,
         'axes3d.grid': True,
         'xtick.major.size': 4,
         'xtick.minor.size': 2,
         'xtick.major.width': 0.5,
         'xtick.minor.width': 0.5,
         'xtick.major.pad': 4,
         'xtick.minor.pad': 4,
         'xtick.color': 'k',
         'xtick.labelsize': 12,
         'xtick.direction': 'in',
         'ytick.major.size': 4,
         'ytick.minor.size': 2,
         'ytick.major.width': 0.5,
         'ytick.minor.width': 0.5,
         'ytick.major.pad': 4,
         'ytick.minor.pad': 4,
         'ytick.color': 'k',
         'ytick.labelsize': 12,
         'ytick.direction': 'in',
         'grid.color': '0.75',
         'grid.linestyle': '-',
         'grid.linewidth': 0.5,
         'grid.alpha': 0.5,
         'legend.fancybox': True,
         'legend.isaxes': True,
         'legend.numpoints': 1,
         'legend.fontsize': 12,
         'legend.borderpad': 0.5,
         'legend.markerscale': 1.0,
         'legend.labelspacing': 0.5,
         'legend.handlelength': 2.,
         'legend.handleheight': 0.7,
         'legend.handletextpad': 0.8,
         'legend.borderaxespad': 0.5,
         'legend.columnspacing': 2.,
         'legend.shadow': True,
         'legend.frameon': True,
         'legend.framealpha': 1.0,
         'legend.scatterpoints': 1,
         'figure.figsize': (8, 6),
         'figure.dpi': 80,
         'figure.facecolor': 'w',
         'figure.edgecolor': 'w',
         'figure.autolayout': False,
         'figure.max_open_warning': 20,
         'figure.subplot.left': 0.125,
         'figure.subplot.right': 0.9,
         'figure.subplot.bottom': 0.1,
         'figure.subplot.top': 0.9,
         'figure.subplot.wspace': 0.2,
         'figure.subplot.hspace': 0.2,
         'image.aspect': 'auto',
         'image.interpolation': 'bilinear',
         'image.cmap': 'gnuplot2_r',
         'image.lut': 256,
         'image.origin': 'lower',
         'image.resample': False,
         'contour.negative_linestyle': 'dashed',
         'path.simplify': True,
         'path.simplify_threshold': 0.1,
         'path.snap': True,
         'path.sketch': None,
         'savefig.dpi': 100,
         'savefig.facecolor': 'w',
         'savefig.edgecolor': 'w',
         'savefig.format': 'pdf',
         'savefig.bbox': 'tight',
         'savefig.pad_inches': 0.1,
         'savefig.jpeg_quality': 95,
         'savefig.directory': '',
         'savefig.transparent': False}
for key in style:
    mpl.rcParams[key] = style[key]
