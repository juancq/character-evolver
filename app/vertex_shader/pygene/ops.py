import math

def add(x,y):
    #print "add: x=%s y=%s" % (repr(x), repr(y))
    try:
        return x+y
    except:
        #raise
        return x

def sub(x,y):
    #print "sub: x=%s y=%s" % (repr(x), repr(y))
    try:
        return x-y
    except:
        #raise
        return x

def mul(x,y):
    #print "mul: x=%s y=%s" % (repr(x), repr(y))
    try:
        return x*y
    except:
        #raise
        return x

def div(x,y):
    #print "div: x=%s y=%s" % (repr(x), repr(y))
    try:
        return x / y
    except:
        #raise
        return x

def sqrt(x):
    #print "sqrt: x=%s" % repr(x)
    try:
        return math.sqrt(x)
    except:
        #raise
        return x

def pow(x,y):
    #print "pow: x=%s y=%s" % (repr(x), repr(y))
    try:
        return x ** y
    except:
        #raise
        return x

def log(x):
    #print "log: x=%s" % repr(x)
    try:
        return math.log(float(x))
    except:
        #raise
        return x

def sin(x):
    #print "sin: x=%s" % repr(x)
    try:
        return math.sin(float(x))
    except:
        #raise
        return x
    
def cos(x):
    #print "cos: x=%s" % repr(x)
    try:
        return math.cos(float(x))
    except:
        #raise
        return x
        
def tan(x):
    #print "tan: x=%s" % repr(x)
    try:
        return math.tan(float(x))
    except:
        #raise
        return x
