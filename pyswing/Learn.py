'''
Theanets "Hello, world!" - train a simple neural network for classifying
simple data and evaluate the results.

[Theanets](https://github.com/lmjohns3/theanets) allows to build and train
neural networks on top of the [Theano](https://github.com/Theano/Theano)
compiler.

The goal is to get familiar with theanets on some simple example. You can
modify this example bit by bit to work on more complex data and models.

In this example we generate some synthetic data (via scikit-learn) - two 2D
blobs with Gaussian distribution which are in addition linearly separable.
Thus any classification model should have no problem with such data.

We create a neural network with three layers - input, hidden and output - each
with two dimensions (2D featues, two classes). The input and hidden layer has
by default sigmoid activation, the output clasification layer has softmax
actiovation by default. The model is trained via the stochastic gradient descent
algorithm.

Finally the model is evaluated by functions provided by scikit-learn.
'''

# some utilities for command line interfaces
import climate
# deep neural networks on top of Theano
import theanets
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

climate.enable_default_logging()

# -- generate some data --

# TODO: Load the share data...
# select matchString, ExitValue from HistoricMatches h
# inner join "Exit Yesterday MaximumStop2.0 RiskRatio3" ev on ev.Code = h.Code and ev.MatchDate = h.Date and ev.Type = 'Buy'
# where h.Code = "CBA.AX" and h.Date < '2015-10-01 00:00:00';


X = np.array([[0,0,0],[0,1,1],[1,1,1],[1,0,1],[0,0,1],[0,1,1],[1,1,1],[1,0,1],[0,0,1],[0,1,1],[1,1,1],[1,0,1],[0,0,1],[0,1,1],[1,1,1],[1,0,1],[0,0,1],[0,1,1],[1,1,1],[1,0,1]], np.int32)
y = np.array([0,2,3,2,1,2,3,2,1,2,3,2,1,2,3,2,1,2,3,2], np.int32)

X_2 = np.array([[0,0,1],[0,1,1],[1,1,1],[1,0,1]], np.int32)
y_2 = np.array([1,2,3,2], np.int32)

X_3 = np.array([[0,0,0],[0,0,1],[0,1,1],[1,1,1],[1,0,1],[1,1,0]], np.int32)
# y_3 = np.array([0,1,2,3,2,2], np.int32)

# -- create and train the model --

# plain neural network with a single hidden layer
net = theanets.Classifier(layers=[3, 3, 4])

train = (X, y)
valid = (X_2, y_2)

net.train(train, valid, algo='rmsprop', min_improvement=0.005)

# for loop in range(1, 100000):
#     net.itertrain(train, valid, algo='rmsprop')

net.save('learn.nn')


print(net.predict(X_3))

# -- evaluate the model on test data --

# X_test, y_test = datasets['test']
# y_pred = exp.network.classify(X_3)
#
# print('classification_report:\n', classification_report(y_3, y_pred))
# print('confusion_matrix:\n', confusion_matrix(y_3, y_pred))