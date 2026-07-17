# COVID-19 Symptom Classification Machine-Learning Workflow

This repository contains a reproducible workflow for classifying COVID-19 test outcomes from symptom and testing-context data.

The original experiment compared seven classifiers on the first 1,000,000 records. The corrected temporal-validation workflow uses all 5,861,480 records with separate chronological development, validation and untouched temporal-holdout periods.

## Dataset

Download the **COVID-19 Dataset for Year 2020** from Kaggle:

https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020

Extract the archive locally and place this file in the repository root:

```text
covid_data_2020-2021.csv
```

The dataset and its ZIP archive are intentionally excluded from Git. Do not commit or redistribute them from this repository.

## Corrected Temporal-Validation Design

The repository-ready script `run_rigorous_temporal_holdout.py` uses whole-date, non-overlapping partitions:

- Development: 20 March 2020 to 3 March 2021; 4,386,596 records
- Validation: 4 March to 7 August 2021; 592,575 records
- Untouched temporal holdout: 8 August to 11 October 2021; 882,309 records

The random forest is fitted only on the development period. Isotonic calibration and F1-based threshold selection use only the validation period. The calibrated model and frozen threshold are then evaluated once on the untouched latest-period holdout.

This is **temporal validation within the same data source**, not true external validation. Validation in a different population, institution or collection system remains recommended future work.

## Main Untouched-Holdout Results

| Metric | Value |
|---|---:|
| ROC-AUC | 0.6938 |
| Average precision | 0.3306 |
| Accuracy | 0.5367 |
| Precision | 0.1357 |
| Recall | 0.7015 |
| Specificity | 0.5190 |
| F1-score | 0.2274 |
| Balanced accuracy | 0.6102 |
| Brier score | 0.1069 |

The holdout result demonstrates substantial temporal degradation compared with validation ROC-AUC of 0.8313. It should not be interpreted as evidence of clinical readiness.

## Installation

Create a fresh environment and install the pinned corrected-workflow dependencies:

```bash
python -m pip install -r requirements_temporal_lock.txt
```

Run the temporal workflow from the repository root:

```bash
python run_rigorous_temporal_holdout.py
```

Outputs are written to `rigorous_temporal_holdout/`, including aggregate metrics, plots and compressed record-level prediction files for the validation and final holdout periods.

When the temporal script is rerun with the Kaggle CSV present, it writes:

- `rigorous_temporal_holdout/validation_predictions.csv.gz`
- `rigorous_temporal_holdout/untouched_temporal_holdout_predictions.csv.gz`

These files contain row index, test date, observed outcome, raw random-forest probability, validation-calibrated probability and the prediction made at the frozen validation-selected threshold. They are generated locally rather than bundled with the source data.

## Repository Files in This Update

- `run_rigorous_temporal_holdout.py` - corrected full-data temporal workflow
- `requirements_temporal_lock.txt` - exact environment used for the corrected analysis
- `rigorous_temporal_holdout/` - partition summary, metrics and final holdout figure
- `extended_analysis/` - reproduced random-split metrics, bootstrap intervals, model agreement, threshold analysis, permutation importance and figures
- `manuscript/COVID19_Manuscript_Major_Revision.docx` - revised manuscript
- `UPDATE_NOTES.md` - overlay and commit guidance

## Important Methodological Notes

- The original random-split workflow used its test set for model selection, so that estimate was not fully independent.
- The first million rows contain many repeated observed profiles and no patient identifier; identical profiles cannot be assumed to be independent patients.
- LightGBM remains part of the original comparison, but the corrected probability-based temporal analysis uses random forest because its repository result was reproduced exactly and its record-level probabilities were available.
- If LightGBM is later retained as the named deployment model, rerun the same locked partitions with saved LightGBM probabilities and repeat calibration, average precision, threshold selection and temporal holdout evaluation.
- True external validation remains a recommendation.

## Data and Code Availability

Dataset: https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020

Repository: https://github.com/Edy-King/covid-19-ml-workflow
