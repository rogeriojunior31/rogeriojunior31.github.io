---
title: "House price predictor"
date: 2024-02-04
summary: "Python machine learning model to estimate house prices."
tags: ["Python", "Machine Learning"]
---

{{< github repo="rogeriojunior31/house_price_predictor" showThumbnail=false >}}

## The problem

Estimate housing values from the California Housing Dataset and explore how its features relate to prices. This is a machine learning study, not a commercial property valuation tool.

## How it works

- Python and scikit-learn to load data and split training and test sets.
- Linear regression as a baseline; Ridge, cross-validation and `GridSearchCV` in the enhanced version.
- RMSE to evaluate predictions on the test set.
- Matplotlib and Seaborn to visualize data features and compare actual and predicted values.

## Run it

With Python 3.9 or later (for the repository's pinned dependencies), in a virtual environment:

```sh
git clone https://github.com/rogeriojunior31/house_price_predictor.git
cd house_price_predictor
python -m venv .venv
# Linux/macOS; on Windows, use .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Running the script produces RMSE and analysis plots. The initial dataset download may require internet access. Results depend on the run; no metric published here establishes performance in other housing markets.

[View code and instructions on GitHub](https://github.com/rogeriojunior31/house_price_predictor)
