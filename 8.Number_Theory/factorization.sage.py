# This file was *autogenerated* from the file factorization.sage
from sage.all_cmdline import *   # import sage library
_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_10 = Integer(10); _sage_const_150 = Integer(150); _sage_const_310 = Integer(310)#!/usr/bin/env sage

# In this exercise, you will get some idea how hard prime
# factorization is.  First you are going to create composite numbers
# from two prime numbers.  Then, you will factorize these numbers and
# measure the time.

import time

def bitLen(n ):
	return len(bin(n )[_sage_const_2 :])
	
def generateNBits9s(n ):
	return _sage_const_1 <<n

def generateN(b):
	"""Generates a b-bits number n=p*q where p and q are prime numbers."""
	# For this assignment, generate a composite number n from two
	# random prime numbers p and q. Your number b shall consist of
	# b binary digits. For example, the decimal number 17 has 5 binary
	# digits, because its binary representation is 10001.
	#
	# Hint: Use Sage function random_prime to generate random primes.
	res = _sage_const_3 
	while bitLen(res) != b:
		num = generateNBits9s(b/_sage_const_2 -_sage_const_1 )
		p = random_prime(num*_sage_const_10 , proof=True, lbound=(num-_sage_const_1 ))
		q = random_prime(num*_sage_const_10 , proof=True, lbound=(num-_sage_const_1 ))
		res = p*q
	return res

def timeToFactor(n):
	"""Returns the time in seconds it takes to factor n."""
	# For this assignment, return the time in seconds it takes
	# to factorize composite number n into its prime factors p and q.
	#
	# Hint: Use Sage function factor() for the actual factorization.
	# Use Python function time.clock() to get the time in seconds.
	
	t0 = time.clock()
	factor(n)
	return time.clock() - t0

def measureTime():
	for i in range(_sage_const_150 ,_sage_const_310 ,_sage_const_10 ):
		n = generateN(i)
		print('Factoring a %d bits number took %.2f seconds.'
			  % (i, timeToFactor(n)))

measureTime()
