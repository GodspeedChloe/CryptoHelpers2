'''
	File: galois_main.py
	Description:	Functions for doing Galois Field crypto/number theory
	Author:	Chloe Jackson
	Version: 11-Jan-2019
'''

#imports


#/imports


'''
	Print a welcome message
'''
def welcome():
	print "****    CRYPTO HELPER: GALOIS FIELD    ****"



'''
	Recursively increase a polynomial

	@param	t		polynomial to increase
	@param	k		current term
	@param	base	modulus of coefficients
'''
def inc_poly(t,k,base):
	t[k] = t[k] + 1
	if t[k] == base:
		t[k] = 0
		return inc_poly(t,k+1,base)
	return t


'''
	Multiply two polynomials together

	@param	t1		polynomial 1
	@param	t2		polynomial 2
	@param	base	base for coefficients
'''
def multiply(t1,t2,base):

	n = len(t2)
	m = len(t1)
	r = [0] * (2*max(n,m))
	for i in range(0,m):
		c1 = t1[i]
		for j in range(0,n):
			c2 = t2[j]
			q = c1 * c2
			q %= base
			r[i + j] = r[i+j] + q
			r[i + j] %= base
	return r



'''
	Divide two polynomials and return quotient, remainder

	@param	t1		numerator
	@param	t2		denominator
	@param	base	base for coefficients
'''
def divide(t1,t2,base):
	quotient = []
	while True:
		n = get_degree(t1)
		m = get_degree(t2)
	
		local_quotient = [0] * (n + 2)
		local_quotient[n-m] = 1
		quotient = add(quotient,local_quotient,base)
		remainder = multiply(local_quotient,t2,base)
		remainder = trim(remainder)
		remainder = subtract(t1,remainder,base)
		if get_degree(remainder) < get_degree(t2):
			break
		t1 = remainder
	return trim(quotient), remainder
	
	
'''
	Get the degree of a polynomials

	@param	t		polynomial
'''
def get_degree(t):
	k = len(t) - 1
	while k >= 0:
		if t[k] != 0:
			return k
		k -= 1
	return -1


'''
	Divide two polynomials and get inverse
	
	@param	px		modulus
	@param	fx		polynomial in ring
	@param	base	base for coefficients
'''
def inverse(px,fx,base):

	qs = []
	r1 = px
	r2 = fx
	remainder = [1]
	while True:
		quotient, remainder = divide(trim(r1),trim(r2),base)
		qs += [quotient]
		r1 = r2
		r2 = remainder
		if trim(remainder) == []:
			break
	t1 = [0]
	t2 = [1]
	t = []
	# using t = t1 - (q * t2)
	for i in range(0,len(qs)-1):
		temp = multiply_mod(qs[i],t2,base,px)
		t = subtract(t1,temp,base)
		t1 = t2
		t2 = t
	return t2
	
'''
	Add two polynomials together

	@param	t1		polynomial 1
	@param	t2		polynomial 2
	@param	base	base for coefficients
'''
def add(t1,t2,base):
	if len(t1) < len(t2):
		r = t2
		t2 = t1
		t1 = r

	r = [0] * len(t1)

	i = 0
	while i < len(t2):
		c = t2[i] + t1[i]
		c = c % base
		r[i] = c
		i += 1	

	while i < len(t1):
		r[i] = t1[i]
		i += 1

	return r


'''
	Trim trailing zeroes

	@param	t		polynomial
'''
def trim(t):
	k = len(t) - 1
	while k >= 0:
		if t[k] != 0:
			break
		k -= 1

	return t[:k+1]


'''
	Subtract two polynomials together

	@param	t1		polynomial 1
	@param	t2		polynomial 2
	@param	base	base for coefficients
'''
def subtract(t1,t2,base):


	r = []
	i = 0
	while i < min(len(t2),len(t1)):
		c = t1[i] + (base - t2[i])
		c = c % base
		r += [c]
		i += 1

	if len(t2) != len(t1):
		if len(t2) > len(t1):
			r += t2[i:]
		else:
			r += t1[i:]
	return r

	
'''
	Check if a polynomial has been reduced completely

	@param	t		polynomial
	@param	n		degree of modulus
'''
def is_reduced(t,n):
	x = len(t) - 1
	while x >= 0:
		if t[x] != 0:
			if x >= n:
				return x
		x -= 1
	return -1


