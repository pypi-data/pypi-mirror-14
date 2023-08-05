#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr

from __future__ import unicode_literals


"""Key Background Model"""


import numpy as np
import itertools
from sklearn.mixture import GMM
import logging
from pyannote.core import SlidingWindow


class KeyBackgroundModel(object):
    """

    Parameters
    ----------

    covariance_type : string, optional
        String describing the type of covariance parameters to
        use.  Must be one of 'diag' or 'full'. Defaults to 'full'.

    n_components : int, optional
        Defaults to 2000.

    duration : float, optional
        Window duration, in seconds. Default to 2.

    """

    def __init__(self, covariance_type='full', logger=None):

        super(KeyBackgroundModel, self).__init__()

        self.covariance_type = covariance_type
        self.duration = duration
        self.n_components = n_components

        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())
        self.logger = logger

    def fit(self, features):

        end = features.getExtent().duration



        sliding_window = SlidingWindow(duration=duration, step=step,
                                       start=0.0, end=end)
        for window

        gaussian = Gaussian(covariance_type='full')


        pass

    def apply(self, X):
        """Estimate model parameters with KeyBackgroundModel initialization and
        the expectation-maximization algorithm.

        Parameters
        ----------
        X : array_like, shape (n, n_features)
            List of n_features-dimensional data points.  Each row
            corresponds to a single data point.
        """

        for gmm, _ in self.apply_partial(X):
            pass

        return gmm
