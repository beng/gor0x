#!/usr/bin/pypy
# markov.py - Vedant Kumar <vsk@berkeley.edu>

"""
A node is some atomic, fundamental unit.
A state is an ordered collection of nodes (a history).
A branch contains a list of nodes that can follow a given state (the future).
A Markov chain maps states to their branches.
"""

import random
from collections import defaultdict, deque

class Branch:
        def __init__(self):
                '''Node => Frequency'''
                self.total = 0.0
                self.counts = defaultdict(int)

        def update(self, node):
                '''Add a future node to this branch.'''
                self.total += 1
                self.counts[node] += 1

        def merge_branch(self, branch):
                '''Merge another branch into this one.'''
                self.total += branch.total
                for node, freq in branch.counts.iteritems():
                        self.counts[node] += freq

        def sample(self):
                '''Randomly sample a node from this branch.'''
                thresh = random.random()
                for node, freq in self.counts.iteritems():
                        probability = freq / self.total
                        if probability >= thresh:
                                return node
                        thresh -= probability
                return random.choice(list(self.counts.keys()))

class MarkovChain:
        def __init__(self, n_limit):
                '''State => Branch
                n_limit: Maximum history per node.'''
                self.n_limit = n_limit
                self.transitions = defaultdict(Branch)

        def add_sequence(self, seq):
                '''seq: List of hash-able information.'''
                for state, node in self._find_transitions(seq):
                        self.transitions[state].update(node)
                self._update_state_list()

        def random_state(self):
                '''Pick a random state in the chain.'''
                return random.choice(self._state_list)

        def walk(self):
                '''Generate a walk through the chain.'''
                start = self.random_state()
                history = deque(start, maxlen=self.n_limit)
                while True:
                        node = self.walk_from(tuple(history))
                        history.append(node)
                        yield node

        def walk_from(self, state):
                '''Take one random step in the chain.'''
                while len(state):
                        branch = self.transitions[state]
                        if branch.total > 0:
                                return branch.sample()
                        state = tuple(state[1:])
                return self.walk_from(self.random_state())

        def merge_chain(self, chain):
                '''Merge another chain into this one.'''
                for state, branch in chain.transitions.iteritems():
                        self.transitions[state].merge_branch(branch)
                self._update_state_list()

        def _find_transitions(self, seq):
                '''Generate all states and their futures.'''
                for i in xrange(len(seq)):
                        for j in xrange(1, self.n_limit + 1):
                                state = seq[i:i+j]
                                if len(state) == j and (i + j) < len(seq):
                                        yield tuple(state), seq[i + j]

        def _update_state_list(self):
                self._state_list = list(self.transitions.keys())
 
class SparseMarkovChain(MarkovChain):
        def _find_transitions(self, seq):
                for i in xrange(len(seq)):
                        state = seq[i:self.n_limit+i]
                        if len(state) == self.n_limit and (i + self.n_limit) < len(seq):
                                yield tuple(state), seq[i + self.n_limit]

