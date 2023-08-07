import numpy as np
from collections import defaultdict


class BaseEstimator:
    y_required = True
    fit_required = True

    def fit(self, X, y=None):
        X, y = self._check_input(X, y)
        self._fit(X, y)

    def predict(self, X):
        X = self._check_x(X)
        if self.fit_required:
            raise ValueError("Fit method should be called first.")
        return self._predict(X)

    def _check_x(self, X):
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if X.size == 0:
            raise ValueError("The array X must be non-empty")
        elif X.ndim > 2:
            raise ValueError("Input must be a 2-dimensional array.")
        elif X.ndim == 1:
            X = np.expand_dims(X, axis=1)
        return X

    def _check_input(self, X, y=None):
        X = self._check_x(X)

        if self.y_required:
            if y is None:
                raise ValueError("Argument y is required.")
            if not isinstance(y, np.ndarray):
                y = np.array(y)
            if y.size == 0:
                raise ValueError("The array y must be non-empty")
        return X, y

    def _fit(self, X, y=None):
        raise NotImplementedError("Subclasses must implement _fit method.")

    def _predict(self, X):
        raise NotImplementedError("Subclasses must implement _predict method.")


class BaseOptimizer:
    def __init__(
            self,
            gradient_fn,
            parameters,
            learning_rate,
            batch_size,
            tolerance=1e-8,
            max_iter=1000
    ):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.gradient_fn = gradient_fn
        self.parameters = parameters
        self.tol = tolerance
        self.max_iter = max_iter
        self.history = defaultdict(list)

    def batch_generator(self, X, y):
        n_samples = X.shape[0]
        batch_size = self.batch_size
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        for i in range(0, n_samples, batch_size):
            batch_indices = indices[i:i+batch_size]
            yield X[batch_indices], y[batch_indices]
  
    def clear_history(self):
        self.history = defaultdict(list)

    def update_parameters(self, parameters, gradient):
        raise NotImplementedError(
            "Subclasses must implement update_parameters method.")

    def optimize(self):
        raise NotImplementedError("Subclasses must implement optimize method.")
