thLib - Documentation
=====================

*thLib* is a library for scientific data analysis, with a focus on 3d
kinematics.

*quat*  Functions for working with quaternions:
    - quaternion multiplication, inversion, conjugate
    - conversions to rotation matrices, axis angles, vectors
    - a *Quaternion* class, including operator overloading for multiplication
      and division
    - also work on data arrays

*rotmat*  Functions for working with rotation matrices
    - rotation matrices for rotations about the x-, y-, and z-axis
    - symbolic rotation matrices
    - conversions to Euler, Fick, Helmholtz angles

*vector*  Functions for working with vectors
    - angle between vectors
    - Gram-Schmidt orthogonalization
    - projection
    - normalization
    - rotation
    - also work on data arrays

*imus*  Analysis routines for IMU-recordings
    - calculation of orientation from velocity, recorded with IMUs or
      space-fixed systems (four different algorithms are implemente here:

      - simple quaternion integration
      - a quaternion Kalman filter
      - Madgwick's algorithm
      - Mahony's algorithm

    - calculation of position and orientation from IMU-signals
    - utility to read in data from an XSens system

*markers*  Analysis routines for 3D movements from marker-based video recordings
    - a function that takes recordings from video-systems (e.g. Optotrak)
      and calculates position and orientation
    - calculation of joint movements from marker recordings

*fits*  Contains examples for a number of fitting applications, for fitting
    - lines
    - circles (with RANSAC, or directly)
    - exponential decays
    - sine waves
    - ellipses
    - regressions (including confidence intervals)

*signals*  Has functions that manipulate data
    - a Savitzky-Golay for data smoothing and derivatives
    - a power spectrum
    - a function to calculate and show mean and standard error for
      time series data.
    - a visualization for cross- and auto-correlations

*sounds*  Allows you to work with sounds in Python. Note that to use it with (almost) arbitrary sound-files, you need to have FFMPEG installed. The class *Sound* lets you
    - read sounds
    - play sounds
    - write sounds
    - define *Sound*-objects

*ui*  Provides GUIs for
    - file- and directory selection, and for saving files
    - a listbox (item selection from a list)
    - a progress bar
    - a waitbar

*viewer*  Allows you to interactively explore time-series data in your workspace

.. figure:: _static/viewer_large.png
    :scale: 50%

    Interactively analyze time-series data.


Installation
------------

The simplest way to install thLib is

>>> pip install thLib

For upgrading to the latest version, you have to type

>>> pip install thLib -U

Dependencies
^^^^^^^^^^^^
numpy, scipy, matplotlib, pandas, statsmodels, skimage, sympy

If you want to work not only with WAV-sound-files, but also with other sound
formats, you need to install FFMPEG (free from http://www.ffmpeg.org).

Modules
-------

.. toctree::
   :maxdepth: 2

   quat
   rotmat
   imus
   markers
   fits
   signals
   sounds
   ui
   vector
   viewer


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. note::
    | *Author:*     Thomas Haslwanter
    | *Version:*    0.11.8
    | *Date:*       Apr 2016
    | *email:*      thomas.haslwanter@fh-linz.at
    | *Copyright (c):*      2016, Thomas Haslwanter. All rights reserved.
    | *Licence:*    This work is licensed under the `BSD 2-Clause License <http://opensource.org/licenses/BSD-2-Clause>`_

.. image:: _static/cc_licence.png
   :scale: 100 %

