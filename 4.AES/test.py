#!/usr/bin/env sage


def int2blist(n, length):
    b = bin(n)
    l = string2blist(b[2:])
    return([0]*(length-len(l)) + l)
    
def string2blist(s):
    return(map(int, list(s)))

def sbox_sub(nib):
	b0 = nib & 0x1
	b1 = (nib>>1) & 0x1
	b2 = (nib>>2) & 0x1
	b3 = (nib>>3) & 0x1
	
	L.<a> = GF(2^4)
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
		b = \
		  V(int2blist((~L([b3,b2,b1,b0])).integer_representation(),
					  4))
		sbox_out = list(m*b+a)
	return sbox_out

def sbox(nib):
	sbox = sbox_sub(nib)
	res = 0
	if (sbox[0] == 1):
		res |= 1<<3
	if (sbox[1] == 1):
		res |= 1<<2
	if (sbox[2] == 1):
		res |= 1<<1
	if (sbox[3] == 1):
		res |= 1
	return res

# 8 Bit Nibble. 
def rotNib(nib):
	# Die 4 ersten Bits und die 4 zweiten Bits tauschen!
	return ((nib & 0xf) << 4) | ((nib >> 4) & 0xf)

# 8 Bit Nibble.
def subNib(nib):
	return sbox(nib)

def generateKeys(key):
	keys = []
	# 16bit-Key splitten in w0, w1:
	w0 = key & 0xff00
	w1 = key & 0xff
	keys.insert(0,hex(key))
	
	
	#w2 = 
	
	
	
	return keys
	
	
	
print generateKeys(0x4af5)
