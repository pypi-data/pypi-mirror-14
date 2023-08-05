from __future__ import absolute_import

import numpy as np
import pytest

from hmmlearn import hmm

from . import log_likelihood_increasing, normalized


class TestMultinomialAgainstWikipedia(object):
    """Using examples from Wikipedia

    - http://en.wikipedia.org/wiki/Hidden_Markov_model
    - http://en.wikipedia.org/wiki/Viterbi_algorithm
    """
    def setup_method(self, method):
        n_components = 2   # ['Rainy', 'Sunny']
        n_features = 3     # ['walk', 'shop', 'clean']
        self.h = hmm.MultinomialHMM(n_components)
        self.h.n_features = n_features
        self.h.startprob_ = np.array([0.6, 0.4])
        self.h.transmat_ = np.array([[0.7, 0.3], [0.4, 0.6]])
        self.h.emissionprob_ = np.array([[0.1, 0.4, 0.5],
                                         [0.6, 0.3, 0.1]])

    def test_decode_viterbi(self):
        # From http://en.wikipedia.org/wiki/Viterbi_algorithm:
        # "This reveals that the observations ['walk', 'shop', 'clean']
        #  were most likely generated by states ['Sunny', 'Rainy', 'Rainy'],
        #  with probability 0.01344."
        X = [[0], [1], [2]]
        logprob, state_sequence = self.h.decode(X, algorithm="viterbi")
        assert round(np.exp(logprob), 5) == 0.01344
        assert np.allclose(state_sequence, [1, 0, 0])

    def test_decode_map(self):
        X = [[0], [1], [2]]
        _logprob, state_sequence = self.h.decode(X, algorithm="map")
        assert np.allclose(state_sequence, [1, 0, 0])

    def test_predict(self):
        X = [[0], [1], [2]]
        state_sequence = self.h.predict(X)
        posteriors = self.h.predict_proba(X)
        assert np.allclose(state_sequence, [1, 0, 0])
        assert np.allclose(posteriors, [
            [0.23170303, 0.76829697],
            [0.62406281, 0.37593719],
            [0.86397706, 0.13602294],
        ])


class TestMultinomailHMM(object):
    def setup_method(self, method):
        self.n_components = 2
        self.n_features = 3
        self.h = hmm.MultinomialHMM(self.n_components)
        self.h.startprob_ = np.array([0.6, 0.4])
        self.h.transmat_ = np.array([[0.7, 0.3], [0.4, 0.6]])
        self.h.emissionprob_ = np.array([[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]])

    def test_attributes(self):
        with pytest.raises(ValueError):
            self.h.emissionprob_ = []
            self.h._check()

        with pytest.raises(ValueError):
            self.h.emissionprob_ = np.zeros((self.n_components - 2,
                                             self.n_features))
            self.h._check()

    def test_score_samples(self):
        idx = np.repeat(np.arange(self.n_components), 10)
        n_samples = len(idx)
        X = np.random.randint(self.n_features, size=(n_samples, 1))

        ll, posteriors = self.h.score_samples(X)
        assert posteriors.shape == (n_samples, self.n_components)
        assert np.allclose(posteriors.sum(axis=1), np.ones(n_samples))

    def test_sample(self, n_samples=1000):
        X, state_sequence = self.h.sample(n_samples)
        assert X.ndim == 2
        assert len(X) == len(state_sequence) == n_samples
        assert len(np.unique(X)) == self.n_features

    def test_fit(self, params='ste', n_iter=5):
        h = self.h
        h.params = params

        lengths = np.array([10] * 10)
        X, _state_sequence = h.sample(lengths.sum())

        # Mess up the parameters and see if we can re-learn them.
        h.startprob_ = normalized(np.random.random(self.n_components))
        h.transmat_ = normalized(
            np.random.random((self.n_components, self.n_components)),
            axis=1)
        h.emissionprob_ = normalized(
            np.random.random((self.n_components, self.n_features)),
            axis=1)

        assert log_likelihood_increasing(h, X, lengths, n_iter)

    def test_fit_emissionprob(self):
        self.test_fit('e')

    def test_fit_with_init(self, params='ste', n_iter=5):
        lengths = [10] * 10
        X, _state_sequence = self.h.sample(sum(lengths))

        # use init_function to initialize paramerters
        h = hmm.MultinomialHMM(self.n_components, params=params,
                               init_params=params)
        h._init(X, lengths=lengths)

        assert log_likelihood_increasing(h, X, lengths, n_iter)

    def test__check_input_symbols(self):
        assert self.h._check_input_symbols([[0, 0, 2, 1, 3, 1, 1]])

        # a) non-contigous
        assert not self.h._check_input_symbols([[0, 0, 3, 5, 10]])
        # b) not enough data
        assert not self.h._check_input_symbols([[0]])
        # c) non-integral
        assert not self.h._check_input_symbols([[0., 2., 1., 3.]])
        # d) negative integers
        assert not self.h._check_input_symbols([[0, 0, -2, 1, 3, 1, 1]])
