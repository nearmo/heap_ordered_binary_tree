#!/usr/bin/env python3

from math import log, floor
from statistics import mean
from re import findall

class PQ(object):
    '''Initialises instance'''
    def __init__(self):
        self.d = {}
        self.N = 0

    '''swaps the position of two values'''
    def exch(self, i, j):
        self.d[i], self.d[j] = self.d[j], self.d[i]

    '''inserts a new element into the heap at position N'''
    def insert(self, v):
        self.N += 1
        self.d[self.N] = v
        self.swim(self.N)

    '''element moves up in the tree until its parent node is larger than itself'''
    def swim(self, k):
        while k > 1 and self.d[k // 2] < self.d[k]:
            self.exch(k // 2, k)
            k = k // 2

    '''returns True if the heap is empty False otherwise'''
    def is_empty(self):
        return self.size() == 0

    '''returns the size of the heap'''
    def size(self):
        return self.N

    '''returns the max of the heap which resides at the top'''
    def getMax(self):
        return self.d[1]

    ''' Return the bigger of nodes i and j'''
    def bigger(self, i, j):
        try:
            return max([i, j], key=self.d.__getitem__)
        except KeyError:
            return i

    ''' Deletes and returns the maximum node in the heap.'''
    def delMax(self):
        v = self.d[1]
        self.exch(1, self.N)
        del(self.d[self.N])
        self.N -= 1
        self.sink(1)
        return v

    ''' Node k sinks down the heap until its child node is smaller than itself'''
    def sink(self, k):
        # While there is a child left
        while 2 * k <= self.N:
            # Indexing of left child
            j = 2 * k
            # Select bigger child
            j = self.bigger(j, j + 1)
            # Done if >= both children
            if self.d[k] >= self.d[j]:
                break
            # Swap with larger child
            self.exch(k, j)
            k = j

    ''' Returns the size of a heap based on the number of rows'''
    def len(self, row):
        if row == 1:
            return 1
        return self.len(row - 1) + 2 ** (row - 1)

    ''' Returns the base layer of the heap in str form'''
    def base(self):
        self.a_len = len(self.d)
        self.no_row = floor(log(self.a_len, 2) + 1)
        self.t_len = self.len(self.no_row)
        t_base = 2 ** (self.no_row - 1)
        a_base = t_base - (self.t_len - self.a_len)
        return ' '.join(self.elements()[-a_base:])

    ''' Returns a list of lists consisting of the elements in each individual row'''
    def rows(self):
        elements = self.elements()
        rows = []
        for i in range(self.no_row):
            row = []
            j = 0
            while j < len(elements) and j < 2 ** i:
                row.append(elements[j])
                j += 1
            rows.append(row)
            elements = elements[2 ** i:]
        return rows

    ''' Returns a list of each element in the heap in indexed form'''
    def elements(self):
        elements = []
        for v in self.d.values():
            elements.append(str(v))
        return elements

    ''' Returns the second last layer of the heap so as to function as a base
    for each layer above'''
    def layer(self):
        layer = ' ' * self.t_len
        p = 1
        for i in range(len(self.rows()[-2])):
            n = self.rows()[-2][i]
            layer = layer[:p] + n + layer[p + len(n):]
            p += 4
        return layer

    ''' Returns a list of strings of each layer in the heap from the second
    upward'''
    def lines(self):
        line = ' ' * self.t_len
        lines = [line] * (self.no_row - 2)
        lines.append(self.layer())
        #i represents every line to be outputted
        for i in range(1, len(lines)):
            i = -i - 1
            #j represents the position of every element in the line of i
            for j in range(1, len(self.rows()[i - 1]) + 1):
                #l and h represents to two child nodes of j
                l, h = self.rows()[i][(j * 2) - 2], self.rows()[i][(j * 2) - 1]
                l, h = lines[i + 1].find(l), lines[i + 1].find(h)
                p = mean([l, h])
                n = self.rows()[i - 1][j - 1]
                lines[i] = lines[i][:p] + n + lines[i][(p + len(n)):]
        return lines

    ''' Returns the heap-ordered binary tree in string format'''
    def __str__(self):
        base = self.base()
        lines = self.lines()
        return '\n'.join(lines) + '\n' + base
