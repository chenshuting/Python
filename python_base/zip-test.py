#!/usr/bin/python 

list_1 = ['idan', 'stuart', 'david']
list_2 = ['bairnson', 'elliott','paton']

list = zip(list_1, list_2);
print list;

for i, j in zip(list_1, list_2):
	print ('%s %s' % (i, j))#.title();

