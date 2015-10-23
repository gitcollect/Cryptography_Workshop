#!/usr/bin/env python2

DEBUG=0

# We are going to use the following keys and plaintexts in this
# assignment.
plaintext0 = 0x02468ACEECA86420
plaintext1 = 0x12468ACEECA86420
key0       = 0x08C73A08514436F2E150A865EB75443F904396E66638E182170C1CA1CB6C1062
key1       = 0x18C73A08514436F2E150A865EB75443F904396E66638E182170C1CA1CB6C1062

# We use the s-boxes of Central Bank of Russian Federation in this
# assignment.
sboxes = [ [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
           [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
           [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
           [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
           [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
           [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
           [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
           [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12] ]

# This week's assignment is to meausure the avalance effect in GOST,
# both for changes in the plaintext and in the key. As you can see,
# the two plaintexts and the two keys differ in 1 bit, respectively.
#
# In order to measure the avalance effect for differences in the
# plaintext, you encrypt both plaintext0 and plaintext1 with
# key0. After each round of encryption, you measure how many bits of
# the intermediate ciphertexts differ.
#
# In order to measure the avalance effect for difference in the key,
# you encrypt plaintext0 both with key0 and with key1. Again, you
# measure how many bits of the intermediate ciphertexts differ.
#
# In order to complete this assignment, you have to write your own
# implementation of GOST. You can use function testEncrypt() to check
# if your implementation is correct. Even if your implementation does
# not encrypt to the same ciphertext as in the example, please carry
# on and measure the avalance effects for your implementation.


def generateNTimesFourOneBits ( n):
	res = 0
	for i in range( n):
		res = res << 0x4 | 0xf
	return res

# at ist ein Wert zwischen 0 und 7.
# 7 waeren die obersten 8 Bit, 0 die kleinsten (rechts) 8  Bit.
def getKeyAt(bigKey, at):
	mask = generateNTimesFourOneBits(8)
	return (bigKey >> at*32) & mask
	
# Getestet, funktioniert!
def generateSubKey(bigKey, rounds):
	if rounds < 24:
		rounds = rounds % 8
	else:
		rounds = 7 - (rounds % 8)
	
	return getKeyAt(bigKey, rounds)

# Bekommt 32 Bit rein.
# In 4er Bloecke teilen und ersetzen.
def useSBox(data):
	mask = generateNTimesFourOneBits(1)
	newData = data
	for i in range(8):
		# 4 Bits herausfiltern
		subData = (newData & mask) >> 4*i
		# 4 Bits ersetzen mit S-Box
		subData = sboxes[i][subData]
		# 4 Bits wieder in das Data einordnen
		# 4 Bits in Data leer machen und subData einfuegen
		newData = (newData & ~mask) | (subData << 4*i)
		mask = mask << 4
	return newData
		
	
	
# Besteht aus:
# - Addiere Key + r mod 2^32 
# - S-Box Anwenden
# - 11 Bit nach links shiften und die 11 Bit rechts reinshiften
#
def f(key, r):
	# key + r
	data = (key + r) % (2**32)
	# S-Box anwenden
	data = useSBox(data)
	
	# Ersten 11 Bits merken
	first11Bits = (data >> (32-11)) & 0x7ff
	# 11 Bits rausshiften und abschneiden.
	data = (data << 11) & generateNTimesFourOneBits(8)
	# Gemerkte 11 Bits links reinshiften.
	data = data | first11Bits
	
	return data

def gostEncrypt(plaintext, key, rounds=32):
	
	if rounds <= 0:
		return plaintext
	
	newA = plaintext >> 32
	newB = plaintext & generateNTimesFourOneBits(8)
	
	subKey = generateSubKey(key, 32-rounds)
	
	tmpB = newB
	newB = newA ^ f(subKey, newB)
	newA = tmpB
	
	# Text zusammenfuehren fuer die naechste Rekursion
	newText = (newA << 32) | newB
	
	return gostEncrypt(newText, key, rounds-1)


def bitDifference(a, b):
    """Return number of bits different between a and b."""
    diff = 0
    while a > 0 or b > 0:
		if ((a & 1) ^ (b & 1)) == 1:
			diff += 1
		a >>= 1
		b >>= 1
    
    return diff
    

def testEncrypt():
    assert(gostEncrypt(plaintext=plaintext0, key=key0) ==
           0x8470BE35A752F0CB)
    # Since it is notoriously hard to get bit ordering in crypto
    # algorithms right, here are the temporary values for the first
    # four rounds of encryption:
    #
    # Round:             1
    # Left:              0x02468ACE
    # Right:             0xECA86420
    # Round Key:         0xCB6C1062
    # R + Round Key:     0xB8147482
    # S-Box Application: 0xE0B5FA29
    # Shift Left:        0xAFD14F05
    # Round:             2
    # Left:              0xECA86420
    # Right:             0xAD97C5CB
    # Round Key:         0x170C1CA1
    # R + Round Key:     0xC4A3E26C
    # S-Box Application: 0x638151F7
    # Shift Left:        0x0A8FBB1C
    # Round:             3
    # Left:              0xAD97C5CB
    # Right:             0xE627DF3C
    # Round Key:         0x6638E182
    # R + Round Key:     0x4C60C0BE
    # S-Box Application: 0x5616B515
    # Shift Left:        0xB5A8AAB0
    # Round:             4
    # Left:              0xE627DF3C
    # Right:             0x183F6F7B
    # Round Key:         0x904396E6
    # R + Round Key:     0xA8830661
    # S-Box Application: 0x303174FA
    # Shift Left:        0x8BA7D181
    #
    # Do not worry if you are not able to reproduce this encryption,
    # just carry on with the rest of this assignment.

def plaintextAvalance():
    print('\nAvalance effect for changes in plaintext.')
    print('Original difference: %d' %
          bitDifference(plaintext0, plaintext1))
    for rounds in xrange(32):
        c0 = gostEncrypt(plaintext=plaintext0, key=key0, rounds=rounds)
        c1 = gostEncrypt(plaintext=plaintext1, key=key0, rounds=rounds)
        print('Round: %02d Delta: %d' % (rounds+1, bitDifference(c0, c1)))

def keyAvalance():
    print('\nAvalance effect for changes in key.')
    print('Original difference: %d' % 
          bitDifference(plaintext0, plaintext0))
    for rounds in xrange(32):
        c0 = gostEncrypt(plaintext=plaintext0, key=key0, rounds=rounds)
        c1 = gostEncrypt(plaintext=plaintext0, key=key1, rounds=rounds)
        print('Round: %02d Delta: %d' % (rounds+1, bitDifference(c0, c1)))

testEncrypt()
plaintextAvalance()
keyAvalance()

