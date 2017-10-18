from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas
from numpy import *
import operator
import matplotlib.pyplot as plt

exprStack = []

def pushFirst( strg, loc, toks ):
    exprStack.append( toks[0] )
def pushUMinus( strg, loc, toks ):
    if toks and toks[0]=='-': 
        exprStack.append( 'unary -' )
        #~ exprStack.append( '-1' )
        #~ exprStack.append( '*' )

bnf = None
def BNF():
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | T | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    global bnf
    if not bnf:
        point = Literal( "." )
        e     = CaselessLiteral( "E" )
        fnumber = Combine( Word( "+-"+nums, nums ) + 
                           Optional( point + Optional( Word( nums ) ) ) +
                           Optional( e + Word( "+-"+nums, nums ) ) )
        ident = Word(alphas, alphas+nums+"_$")

        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )
        pi    = CaselessLiteral( "PI" )
        x     = CaselessLiteral( "X" )

        expr = Forward()
        atom = (Optional("-") + ( pi | e | x | fnumber | ident + lpar + expr + rpar ).setParseAction( pushFirst ) | ( lpar + expr.suppress() + rpar )).setParseAction(pushUMinus) 

        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-righ
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( pushFirst ) )

        term = factor + ZeroOrMore( ( multop + factor ).setParseAction( pushFirst ) )
        expr << term + ZeroOrMore( ( addop + term ).setParseAction( pushFirst ) )
        bnf = expr
    return bnf

# map operator symbols to corresponding arithmetic operations
epsilon = 1e-12
opn = { "+" : operator.add,
        "-" : operator.sub,
        "*" : operator.mul,
        "/" : operator.truediv,
        "^" : operator.pow }
fn  = { "sin" : sin,
        "cos" : cos,
        "tan" : tan,
        "abs" : abs,
        "trunc" : lambda a: int(a),
        "round" : round,
        "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}

def evaluateStack( s ,x1,y):
    if x1 is None:
        x1 = 0
    op = s.pop()
    if op == 'unary -':
        return -evaluateStack( s,x1,y )
    if op in "+-*/^":
        op2 = evaluateStack( s,x1,y )
        op1 = evaluateStack( s,x1,y )
        return opn[op]( op1, op2 )
    elif op == "PI":
        return math.pi # 3.1415926535
    elif op == "E":
        return math.e  # 2.718281828
    elif op == "X":
        return linspace(x1, y, 300)
    elif op in fn:
        return fn[op]( evaluateStack( s,x1,y ) )
    elif op[0].isalpha():
        return 0
    else:
        return float( op )

def compute(s,x1,y):
    if x1 is None:
        x1 = 0   
    global exprStack
    exprStack = []
    results = BNF().parseString( s )
    val = evaluateStack( exprStack[:] ,x1,y)
    return val

yun=raw_input("Please input function to be plotted on y-axis in terms of parameter : ")
xun=raw_input("Please input function to be plotted on x-axis in terms of parameter : ")
x1=input("Set lower limit of x-axis")
x2=input("Set upper limit of x-axis")
fx=compute(xun,x1,x2)

y1=input("Set lower limit of y-axis")
y2=input("Set upper limit of y-axis")
fy=compute(yun,y1,y2)

fls = plt.figure()
a = fls.add_subplot(111)
a.plot(fx, fy)
a.set_title("Title")
a.set_xlabel("xlabel")
a.set_ylabel("ylabel")

plt.show()




