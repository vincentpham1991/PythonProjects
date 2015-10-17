#Name: Vincent Pham

def rot13(message):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	map = alphabet[13:] + alphabet[:13]
	ceasarMsg = ""
	for letter in message:
		letterNum = ord(letter)
		if (letter >= 'a' and letter <='z'):
			index = letterNum - ord('a')
			ceasarMsg += map[index]
		elif (letter >= 'A' and letter <= 'Z'):
			index = letterNum - ord('A')
			ceasarMsg += map[index].upper()
		else:
			ceasarMsg += letter
	return ceasarMsg
	
msg = "See Spot run!"
hiddenMsg = rot13(msg)

print "original message: " + msg
print "hiddem message: " + hiddenMsg