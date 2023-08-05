import math
import numbers
import fractions
import operator
import functools
import pickle

class Decomposition(dict):
    """
    Decompose a number and store its prime factorization.
    
    Should be primarily called through decompose(n), to memoize the result.
    
    d = Decomposition(n) creates an object satisfying:
    if p is prime:
        d[p] = e, where e is the exponent of p in the unique prime
        factorization of n. This means e = 0 if p does not divide n.
    if p is not prime:
        Accessing d[p] raises an exception.
    """    
    def __init__(self, arg):
        dict.__init__(self)
        if type(arg) is int:
            self.n = arg
            candidates = primes(int(math.floor(math.sqrt(self.n))))
            d = self.n
            for c in candidates:
                while d % c == 0:
                    self[c] += 1
                    d /= c
        elif isinstance(arg, dict):
            for d in arg:
                self[d] = arg[d]
            self.n = product([pow(d, self[d]) for d in self])
    def __getitem__(self, d):
        assert_prime(d)
        return dict.__getitem__(self, d)
    def __missing__(self, d):
        return 0
    def __setitem__(self, d, e):
        assert_prime(d)
        assert_natural(e, 0)
        if e == 0:
            return
        dict.__setitem__(self, d, e)
    def __delitem__(self, d):
        self.n /= pow(d, self[d])
        dict.__delitem__(self, d)
    def __repr__(self):
        return type(self).__name__ + '(' + str(self.n) + ')'
    def __add__(self, rhs):
        if type(rhs) is int:
            return self + decompose(rhs)
        if type(rhs) is type(self):                                             
            return decompose(self.n + rhs.n)
    def __radd__(self, lhs):
        return self + rhs
    def __mul__(self, rhs):
        if type(rhs) is int:
            return decompose(self.n * rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            return Decomposition({d: self[d] + rhs[d] for d in factors})
    def __rmul__(self, lhs):
        return self * lhs

def needs_decomp(f):
    """
    Decorator for typing arguments as Decomposition.
    
    If the argument not already a Decomposition, this makes one out of it.
    """
    @functools.wraps(f)
    def wrapper(arg):
        if type(arg) is Decomposition:
            return f(arg)
        assert_natural(arg)
        return f(decompose(arg))
    return wrapper

#put somewhere, decorate?
def product(container):
    return reduce(operator.mul, container, 1)

def memoize(f): # works!
    """
    Memoization decorator for a function taking a single argument
    """
    class Memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, n):
            return self[n]
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return Memodict(f)

def memoize_with_log(f): # works!
    """
    Goal: make the above print
    """
    print '! Memoizing ' + f.__name__
    class Memodict(dict):
        def __init__(self, f):
            self.__name__ = f.__name__
            self.f = f
        def __call__(self, n):
            return self[n]
        def __missing__(self, key):
            ret = self[key] = self.f(key)
            return ret
    f = Memodict(f)
    @functools.wraps(f)
    def final(n):
        log = '! called ' + f.__name__ + '(' + str(n) + ')'
        print log
        return f(n)
    print '! Memoized ' + final.__name__
    return final

def optional_arguments(d):
    """
    Decorate the input decorator d to accept optional arguments.
    """
    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return d(args[0])
        else:
            def real_decorator(decoratee):
                return d(decoratee, *args)
            return real_decorator
    return wrapped_decorator

@optional_arguments
def natural_input(f, m = 1):
    """
    Decorate the input function f to only take ints above m.
    """
    @functools.wraps(f)
    def final(n):
        assert_natural(n, m)
        return f(n)
    return final

def with_print_name(f): # works
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        print '! ' + f.__name__ + ' called'
        return f(*args, **kwds)
    return wrapper

@natural_input
def primes(n):
    """
    Return a list of primes no greater than n.
    """
    return [2, 3, 5, 7, 11, 13, 17, 19, 23]

@natural_input
def is_prime(n):
    """
    Return whether n is prime.
    """
    return n in primes(n)

def mt(f):
    """
    Return the mobius transform of the input function f.
    """
    @natural_input
    def mf(n):
        return sum([mobius(n/d) * f(d) for d in divisors(n)])
    return mf

