import socket
import time
#from Xlib import display

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

def stringToHexArray(s):
	res = []
	for i in s:
		res.append(hex(ord(i))[2:])
	return res
	
def reduceArray (array):
	res = ""
	for c in array:
		res += c
	return res

def simple_hash_function(s):
	ret = 0
	for i in s:
		ret = 31*ret + ord(i) << 3
	return ret

def crossFoot(d):
	res = 0
	for i in d:
		res += ord(i)
	return res
		
def generateKey(digit):
	key = ""
	while len(key) < 64:
		key += digit		
	return key[:64]
	
def str2hex(s):
    oneLongString = " ".join(map(lambda x: "%02X" % ord(x), s))
    splitString = ""
    hexBytesPerLine = 16
    for i in xrange(0,len(oneLongString), hexBytesPerLine*3):
        splitString += oneLongString[i:i+hexBytesPerLine*3] + '\n'
    return(splitString)
    
def hex2str(s):
    return("".join(map(lambda x: chr(int(x, 16)), s.split())))
		
def createNetworkNoise(fileName):
	
	result = []
	#create an INET, raw socket
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

	startTime = time.time()
	lastCrossFoot = "333"

	# receive a packet
	while len(result) < 2500:
		#print str("%.16f" % (time.time() - startTime))[2:]
		traffic = s.recvfrom(65565)
		#print traffic[0][:16]
		
		packet = traffic[0][7:7+16]
		diffT  = str("%.16f" % (time.time() - startTime))[2:]
		thisCrossFoot = str(crossFoot(diffT)) + diffT
		
		packetArray = stringToHexArray(packet)
		diffTArray  = stringToHexArray(str(simple_hash_function(diffT))[:16])
		
		xored = reduceArray(hexArrayToChar(xorHexArray(packetArray, diffTArray)))
		
		plaintext = reduceArray(xorHexArray(packetArray, diffTArray))[:64]
		key       = reduceArray(stringToHexArray(generateKey(lastCrossFoot)))
		
		tmpResult = xorHexArray(packetArray, diffTArray)
		#print key
		
		#print gostEncrypt(plaintext, key, 30)
		
		startTime = time.time()
		
		lastCrossFoot = reduceArray(hexArrayToChar(xorHexArray(stringToHexArray(thisCrossFoot), stringToHexArray(lastCrossFoot))))
		result += tmpResult

	endResult = ""

	for char in result[:2500]:
		endResult += chr(int(char,16))
	return endResult

print createNetworkNoise("")






















