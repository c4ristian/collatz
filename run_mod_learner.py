"""
This script tries to find the formula for a relation
between different mod values by machine learning.
"""

# Imports
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Main Script

# Create data
a = np.array([1, 2, 3, 4]).reshape(-1, 1)
b = np.array([4, 3, 1, 2])

# Train linear model
model = LinearRegression()
model.fit(a, b)

# Test the model
r_sq = model.score(a, b)
print('R2 linear:', r_sq)

# Train polynomial model
transformer = PolynomialFeatures(degree=2, include_bias=False)
transformer.fit(a)
ap = transformer.transform(a)

model_p = LinearRegression().fit(ap, b)

# Test the model
r_sq_p = model_p.score(ap, b)
print('R2 polynomial:', r_sq_p)
