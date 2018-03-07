#!/usr/bin/python
import sys

def prompt():
	response = sys.stdin.readline().strip()
	return response

fields = ['Please tell me your name: ', 'What school do you go to?:' , 'What year are you in?:']

answers = []
for field in fields:
	print field,
	v = prompt()
	answers += [v]

print '''Hello %s!
You go to %s
and you are in year %s''' % (answers[0], answers[1], answers[2])

print 'your code worked well, good job!'
