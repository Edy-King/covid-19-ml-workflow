# Prediction File Schema

Running `python run_rigorous_temporal_holdout.py` with `covid_data_2020-2021.csv` in the repository root writes two compressed prediction files:

- `validation_predictions.csv.gz`
- `untouched_temporal_holdout_predictions.csv.gz`

Each file contains one row per source dataset record in the relevant partition.

| Column | Description |
|---|---|
| `row_index` | Zero-based row position in the source CSV |
| `test_date` | Test date used for chronological partitioning |
| `y_true` | Observed outcome, with negative=0 and positive=1 |
| `raw_probability` | Uncalibrated random-forest positive-class probability |
| `calibrated_probability` | Isotonic-calibrated probability using validation-only calibration |
| `prediction_at_frozen_threshold` | Binary prediction using the validation-selected threshold |

The prediction files are generated locally rather than bundled with the source data.
