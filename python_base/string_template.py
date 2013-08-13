#!/usr/bin/python 
from string import Template

s = Template('There are ${howmany} ${lang} Quotation Symblos');
print s.substitute(lang='Python', howmany=3);
print s.safe_substitute(lang='Python');
