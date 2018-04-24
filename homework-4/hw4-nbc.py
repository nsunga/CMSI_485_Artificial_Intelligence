'''
AUTHOR: NICK SUNGA
hw4-nbc.py

Uses a Naive Bayes Classifier to query voting intent given a set of features.
'''

import numpy as np
from sklearn.naive_bayes import BernoulliNB

features = np.genfromtxt('hw4-data.csv', delimiter=",", skip_header=1, dtype=None, usecols=(0,1,2,3,4))
generated_class = np.genfromtxt('hw4-data.csv', delimiter=",", skip_header=1, dtype=None, usecols=(5))

clf = BernoulliNB()
clf.fit(features, generated_class)

# Political leaning, Age group, Immigration, Gun control, Drug decriminalization
print(clf.predict_proba([[1, 0, 0, 0, 0]]))
print(clf.predict_proba([[1, 0, 1, 0, 1]]))
print(clf.predict_proba([[0, 1, 0, 1, 0]]))
