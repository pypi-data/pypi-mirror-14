# pryme

## written by J. Alex Ruble (Calamitizer)

([GitHub repository](https://github.com/Calamitizer/pryme))

## Overview

Note: This module is early in development and not too much super-cool stuff is implemented. Check it out if you're curious, though. The `Decomposition` class is pretty nifty.

This is (/ will be) a Python module for various number-theoretic operations and combinatorial structures. Certain major functions are memoized to disk for efficiency. For example, output data for `decompose()` (which computes the prime factorization of its argument) is stored in `./memo/decompose.pryme`.

This module is *not* intended to be suitable or efficient for large primes (> 2^64). The focus of this module is number theory on a more mundane scale. For efficient large primality tests and factorizations, the user is directed towards such modules as `gmpy2` and `SymPy`.

## Usage Guide

`NotImplemented`

## Changelog

### v0.2 (21 March '16)

* Miller-Rabin primality test implemented.
* `Decomposition`s are properly memoized.
* `Decomposition` testing script begun.

### v0.1 (13 March '16)

This is the first pushed version of pryme. Noteworthy features: the `Decomposition` class and various utility decorators.

## Jolly Cooperation

All contributions to and optimizations of this project are welcome. Just fork pryme on GitHub and follow your heart.

## Implementation

This code is written in Python 2.7.3. (So far) only Python standard library modules are used.

## Author

You can reach the author (Alex Ruble) most easily via GitHub ([Calamitizer](https://github.com/calamitizer)), email ([jaruble@ncsu.edu](mailto:jaruble@ncsu.edu)), or Twitter ([@aknifeallblade](https://twitter.com/aknifeallblade)).

## License

This software has no associated copyrights whatsoever (*i*.*e*. an [unlicense](http://unlicense.org/)). See `LICENSE.txt` for the full description. Crediting me is appreciated, but not required.
