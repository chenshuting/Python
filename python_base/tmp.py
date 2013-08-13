#!/usr/bin/python

class StudentA:
    def __init__(self):
        print 'init-b'
class Student:
    def __init__(self):
        print 'init-a'
class MiniStudent(Student,StudentA):
    def __init__(self):
        Student.__init__(self)
        StudentA.__init__(self)

s = MiniStudent();
