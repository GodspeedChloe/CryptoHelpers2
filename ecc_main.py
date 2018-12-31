"""
File:	ecc_main.py
Author:	Chloe Jackson
Description:	Suite of elliptic curve cryptographic applications for students 
				to use and learn from
"""

import sys
import	fileinput
import	time					# and then there was another dimension
from math import *
from eea import *
from random import *

# import for graphing
import numpy as np
import matplotlib.pyplot as plt


'''
	print a welcome message
'''
def welcome():
        print "****    CRYPTO HELPER: ECC    ****"


'''
	prompt the user which elliptic curve operation they want to do
'''
def parse_input():
	print "Default curve is of the form: y^2 = x^3 + ax + b  (mod p)"
	a = input("Enter value for coefficient a: ")
	b = input("Enter value for constant b: ")
	p = input("Enter prime modulus p: ")
	
	print "If you are computing a point along the curve enter 1.\n"
	print "If you are adding two points together enter 2.\n"
	print "If you are finding the order of a point on the curve, enter 3.\n"
	print "If you are finding the order of entire curve, enter 4.\n"
	
	choice = input()
	
	if choice == 1:
		multiply_point(a,b,p)
	elif choice == 2:
		choice_add_points(a,p)
	elif choice == 3:
		point_order()
	elif choice == 4:
		choice_curve_order(a,b,p)
	return 


'''
	turn an integer into its binary decomposition

	@param	k	some integer

	@return		binary decomposition
'''
def	int_to_bin(k):
	L = [int (x) for x in bin(k)[2:]]
	return L


'''
	turn an integer into its NAF decomposition

	@param	k	some integer
	@param	L	list for storing NAF decomposition

	@return		NAF decomposition
'''
def convert_NAF(k,L):
	L = L + [0]
	i = 0
	while k > 0:
		if k % 2 != 0:
			e = k % 4; L[i] = 2 - e; k -= L[i]
		else:
			L[i] = 0
		k = k//2
		i += 1
	return L


'''
	computes the lambda value for point doubling
'''
def get_2P_s(P,a,p):
	s = inverse(2 * P[1],p) * ((3 * P[0] * P[0]) + a); s %= p
	return s

'''
	computes the lambda value for point addition
'''
def get_s(P,Q,p):
	s = inverse(Q[0] - P[0],p) * (Q[1] - P[1]); s %= p
	return s

'''
	computes the new x value from point addition
'''
def get_x3(P,Q,s,p):
	x3 = (s*s) - (P[0] + Q[0]); x3 %= p	
	return x3


'''
	computes the new y value from point addition
'''	
def get_y3(P,s,x3,p):
	y3 = (s * (P[0] - x3)) - P[1]
	y3 %= p
	return y3

'''
	add two given points together
'''
def add_points(P,Q,p):
	s = get_s(P,Q,p)
	x = get_x3(P,Q,s,p)
	y = get_y3(P,s,x,p)
	return [x,y]


'''
	find a random point on a curve to give the user
'''
def get_random_point(a,b,p):
	x3 = 0; k = 1; x = -1; y = -1
	while x3 != k:	
		y = randint(1,p); k = y * y; k %= p
		x = randint(1,p); x3 = x * x * x; x3 %= p
		x3 += a * x; x3 %= p
		x3 += b; x3 %= p
	return [x,y]

'''
	compute the trivial inverse of a point
'''
def point_inverse(P,p):
	return [P[0],p - P[1]]

'''
	double a given point
'''
def double_a_point(P,a,p):
	s = get_2P_s(P,a,p)
	x = get_x3(P,P,s,p)
	y = get_y3(P,s,x,p)
	return [x,y]

'''
	multiply a point using the binary decomposition

	@param	k	the point factor
	@param	P	some point tuple
	@param	a	curve coefficient a
	@param	p	modulus

	@return		point tuple result
'''
def double_and_add(k,P,a,p):
	R = None
	Q = P
	k.reverse()
	for i in k:
		if i == 1:
			if R == None:
				R = Q
			else:
				R = add_points(R,Q,p)
		Q = double_a_point(Q,a,p)
	return R
		

