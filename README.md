# COVID-19 Symptom Classification Machine Learning Workflow

This project contains my machine learning workflow for classifying COVID-19 test results from patient symptom and context data.

I used 1,000,000 patient records from the COVID-19 dataset published on Kaggle and built an efficient notebook-based workflow that loads the data, cleans it, engineers useful features, trains several machine learning models, compares their performance, tunes the strongest candidates, and saves the best final model.

Dataset source: [COVID-19 Dataset for Year 2020 on Kaggle](https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020)

## Project Files

- `covid_symptom_ml_workflow_exported.ipynb` - final executed notebook with outputs, visualizations, model comparisons, tuning results, and saved-model workflow.
- `covid_symptom_ml_workflow.ipynb` - working executed notebook.
- `requirements_ml.txt` - Python packages required to run the notebook.
- `ml_outputs/baseline_model_results.csv` - baseline model comparison results.
- `ml_outputs/tuned_model_results.csv` - tuned model comparison results.
- `ml_outputs/models/best_covid_symptom_model.joblib` - saved best model.
- `ml_outputs/models/best_covid_symptom_model_metadata.json` - final model metadata, features, parameters, and metrics.
- `build_covid_ml_notebook.py` - script used to generate the notebook structure.

The original dataset is not included in the repository because it is large. To reproduce the work, download the dataset from Kaggle and place the CSV in the project folder as:

```text
covid_data_2020_2021.csv
```

## Dataset

The dataset contains COVID-19 patient test records with symptom indicators and patient context columns. I used the Kaggle version here:

[https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020](https://www.kaggle.com/datasets/mykeysid10/covid19-dataset-for-year-2020)

I used 1,000,000 records and the following original columns:

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

The target variable is:

```text
corona_result
```

where:

- `Negative` is encoded as `0`
- `Positive` is encoded as `1`

## Feature Engineering

I kept the five main symptom features and added simple, explainable features to help the models learn more useful patterns.

Final model features:

- `cough`
- `fever`
- `sore_throat`
- `shortness_of_breath`
- `head_ache`
- `symptom_count`
- `has_any_symptom`
- `has_multiple_symptoms`
- `age_60_and_above_yes`
- encoded gender features
- encoded test indication features
- `test_month`
- `test_dayofweek`

## Models Trained

I trained and compared seven models:

- Logistic Regression
- Random Forest
- Extra Trees
- PCA + Linear SVM
- XGBoost
- LightGBM
- CatBoost

GPU acceleration was attempted for XGBoost, LightGBM, and CatBoost. Where GPU setup was available, the model used GPU; otherwise the notebook can fall back to CPU.

## Evaluation Metrics

Each model was evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

Because the dataset is imbalanced, I used ROC-AUC as the main ranking metric and F1-score as a secondary comparison metric.

## Final Result

The top three models selected for hyperparameter tuning were:

- XGBoost
- LightGBM
- CatBoost

The best final model was:

```text
Tuned LightGBM
```

Final tuned LightGBM performance:

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

## How to Run

Install the required packages:

```bash
pip install -r requirements_ml.txt
```

Download the dataset from Kaggle, place `covid_data_2020_2021.csv` in the project folder, then open and run:

```text
covid_symptom_ml_workflow_exported.ipynb
```

The notebook writes model outputs to:

```text
ml_outputs/
```

## Notes

- I did not overwrite the original dataset.
- I used memory-efficient loading by selecting only the required columns and compact data types.
- I compared several model families before tuning the strongest candidates.
- PCA + Linear SVM was tested, but the boosted tree models performed better on this dataset.
