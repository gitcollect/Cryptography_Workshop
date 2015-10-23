#!/usr/bin/env python
import math


def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def findPrimitivRootOf( n ):
	for num in range(2, n):
		dictionary = dict()
		found = True
		for power in range(1, n):
			key = (num ** power) % n
			if key in dictionary:
				found = False
				break
			else:
				dictionary[key] = 1
		if found:
			print (str(num)),
	
	
findPrimitivRootOf(17)
