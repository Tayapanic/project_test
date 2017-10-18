from sympy import symbols
from sympy.plotting import plot
x = symbols('x')
func = raw_input("type in the function : ")
p1 = plot(func)
while (True):
	x = raw_input("Do you want another plot(y/n) : ")
	if x == 'y':
		func = raw_input("type in the function : ")
		p2 = plot(func)
		p1.extend(p2)
	else :
		break
p1

		

