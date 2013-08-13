#!/usr/bin/python 
import string,os

alphas = string.letters + '_'
nums = string.digits

print 'Welcome to the Identifier checker v1.0'
print 'Testees must be at least 2 chars long'
myInput = raw_input('>');
if len(myInput) > 1:
	if myInput[0] not in alphas:
		print 'invalid: first symbol must be alphabetic'
	else:
		for otherChar in myInput[1:]:
			if otherChar not in alphas + nums:
				print 'invalid: remaining symbol must be alphabetic or numbers'
				break;
else:
	print "okay as Identifier"

