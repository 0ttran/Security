import hashlib
import base64
import sys
import string
from multiprocessing import process
import time
import itertools
from itertools import product
from string import ascii_lowercase
import multiprocessing

salt = "hfT7jp2q"
asd = "g1K8jdg4Ca.00E4vZp/e81"
passBase64 = "Y/iA7VyPo6sV6gI9asORk/"
syms = "abcdefghijklmnopqrstuvwxyz"
alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
isdone = 0

num_combinations = 0
    
def convert64(i, j):
    base64TableCrypt = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    val = ''
    while (j - 1 >= 0):
        j = j - 1
	val = val + base64TableCrypt[i & 0x3f]
	i = i >> 6
    return val

#Converts input string to md5 base 64 and compares it to the password hash, if it matches,
#return 1, else return 0
#Algorithm from https://pythonhosted.org/passlib/lib/passlib.hash.md5_crypt.html
def checkMatching(words):
    for inputString in words:
        #print inputString
        A = inputString + "$1$" + salt
        res = hashlib.md5(inputString + salt + inputString).digest()

        for pl in range(len(inputString),0,-16):
            if pl > 16:
                A = A + res[:16]
            else:
                A = A + res[:pl]

        #if current bit == 1, add first letter of password to A, else add null to A
        i = len(inputString)
        while i:
            if i & 1:
                A = A + chr(0)  
            else:
                A = A + inputString[0]
            i = i >> 1

        res = hashlib.md5(A).digest()
        #1000 rounds (iterations)
        for i in range(0, 1000):
            prev = ''
            if (i & 1):
                prev = prev + inputString
            else:
                prev = prev + res[:16]
            if (i % 3):
                prev = prev + salt
            if (i % 7):
                prev = prev + inputString
            if (i & 1):
                prev = prev + res[:16]
            else:
                prev = prev + inputString
                
            res = hashlib.md5(prev).digest()

        #place bits 16 bytes in following order: 12,6,0,13,7,1,14,8,2,15,9,3,5,10,4,11                             
        pass64 = ''
        pass64 = pass64 + convert64((int(ord(res[0])) << 16) | (int(ord(res[6])) << 8) | (int(ord(res[12]))),4)
        pass64 = pass64 + convert64((int(ord(res[1])) << 16) | (int(ord(res[7])) << 8) | (int(ord(res[13]))), 4)
        pass64 = pass64 + convert64((int(ord(res[2])) << 16) | (int(ord(res[8])) << 8) | (int(ord(res[14]))), 4)
        pass64 = pass64 + convert64((int(ord(res[3])) << 16) | (int(ord(res[9])) << 8) | (int(ord(res[15]))), 4)
        pass64 = pass64 + convert64((int(ord(res[4])) << 16) | (int(ord(res[10])) << 8) | (int(ord(res[5]))), 4)
        pass64 = pass64 + convert64((int(ord(res[11]))), 2)
        #print pass64
        global num_combinations
        num_combinations = num_combinations + 1
    
        if pass64 == passBase64:
            print "hash found: " + pass64
            print "password: " + inputString
            #print "num_combinations: " + str(num_combinations)
            global isdone
            isdone = 1
            exit(90)
            return
        elif isdone == 1:
            #print "num_combinations here: " + str(num_combinations)
            return
    #print "combinations: " + str(num_combinations)
    exit(91)
    
#checks 5 or less combination without multiprocessing
def check5less():
    
    qint = [''.join(i) for i in itertools.product(syms, repeat = 5)]
    checkMatching(qint)

    quad = [''.join(i) for i in itertools.product(syms, repeat = 4)]
    checkMatching(quad)

    triples = [''.join(i) for i in itertools.product(syms, repeat = 3)]
    checkMatching(triples)
    
    doubles = [''.join(i) for i in itertools.product(syms, repeat = 2)]
    checkMatching(doubles)
    
    ones = [''.join(i) for i in itertools.product(syms, repeat = 1)]
    checkMatching(ones)
    
if __name__ == '__main__':
    
    start_time = time.time()
    sixes = [''.join(i) for i in itertools.product(syms, repeat = 6)] #size 308915776
    #partition sixes to different sizes. 308915776 / 26 = 11881376. chose 26 processes
    tmp_val = 0
    new_sixes = []
    jobs = []

    for i in range(0,27):
        new_sixes = sixes[tmp_val:tmp_val + 11881376]
        tmp_val = tmp_val + 1 + 11881376
        
        p = multiprocessing.Process(target=checkMatching, args=(new_sixes,))
        jobs.append(p)
        p.start()
        #p.terminate()

    #infinite loop until all processes are done or a match is found
    chkLoop = 0
    procDone = False
    while not procDone:
        chkLoop = 0
        for p in jobs:
            if p.exitcode == 90:
                procDone = True
                break
            elif p.exitcode == 91:
                chkLoop = chkLoop + 1
                if chkLoop == 26:
                    procDone = True
    
    #kill all ongoing processes
    for p in jobs:
        if p.is_alive():
            p.terminate()
    
    #check 5 or less characters if could not find any 6 char leters
    if chkLoop > 0:
        check5less()
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
    







