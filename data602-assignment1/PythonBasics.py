#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 17:17:36 2017

@author: cspit
"""

# Hello World
'''
this is me 
documenting
my code
'''

# Variables & Datatypes
a = 7 #this is an integer
b = 10
print(a + b)
print(b)
x = 'hello world' #thsi is a string
print(x)
i = False #boolean
o = True #another boolean

print(type(i)
)



# Loops
for n in range(0,len(equities)):
    print(equities[n])
    print(n)

# Functions
def my_first_function(num):
    for n in range(num):
        print("hello!")
        print("see ya!")
    
my_first_function(5)

def multiplier(a,b,c,d,e):
    x = a*b*c*d*e
    return x

z = multiplier(5,2,1,3,2)
print(z)

# Conditions
hungry = 1
thirsty = 2
if hungry==1 and thirsty==1:
    print("yes hungry is 1")
else:
    print("no it failed")

hot = True
temp = 70
while hot==True:
    print("it's hot!")
    if temp < 75:
        hot = False


# Input
input()

# Putting it together

equities = ['AAPL', 'AMZN', 'MSFT', 'INTC', 'SNAP']