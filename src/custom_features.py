#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Adrian Englhardt <adrian.englhardt@gmail.com>
# Licensed under the MIT License - https://opensource.org/licenses/MIT

import dateutil
import numpy as np
import pandas as pd
from tsfresh.feature_extraction import feature_calculators
from tsfresh.feature_extraction.feature_calculators import number_crossing_m
from tsfresh.feature_extraction.feature_calculators import set_property


@set_property("fctype", "simple")
def crest_factor(x):
    """
    Calculate and return the crest factor of x defined by

    .. math::
        \\frac{max(|x|)}{RMS(x)}

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    if len(x) < 1:
        return np.NaN
    return np.max(np.abs(x)) / np.sqrt(np.mean(np.square(x)))


@set_property("fctype", "simple")
def percentage_non_zero_values(x):
    """
    Percentage of non zero values

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return (x.astype(bool)).mean()


@set_property("fctype", "simple")
def num_states(x):
    """
    Count number of different values in the series

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return len(np.unique(x))


@set_property("fctype", "simple")
def num_maxima(x):
    """
    Count occurrences of minimum value of the series

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    maximum = np.max(x)
    return sum(x == maximum) if maximum != np.NaN else np.NaN


@set_property("fctype", "simple")
def num_minima(x):
    """
    Count occurrences of maximum value of the series

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    minimum = np.min(x)
    return sum(x == minimum) if minimum != np.NaN else np.NaN


@set_property("fctype", "simple")
def linear_weighted_average(x):
    """
    Calculate and return the linear weighted average of x defined by

    .. math::
        \\frac{2}{n(n + 1)} \\sum\\limits_1^n i x_i

    where :math:`n` is the length of the time series.


    .. rubric:: References

    |  [1] Wiens, Jenna, Eric Horvitz, and John V. Guttag. "Patient risk stratification for hospital-associated c. diff as a time-series classification task." Advances in Neural Information Processing Systems. 2012.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    n = len(x)
    if n < 1:
        return np.NaN
    return 2 / (n * (n + 1)) * sum(np.array(range(1, n + 1)) * x)


@set_property("fctype", "simple")
def quadratic_weighted_average(x):
    """
    Calculate and return the quadratic weighted average of x defined by

    .. math::
        \\frac{6}{n(n+1)(2n+1)} \\sum\\limits_1^n i^2 x_i

    where :math:`n` is the length of the time series.


    .. rubric:: References

    |  [1] Wiens, Jenna, Eric Horvitz, and John V. Guttag. "Patient risk stratification for hospital-associated c. diff as a time-series classification task." Advances in Neural Information Processing Systems. 2012.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    n = len(x)
    if n < 1:
        return np.NaN
    return 6 / (n * (n + 1) * (2 * n + 1)) * sum(np.array(range(1, n + 1)) ** 2 * x)


@set_property("fctype", "simple")
def number_crossing_mean(x):
    """
    Count the number of times x crosses its own mean.

    .. rubric:: References
    | [1] Kedem, Benjamin, and Sidney Yakowitz. Time series analysis by higher order crossings. New York: IEEE press, 1994.

    :param x: the time series to calculate the feature of
    :type x: pandas.Series
    :return: the value of this feature
    :return type: float
    """
    if not isinstance(x, (np.ndarray, pd.Series)):
        x = np.asarray(x)
    return number_crossing_m(x, x.mean())


# Add new features to tsfresh
feature_calculators.crest_factor = crest_factor
feature_calculators.percentage_non_zero_values = percentage_non_zero_values
feature_calculators.num_states = num_states
feature_calculators.num_maxima = num_maxima
feature_calculators.num_minima = num_minima
feature_calculators.linear_weighted_average = linear_weighted_average
feature_calculators.quadratic_weighted_average = quadratic_weighted_average
feature_calculators.number_crossing_mean = number_crossing_mean


def weekday(x):
    """
    Calculate the week day from x.

    :param x: the time series to calculate the feature of
    :type x: str
    :return: the weekday number (1 = monday, 2 = tuesday, etc.)
    :return type: int
    """
    return dateutil.parser.parse(x).weekday() + 1


def machine_off(data, machine_off_threshold=0):
    """
    Calculate a mask that specifies if the machine is turned off.

    :param data: the data set to use
    :type data: pandas.DataFrame
    :param machine_off_threshold: the threshold current I a machine has to surpass to be on
    :type machine_off_threshold: float
    :return: mask indicating where the machine is turned off
    :return type: pandas.Series
    """
    if 'I2_A' in data.columns:
        return data[['I1_A', 'I2_A', 'I3_A']].max(axis=1).abs() <= machine_off_threshold
    else:
        target = 'IAVR_A' if 'IAVR_A' in data.columns else 'I1_A'
        return data[[target]].abs() <= machine_off_threshold
