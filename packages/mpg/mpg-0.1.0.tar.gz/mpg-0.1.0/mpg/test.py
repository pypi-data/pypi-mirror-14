# Copyright  2016  Kevin Murray <spam@kdmurray.id.au>
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

import itertools as itl

import numpy as np

from .counter import TransitionCounter
from .generator import MarkovGenerator
from .util import (
    iter_kmers,
    hash_to_kmer,
)


def test_iter_kmers():
    dbs = "AACAGATCCGCTGGTTA"
    k = 2
    counts = np.zeros(4**k)
    for kmer in iter_kmers(dbs, k):
        counts[kmer] += 1
    assert counts.sum() == len(dbs) - k + 1, counts.sum()
    assert (counts == 1).all(), counts


def test_hash_to_kmer():
    k = 2
    hashes = range(4**k)
    kmers = map(''.join, list(itl.product(list('ACGT'), repeat=k)))
    for hsh, mer in zip(hashes, kmers):
        h2k = hash_to_kmer(hsh, k)
        assert h2k == mer, (hsh, mer, h2k)


def test_transition_counter_consume():
    dbs = 'AAACAAGAATACCACGACTAGCAGGAGTATCATGATTCCCGCCTCGGCGTCTGCTTGGGTGTTTAA'
    t = TransitionCounter(2)
    t.consume(dbs)
    counts = t.transition_counts
    assert (counts == 1).all(), counts
    P = t.transitions
    assert (P.sum(1) == 1).all(), P.sum(1)
    pi = t.steady_state
    assert pi.sum() == 1, pi.sum()
    assert np.allclose(pi.dot(t.P.toarray()),  pi), pi
