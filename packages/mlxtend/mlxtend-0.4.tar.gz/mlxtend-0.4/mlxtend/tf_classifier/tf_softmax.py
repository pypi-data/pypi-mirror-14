# Sebastian Raschka 2014-2016
# mlxtend Machine Learning Library Extensions
#
# Implementation of Softmax Regression in Tensorflow
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

import tensorflow as tf
import numpy as np
from time import time
from .tf_base import _TfBaseClassifier


class TfSoftmaxRegression(_TfBaseClassifier):
    """Softmax regression classifier.

    Parameters
    ------------
    eta : float (default: 0.5)
        Learning rate (between 0.0 and 1.0)
    epochs : int (default: 50)
        Passes over the training dataset.
    minibatches : int (default: 1)
        Divide the training data into *k* minibatches
        for accelerated stochastic gradient descent learning.
        Gradient Descent Learning if `minibatches` = 1
        Stochastic Gradient Descent learning if `minibatches` = len(y)
        Minibatch learning if `minibatches` > 1
    random_seed : int (default: None)
        Set random state for shuffling and initializing the weights.
    print_progress : int (default: 0)
        Prints progress in fitting to stderr.
        0: No output
        1: Epochs elapsed and cost
        2: 1 plus time elapsed
        3: 2 plus estimated time until completion
    dtype : Array-type (default: None)
        Uses tensorflow.float32 if None.

    Attributes
    -----------
    weights_ : 2d-array, shape=[n_features, n_classes]
        Weights after fitting.
    biases_ : 1D-array, shape=[n_classes]
        Bias units after fitting.
    cost_ : list
        List of floats, the average cross_entropy for each epoch.
    train_acc_ : list
        List of training accuracies for each epoch
    valid_acc_ : list
        List of validation accuracies for each epoch

    """
    def __init__(self, eta=0.5, epochs=50,
                 minibatches=1, random_seed=None,
                 print_progress=0, dtype=None):

        if dtype is None:
            self.dtype = tf.float32
        else:
            self.dtype = dtype
        self.eta = eta
        self.epochs = epochs
        self.minibatches = minibatches
        self.random_seed = random_seed
        self.print_progress = print_progress

    def fit(self, X, y,
            init_weights=True, override_minibatches=None, n_classes=None,
            X_valid=None, y_valid=None):

        """Learn weight coefficients from training data.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.
        y : array-like, shape = [n_samples]
            Target values.
        init_weights : bool (default: True)
            (Re)initializes weights to small random floats if True.
        override_minibatches : int or None (default: None)
            Uses a different number of minibatches for this session.
        n_classes : int (default: None)
            A positive integer to declare the number of class labels
            if not all class labels are present in a partial training set.
            Gets the number of class labels automatically if None.
            Ignored if init_weights=False.
        X_valid : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Optional validation set to store the validation accuracy values
            for each epoch via self.valid_acc_
        y_valid : array-like, shape = [n_samples]
            Target values for X_valid

        Returns
        -------
        self : object

        """
        self._check_arrays(X, y)
        if override_minibatches:
            n_batches = override_minibatches
        else:
            n_batches = self.minibatches

        if y.shape[0] % n_batches != 0:
            raise AttributeError("Training set size %d cannot"
                                 " be divided into %d minibatches without"
                                 " remainder" % (y.shape[0], n_batches))

        if hasattr(X_valid, 'shape'):
            validation = True
        else:
            validation = False

        # Construct the Graph
        g = tf.Graph()
        with g.as_default():

            if init_weights:
                if n_classes:
                    self._n_classes = n_classes
                else:
                    self._n_classes = np.max(y) + 1
                self._n_features = X.shape[1]
                tf_weights_, tf_biases_ = self._initialize_weights(
                    n_features=self._n_features,
                    n_classes=self._n_classes)
                self.cost_ = []
                self.train_acc_ = []
                self.valid_acc_ = []
            else:
                tf_weights_ = tf.Variable(self.weights_)
                tf_biases_ = tf.Variable(self.biases_)

            # Prepare the training data
            y_enc = self._one_hot(y, self._n_classes)
            n_idx = list(range(y.shape[0]))
            tf_X = tf.convert_to_tensor(value=X, dtype=self.dtype)
            tf_y = tf.convert_to_tensor(value=y_enc, dtype=self.dtype)

            if validation:
                tf_X_valid = tf.convert_to_tensor(value=X_valid,
                                                  dtype=self.dtype)
                y_valid_enc = self._one_hot(y_valid, self._n_classes)
                tf_y_valid = tf.convert_to_tensor(value=y_valid_enc,
                                                  dtype=self.dtype)

            tf_idx = tf.placeholder(tf.int32,
                                    shape=[int(y.shape[0] / n_batches)])
            X_batch = tf.gather(params=tf_X, indices=tf_idx)
            y_batch = tf.gather(params=tf_y, indices=tf_idx)

            # Setup the graph for minimizing cross entropy cost
            net = tf.matmul(X_batch, tf_weights_) + tf_biases_
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(net,
                                                                    y_batch)
            cost = tf.reduce_mean(cross_entropy)
            optimizer = tf.train.GradientDescentOptimizer(
                learning_rate=self.eta)
            train = optimizer.minimize(cost)

            # Initializing the variables
            init = tf.initialize_all_variables()

        # random seed for shuffling
        if self.random_seed:
            np.random.seed(self.random_seed)

        # Launch the graph
        with tf.Session(graph=g) as sess:
            sess.run(init)
            self.init_time_ = time()
            for epoch in range(self.epochs):
                if self.minibatches > 1:
                    n_idx = np.random.permutation(n_idx)
                minis = np.array_split(n_idx, self.minibatches)
                costs = []
                for idx in minis:
                    _, c = sess.run([train, cost], feed_dict={tf_idx: idx})
                    costs.append(c)
                avg_cost = np.mean(costs)
                self.cost_.append(avg_cost)

                # compute prediction accuracy
                train_acc = self._accuracy(y, tf_X, tf_weights_, tf_biases_)
                self.train_acc_.append(train_acc)
                if validation:
                    valid_acc = self._accuracy(y_valid, tf_X_valid,
                                               tf_weights_, tf_biases_)
                    self.valid_acc_.append(valid_acc)
                else:
                    valid_acc = None
                self._print_progress(epoch + 1,
                                     cost=avg_cost,
                                     train_acc=train_acc,
                                     valid_acc=valid_acc)

            self.weights_ = tf_weights_.eval()
            self.biases_ = tf_biases_.eval()

    def _accuracy(self, y, tf_X, tf_weights_, tf_biases_):
        logits = tf.nn.softmax(tf.matmul(tf_X, tf_weights_) +
                               tf_biases_)
        y_pred = np.argmax(logits.eval(), axis=1)
        acc = np.sum(y == y_pred, axis=0) / float(y.shape[0])
        return acc

    def _resuse_weights(self, weights, biases):
            w = tf.Variable(weights)
            b = tf.Variable(biases)
            return w, b

    def _initialize_weights(self, n_features, n_classes):
            w = tf.Variable(tf.truncated_normal([n_features, n_classes],
                                                seed=self.random_seed))
            b = tf.Variable(tf.zeros([n_classes]))
            return w, b

    def predict(self, X):
        """Predict class labels of X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.

        Returns
        ----------
        class_labels : array-like, shape = [n_samples]
          Predicted class labels.

        """
        return np.argmax(self.predict_proba(X=X), axis=1)

    def predict_proba(self, X):
        """Predict class probabilities of X from the net input.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.

        Returns
        ----------
        Class probabilties : array-like, shape= [n_samples, n_classes]

        """
        self._check_arrays(X)
        if not hasattr(self, 'weights_'):
            raise AttributeError('The model has not been fitted, yet.')

        with tf.Session():
            tf.initialize_all_variables().run()
            tf_X = tf.convert_to_tensor(value=X, dtype=self.dtype)
            logits = tf.nn.softmax(tf.matmul(tf_X, self.weights_) +
                                   self.biases_)
            return logits.eval()
