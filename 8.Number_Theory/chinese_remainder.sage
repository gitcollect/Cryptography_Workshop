#!/usr/bin/env sage
"""Calculating with Chinese Remainder Theorem"""

# In this assignment, you will use the Chinese Remainder Theorem to do
# some calculations. First, you will have to write a function that
# converts a given integer i in Z_M to a tuple of remainders and back.
#
# In this assignment, we use the following data structure to represent
# the residuals:
#
# [(r_1, m_1), (r_2, m_2), ..., (r_3, m_3)]
#
# For example, Sun Zi's problem is represented as
#
# [(2,3), (3,5), (2,7)]
#
# Hint: sage function factor() factorizes a number into its prime
# factors.

#
# Statt i mod M zu berechnen (was bei grossen Zahlen sehr aufwaendig ist),
# berechnen wir die Primfaktoren von M und rechnen:
# [(i mod M_0, M_0), (i mod M_1, M_1)]
#
def int2remainder(i, M): # i == 23
	"""Convert an integer number to a list of pairs (residual, modulus).

	M shall be the product of the moduli, i.e. M=m_1;\ldots;m_n."""
	res = []
	
	for prime in list(factor(M)):
		res.append(tuple([i % prime[0]**prime[1], prime[0]**prime[1]]))
		
	return res

def extractProductExceptAtN(chineseRemainder, n):
	res = 1
	for i in range(len(chineseRemainder)):
		if i != n:
			res *= chineseRemainder[i][1]
	return res
	
def extractModulusNumber(chineseRemainder):
	return chineseRemainder[0][1] * extractProductExceptAtN(chineseRemainder, 0)

def findNumberModZeroExceptForI(chineseRemainder, product, at):
	factor = 1
	while True:
		found = True
		for i in range(len(chineseRemainder)):
			if i == at:
				# muss != 0 sein!
				if (factor*product) % chineseRemainder[i][1] != chineseRemainder[i][0]:
					found = False
					break
			else:
				# muss == 0 sein!
				if (factor*product) % chineseRemainder[i][1] != 0:
					found == False
					break
		if found:
			return factor*product
		factor += 1


def remainder2int(chineseRemainder):
	"""Convert a list of pairs (residual, modulus) to an integer."""

	bigNumber = 0
	
	for i in range(len(chineseRemainder)):
		product = extractProductExceptAtN(chineseRemainder, i)
		bigNumber += findNumberModZeroExceptForI(chineseRemainder, product, i)
	
	return bigNumber % extractModulusNumber(chineseRemainder)	

def remainderAdd(a, b, M):
	"""Calculate (a+b) % M using the Chinese Remainder Theorem."""
	
	lista = int2remainder(a, M)
	listb = int2remainder(b, M)
	listc = []
	
	for i in range(min(len(lista), len(listb))):
		listc.append( tuple([(lista[i][0] + listb[i][0]) % lista[i][1], lista[i][1]]))
		
	return remainder2int(listc)

def testRepresentation():
	# Lady
	x=[(4,5), (7,8), (3,9)]
	assert(remainder2int(x) == 39)
	# Stallings, p. 280
	x=int2remainder(973,1813)
	assert((remainder2int(x))== 973)
	# Sun Zi
	x=[(2,3), (3,5), (2,7)]
	assert(remainder2int(x) == 23)
	
def testAdd():
	# Stallings, p. 264
	assert(remainderAdd(678, 973, 1813) == (678+973))

if __name__ == "__main__":
	testRepresentation()
	testAdd()
