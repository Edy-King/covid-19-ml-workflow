# Repository Update Notes

## How to Apply

1. Back up the current repository or create a new branch.
2. Extract this bundle into the repository root, allowing matching files to be replaced.
3. Confirm that the Kaggle dataset is stored locally as `covid_data_2020-2021.csv` and remains ignored by Git.
4. Review the staged diff before committing.
5. Run the checks below.

## Suggested Checks

```bash
python -m pip install -r requirements_temporal_lock.txt
python run_rigorous_temporal_holdout.py
git status --short
```

The full temporal run fits 300 random-forest trees on more than four million development records and can take several minutes.

Running the temporal script writes aggregate metrics, plots and compressed record-level prediction files:

- `rigorous_temporal_holdout/validation_predictions.csv.gz`
- `rigorous_temporal_holdout/untouched_temporal_holdout_predictions.csv.gz`

These probability files support independent checks of calibration, PR-AUC, threshold performance and final holdout classification.

## Suggested Commit

```text
Add corrected untouched temporal validation workflow
```

## What Changed

- Added non-overlapping development, validation and untouched temporal-holdout periods.
- Restricted calibration and threshold selection to validation data.
- Added probability-based evaluation and final-holdout plots.
- Updated the temporal script to save validation and final-holdout probabilities.
- Added a pinned dependency file for the corrected random-forest temporal workflow.
- Updated the manuscript with reproducibility, calibration, permutation-importance, model-agreement and temporal-validation findings.
- Clarified that the temporal holdout is not true external validation.
- Corrected dataset instructions and pointed them to the Kaggle source.

## Do Not Commit

- `archive.zip`
- `covid_data_2020-2021.csv`
- Any other copy of the Kaggle source dataset

Dataset source:

https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020
