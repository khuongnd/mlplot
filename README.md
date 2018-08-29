[![CircleCI](https://circleci.com/gh/sbarton272/mlplot.svg?style=svg)](https://circleci.com/gh/sbarton272/mlplot)
[![Documentation Status](https://readthedocs.org/projects/mlplot/badge/?version=latest)](https://mlplot.readthedocs.io/en/latest/?badge=latest)


# mlplot
Machine learning evaluation plots using matplotlib

# Plots

Starting from [sklearn](http://scikit-learn.org/stable/modules/model_evaluation.html).

## Classification

### ROC with AUC number
![ROC plot](https://raw.githubusercontent.com/sbarton272/mlplot/master/mlplot/test/output/test_roc.png)

### Calibration
![calibration plot](https://raw.githubusercontent.com/sbarton272/mlplot/master/mlplot/test/output/test_calibration.png)

### Precision-Recall
![precision recall curve plot](https://raw.githubusercontent.com/sbarton272/mlplot/master/mlplot/test/output/test_precision_recall.png)
![precision recall threshold plot](https://raw.githubusercontent.com/sbarton272/mlplot/master/mlplot/test/output/test_precision_recall_threshold.png)

### TODO
- Population histograms
- Residual plot --> what is the real name?
- Confusion matrix
- Full report
  - Accuracy score
  - F1 score
  - Number of samples of each class

## Regression

- Full report
  - Mean sqr error
  - Mean abs error
  - Target mean, std
  - R2
- Residual plot
- Scatter plot
- Histogram of regressor
