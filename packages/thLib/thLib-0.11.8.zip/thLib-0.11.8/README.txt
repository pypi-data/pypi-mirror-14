=====
thLib
=====

*thLib* primarily contains functions for working with 3D kinematics. (i.e.
quaternions and rotation matrices). In addition, it has a number of routines
for fitting circles, lines, sine-waves, and exponential decays. For signal
processing, a Savitzky-Golay filter is included, as well as a demonstration of
the calculation of a power spectrum. UI utilities, and a few useful vector
functions (e.g. an implementation of the Savitzky-Golay algorithm) round off
*thLib*.

Compatible with Python 2 and 3.

Dependencies
------------
numpy, scipy, matplotlib, pandas, statsmodels, skimage, sympy

Homepage
--------
http://work.thaslwanter.at/thLib/html/

Author:  Thomas Haslwanter
Date:    05-04-2016
Ver:     0.11.8
Licence: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)
        Copyright (c) 2016, Thomas Haslwanter
        All rights reserved.

Installation
------------
You can install thlib with

    pip install thLib

and upgrade to a new version with

    pip install thLib -U

Vectors
=======

Routines for working with vectors
These routines can be used with vectors, as well as with matrices containing a vector in each row.

- vector.normalize ... Vector normalization
- vector.project ... Projection of one vector onto another one
- vector.GramSchmidt ... Gram-Schmidt orthogonalization of three points
- vector.qrotate ... Quaternion indicating the shortest rotation from one vector into another.
- vector.rotate_vector ... Rotation of a vector


Quaternions
===========

Note that all these functions work with single quaternions and quaternion vectors,
as well as with arrays containing these.

Quaternion class
----------------

- quat.Quaternion ... class, including overloading for multiplication and
                    division (e.g. "quatCombined = quat1 * quat2"), import and export

Functions for working with quaternions
--------------------------------------

- quat.quatconj ... Conjugate quaternion 
- quat.quatinv ... Quaternion inversion
- quat.quatmult ... Quaternion multiplication

Conversion routines
-------------------

- quat.deg2quat ... Convert number or axis angles to quaternion vectors
- quat.quat2deg ... Convert quaternion to corresponding axis angle
- quat.quat2rotmat ... Convert quaternion to corresponding rotation matrix
- quat.quat2vect ... Extract the vector part from a quaternion
- quat.rotmat2quat ... Convert a rotation matrix to the corresponding quaternion
- quat.vect2quat ... Externd a quaternion vector to a unit quaternion.
- quat.vel2quat ... Calculate orientation from a starting orientation and angular velocity.


Rotation Matrices
=================

Definition of rotation matrices
-------------------------------

- rotmat.R1 ... 3D rotation matrix for rotation about the 1-axis
- rotmat.R2 ... 3D rotation matrix for rotation about the 2-axis
- rotmat.R3 ... 3D rotation matrix for rotation about the 3-axis

Conversion Routines
-------------------
- rotmat.rotmat2Fick ... Calculation of Fick angles
- rotmat.rotmat2Helmholtz ... Calculation of Helmholtz angles

Symbolic matrices
-----------------

- rotmat.R1_s() ... symbolix matrix for rotation about the 1-axis
- rotmat.R2_s() ... symbolix matrix for rotation about the 2-axis
- rotmat.R3_s() ... symbolix matrix for rotation about the 3-axis

For example, you can e.g. generate a Fick-matrix, with

>>> R_Fick = R3_s() * R2_s() * R1_s()
    
Markers
=======

Analysis of signals from video-based marker-recordings of 3D movements

- markers.analyze3Dmarkers ... Kinematic analysis of video-basedrecordings of 3D markers
- markers.movement_from_markers ... Calculation of joint-movements from 3D marker positions

IMUs
====

Analysis of signals from IMUs (intertial-measurement-units).

General
-------
- kinematics.getXSensData ... Read in Rate and stored 3D parameters from XSens IMUs

MARG Systems
------------
- imus.calc_QPos ... Calculate orientation and position, from angular velocity and linear acceleration
- imus.kalman_quat ... Calculate orientation from IMU-data using an Extended Kalman Filter.

- imus.IMU ... Class for working with data from IMUs
    - imus.IMU.calc_orientation ... calculate orientation
    - imus.IMU.calc_position ... calculate position
    - imus.IMU.setData ... set the properties of an IMU-object
- imus.MadgwickAHRS ... Class for calculating the 3D orientation with the Madgwick-algorithm
- imus.MahonyAHRS ... Class for calculating the 3D orientation with the Mahony-algorithm

Fits
====

Functions
---------

- fits.demo_ransac ... RANSAC fit of best circle in image
- fits.fit_circle ... basic circle fit
- fits.fit_exp ... exponential fit
- fits.fit_line ... linear regression fit, complete with confidence intervals for mean and values, and with plotting
- fits.fit_sin ... sine fit
- fits.fit_ellipse ... ellipse fit (Taubin's method)
- fits.regress ... multilinear regression fit, similar to MATLAB
    
Signal Processing Utilities
===========================

- signals.pSpect ... simple power spectrum from FFT
- signals.savgol ... Savitzky-Golay filter

Sound Processing Utilities
==========================

- sounds.Sound ... class, with methods
    * readSound
    * play
    * setData
    * writeWav

GUI Utilities
=============

- ui.getfile ... GUI for selecting an existing file
- ui.getdir ... GUI for selecting a directory
- ui.listbox ... GUI for item selection
- ui.progressbar ... Show a progressbar, for longer loops
- ui.savefile ... GUI for saving a file
- ui.get_screensize ... width and height of screen

Interactive Data Analysis
=========================

- viewer.ts ... interactive viewer for time series data
