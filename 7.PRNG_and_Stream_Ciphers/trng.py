#!/usr/bin/env python

import socket
import time
import alsaaudio, time, audioop

"""True Random Number Generator"""

# Write a true random number generator. In order to do so, you have to
# identify a source of true randomness. Creative sources of randomness
# are appreciated. If you cannot use Python/Sage for this assignment,
# e.g. because you want to access low-level functionality not
# available in Python/Sage, you may also submit C code for this
# assignment.
#
# Your function shall output 20000 random bits as byte values,
# i.e. it should write a file of 2500 random bytes.

FILENAME='random.dat'
N=2500

def str2hex(s):
    oneLongString = " ".join(map(lambda x: "%02X" % ord(x), s))
    splitString = ""
    hexBytesPerLine = 16
    for i in xrange(0,len(oneLongString), hexBytesPerLine*3):
        splitString += oneLongString[i:i+hexBytesPerLine*3] + '\n'
    return(splitString)

def xorHex(a,b):
	return hex(int(a,16) ^ int(b,16))[2:]

def reduceArray (array):
	res = ""
	for c in array:
		res += c
	return res
	
def hexArrayToChar(a):
	res = []
	for i in a: 
		res.append(chr(int(i,16)))
	return res
	
def xorHexArray(a, b):
	res = []
	for i in range(min(len(a), len(b))):
		res.append(hex(int(a[i], 16) ^ int(b[i], 16))[2:])
	return res
	
def generateKey(digit):
	key = ""
	while len(key) < 64:
		key += digit		
	return key[:64]

def simple_hash_function(s):
	ret = 0
	for i in s:
		ret = 31*ret + ord(i) << 3
	return ret

def stringToHexArray(s):
	res = []
	for i in s:
		res.append(hex(ord(i))[2:])
	return res

def crossFoot(d):
	res = 0
	for i in d:
		res += ord(i)
	return res

def createMicrophoneNoise(n):
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

	inp.setchannels(1)
	inp.setrate(8000)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

	inp.setperiodsize(n/2)
	l,data = inp.read()

	result = ""

	while len(result) < n:
		l,data = inp.read()
		if l:
			result += data
			time.sleep(.001)
			
	return result[:n]

def createNetworkNoise(n):
	
	result = []
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

	startTime = time.time()
	lastCrossFoot = "333"
	start = 0

	# receive a packet
	while len(result) < n:
		traffic = s.recvfrom(65565)
		
		packet = traffic[0][start:start+16]
		diffT  = str("%.16f" % (time.time() - startTime))[2:]
		thisCrossFoot = str(crossFoot(diffT)) + diffT
		
		packetArray = stringToHexArray(packet)
		diffTArray  = stringToHexArray(str(simple_hash_function(diffT))[:16])
		
		tmpResult = xorHexArray(packetArray, diffTArray)
		startTime = time.time()
		
		#lastCrossFoot = reduceArray(hexArrayToChar(xorHexArray(stringToHexArray(thisCrossFoot), stringToHexArray(lastCrossFoot))))
		result += tmpResult
		start += 1

	endResult = ""
	
	inverseResult = result[::-1]
	length = len(result[:n])
	
	for i in range(len(result)):
		index = (i*3) % length
		result[i] = xorHex(result[i], inverseResult[index])
	
	#for char in result[:n]:
	#	endResult += chr(int(char,16))
	endResult = hexArrayToChar(result[:n])
	
	return endResult

def trng(filename, n):
	rn = []

	a = str2hex(createNetworkNoise(n)).split(' ')
	b = str2hex(createMicrophoneNoise(n)).split(' ')
	
	rn = reduceArray(hexArrayToChar(xorHexArray(a, b)))
	
	rnFile = open(filename, 'wb')
	for i in rn:
		rnFile.write(i)
	rnFile.close()

if __name__ == "__main__":
	trng(filename=FILENAME, n=N)
