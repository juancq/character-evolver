#! /usr/bin/env python

"""
Demo of genetic programming

This gp setup seeks to breed an organism which
implements func x^2 + y

Takes an average of about 40 generations
to breed a matching program
"""

import math
from random import random, uniform
from pygene.prog import ProgOrganism
from pygene.population import Population

from iga.gacommon import gaParams
# a tiny batch of functions
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

# define the class comprising the program organism
class MyProg(ProgOrganism):
    """
    """
    funcs = {
        '+': add,
        '-':sub,
        '*': mul,
        '/':div,
        #'**': pow,
        #'pow': pow,
        'sqrt': sqrt,
        'log' : log,
        'sin' : sin,
        'cos' : cos,
        'tan' : tan,
        }
    vars = ['p.x', 'p.y', 'p.z', 'factor' ,'time']#, 'time', 'time']
    consts = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]
    eqs = ['p.x', 'p.y', 'p.z', 'p.xyz']
    #eqs = ['p.xyz']

    user =  gaParams.getVar('user')
    collab =  gaParams.getVar('collaborate')

    if collab:
        t_id = int(user.split('_')[0][-1])
        print '%' * 10
        print t_id
        
        if t_id % 2:
            funcs.pop('sin', None)
            funcs.pop('cos', None)
            funcs.pop('tan', None)
        else:
            funcs.pop('*', None)
            funcs.pop('/', None)

        #if t_id % 2:
        #    if 'time' in self.vars:
        #        self.vars.remove('time')
        #else:
        #    if 'p.x' in self.vars:
        #        self.vars.remove('p.x')

        #    if 'p.y' in self.vars:
        #        self.vars.remove('p.y')

        #    if 'p.z' in self.vars:
        #        self.vars.remove('p.z')
    else:
        #if 'time' in self.vars:
        #    self.vars.remove('time')
        funcs.pop('*', None)
        funcs.pop('/', None)

    mutProb = 0.01

    
    def testFunc(self, **vars):
        """
        Just wanting to model x^2 + y
        """
        return 1.0
        #return vars['x'] ** 2 + vars['y']*vars['y']*8

    def fitness(self):
        # choose 10 random values
        return 10
        
    # maximum tree depth when generating randomly
    initDepth = 6
