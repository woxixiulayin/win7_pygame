__author__ = 'liuzhigang'

class Student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score
    def ls(self):
        print self.__name, self.__score
a = Student('liu', 100)
a.ls()
a.s = 1

