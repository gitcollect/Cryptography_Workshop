def f(r):
	return ~r;

def feistel(a, b):
	newA = ord(a)
	newB = ord(b)
	print str(newA) + ", " + str(newB)
	for i in range(16):
		tmpA = newA
		newA = newB
		newB = tmpA ^ f(newB)
	print str(newA) + ", " + str(newB)
	print "test: a xor b xor 1: " + str(ord(a)^~ord(b))

feistel('z', 'b')
