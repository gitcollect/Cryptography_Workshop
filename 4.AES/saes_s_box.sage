#!/usr/bin/env sage
# -*- coding: utf-8 -*-

# Implemented the Simplified AES algorithm as described in
# Stalling's book and the following paper:
# 
#
# Hint: A detailed walk-through of an encryption and a decryption
# operation is given in the following paper:
# 

def xor(a, b):
    def h(x,y):
        if(x==y):
            return(0)
        else:
            return(1)
    return(map(lambda (x, y): h(x,y), zip(a,b)))


def int2blist(n, length):
    b = bin( n )
    l = string2blist(b[2:])
    return([0]*(length-len(l)) + l)
    
def string2blist(s):
    return(map(int, list(s)))

# Sonst stehen hier nach der S-Box: 
# 'sage.rings.finite_rings.element_givaro.FiniteField_givaroElement'
# drin. Dann schlagen später Operationen fehl...
def convertToIntList(data):
	res = []
	for i in range(4):
		res.append(int(data[i]))
	return res

def sbox(nib):
	b0 = nib[0]
	b1 = nib[1]
	b2 = nib[2]
	b3 = nib[3]
	
	L. = GF(2^4)
	V = VectorSpace(GF(2),4)
	m = Matrix(L,
			   [ [1, 0, 1, 1]
			   , [1, 1, 0, 1]
			   , [1, 1, 1, 0]
			   , [0, 1, 1, 1]
			   ])
	a = V([1, 0, 0, 1])

	sbox_in = [b0,b1,b2,b3]
	
	# [0,0,0,0] is a special case.
	if sbox_in == [0,0,0,0]:
		sbox_out = [1,0,0,1]
	else:
		b = V(int2blist((~L([b3,b2,b1,b0])).integer_representation(),
					  4))
		sbox_out = convertToIntList(list(m*b+a))
	return sbox_out
	
def bigSBox(data):
	return sbox(data[:4]) + sbox(data[4:8]) + sbox(data[8:12]) + sbox(data[12:])
		
def inv_sbox(nub):
	L. = GF(2^4)
	V = VectorSpace(GF(2),4)
	m = Matrix(L,
			   [ [1, 0, 1, 1]
			   , [1, 1, 0, 1]
			   , [1, 1, 1, 0]
			   , [0, 1, 1, 1]
			   ])
	a = V([1, 0, 0, 1])
	for b0 in xrange(0,2):
		for b1 in xrange(0,2):
			for b2 in xrange(0,2):
				for b3 in xrange(0,2):
					sbox_in = [b0,b1,b2,b3]
					# [0,0,0,0] is a special case.
					if sbox_in == [0,0,0,0]:
						sbox_out = [1,0,0,1]
					else:
						b = V(int2blist((~L([b3,b2,b1,b0])).integer_representation(),
									  4))
						sbox_out = list(m*b+a)
						
					if sbox_out == nub:
						return sbox_in
	
def inv_bigSBox(data):
	return inv_sbox(data[:4]) + inv_sbox(data[4:8]) + inv_sbox(data[8:12]) + inv_sbox(data[12:])

# 8 Bit Nibble. 
def rotNib(nib):
	return nib[4:] + nib[:4]
	
# 8 Bit Nibble.
def subNib(nib):
	return sbox(nib[:4]) + sbox(nib[4:])

def pp(b):
    """Pretty print bit lists"""
    t = "".join(map(str, b))
    r = ""
    for i in xrange(0, len(t), 4):
        r += t[i:i+4] + ' '
    return(r)

# Since the mix column operations are tricky, the following
# implementations are provided for your convenience.
def mix_col(d, inv=False):
    L. = GF(2^4);
    V = VectorSpace(GF(2),8)
    if inv:
        MixColumns_matrix = Matrix(L, [[a^3+1,a],[a,a^3+1]])
    else:
        MixColumns_matrix = Matrix(L, [[1,a^2],[a^2,1]])
    d0 = d[0:4]
    d0.reverse()
    d1 = d[4:8]
    d1.reverse()
    d2 = d[8:12]
    d2.reverse()
    d3 = d[12:16]
    d3.reverse()
    
    dMatrix = Matrix(L, [[d0, d2], [d1, d3]])
    
    matrixProduct = MixColumns_matrix*dMatrix
    r = []
    for j in xrange(2):
        for i in xrange(2):
            r += int2blist(int(matrixProduct[i][j]._int_repr()), 4)
    return(r)

def inv_mix_col(d):
    return(mix_col(d=d, inv=True))

def generateKeys(key):
	keys = []
	
	w0 = key[:8]
	w1 = key[8:]
	w2 = xor(w0, xor(int2blist(0x80, 8), subNib(rotNib(w1))))
	w3 = xor(w2, w1)
	w4 = xor(w2, xor(int2blist(0x30, 8), subNib(rotNib(w3))))
	w5 = xor(w4, w3)
	keys.append(w0+w1)
	keys.append(w2+w3)
	keys.append(w4+w5)
	
	return keys
	
def shiftRow(data):
	return data[:4] + data[12:] + data[8:12] + data[4:8]

def addRoundKey(data, key):
	return xor(data, key)

def saes_encrypt(plaintext, key):
    
    ciphertext = plaintext
    keys = generateKeys(key)    
    ciphertext = addRoundKey(ciphertext, keys[0])
    
    ####### Round 1:
    ciphertext = bigSBox(ciphertext)
    ciphertext = shiftRow(ciphertext)  
    ciphertext = mix_col(ciphertext)    
    ciphertext = addRoundKey(ciphertext, keys[1])
    
    ###### Round 2:    
    ciphertext = bigSBox(ciphertext)
    ciphertext = shiftRow(ciphertext)
    ciphertext = addRoundKey(ciphertext, keys[2])    
    
    return ciphertext
    
def saes_decrypt(ciphertext, key):
    
    plaintext = ciphertext
    keys = generateKeys(key)
    plaintext = addRoundKey(plaintext, keys[2])
    plaintext = shiftRow(plaintext)
    
    plaintext = inv_bigSBox(plaintext)
    plaintext = addRoundKey(plaintext, keys[1])
    plaintext = inv_mix_col(plaintext)
    
    plaintext = shiftRow(plaintext)
    plaintext = inv_bigSBox(plaintext)
    plaintext = addRoundKey(plaintext, keys[0])
    
    return plaintext

def test():
    for (plaintext, key, ciphertext) in [
         (# Stallings, Exercise 5.10 / 5.12 / 5.14
          '0110111101101011',
          '1010011100111011',
          '0000011100111000')
        ,(# Gordon
          '1101011100101000',
          '0100101011110101',
          '0010010011101100')
        ,(# Holden
          '0110111101101011',
          '1010011100111011',
          '0000011100111000')
        ]:
        plaintext = string2blist(plaintext)
        ciphertext = string2blist(ciphertext)
        key = string2blist(key)
        assert(saes_encrypt(plaintext=plaintext, key=key)
               == ciphertext)
        assert(saes_decrypt(ciphertext=ciphertext, key=key)
               == plaintext)
test()