'''
	Multiply two polynomials together mod p(x)

	@param	t1		polynomial 1
	@param	t2		polynomial 2
	@param	base	base for coefficients
	@param	mod		modulus polynomial p(x)
'''
def multiply_mod(t1,t2,base,mod):

	# r : result
	r = multiply(t1,t2,base)
	n = len(mod) - 1	
	xn = mod[:len(mod)-1]	

	# reduce terms in r inefficiently
	k = is_reduced(r,n)
	while k != -1:
		temp = [0] * len(r)
		temp[k-n] = r[k]
		temp = multiply(temp,xn,base)
		r = add(temp,r[:k],base)
		k = is_reduced(r,n)

	return trim(r)


'''
	Generate field's elements

	@param	exp		field exponent
	@param	base	field base
'''
def GF(base,exp):
	Field = []
	N = pow(base,exp)
	t = [0] * exp
	for i in range(0,N):
		r = []
		for k in t:
			r.append(k)
		Field.append(r)
		if i == N-1:
			break
		t = inc_poly(t,0,base)

	return Field

'''
	Generate the multiplication table for a field

	@param	base	the base of the field
	@param	exp		the exponent of the field
	@param	mod		the modulus polynomial
	@param	N		base^exp
'''
def multiplication_table(base,exp,mod,N):
	
	# generate the field's elements
	Field = GF(base,exp)
	table = []
	for t1 in Field:
		for t2 in Field:
			# multiply together
			table.append(multiply_mod(t1,t2,base,mod))
	return table


'''
	Generate the addition table for a field
	
	@param	base	the base of the field
	@param	exp		the exponent of the field
	@param	N		base ^ exp
'''
def addition_table(base,exp,N):
	
	# generate the field's elements
	Field = GF(base,exp)
	table = []
	for t1 in Field:
		for t2 in Field:
			# add together 
			table += [add(t1,t2,base)]
	return table


'''
	Display a table neatly

	@param	table	2D array of polynomials
	@param	exp		field exponent
	@param	N		(base^exp)
'''
def display_table(table,exp,N,opt):
	for i in range(0,N):
		line = ''
		for j in range(0,N):
			v = table[i*N+j]
			v = v[:exp]
			if opt == 'Y':
				line = line + '  ' + display_poly(v)
				continue
			v.reverse()
			r = ''
			for c in v:
				r = r + str(c)
			line = line + '  ' + r
		print line


'''
	Display a polynomial given its coefficients
	
	@param	poly	a list of coefficients
'''
def display_poly(poly):
	n = len(poly) - 1
	k = n
	string = ''
	for i in range(0,n):
		if poly[i] > 1:
			string += str(poly[i])
			k -= 1
		elif poly[i] == 0:
			k -= 1
			continue
		if k == 0:
			string += 'x+'
			k -= 1
			continue
		string += 'x^' + str(k) + '+'
		k -= 1

	if poly[n] != 0 or len(string) == 0:
		return string + str(poly[n])
	return string[:len(string) - 3]
	

'''
	Compute the values in a field and print them
'''
def main():
	welcome()
	f_base = input("\nEnter the field base i.e. GF(base^exponent): ")
	f_exp = input("Enter the field exponent now: ")
	degree = input("Enter the degree of the modulus polynomial: ")

	print "Enter the polynomial coefficients including quotation marks."
	print "Ex.  2x^6 + x^2 + 2  is \"2 0 0 0 1 0 2\""
	poly = input("\npoly: ").split(" ")
	poly = map(int, poly)
	print "Your modulus: ", display_poly(poly)
	poly.reverse()

	if len(poly) != (degree + 1):
		print "Degree does not match polynomial given"
		quit()

	N = pow(f_base,f_exp)
	
	c = raw_input("\nDo you wish to display the addition and multiplication tables (Y/n)?: ")

	# generate tables
	m_table = multiplication_table(f_base,f_exp,poly,N)
	a_table = addition_table(f_base,f_exp,N)
	if c == "Y":
		opt = raw_input("Would you like pretty print (Y/n)? ")	
		print '\nAddition table for GF(',N,')'
		display_table(a_table,f_exp,N,opt)

		print '\nMultiplication table for GF(',N,')'
		display_table(m_table,f_exp,N,opt)

	# get option
	print "For finding a polynomial's inverse, enter 1."
	opt = input()


	if opt == 1:
		t = input("\npolynomial to find inverse for: ").split(" ")
		t = map(int,t)
		t.reverse()
		inv = [0]
		if trim(t) == []:
			print "0 has no multiplicative inverse ever."
			return
		inv = inverse(poly,t,f_base)
		inv.reverse()
		print "Your inverse: ", display_poly(inv)	

main()
