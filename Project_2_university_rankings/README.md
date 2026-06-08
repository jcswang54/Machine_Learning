# World University Rankings — Machine Learning analysis (Part II)

## Overview
The 5 academic score columns in the Times Higher Education rankings 
(teaching, research, citations, international, income) span only ~3–4 
effective dimensions, despite living in R^5. 
This is corroborated by PCA explained variance ratios, which show 3 components capturing ~90% of variance. 
Independently, coloring the PC1 vs PC2 scatter by label reveals an approximately linear boundary. 
Together these explain why Logistic Regression matches Random Forest at AUC = 0.99 (in comparison, the single Decision Tree trails at AUC = 0.89), and the problem does not require nonlinearity.

## Key findings
| Model | AUC |
|---|---|
| Logistic Regression | 0.99 |
| Random Forest | 0.99 |
| Decision Tree | 0.89 |

- PCA confirms ~3–4 effective dimensions: the first 3 principal components 
  capture ~90% of variance, consistent with the Gram matrix result from Part I
- Coloring the PC1 vs PC2 scatter by top-100 label reveals an approximately linear boundary, 
providing the geometric justification for why logistic regression suffices
- K-Means clustering (k=2) achieves ARI = 0.61 against the top-100 label,
  hence the boundary is real but not a hard cut in feature space.

## Mathematical angle
The Gram matrix X^TX and the PCA covariance matrix (1/n)X^TX are proportional,
where X is the (n x 5) data matrix of centered score columns.
Therefore, they have the same eigenvectors and proportional eigenvalues. 
Both measure the same geometric fact: how many independent directions contain meaningful variation in the data. 

Note that low dimensionality alone does not guarantee linear separability. 
But the PCA scatter reveals an approximately linear boundary on the PC1-PC2 plane, which explains why a simple linear model matches a complex ensemble.

## Methods
- Data cleaning: dtype conversion, null removal on score columns
- Classification: Logistic Regression, Decision Tree, Random Forest via 
  sklearn Pipelines (preventing data leakage)
- Evaluation: confusion matrix, classification report, ROC-AUC
- Unsupervised: PCA (5 components), K-Means (k=2,3,4), Adjusted Rand Index

## Dataset
Times Higher Education World University Rankings (Kaggle).
File: timesData.csv — 2,603 rows, 14 columns, years 2011–2016.

## Tools
Python · Pandas · NumPy · scikit-learn · Matplotlib

## Author
JinCheng Wang | Tufts University | Department of Mathematics