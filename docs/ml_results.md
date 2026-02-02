# ML Training Results

## Models Evaluated
- Logistic Regression (baseline)
- Gradient Boosting Classifier

## Key Findings
- Gradient Boosting outperformed Logistic Regression in ROC-AUC and precision
- Precision prioritized to minimize false approvals
- No significant disparity observed across gender
- Higher eligibility rates observed for applicants with disabilities, aligned with policy intent

## Conclusion
The trained model is suitable for use within the agentic eligibility scoring workflow with human-in-the-loop governance.


## Note:
The high ROC–AUC values are expected due to policy-driven synthetic labels.
Model performance will be stress-tested further using noisy, document-extracted features in later stages.
