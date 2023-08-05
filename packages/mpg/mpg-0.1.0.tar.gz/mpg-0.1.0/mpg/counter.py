# Copyright 2016 Kevin Murray <spam@kdmurray.id.au>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import screed
import numpy as np
import scipy as sp
from scipy import sparse
from scipy.sparse import linalg
import yaml

from .util import (
    iter_kmers,
)


class TransitionCounter(object):

    def __init__(self, k, alphabet=set("ACGT")):
        self.bitmask = 2**(2 * k) - 1  # Set lowest 2*k bits
        self.k = k
        self.alphabet = set(alphabet)
        self.n = len(alphabet) ** k
        self.transition_counts = np.zeros((self.n, len(alphabet)))
        self._transitions = None
        self._P = None

    def _clear(self):
        self._transitions = None
        self._P = None

    def save(self, filename):
        data = {
            'alphabet': list(sorted(self.alphabet)),
            'k': self.k,
            'transitions': self.transitions.tolist(),
        }
        with open(filename, 'w') as fh:
            yaml.dump(data, fh)

    def load(self, filename):
        with open(filename, 'r') as fh:
            data = yaml.load(fh)
        datakeys = list(sorted(data.keys()))
        if datakeys != ['alphabet', 'k', 'transitions']:
            exc = ValueError("Data file is not valid")
            exc.keys = datakeys
            raise exc
        self.__init__(data['k'], data['alphabet'])
        self._transitions = np.array(data['transitions'])
        self.transition_counts = np.array(data['transitions'])

    def consume(self, sequence):
        self._clear()
        for subseq in sequence.split('N'):
            if not subseq or len(subseq) < self.k:
                continue
            kmers = iter_kmers(subseq, self.k)
            # pop the first kmer
            fr = next(kmers)
            for to in kmers:
                self.transition_counts[fr, to & 3] += 1
                fr = to

    def consume_file(self, filename):
        self._clear()
        with screed.open(filename) as sequences:
            for seq in sequences:
                self.consume(seq['sequence'])

    @property
    def transitions(self):
        if self._transitions is not None:
            return self._transitions
        transitions = self.transition_counts
        transitions /= transitions.sum(1)[:, np.newaxis]
        self._transitions = transitions
        return transitions

    @property
    def P(self):
        if self._P is not None:
            return self._P
        sparse_P = sparse.lil_matrix((self.n, self.n))
        num_kmers, alpha_size = self.transitions.shape
        for fr in range(num_kmers):
            for a in range(alpha_size):
                to = (fr << 2 | a) & self.bitmask
                sparse_P[fr, to] = self.transitions[fr, a]
        self._P = sparse_P
        return sparse_P

    @property
    def steady_state(self):
        v, w = linalg.eigs(self.P.transpose(), which='LR')
        ssf = np.real(w[:, v.argmax()])
        ssf /= ssf.sum()
        return ssf
