#!/usr/bin/env python

"""FIPS 140-2: RNG Power-Up Tests"""

# Asses the quality of your TRNG by running the statistical random
# number generator tests from Chapter 4.9.1 (Power-Up Tests) of "FIPS
# PUB 140-2 - SECURITY REQUIREMENTS FOR CRYPTOGRAPHIC MODULES". The
# document is available on the handout server.

FILENAME='random.dat'

def readRandomBits(filename):
	"""Read file and return it as list of bits."""
	rn = []
	rnFile = open(filename, 'rb')
	rn = map(ord, rnFile.read())
	rnFile.close()
	return(reduce(lambda x,y: x+int2bin(y,8), rn, []))

def int2bin(x, n):
	"""Convert integer to array of bits.

	x : integer
	n : length of bit array"""
	b = map(lambda x: ord(x)-ord('0'), list(bin(x)[2:]))
	return([0]*(n-len(b)) + b)

def bin2int(b):
	"""Convert array of bits to integer."""
	return(int("".join(map(lambda x: chr(x+ord('0')), b)), 2))

def testRandomNumbers(randomBits):
	assert (monobitTest(randomBits))
	assert (pokerTest(randomBits))
	assert (runsTest(randomBits))
	assert (longRunsTest(randomBits))
	#print (monobitTest(randomBits))
	#print (pokerTest(randomBits))
	#print (runsTest(randomBits))
	#print (longRunsTest(randomBits))

def monobitTest(randomBits):
	"""FIPS 140-2 monobit test"""
	# Count the number of ones in the 20,000 bit stream. Denote this
	# quantity by x.
	#
	# The test is passed if 9725 < x < 10275
	
	x = 0
	for i in randomBits:
		x += i
	
	return 9725 < x and x < 10275
	
	
def pokerTest(randomBits):
	"""FIPS 140-2 poker test"""
	# Divide the 20000 bit stream into 5000 contiguous 4 bit
	# segments. Count and store the number of occurrences of the 16
	# possible 4 bit values. Denote f[i] as the number of each 4 bit
	# value i where 0 < i < 15.
	#
	# Evaluate the following:
	#				   15
	#				   --
	# x = (16/5000) * ( \  f[i]^2 ) - 5000
	#				   /
	#				   --
	#				  i=0
	#
	# The test is passed if 2.16 < x < 46.17
	#
	# See fips_140_2.pdf, page 39-40
	
	bitArray = []
	for i in range(5000):
		bitArray.append(tuple(randomBits[i*4:i*4+4]))
		
	dictionary = dict()
	
	for key in bitArray:
		if key in dictionary:
			dictionary[key] = dictionary[key] + 1
		else:
			dictionary[key] = 1
			
	x = 0
	for i in dictionary:
		x += dictionary[i]*dictionary[i]
	
	x = (16.0/5000.0) * x - 5000.0
	
	return 2.16 < x and x < 46.17	
	
def addToDict(dictionary, key):
	if key in dictionary:
		v = dictionary[key]
		dictionary[key] = v+1
	else:
		dictionary[key] = 1

def runsTest(randomBits):
	"""FIPS 140-2 runs test"""
	# A run is defined as a maximal sequence of consecutive bits of
	# either all ones or all zeros that is part of the 20000 bit
	# sample stream. The incidences of runs (for both consecutive
	# zeros and consecutive ones) of all lengths (>= 1) in the
	# sample stream should be counted and stored.
	#
	# The test is passed if the runs that occur (of lengths 1 through
	# 6) are each within the corresponding interval specified in the
	# table below. This must hold for both the zeros and ones (i.e.,
	# all 12 counts must lie in the specified interval). For the
	# purposes of this test, runs of greater than 6 are considered to
	# be of length 6.
	#
	# Length	  Required Interval
	# of Run 
	# 1		   2343 - 2657
	# 2		   1135 - 1365
	# 3			542 -  708
	# 4			251 -  373
	# 5			111 -  201
	# 6+		   111 -  201
	#
	# See fips_140_2.pdf, page 40
	
	if randomBits[0] == 0:
		randomBits = [1] + randomBits
	else:
		randomBits = [0] + randomBits
	if randomBits[-1] == 0:
		randomBits = randomBits + [1]
	else:
		randomBits = randomBits + [0]
	
	samples = [ (1, [[0,1,0], [1,0,1]]),
				(2, [[0,1,1,0], [1,0,0,1]]),
				(3, [[0,1,1,1,0], [1,0,0,0,1]]),
				(4, [[0,1,1,1,1,0], [1,0,0,0,0,1]]),
				(5, [[0,1,1,1,1,1,0], [1,0,0,0,0,0,1]]),
				(6, [[0,1,1,1,1,1,1,0], [1,0,0,0,0,0,0,1]])]
	
	dictionary0 = dict()
	dictionary1 = dict()
	
	i = 0
	while i < len(randomBits):
		foundSample = False
		for s in samples:
			if s[1][0] == randomBits[i:i+s[0]+2]:
				addToDict(dictionary1, s[0])
				foundSample = True
				i += s[0]-1
				break
			if s[1][1] == randomBits[i:i+s[0]+2]:
				addToDict(dictionary0, s[0])
				foundSample = True
				i += s[0]-1
				break
		if not foundSample and not i > len(randomBits)-7:
			if (randomBits[i+6] == 0):
				addToDict(dictionary0, 6)
			else:
				addToDict(dictionary1, 6)
			bit = randomBits[i+1]
			while randomBits[i+1] == bit:
				i += 1
			i -= 1
		i += 1
		
	dictionaries = [dictionary0, dictionary1]
	tests = [False, False]
	
	for i in range(2):
		tests[i] = dictionaries[i][1] >= 2343 and dictionaries[i][1] <= 2657 and \
				dictionaries[i][2] >= 1135 and dictionaries[i][2] <= 1365 and \
				dictionaries[i][3] >= 542  and dictionaries[i][3] <= 708  and \
				dictionaries[i][4] >= 251  and dictionaries[i][4] <= 373  and \
				dictionaries[i][5] >= 111  and dictionaries[i][5] <= 201  and \
				dictionaries[i][6] >= 111  and dictionaries[i][6] <= 201;
	return tests[0] and tests[1]
		
def longRunsTest(randomBits):
	"""FIPS 140-2 long runs test"""
	# A long run is defined to be a run of length 26 or more (of
	# either zeros or ones). On the sample of 20000 bits, the test is
	# passed if there are no long runs.
	#
	# See fips_140_2.pdf, page 40
	
	lastBit = randomBits[0]
	count = 0
	maxCount = 0
	for i in randomBits:
		if lastBit == i:
			count += 1
			if count > maxCount:
				maxCount = count
		else:
			count = 1
			lastBit = i
	
	return maxCount < 26
	

if __name__ == "__main__":
	randomBits = readRandomBits(filename=FILENAME)
	testRandomNumbers(randomBits=randomBits)
