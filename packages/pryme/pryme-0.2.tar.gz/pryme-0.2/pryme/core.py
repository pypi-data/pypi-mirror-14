import math
import numbers
import fractions
import operator

from .decorators import *

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
    def __init__(self, arg={}):
        dict.__init__(self)
        if type(arg) is int:
            self.n = 1
            candidates = primes(int(math.floor(math.sqrt(arg))))
            print 'cand: ' + `candidates`
            r = arg
            for p in candidates:
                if r == 1:
                    break
                while r % p == 0:
                    self[p] += 1
                    r //= p
            if is_prime(r):
                self[r] = 1
            return
        elif isinstance(arg, dict):
            self.n = 1
            for key in arg:
                self[key] = arg[key]
            return
        class DecompConstructionError(Exception):
            def __init__(self, arg):
                message = 'Invalid Decomposition constructor argument: {c}'
                message = message.format(c=repr(arg))
                Exception.__init__(self, message)
        raise DecompConstructionError(arg)
    def __getitem__(self, p):
        assert_prime(p)
        return dict.__getitem__(self, p)
    def __missing__(self, p):
        return 0
    def __setitem__(self, p, e):
        assert_prime(p)
        assert_natural(e, 0)
        if e == 0:
            if p in self:
                dict.__delitem__(self, p)
            return
        if e >= self[p]:
            self.n *= p ** (e - self[p])
        else:
            self.n //= p ** (self[p] - e)
        dict.__setitem__(self, p, e)
    def __delitem__(self, p):
        self.n //= p ** self[p]
        dict.__delitem__(self, p)
    def __str__(self):
        return str(int(self))
    def __repr__(self):
        return type(self).__name__ + '(' + str(self.n) + ')'
    def __format__(self, code):
        if code == 'd':
            return str(int(self))
        return dict.__format__(self, code)
    def __int__(self):
        return self.n
    def __bool__(self):
        return True
    def __lt__(self, rhs):
        return int(self) < int(rhs)
    def __le__(self, rhs):
        return int(self) <= int(rhs)
    def __gt__(self, rhs):
        return int(self) > int(rhs)
    def __ge__(self, rhs):
        return int(self) >= int(rhs)
    def __eq__(self, rhs):
        return int(self) == int(rhs)
    def __ne__(self, rhs):
        return int(self) != int(rhs)
    def __hash__(self):
        return dict.__hash__(self)
    def __add__(self, rhs):
        if type(rhs) in [int, type(self)]:
            return decompose(int(self) + int(rhs))
        self._raisetypeerror(rhs)
    def __radd__(self, lhs):
        return self + lhs
    def __sub__(self, rhs):
        if type(rhs) in [int, type(self)]:
            return decompose(int(self) - int(rhs))
        self._raisetypeerror(rhs)
    def __rsub__(self, lhs):
        if type(lhs) in [int, type(self)]:
            return decompose(int(lhs) - int(self))
        self._raisetypeerror(lhs)
    def __mul__(self, rhs):
        if type(rhs) is int:
            return self * decompose(rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            return Decomposition({p: self[p] + rhs[p] for p in factors})
        self._raisetypeerror(rhs)
    def __rmul__(self, lhs):
        return self * lhs
    def __div__(self, rhs):
        if type(rhs) is int:
            assert_divides(rhs, int(self))
            return self / decompose(rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            quotient = Decomposition(1)
            # use comprehension
            return Decomposition({p: max(self[p] - rhs[p], 0) for p in factors})
        self._raisetypeerror(rhs)
    def __rdiv__(self, lhs):
        if type(lhs) is int:
            assert_divides(int(self), lhs)
            return decompose(lhs) / self
        if type(lhs) is type(self):
            return lhs / self
        self._raisetypeerror(lhs)
    def __pow__(self, rhs):
        if type(rhs) in [int, type(self)]:
            return Decomposition({p: self[p] * int(rhs) for p in self})
        self._raisetypeerror(rhs)
    def __rpow__(self, lhs):
        if type(lhs) in [int, type(self)]:
            return Decomposition({p: lhs[p] * int(self) for p in decompose(lhs)})
        self._raisetypeerror(lhs)
    def __and__(self, rhs):
        if type(rhs) is int:
            return rhs & decompose(rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            return Decomposition({p: min(self[p], rhs[p]) for p in factors})
        self._raisetypeerror(rhs)
    def __rand__(self, lhs):
        return self & lhs
    def __or__(self, rhs):
        if type(rhs) is int:
            return rhs & decompose(rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            return Decomposition({p: max(self[p], rhs[p]) for p in factors})
        self._raisetypeerror(lhs)
    def __ror__(self, lhs):
        return self | lhs
    def _print(self):
        for p in self:
            print 'items:'
            print `p` + ': ' + `self[p]`
    def _raisetypeerror(self, arg):
        message = 'unsupported operand type(s): {0} and {1}'
        message = message.format(type(self).__name__, type(arg).__name__)
        raise TypeError(message)
    def expansion(self):
        factors = []
        for p in self:
            factors.append('({p}^{e})'.format(p=p, e=self[p]))
        expansion = '*'.join(factors) if factors else '1'
        return '{n} = '.format(n=int(self)) + expansion

class _Decomposer(object):
    def __init__(self):
        self._filename = 'decompose.pryme'
        self._file = None
    def __call__(self, n):
        self._open()
        try:
            d = self._decode(self._file[str(n)])
        except KeyError:
            d = Decomposition(n)
            self._file[str(n)] = self._encode(d)
        self._close()
        return d
    def _open(self):
        if self._file is None:
            self._file = anydbm.open(self._filename, 'c')
    def _close(self):
        if self._file is not None:
            self._file.close()
            self._file = None
    def _encode(self, decomp):
        return json.dumps(dict(decomp))
    def _decode(self, decompstr):
        d = ast.literal_eval(decompstr)
        return Decomposition({int(p): d[p] for p in d})

decompose = _Decomposer()

class _PrimeTable(object):
    def __init__(self):
        self.max = 1

class MemoFile(dict):
    def __init__(self, name):
        dict.__init__(self)
        self.name = name
    def __getitem__(self, n):
        assert_natural(n)
        with self.open() as datafile:
            pass # Read
    def __setitem__(self, n):
        assert_natural(n)
        with self.open() as datafile:
            pass # Write

def needs_decomp(f): #move
    """
    Decorator for typing arguments as Decomposition.
    
    If the argument is not already a Decomposition, this makes one out of it.
    """
    @functools.wraps(f)
    def wrapper(arg):
        if type(arg) is Decomposition:
            return f(arg)
        assert_natural(arg)
        return f(decompose(arg))
    return wrapper

def needs_int(f): #move
    """
    Decorator for typing arguments as int from Decomposition.
    """
    @functools.wraps(f)
    def wrapper(arg):
        if type(arg) is int:
            assert_natural(arg)
            return f(arg)
        return f(decompose(arg))
    return wrapper

class DecompTable(dict):
    def __init__(self):
        dict.__init__(self)
    def __getitem__(self, n):
        assert_natural(n)
        return dict.__getitem(self, n)
    def __setitem__(self, n, d):
        assert_natural(n)
        assert type(d) is Decomposition
        assert int(d) == n 
        dict.__setitem__(n, d)
    def __missing__(self, n):
        d = decompose(n)
        self.__setitem__(n, d)
        return d

def assert_prime(n):
    message = str(n) + ' is not a prime (of type int).'
    assert is_prime(n), message

#put somewhere, decorate?
def product(container):
    return reduce(operator.mul, container, 1)

@natural_input
def mr_prime(n):
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    d = n - 1
    s = 0
    while (d % 2 == 0):
        d //= 2
        s += 1
    witnesses = mr_witnesses(n)
    if not witnesses:
        m = min(n - 1, int(math.floor((2 * math.log(n)) ** 2)))
        witnesses = xrange(2, m + 1)
    for a in witnesses:
        if all([(a ** d) % n != 1 and (a ** ((2 ** r) * d)) % n != n - 1 for r in xrange(s)]):
            return False
    return True

@natural_input
def mr_witnesses(n):
    if n < 2047:
        return [2]
    if n < 1373653:
        return [2, 3]
    if n < 9080191:
        return [31, 73]
    if n < 25326001:
        return [2, 3, 5]
    if n < 3215031751:
        return [2, 3, 5, 7]
    return None

@natural_input
def primes(n):
    """
    Return a list of primes no greater than n.
    """
    return [i for i in xrange(1, n + 1) if mr_prime(i)]

@natural_input
def is_prime(n):
    """
    Return whether n is prime.
    """
    return mr_prime(n)

def dirichlet_conv(f, g):
    """
    Return the Dirichlet convolution of input functions f and g.
    """
    @natural_input
    def fg(n):
        return sum([f(d) * g(n//d) for d in divisors(n)])
    return fg

def mobius_transform(f):
    """
    Return the Mobius transform of the input function f.
    """
    return dirichlet_conv(f, mobius)

@needs_decomp
def divisors(decomp):
    """
    Return a set of all divisors of the argument.
    """
    combine = lambda acc, p: set(a * (p ** e) for a in acc for e in xrange(decomp[p] + 1))
    return reduce(combine, decomp, {1})

@natural_input
def decompose(n):
    """
    Return a memoized Decomposition of n.
    
    e.g. decompose(12) = {2: 2, 3: 1}
    """
    if type(n) is Decomposition:
        return n
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
        return n ** k
    return power_k

@natural_input
def unit(n):
    return int(n == 1)

@needs_decomp
def totient(decomp):
    factors = [1 - fractions.Fraction(1, d) for d in decomp]
    return int(int(decomp) * product(factors))

@needs_decomp
def mobius(decomp): #fix 1 value
    """
    Return the mobius function evaluated at the argument.
    
    Accepts an int or a Decomposition.
    Called lowercase-mu in number theory.
    mobius(n) = (-1)^support(n) if n is square-free, 0 otherwise.
    """
    return 0 if any([decomp[p] >= 2 for p in decomp]) else (-1) ** (breadth(decomp) % 2)

@needs_decomp
def num_divisors(decomp):
    return product([decomp[p] + 1 for p in decomp])

@needs_decomp
def sum_divisors(decomp):
    a = [(p ** (decomp[p] + 1)) - 1 for p in decomp]
    b = [p - 1 for p in decomp]
    factors = [fractions.Fraction(x, y) for x, y in zip(a, b)]
    return int(product(factors))

@natural_input(0)
def sigma_gen(k):
    if k == 0:
        return num_divisors
    if k == 1:
        return sum_divisors
    @needs_decomp
    def sigma_k(decomp):
        a = [(p ** ((decomp[p] + 1) * k)) - 1 for p in decomp]
        b = [p ** k - 1 for p in decomp]
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
    return -1 ** breadth(n)

@natural_input
def gamma(n):
    return -1 ** breadth(n)

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















