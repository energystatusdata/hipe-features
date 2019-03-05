#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Adrian Englhardt <adrian.englhardt@gmail.com>
# Licensed under the MIT License - https://opensource.org/licenses/MIT

import logging
import os
import pandas as pd
import shutil
import urllib.request
from config import *
from custom_features import *
from tsfresh.feature_extraction import extract_features
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')


def check_hipe_files(f):
    full_file_path = os.path.join(DATA_PATH, f)
    if os.path.isfile(full_file_path):
        logging.info(f"Found '{f}'.")
    else:
        logging.info(f"File '{f}' missing. Downloading...")
        urllib.request.urlretrieve(HIPE_URL + f, full_file_path)
        logging.info(f"File '{f}' downloaded.")


def calc_aggregation_datetime(datetimes, aggregation):
    # Aggregation is calculated from dates via string manipulation to avoid expensive date parsing
    if aggregation == 'minute':
        return datetimes.apply(lambda x: x[:16] + ':00.000' + x[-3:])
    elif aggregation == '10minutes':
        return datetimes.apply(lambda x: x[:15] + '0:00.000' + x[-3:])
    elif aggregation == '15minutes':
        return datetimes.apply(lambda x: x[:14] + f'{int(x[14:16]) // 15 * 15:02d}:00.000' + x[-3:])
    elif aggregation == '1hour':
        return datetimes.apply(lambda x: x[:13] + ':00:00.000' + x[-3:])
    elif aggregation == '1day':
        result = datetimes.apply(lambda x: x[:11] + '00:00:00.000' + x[-3:])
        return result.replace({DATE_CHANGE_WINTER[:-1] + '1': DATE_CHANGE_WINTER})
    else:
        raise NotImplementedError(f"Unsupported aggregation level '{aggregation}'.")


def remove_machine_off_data(data, machine_off_threshold=0):
    data_length = len(data)
    data['machine_off'] = machine_off(data, machine_off_threshold)
    logging.info(f"Removing {data['machine_off'].sum()}/{data_length} rows where machine is turned off.")
    data = data[~data['machine_off']][data.columns[:-1]]
    return data


def extract_features_from_file(input_file, output_file, aggregation, target_columns, data_columns,
                               prune_data=False, machine_off_threshold=0):
    # Load data
    data = pd.read_csv(input_file)
    present_columns = set(target_columns).intersection(set(data.columns))
    missing_columns = set(target_columns) - set(data.columns)
    if len(missing_columns) > 0:
        logging.info(f"Missing columns: '{missing_columns}'")
    data = data[list(present_columns)]

    # Optionally prune data where machine is turned off
    if prune_data:
        data = remove_machine_off_data(data, machine_off_threshold)
        if len(data) == 0:
            logging.info("No data left after pruning. Skipping file.")
            return

    # Add column for aggregation and reorder
    data['id'] = calc_aggregation_datetime(data[DATE_COLUMN], aggregation)
    data = data[['id'] + list(set(data_columns).intersection(present_columns))]

    # Run feature extraction
    feature_data = extract_features(data,
                                    column_id='id',
                                    default_fc_parameters=features,
                                    n_jobs=NUM_THREADS)

    # Add weekday feature
    weekday_data = feature_data.index.to_series().apply(weekday)
    feature_data.insert(loc=0, column='weekday', value=weekday_data)

    # Write output file
    feature_data.to_csv(output_file)


def process_file(input_file, output_file, aggregation, prune_data=False):
    output_file = f'{output_file}_{aggregation}-agg'
    logging.info(f"Processing '{input_file}.")
    zf = ZipFile(os.path.join(DATA_PATH, input_file))
    filenames = [filename for filename in zf.namelist() if '.csv' in filename]
    logging.info(f'Found {len(filenames)} files.')

    output_dir = os.path.join(DATA_PATH, output_file)
    os.makedirs(output_dir, exist_ok=True)

    for f in filenames:
        logging.info(f'Start processing {f}')
        machine_off_threshold = MACHINE_OFF_THRESHOLDS[f.split("_")[0]]
        machine_phase_count = f"{f.split('_')[2]} phase"
        extract_features_from_file(zf.open(f), os.path.join(output_dir, f), aggregation,
                                   TARGET_COLUMNS[machine_phase_count], DATA_COLUMNS[machine_phase_count],
                                   prune_data=prune_data, machine_off_threshold=machine_off_threshold)
        logging.info(f'Finished processing {f}')

    logging.info(f'Compressing output files.')
    output_file_path = os.path.join(DATA_PATH, output_file)
    shutil.make_archive(output_file_path, 'zip', output_file_path)
    logging.info(f'Compressing done.')
    logging.info(f"Finished. The output is file '{output_file_path + '.zip'}'.")


def main():
    check_hipe_files(HIPE_MONTH_FILE)

    # 15 minutes
    process_file(HIPE_MONTH_FILE, HIPE_MONTH_FEATURE_OUTPUT, '15minutes')
    process_file(HIPE_MONTH_FILE, HIPE_MONTH_FEATURE_OUTPUT_ONLY_ON, '15minutes', prune_data=True)

    # 1 hour
    process_file(HIPE_MONTH_FILE, HIPE_MONTH_FEATURE_OUTPUT, '1hour')
    process_file(HIPE_MONTH_FILE, HIPE_MONTH_FEATURE_OUTPUT_ONLY_ON, '1hour', prune_data=True)


if __name__ == "__main__":
    main()
