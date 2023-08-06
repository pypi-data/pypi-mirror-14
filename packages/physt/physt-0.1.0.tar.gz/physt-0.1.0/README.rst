physt
=====

P(i/y)thon h(i/y)stograms. Inspired (and based on) numpy.histogram, but
designed for humans(TM) on steroids(TM).

The goal is to unify different concepts of histograms as occurring in
numpy, pandas, matplotlib, ROOT, etc. and to create one representation
that is easily manipulated with from the data point of view and at the
same time provides nice integration into IPython notebook and various
plotting options. In short, whatever you want to do with histograms,
**physt** aims to be at your side.

Simple example
--------------

.. code:: python

    from physt import histogram

    heights = [160, 155, 156, 198, 177, 168, 191, 183, 184, 179, 178, 172, 173, 175,
               172, 177, 176, 175, 174, 173, 174, 175, 177, 169, 168, 164, 175, 188,
               178, 174, 173, 181, 185, 166, 162, 163, 171, 165, 180, 189, 166, 163,
               172, 173, 174, 183, 184, 161, 162, 168, 169, 174, 176, 170, 169, 165]
               
    hist = histogram(heights, 10)
    hist.plot()

.. figure:: doc/heights.png
   :alt: Heights plot

   Heights plot
See more in
https://github.com/janpipek/physt/blob/master/doc/Tutorial.ipynb

Installation
------------

``pip install physt``

Features
--------

Implemented
~~~~~~~~~~~

-  1D histograms
-  Input: any numpy-array-like object
-  Keep underflow / overflow
-  Basic numeric operations (\* / + -)
-  Items / slice selection (including mask arrays)
-  Add new values (fill)
-  Cumulative values, densities
-  Simple plotting (matplotlib)

Planned
~~~~~~~

-  Algorithms for optimized binning
-  human-friendly
-  mathematical
-  Rebinning
-  using reference to original data
-  merging bins
-  Statistics (based on original data)?
-  Stacked histograms (with names)
-  Input: pandas.Series, pandas.DataFrame, ...
-  More plotting backends
-  2D histograms, (ND)-histograms

