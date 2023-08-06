.. Bob skin color filter documentation master file, created by
   sphinx-quickstart on Mon Apr  4 14:15:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _bob.ip.skincolorfilter:


========================
 Bob's Skin Color Filter
========================

This module contains the implementation of the skin color filter described in [taylor-spie-2014]_.
The skin color is modeled as a 2-dimensional gaussian in the normalised rg colorspace. Note that
the estimation of the gaussian parameters should be done using a cropped face image. As a consequence,
this pacakge depends on the Bob's face detection package.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   guide
   py_api


References
----------

.. [taylor-spie-2014]  *M.J. Taylor and T. Morris*. **Adaptive skin segmentation via feature-based face detection,** Proc SPIE Photonics Europe, 2014. `pdf <http://www.cs.man.ac.uk/~tmorris/pubs/AdaptSS_SPIE.pdf>`__

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
