This library provides Python functions for hierarchical clustering. It
generates hierarchical clusters from distance matrices or from vector data.

Part of this module is intended to replace the functions ::

    linkage, single, complete, average, weighted, centroid, median, ward

in the module ``scipy.cluster.hierarchy`` with the same functionality but much
faster algorithms. Moreover, the function ``linkage_vector`` provides
memory-efficient clustering for vector data.

The interface is very similar to MATLAB's Statistics Toolbox API to make code
easier to port from MATLAB to Python/NumPy. The core implementation of this
library is in C++ for efficiency.

**User manual:** `fastcluster.pdf
<https://github.com/dmuellner/fastcluster/raw/master/docs/fastcluster.pdf>`_.

Installation files for Windows are provided on `PyPI
<https://pypi.python.org/pypi/fastcluster>`_ and on `Christoph Gohlke's web
page <http://www.lfd.uci.edu/~gohlke/pythonlibs/#fastcluster>`_.

**The fastcluster package is considered stable and will undergo few changes
from now on. If some years from now there have not been any updates, this
does not necessarily mean that the package is unmaintained but maybe it just
was not necessary to correct anything. Of course, please still report potential
bugs and incompatibilities to daniel@danifold.net.**

Reference: Daniel Müllner, *fastcluster: Fast Hierarchical, Agglomerative
Clustering Routines for R and Python*, Journal of Statistical Software, **53**
(2013), no. 9, 1–18, http://www.jstatsoft.org/v53/i09/.


