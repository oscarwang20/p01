import random
from requestMaker import *

def makeList(title):
    l = getLinks(title)
    return l

#returns a list of random items popped from a source list
def popList(num, source):
    l2 = []
    if (num > len(source)):
        num = len(source)
    for i in range(num):
        l2.append(source.pop(random.randint(0, len(source)-1)))
    return l2

def main():
    title = input("Enter a title: ")
    l = makeList(title)
    while l != []:
        print("remaining:")
        print(l)
        print("pooped:")
        print(popList(10, l))

if __name__ == '__main__':
    main()