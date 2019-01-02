"""
File:	rsa_main.py
Author:	Chloe Jackson
Description:	RSA helpers for students
"""

#import
import fileinput
import time			# and then there was another dimension
from eea import * 
from sq_mul import *
from math import *
#/import


# Greet and meet

'''
	Print a welcome message and instructions
'''
def welcome():
	print "****    CRYPTO HELPER: RSA    ****"
	print "If you are decrypting a ciphertext enter 1."
	print "If you are computing a key value k enter 2."
	print "If you are factoring an integer n  enter 3."

'''
	Parse the user's desired option
'''	
def parse_input():
	line = input()	
	if line == 1:
		decrypt_option()
		return
	elif line == 2:
		dlp_option()
		return
	elif line == 3:
		ifp_option()
		return
	else:
		print 'Invalid answer.  Try again.'
	return



# Decrypt RSA ciphertext


'''
	Decrypt a number
'''
def decrypt_option():
	p = input("Please input prime modulus p: ")
	q = input("Please enter second modulus q: ")
	n = p * q
	phi_n = (p-1)*(q-1)
	e_or_d = input("Enter 1 if d is known.  Enter 2 if d is unknown: ")
	d = 0
	
	if e_or_d == 1:
		d = input("Enter value for d: ")
	else:
		e = input("Enter value for e: ")
		d = inverse(e,phi_n)
	print "Please enter the ciphertext followed by END."
	print "ex: 45 32 67\nEND\n" 
	ciphertext = list()
	for line in fileinput.input():
		if line == "END\n":
			break
		l = line.split()
		for i in range(0,len(l)):
			l[i] = int(l[i])
		ciphertext = ciphertext + l
	for i in range(0,len(ciphertext)):
		ciphertext[i] = square_multiply(ciphertext[i],d,n)
	print "\nDecrypted to plaintext: " , ciphertext,"\n"

# Shanks' algorithm for discrete logs

'''
	Shank's algorithm for the discrete log problem
'''
def shanks(p, base, k):
	m = int(ceil(sqrt(p-1)))
	L = {}
	tmp = base	# alpha 
	r = tmp
	L[1] = 0
	for j in range(1,m):
		L[tmp] = j
		tmp = tmp * r		# alpha ^ j mod p
		tmp %= p
	tmp = inverse(base,p)
	tmp = square_multiply(tmp,m,p) # alpha ^ -m mod p
	y = k
	for i in range(0,m):	
		if y in L:
			return (i * m + L[y])
		y = y * tmp
		y %= p
	return -1


# Pollard's Rho algorithm for discrete logs

'''
	Helper function for the Pollard-Rho algorithm
'''
def	partition(xab, N, alpha, beta):
	n = N - 1
	j = xab[0] % 3
	if j == 0:
		xab[0] = xab[0] * xab[0]; xab[0] %= N
		xab[1] = xab[1] * 2; xab[1] %= n
		xab[2] = xab[2] * 2; xab[2] %= n
	elif j == 1:
		xab[0] = xab[0] * alpha; xab[0] %= N
		xab[1] = xab[1] + 1; xab[1] %= n
	else:
		xab[0] = xab[0] * beta; xab[0] %= N
		xab[2] = xab[2] + 1; xab[2] %= n
	return xab

'''
	Helper function for the Pollard-Rho algorithm
'''
def check_ans(a,b,X,A,B,n):
	r = a - A; r %= n
	s = B - b; s %= n
	r = r / s
	return r


'''
	Pollard-Rho algorithm
'''
def pollard_rho_log(alpha,beta,n):
	N = n + 1
	x = 1; X = x
	a = 0; A = a
	b = 0; B = b
	for i in range (1,n):
		xab = partition([x,a,b],N,alpha,beta)
		x = xab[0]; a = xab[1]; b = xab[2]
		XAB = partition([X,A,B],N,alpha,beta)
		XAB = partition(XAB,N,alpha,beta)
		X = XAB[0]; A = XAB[1]; B = XAB[2]
		if x == X:
			print "i: ",i," x: ",x," a: ",a," b: ",b," X: ",X," A: ",A," B: ",B,"\n"
			print "Exponent ",check_ans(a,b,X,A,B,n)
			break
	return


# Pollard's Rho algorithm for factoring integers

'''
	Function F for the Pollard-Rho factoring algorithm
'''
def fp(x,p):
    x = x * x + 1
    x %= p
    return x

'''
	Pollard-Rho factoring algorithm
'''
def pollard_rho(n,x1):
	x = x1
	xp = fp(x,n)
	p = gcd(x - xp, n)
	while p == 1:
		x = fp(x,n)
		xp = fp(fp(xp,n),n)
		p = gcd(abs(x - xp),n)
	if p == n:
		return -1
	return p

'''
	Pollard-Rho algorithm with Brent's accumulator for faster Monte-Carlo-esque solving
'''
def pollard_brent(n,x1,k):
	x = x1
	xp = fp(x,n)
	p = gcd(x - xp, n)
	r = k
	z = 1
	while p == 1:
		x = fp(x,n)
		xp = fp(fp(xp,n),n)
		k += 1
		z *= abs(x - xp)
		z %= n
		if k > r:
			k = 0
			p = gcd(z,n)
	if p == n:
		return -1
	return p

# Compute a key value (exponent)

'''
	User option to solve a discrete log
'''
def dlp_option():
	p = input("Please input prime modulus p: ")
	q = input("Please enter second modulus q: ")
	n = p * q
	base = input("Please input base: ")
	k = input("Please input k value: ")
	c = raw_input("Do you wish to continue with Pollard-Rho algorithm (Y/n)?: ")
	if	c == "Y":
		start = time.clock()
		pollard_rho_log(base,k,n)
		stop = time.clock()
		print "Discrete log computation took ", stop, " seconds"
	c = raw_input("Do you wish to continue with Shanks algorithm (Y/n)?: ")
	if c == "Y":
		print "WARNING: Shank's algorithm may use too much memory and crash."
		c = raw_input("Do you still wish to continue? (Y/n): ")
		if c == "Y":
			start = time.clock()
			print shanks(n, base, k)
			stop = time.clock() - start
			print "Discrete log computation took ", stop, " seconds"
		else:
			print "Thanks for using this program.  Wishing you all the best"
			print "on your assignments! - CJ"
	else:
		print "Thanks for using this program.  Wishing you all the best"
		print "on your assignments! - CJ"


'''
	User option for factoring an integer
'''
def ifp_option():
	n = input("Please input modulus n: ")
	c = raw_input("Do you wish to use Pollard's algorithm with accumulator (Y/n)?: ")
	if c == "Y":
		k = input("Please input number of iterations for accumulator: ")
		start = time.clock()
		p = pollard_brent(n,2,k)
		stop = time.clock() - start
		if p != -1:
			print "Factor found: ", p, " in ", stop, " seconds"
		else:
			print "No factor detected.  Exiting"
		return
	else:
		start = time.clock()
        p = pollard_rho(n,2)
        stop = time.clock() - start
        if p != -1:
            print "Factor found: ", p, " in ", stop, " seconds"
        else:
            print "No factor detected.  Exiting"
        return

if __name__ == "__main__":
	welcome()
	parse_input()
