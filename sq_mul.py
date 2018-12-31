"""
File: sq_mul.py
Author:	Chloe Jackson
Description:	contains the square and multiply algorithm for integers
				raised to some exponent in an integer ring
"""



"""
function	square_multiply(a,e,n)
@param	a	the base integer
@param	e	the exponent
@param	n	the modulus
@return	r	the result
"""
def square_multiply(a,e,n):
	r = a
	binary = []
	b = "{0:b}".format(e)
	b = b[::-1]
	for bit in b:
		binary.append(bit)
	i = 1
	while i < len(binary):
		r = r * r
		r %= n
		if binary[i] == '1':
			r = r * a
			r %= n
		i += 1
	return r
