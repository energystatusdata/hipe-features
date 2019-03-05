# HIPE Feature Data Set
_Scripts to extract features from energy time series_

This repository contains code to generate features from energy time series.
The code can be used to reproduce the feature data set that is used in the manuscript

> Michael Vollmer, Holger Trittenbach, Shahab Karrari, Adrian Englhardt, Pawel Bielski, Klemens Böhm, "Energy Time-Series Features for Emerging Applications on the Basis of Human-Readable Machine Descriptions" submitted to [Second International Workshop on Energy Data and Analytics (ACM e-Energy Workshop 2019)](https://www.energystatusdata.kit.edu/eda2019.php), 05 Mar 2019.

For a download of the extracted feature data set and further information, see the [companion website](https://www.energystatusdata.kit.edu/hipe-features.php).

The code is licensed under a [MIT License](https://github.com/kit-dbis/ocal-evaluation/blob/master/LICENSE.md) and the data set under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
If you use this code or data set in your scientific work, please reference the companion paper.

## Reproducing the feature data

Steps to generate the feature data from raw measurements:

1. Install `python3.6`, `python3.6-dev` and `pipenv`.
2. Run `pipenv install` to fetch all python dependencies.
3. Run `pipenv run feature-extraction` to calculate the features. The script automatically downloads the [HIPE](https://www.energystatusdata.kit.edu/hipe.php) data set and runs the feature extraction. The final feature data sets are then in `data/`.

## Author
For questions and comments, please contact [Adrian Englhardt](https://github.com/englhardt).
