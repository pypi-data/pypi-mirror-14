.. py:currentmodule:: bob.ip.skincolorfilter

.. testsetup:: *

   from __future__ import print_function
   import bob.io.base
   import bob.io.base.test_utils
   import bob.io.image
   import bob.ip.facedetect
   import bob.ip.skincolorfilter

   import pkg_resources
   face_image = bob.io.base.load(bob.io.base.test_utils.datafile('test-face.jpg', 'bob.ip.skincolorfilter'))

=============
 User Guide
=============

This skin color filter relies on the result of face detection, hence you might want to
use :py:mod:`bob.ip.facedetect` (and in particular :py:func:`bob.ip.facedetect.detect_single_face`) 
to first detect a face in the image. 

The skin color distribution is modeled as a bivariate gaussian in the normalised rg colorspace. 
The parameters of the distribution are estimated from a circular region centered on the face,
where extreme luma values have been eliminated (see [taylor-spie-2014]_ for details). 


Skin pixels detection in a single image
---------------------------------------

The function to detect skin pixels will return a mask (logical numpy array of the
same size of the image) where location corresponding to skin color pixels is True.
Hence, to detect skin pixels inside a face image, you should do the following:

.. doctest::

   >>> face_image = bob.io.base.load('test-face.jpg') # doctest: +SKIP
   >>> detection = bob.ip.facedetect.detect_single_face(face_image)
   >>> bounding_box, quality = bob.ip.facedetect.detect_single_face(face_image)
   >>> face = face_image[:, bounding_box.top:bounding_box.bottom, bounding_box.left:bounding_box.right]
   >>> skin_filter = bob.ip.skincolorfilter.SkinColorFilter()
   >>> skin_filter.estimate_gaussian_parameters(face)
   >>> skin_mask = skin_filter.get_skin_mask(face_image, 0.5)


.. plot:: plot/detect_skin_pixels.py
   :include-source: False

Picture taken from https://stocksnap.io/photo/W7GS1022QN

Skin pixels detection in videos
-------------------------------
To detect skin pixels in video, you do not need to re-estimate the gaussian parameters at each frame.
However, you can do it by calling :py:meth:`SkinColorFilter.estimate_gaussian_parameters`.

