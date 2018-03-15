#!/usr/bin/env python3

from __future__ import print_function

try:
    from builtins import __wraparmor__
except Exception:
    from __builtin__ import __wraparmor__
def wraparmor(func):
    def wrapper(*args, **kwargs):
         __wraparmor__(func)
         try:
             return func(*args, **kwargs)
         finally:
             __wraparmor__(func, 1)
    wrapper.__module__ = func.__module__
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__dict__.update(func.__dict__)
    func.__refcalls__ = 0
    # Only for test
    wrapper.orig_func = func
    return wrapper


"""
N queens problem.

The (well-known) problem is due to Niklaus Wirth.

This solution is inspired by Dijkstra (Structured Programming).  It is
a classic recursive backtracking approach.
"""

N = 8                                   # Default; command line overrides

class Queens:

    @wraparmor
    def __init__(self, n=N):
        self.n = n
        self.reset()

    @wraparmor
    def reset(self):
        n = self.n
        self.y = [None] * n             # Where is the queen in column x
        self.row = [0] * n              # Is row[y] safe?
        self.up = [0] * (2*n-1)         # Is upward diagonal[x-y] safe?
        self.down = [0] * (2*n-1)       # Is downward diagonal[x+y] safe?
        self.nfound = 0                 # Instrumentation

    @wraparmor
    def solve(self, x=0):               # Recursive solver
        for y in range(self.n):
            if self.safe(x, y):
                self.place(x, y)
                if x+1 == self.n:
                    self.display()
                else:
                    self.solve(x+1)
                self.remove(x, y)

    @wraparmor
    def safe(self, x, y):
        return not self.row[y] and not self.up[x-y] and not self.down[x+y]

    @wraparmor
    def place(self, x, y):
        self.y[x] = y
        self.row[y] = 1
        self.up[x-y] = 1
        self.down[x+y] = 1

    @wraparmor
    def remove(self, x, y):
        self.y[x] = None
        self.row[y] = 0
        self.up[x-y] = 0
        self.down[x+y] = 0

    silent = 0                          # If true, count solutions only

    @wraparmor
    def display(self):
        self.nfound = self.nfound + 1
        if self.silent:
            return
        print('+-' + '--'*self.n + '+')
        for y in range(self.n-1, -1, -1):
            print('|', end=' ')
            for x in range(self.n):
                if self.y[x] == y:
                    print("Q", end=' ')
                else:
                    print(".", end=' ')
            print('|')
        print('+-' + '--'*self.n + '+')

@wraparmor
def main():
    import sys
    silent = 0
    n = N
    if sys.argv[1:2] == ['-n']:
        silent = 1
        del sys.argv[1]
    if sys.argv[1:]:
        n = int(sys.argv[1])
    q = Queens(n)
    q.silent = silent
    q.solve()
    print("Found", q.nfound, "solutions.")

if __name__ == "__main__":
    main()
    import dis
    print(dis.dis(Queens))
    print(dis.dis(main))