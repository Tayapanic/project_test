from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas
from numpy import *
import operator
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sys
from matplotlib.widgets import Slider, Button, RadioButtons

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def destroy(e):
    sys.exit()

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
        "sqrt": sqrt,
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
        return linspace(x1, y, 200)
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

fun=raw_input("Please input a function to be evaluated: ")
x1=input("Set x")
y=input("Set y")
g=compute(fun,x1,y)

#labels
xlabel=raw_input("Please input x-label: ")
ylabel=raw_input("Please input y-label: ")
#title
Title=raw_input("Please input title of graph: ")
#linestyle

f = []
z=x1
for i in range(200):
       z=x1+(i*float(y-x1)/200)
       f.append(z)

root = Tk.Tk()
root.wm_title("Hamara bajaj")
fls = Figure(figsize=(5, 4), dpi=100)
a = fls.add_subplot(111)
a.plot(f, g)
a.set_title(Title)
a.set_xlabel(xlabel)
a.set_ylabel(ylabel)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(fls, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.BOTTOM)
axcolor = 'lightgoldenrodyellow'
rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


def colorfunc(label):
    l.set_color(label)
    fls.canvas.draw_idle()
radio.on_clicked(colorfunc)
plt.show()

Tk.mainloop()