# ML Model Design & Fairness

## Problem Type
Binary classification: Eligibility for social support.

## Feature Strategy
- Financial & family features used directly
- Disability flag included as a legitimate vulnerability signal
- Gender & nationality excluded from training, used only for bias audits

## Models
- Baseline: Logistic Regression
- Primary: Gradient Boosting Classifier

## Metrics
- Precision (primary)
- ROC-AUC
- Confidence calibration

## Fairness Monitoring
- Gender parity
- Nationality parity
- Disability-positive prioritization (expected skew)