'''
	multiply a point using the NAF decomposition

	@param	k	the point factor
	@param	P	some point tuple
	@param	a	curve coefficient a
	@param	p	modulus

	@return point tuple result
'''
def double_and_add_or_subtract(k,P,a,p):
	R = None
	Q = P
	for i in k:
		if i == -1:
			if R == None:
				R = point_inverse(Q,p)
			else:
				R = add_points(R,point_inverse(Q),p)
		elif i == 1:
			if R == None:
				R = Q
			else:
				R = add_points(R,Q,p)
		Q = double_a_point(Q,a,p)
	return R


'''
	verifies that a given point actually lies on the curve
'''
def check_point(x,y,a,b,p):
	lhs = y * y; lhs %= p
	rhs = (x * x * x) + (a * x) + b; rhs %= p
	if lhs != rhs:
		print "ERROR: point must be on the curve\n"
		print "Run with option 4 to see what points are valid"
		sys.exit()


'''
	option to multiply a point on the curve

	@param	a	curve coefficient a
	@param	b	curve coefficient b
	@param	p	modulus
'''
def multiply_point(a,b,p):
	print "random point on curve: ", get_random_point(a,b,p)
	P = [0,0]; P[0] = input("Enter point x value: "); P[1] = input("Enter point y value: ")
	k = input("Enter point coefficient k (as in kP): ")
	check_point(P[0],P[1],a,b,p)
	choice = raw_input("Do you wish to also use the NAF form as well (Y/n)? ")
	
	k1 = int_to_bin(k); k2 = k1
	k2 = convert_NAF(k,k2)
	start = time.clock()	# begin DOUBLE_AND_ADD algorithm
	R = double_and_add(k1,P,a,p)
	stop = time.clock() - start
	print "point ", k, "P: (",R[0],",",R[1],") computed in ",stop," seconds with double and add algorithm"

	if choice == 'Y':
		start = time.clock()
		R = double_and_add_or_subtract(k2,P,a,p)
		stop = time.clock() - start
		print "point ", k, "P: (",R[0],",",R[1],") computed in ",stop," seceonds with double and add or subtract algorithm"


'''
	option to add two points on the curve

	@param	a	curve coefficient a
	@param	p	modulus
'''
def choice_add_points(a,p):
	P = [0,0]; P[0] = input("Enter first point x value: "); P[1] = input("Now enter y value: ")
	Q = [0,0]; Q[0] = input("Enter second point x value: "); Q[1] = input("Now enter y value: ")
	if P[0] == Q[0] and P[1] == Q[1]:
		Q = double_point(P,a,p)
		print "Doubling the point yields point (",Q[0],",",Q[1],")"
		return
	Q = add_point(P,Q,p)
	print "Point addition yields point (",Q[0],",",Q[1],")"
	return



'''
	determines if a value is a quadratic residue

	@param	z	potential residue
	@param	p	modulus
'''
def is_quadratic_residue(z,p):
	for i in range(0,p):
		j = i * i; j %= p
		if j == z:
			return i
	return 0.5


'''
	computes precise order of a curve

	@param	a	coefficient a
	@param	b	coefficient b
	@param	p	modulus
'''
def choice_curve_order(a,b,p):
	xvals = []
	yvals = []
	t = int(2 * round(sqrt(p)))
	lower = (p + 1) - t
	upper = (p + 1) + t
	print 'Hasse bound: ',lower,' <= #E <= ',upper 
	order = 0 
	for x in range(0,p):
		z = x * x * x; z %= p
		z = z + (a * x); z %= p
		z += b; z %= p
		y = is_quadratic_residue(z,p)
		if y != 0.5:
			xvals.append(x)
			xvals.append(x)
			yvals.append(y)
			yvals.append(p-y)
			order += 2

	# point of infinity
	order += 1
	print 'Order of curve   y^2 = x^3 +',a,"x +",b, 'is ',order	
	
	# graph the points
	plt.figure(1)
	plt.plot(xvals,yvals,'bo')
	plt.title('Points on curve E')
	plt.show()
	


# send it
if __name__ == "__main__":
	welcome()
	parse_input()

