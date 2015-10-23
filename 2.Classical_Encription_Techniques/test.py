
en_alphabet = "abcdefghijklmnopqrstuvwxyz"

def compute_incidence(ciphertext):
	resList = []
	for ch in en_alphabet:
		resList.append((ch, ciphertext.count(ch)))
	return sorted(resList, key=lambda x: x[1])

def char_to_num(c):
	return en_alphabet.index(c.lower())

def is_alphabetic_char(c):
	return (c.lower() in en_alphabet)

def monoalphabetic_substitution(text, subs):
	# Beispiel:
	#	text: 'aabbccddeeffggzz'
	#	subs: 'bcd_fg...a'
	#	out : 'bbccddDDffgghhaa'
	
	plainText = ""
	
	for ch in text:
		if is_alphabetic_char(ch):
			if subs[char_to_num(ch)] == '_':
				plainText += ch.upper()
			else:
				plainText += subs[char_to_num(ch)].lower()
			print "substitute: " + ch + " with: " + subs[char_to_num(ch)].lower()
		else:
			plainText += ch
			
	return plainText
			

print monoalphabetic_substitution("hallo du da", "_cdefghijklmnopqrstuvwxyza")
