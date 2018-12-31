"""
File:	eea.py
Author:	Chloe Jackson
Description:	Simple Extended Euclid's Algorithm for computing
				the inverse of a number modulo some integer n
"""


"""
function	gcd(a,b)
@param	a	first integer
@param	b	second integer
@return a	the greatest common divisor of a and b
"""
def gcd(a,b):
	remainder = 0
	while b != 0:
		remainder = a % b
		a = b
		b = remainder
	return a

"""
function	inverse(a,n)
@param	a	the number to invert
@param	n	the modulus
@return	-1	if no inverse exists
		t	the inverse of a mod n
"""
def inverse(a,n):
	t = 0
	r = n
	new_t = 1
	new_r = a
	while (new_r != 0):
		quotient = r / new_r
		save_t = t
		t = new_t
		new_t = save_t - (quotient * new_t)
		save_r = r
		r = new_r
		new_r = save_r - (quotient * new_r)
	if r > 1:
		return -1 # not invertible
	if t < 0:
		t = t + n
	return t
