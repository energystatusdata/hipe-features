#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Adrian Englhardt <adrian.englhardt@gmail.com>
# Licensed under the MIT License - https://opensource.org/licenses/MIT

from collections import defaultdict

NUM_THREADS = 1
DATA_PATH = "data"
HIPE_URL = "https://www.ipd.kit.edu/mitarbeiter/hipe/"
HIPE_MONTH_FILE = "hipe_cleaned_v1.0.1_geq_2017-10-01_lt_2018-01-01.zip"

FEATURE_OUTPUT_VERSION = "v1.0.0"
HIPE_MONTH_FEATURE_OUTPUT = f"{HIPE_MONTH_FILE[:-4]}_features_{FEATURE_OUTPUT_VERSION}_all"
HIPE_MONTH_FEATURE_OUTPUT_ONLY_ON = f"{HIPE_MONTH_FILE[:-4]}_features_{FEATURE_OUTPUT_VERSION}_only-on"

DATE_COLUMN = "SensorDateTime"
DATE_CHANGE_WINTER = '2017-10-29T00:00:00.000+02'
DATA_COLUMNS = {
    "2 phase": ["V1_V", "F_Hz", "I1_A", "P_kW", "Q_kvar", "S_kVA", "L1_F"],
    "3 phase": ["VAVR_V", "F_Hz", "IAVR_A", "P_kW", "Q_kvar", "S_kVA", "L_F"]
}
TARGET_COLUMNS = {
    k: [DATE_COLUMN] + v for (k, v) in DATA_COLUMNS.items()
}

MACHINE_OFF_THRESHOLDS = defaultdict(lambda: 0.0, PickAndPlaceUnit=0.3)

features = {
    # Interpretable: yes, Scope: a-temporal, Values: single, Parametrized: No, Requirements: none
    "count_above_mean": None,
    "count_below_mean": None,
    "has_duplicate": None,
    "has_duplicate_max": None,
    "has_duplicate_min": None,
    "kurtosis": None,
    "length": None,
    "percentage_non_zero_values": None,
    "maximum": None,
    "minimum": None,
    "mean": None,
    "median": None,
    "crest_factor": None,
    "percentage_of_reoccurring_values_to_all_values": None,
    "percentage_of_reoccurring_datapoints_to_all_datapoints": None,
    "num_states": None,
    "skewness": None,
    "standard_deviation": None,
    # Interpretable: yes, Scope: local, Values: single, Parametrized: No, Requirements: none
    "absolute_sum_of_changes": None,
    "mean_second_derivative_central": None,
    "first_location_of_maximum": None,
    "first_location_of_minimum": None,
    "last_location_of_maximum": None,
    "last_location_of_minimum": None,
    "num_maxima": None,
    "num_minima": None,
    "longest_strike_above_mean": None,
    "longest_strike_below_mean": None,
    "mean_abs_change": None,
    "mean_change": None,
    "number_crossing_mean": None,
    # Interpretable: yes, Scope: global, Values: single, Parametrized: No, Requirements: none
    "linear_weighted_average": None,
    "linear_trend": [{"attr": "slope"}],
    "quadratic_weighted_average": None,
    "sample_entropy": None,
    "cid_ce": [{"normalize": True}],
}
