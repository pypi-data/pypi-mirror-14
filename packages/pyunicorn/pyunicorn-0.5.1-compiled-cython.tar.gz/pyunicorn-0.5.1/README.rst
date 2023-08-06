
pyunicorn
=========

``pyunicorn`` (**Uni**\ fied **Co**\ mplex Network and **R**\ ecurre\ **N**\ ce
analysis toolbox) is a fully object-oriented Python package for the advanced
analysis and modeling of complex networks. Above the standard measures of
complex network theory such as degree, betweenness and clustering coefficient
it provides some **uncommon but interesting statistics** like Newman's random
walk betweenness. ``pyunicorn`` features novel **node-weighted (node splitting
invariant)** network statistics as well as measures designed for analyzing
**networks of interacting/interdependent networks**.

Moreover, ``pyunicorn`` allows to easily **construct networks from uni- and
multivariate time series data** (functional (climate) networks and recurrence
networks). This involves linear and nonlinear measures of time series analysis
for constructing functional networks from multivariate data as well as modern
techniques of nonlinear analysis of single time series like recurrence
quantification analysis (RQA) and recurrence network analysis.

Code
----
`Stable releases <https://github.com/pik-copan/pyunicorn/releases>`_,
`Development version <https://github.com/pik-copan/pyunicorn>`_

`Changelog <docs/source/changelog.rst>`_, `Contributions <CONTRIBUTIONS.rst>`_

Documentation
-------------
For extensive HTML documentation, jump right to the `pyunicorn homepage
<http://www.pik-potsdam.de/~donges/pyunicorn/>`_. Recent `PDF versions
<http://www.pik-potsdam.de/~donges/pyunicorn/docs/>`_ are also available.

On a local development version, HTML and PDF documentation can be generated
using ``Sphinx``::

    $> pip install --user -e .
    $> cd docs; make clean html latexpdf

Dependencies
------------
``pyunicorn`` relies on the following open source or freely available packages
which have to be installed on your machine.

Required:
  - `Numpy <http://numpy.scipy.org/>`_ 1.8+
  - `Scipy <http://www.scipy.org/>`_ 0.14+
  - `Weave <https://github.com/scipy/weave>`_ 0.15+
  - `igraph, python-igraph <http://igraph.sourceforge.net/>`_ 0.7+

Optional *(used only in certain classes and methods)*:
  - `PyNGL <http://www.pyngl.ucar.edu/Download/>`_ (for class NetCDFDictionary)
  - `netcdf4-python <http://code.google.com/p/netcdf4-python/>`_ (for classes
    Data and NetCDFDictionary)
  - `Matplotlib <http://matplotlib.sourceforge.net>`_ 1.3+
  - `Matplotlib Basemap Toolkit <http://matplotlib.org/basemap/>`_ (for drawing
    maps)
  - `mpi4py <http://code.google.com/p/mpi4py/>`_ (for parallelizing costly
    computations)
  - `Sphinx <http://sphinx-doc.org/>`_ (for generating documentation)
  - `Cython <http://cython.org/>`_ 0.21+ (for compiling code during
    development)

Installing
----------
**Stable release**
    Via the Python Package Index::

        $> pip install pyunicorn

**Development version**
    For a simple system-wide installation::

        $> pip install .

    Depending on your system, you may need root privileges. On UNIX-based
    operating systems (Linux, Mac OS X etc.) this is achieved with ``sudo``.

    For development, especially if you want to test ``pyunicorn`` from within
    the source directory::

        $> pip install --user -e .

Test suite
----------
Before committing changes to the code base, please make sure that all tests
pass. The test suite is managed by `tox <https://testrun.org/tox/>`_ and
configured to use system-wide packages when available. Thus to avoid frequent
waiting, we recommend you to install the current versions of the following
packages::

    $> pip install tox nose networkx Sphinx
    $> pip install pylint pytest pytest-xdist pytest-flakes pytest-pep8

The test suite can be run from anywhere in the project tree by issuing::

    $> tox

To expose the defined test environments and target them independently::

    $> tox -l
    $> tox -e py27-units,py27-pylint

To test single files::

    $> tests/test_doctests.py core.network      # doctests
    $> nosetests -vs tests/core/TestNetwork.py  # unit tests
    $> pylint pyunicorn/core/network.py         # code analysis
    $> py.test pyunicorn/core/network.py        # style

Mailing list
------------
Not implemented yet.

Reference
---------
Please acknowledge and cite the use of this software and its authors when
results are used in publications or published elsewhere. You can use the
following reference:

    J.F. Donges, J. Heitzig, B. Beronov, M. Wiedermann, J. Runge, Q.-Y. Feng, L. Tupikina, V. Stolbova, R.V. Donner, N. Marwan, H.A. Dijkstra, and J. Kurths,
    Unified functional network and nonlinear time series analysis for complex systems science: The pyunicorn package,
    `Chaos 25, 113101 (2015), doi:10.1063/1.4934554,
    <http://dx.doi.org/10.1063/1.4934554>`_
    `Preprint: arxiv.org:1507.01571 [physics.data-an].
    <http://arxiv.org/abs/1507.01571>`_

License
-------
``pyunicorn`` is `BSD-licensed <LICENSE.txt>`_ (3 clause).
