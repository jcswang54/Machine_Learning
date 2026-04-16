# World University Rankings — A Data Analysis

## Question
University rankings aggregate metrics — teaching, research, 
citations, international outlook — into a single number.
In this project, we try to answer questions including:
    - which metrics drive up the rank the most 
    - how stable are rankings across years
    - does geographic region predict performance 
        beyond individual institution effects?

## Mathematical angle
The five score columns define a point in R^5 for each university. Centering and 
normalizing these columns yields a matrix X of shape (N, 5); the correlation matrix 
is the Gram matrix of the normalized feature vectors.

The high correlation between teaching and research 
(~0.9) means those two axes nearly coincide, and we can view that the data lives in a lower-dimensional 
subspace. Equivalently, PCA on this matrix would show that the first principal component captures the majority of variance.

This serves as a concrete instance that dimensionality reduction can be viewed motivated by geometry: this correlation structure tells us that such a 5-metric ranking system has lower degrees of freedom.

## What this project demonstrates
- Data loading, inspection, dtype fixing, and cleaning
- Multi-column groupby aggregations and pivot tables
- Relational modeling: 3 normalized tables queried via SQL
- SQL queries replicated in pandas (verified to match)
- Numpy vectorized statistics and manual correlation matrix

## Dataset
Times Higher Education World University Rankings (Kaggle).
File: timesData.csv — 2,603 rows, 14 columns, years 2011–2016.

## Tools
Python · pandas · NumPy · SQLite

## Author
JinCheng Wang | Tufts University | Department of Mathematics