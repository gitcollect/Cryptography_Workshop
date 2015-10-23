import socket
import time
import alsaaudio, time, audioop
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
		
#def createMicrophoneNoise(fileName):

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(1250)
l,data = inp.read()

result = ""

while len(result) < 2500:
	# Read data from device
	l,data = inp.read()
	#print l
	if l:
		# Return the maximum of the absolute value of all samples in a fragment.
		#print audioop.max(data, 2)
		print data
		result += data
		time.sleep(.001)
		
print result		
#print createMicrophoneNoise("")






