@needs_decomp
def divisors(decomp):
    print 2
    """
    Return a set of all divisors of the argument.
    """
    combine = lambda acc, p: set(a * pow(p, e) for a in acc for e in xrange(decomp[p] + 1))
    return reduce(combine, decomp, {1})

@natural_input
def decompose(n):
    """
    Return a memoized Decomposition of n.
    
    e.g. decompose(12) = {2: 2, 3: 1}
    """
    return Decomposition(n)

@memoize_with_log
def fib(n):
    assert_natural(n, 0)
    if n in xrange(2):
        return n
    return fib(n - 1) + fib(n - 2)

@natural_input
def decompose(n):
    return Decomposition(n)

def assert_natural(n, m = 1):
    """
    Asserts that n is of type int and is greater than m.
    """
    message = str(n) + ' is not a natural number (of type int).'
    assert (type(n) is int) and (n >= m), message

def assert_prime(n):
    message = str(n) + ' is not a prime (of type int).'
    assert is_prime(n), message

@natural_input
def constant(n):
    """
    Return 1.
    
    Needs to accept a Decomposition.
    """
    return 1

@natural_input
def identity(n):
    """
    Return n.
    
    Needs to accept a Decomposition.
    """
    return n

@natural_input(0)
def power_gen(k):
    """
    Return a function yielding the k-th power of its argument.
    """
    if k == 0:
        return constant
    if k == 1:
        return identity
    @natural_input
    def power_k(n):
        return pow(n, k)
    return power_k

@natural_input
def unit(n):
    return int(n == 1)

@needs_decomp
def totient(decomp):
    factors = [1 - fractions.Fraction(1, d) for d in decomp]
    return int(decomp.n * product(factors))

@needs_decomp
def mobius(decomp):
    """
    Return the mobius function evaluated at the argument.
    
    Accepts an int or a Decomposition.
    Called lowercase-mu in number theory.
    mobius(n) = (-1)^support(n) if n is square-free, 0 otherwise.
    """
    return 0 if any([p >= 2 for _, p in decomp]) else pow(-1, (breadth(decomp) % 2))

@needs_decomp
def num_divisors(decomp):
    return product([decomp[d] + 1 for d in decomp])

@needs_decomp
def sum_divisors(decomp):
    a = [pow(d, decomp[d] + 1) - 1 for d in decomp]
    b = [d - 1 for d in decomp]
    factors = [fractions.Fraction(x, y) for x, y in zip(a, b)]
    #factors = [fractions.Fraction(pow(d, decomp[d] + 1), pow(d, decomp[d])) for d in decomp]
    return int(product(factors))

@natural_input(0)
def sigma_gen(k):
    if k == 0:
        return num_divisors
    if k == 1:
        return sum_divisors
    @needs_decomp
    def sigma_k(decomp):
        a = [pow(pow(d, decomp[d] + 1), k) - 1 for d in decomp]
        b = [pow(d, k) - 1 for d in decomp]
        # rewrite this line, jeez
        factors = [fractions.Fraction(x, y) for x, y in zip(a, b)]
        return int(product(factors))
    return sigma_k

@needs_decomp
def num_abel(decomp):
    """
    Return the number of isodistinct Abelian groups of the given order.
    """
    return product([partitions(decomp[p]) for p in decomp])

@natural_input
def liouville(n):
    return pow(-1, breadth(n))

@natural_input
def gamma(n):
    return pow(-1, breadth(n))

@natural_input
def ramanujan(n):
    return 1

@needs_decomp
def support(decomp):
    """
    Return the number of distinct prime factors of the argument.
    
    Accepts an int or a Decomposition.
    Called lowercase-omega in number theory.
    """
    return len(decomp)

@needs_decomp
def breadth(decomp):
    """
    Return the sum of the exponents in the decomposition of the argument.
    
    Accepts an int or a Decomposition.
    Called uppercase-Omega in number theory.
    """
    return sum([decomp[d] for d in decomp])

def main():
    x = decompose(20)
    y = decompose(12)
    z1 = x + y
    #print z1
    z2 = x * y

if __name__ == '__main__':
    main()















