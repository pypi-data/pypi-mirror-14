tinfiltering
============

This is the tinfiltering package, created to perform the automated filtering of 2D data points, based on the edges distance distribution of a Delaunay triangulation.

The methodology upon which this package is based on the initial steps of the algorithm proposed by Yang and Cui (2010) in the paper "A Novel Spatial Clustering Algorithm Based on Delaunay Triangulation".

This package was developed while in my PhD research in the Department of Geography at University College London, supervised by Dr Mat Disney (Earth Observation/Remote Sensing).

If you have any problem, question or suggestion, please, don't hesitate to contact the author.


Usage as module
---------------

	>>> import tinfiltering
	>>> tinfiltering.apply_filter(x, y)



Parameters
''''''''''
    x, y: list or numpy.ndarray
	Coordinates for the set of points to be filtered.

Returns
'''''''
    out_points: 2D numpy.ndarray
	Coordinates for the filtered set of points.

Raises
''''''
    ValueError
        If input is the wrong shape or type (the inputs must be a 1-D array or
        list).


Usage in console
----------------

	>>> tinfiltering in_filename out_filename

Parameters
''''''''''
    in_filename: str
            Name of the file containing the numpy array point data to be
            filtered.
    out_filename: str
            Name of the file to save the numpy array of filtered point data.


Packages
========

* tinfiltering
* tinfiltering.test
* tinfiltering.tin
* Version 0.1.2

Dependencies
============

* numpy
* scipy
* sys
* os

Author
======

* Matheus Boni Vicari (@matt_bv)

Who do I talk to?
-----------------

* Matheus Boni Vicari (matheus.boni.vicari@gmail.com or matheus.vicari.15@ucl.ac.uk)


References
==========

    .. [1] X. Yang and W. Cui, "A Novel Spatial Clustering Algorithm Based on
           Delaunay Triangulation," Journal of Software Engineering and
           Applications, Vol. 3 No. 2, 2010, pp. 141-149. doi:
           10.4236/jsea.2010.32018.
