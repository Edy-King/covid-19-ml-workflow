# Model Card: COVID-19 Symptom Classification

## Model Overview

This model predicts whether a COVID-19 test result is positive or negative using symptom indicators and basic patient context features.

The final selected model is a tuned LightGBM binary classifier.

## Intended Use

This work is intended for machine learning experimentation and educational analysis. It should not be used as a clinical diagnostic system or as a replacement for professional medical testing or advice.

## Data Used

I used 1,000,000 records from the COVID-19 dataset published on Kaggle. The source file was kept unchanged.

Dataset source: [COVID-19 Dataset for Year 2020 on Kaggle](https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020)

Original columns used:

- `test_date`
- `cough`
- `fever`
- `sore_throat`
- `shortness_of_breath`
- `head_ache`
- `corona_result`
- `age_60_and_above`
- `gender`
- `test_indication`

## Features

The final training features included the five symptom columns plus engineered context features:

- symptom count
- any symptom flag
- multiple symptoms flag
- age over 60 flag
- gender encoding
- test indication encoding
- month and day-of-week features

## Models Compared

Seven models were trained and compared:

- Logistic Regression
- Random Forest
- Extra Trees
- PCA + Linear SVM
- XGBoost
- LightGBM
- CatBoost

The top three models were tuned with randomized hyperparameter search.

## Final Model

Final selected model:

```text
Tuned LightGBM
```

Best parameters:

```text
subsample: 0.85
num_leaves: 31
n_estimators: 300
min_child_samples: 100
learning_rate: 0.08
colsample_bytree: 0.8
```

## Performance

Test set performance:

| Metric | Value |
|---|---:|
| Accuracy | 0.923175 |
| Precision | 0.628901 |
| Recall | 0.380788 |
| F1-score | 0.474359 |
| ROC-AUC | 0.743358 |

Confusion matrix:

```text
[[177702, 4091],
 [11274, 6933]]
```

## Limitations

- The dataset is imbalanced, with many more negative cases than positive cases.
- The model is based on symptom and context data only; it does not include lab results, medical history, vaccination status, or variants.
- The recall for positive cases is limited, so the model misses a meaningful number of positive cases.
- This model should not be used for real medical decision-making without further validation.

## Saved Artifacts

- `ml_outputs/models/best_covid_symptom_model.joblib`
- `ml_outputs/models/best_covid_symptom_model_metadata.json`
- `ml_outputs/baseline_model_results.csv`
- `ml_outputs/tuned_model_results.csv`
