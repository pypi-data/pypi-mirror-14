============================
Markovian Sequence Generator
============================

Generates DNA sequences using a Markov Chain, learned from some reference
sequence(s).

Many thanks to Ben Kaehler for a proof of concept and mathematical assistance.

**Disclaimer**: This is unstable software at the moment. Use with caution.

.. image:: https://travis-ci.org/kdmurray91/mpg.svg?branch=master
    :target: https://travis-ci.org/kdmurray91/mpg

Installation
------------

.. code-block:: shell

    pip install cython numpy nose
    pip install -U -e 'git+https://github.com/kdmurray91/mpg#egg=mpg'


Usage
-----

The script ``mpg`` should have been installed. This learns the transition
probablitlies from sequences (in Fasta format) and generates random sequences
from this Markov chain.

To learn transition probablities for a 5th-order Markov chain from the
Arabidopsis genome and store them in a file (``ath.yml``):

.. code-block:: shell

    mpg -k 5 -d ath.yml TAIR_10.fasta

To use these transition probablitlies to generate a sequence of 1000bp:

.. code-block:: shell

    mpg -l 1000 -r ath.yml

To do the above operations at once:

.. code-block:: shell

    mpg -l 1000 -k 5 TAIR_10.fasta
