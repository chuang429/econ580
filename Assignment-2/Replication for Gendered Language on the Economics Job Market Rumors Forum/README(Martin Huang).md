# README

This repository replicates and extends the analysis in:

Wu, Alice (2018).
"Gendered Language on the Economics Job Market Rumors Forum."
AEA Papers and Proceedings.

## Files and Code Description

### Python Code

#### `lasso-logit-full-sample.py`
Re-estimates the LASSO logit model used in the paper.

This script:
- Loads the word-count matrix and post metadata
- Constructs the training and test samples
- Estimates the LASSO logit model
- Saves intermediate outputs, including:
  - `coef_lasso_logit_full.txt`
  - `ypred_train.txt`
  - `ypred_test0.txt`
  - `ypred_test1.txt`

These files document that the LASSO estimation was re-run.

#### `random_forest/rf-full-sample.py`
Implements a Random Forest classifier as an extension.

This script follows the same data preprocessing, sample selection, and feature construction as the LASSO code, but replaces the estimator with a Random Forest model.

The script outputs:
- `importance_rf_full.txt`
- `ypred_rf_train.txt`
- `ypred_rf_test0.txt`
- `ypred_rf_test1.txt`

Feature importance measures are used to rank predictive words.

### R Code

#### `tables-figures.R`
Loads the processed datasets and model outputs to reproduce:
- Table 1 (original LASSO results)
- Table 1 Random Forest version (`table1_rf`)
- Table 2
- Figure 1

The script also exports the Random Forest version of Table 1 as `rf_table1`.

Figures are generated using ggplot2 and exported from the R plotting interface.

## How to Run

1. Run `lasso-logit-full-sample.py` to re-estimate the baseline model.
2. Run `random_forest/rf-full-sample.py` to estimate the Random Forest model.
3. Run `tables-figures.R` to reproduce all tables and figures.

## Data Files

All data files are from the original replication package.
No additional data are used.

Key data files include:
- `gendered_posts.csv`
- `keys_to_X.csv`
- `X_word_count.npz`
- `vocab10K.csv`
- `trend_stats.csv`

## Notes

Minor path adjustments were made to accommodate the local directory structure.
All estimation procedures and feature definitions follow the original replication package unless otherwise noted.