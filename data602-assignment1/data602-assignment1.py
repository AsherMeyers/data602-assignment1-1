#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 17:25:16 2017

@author: cspit

The following code is my program to allow trading and calculate the P/L associated with it.

The code uses internal python functions but does make use of BeautifulSoup, urllib, datetime and pandas.

No global variables are used except for equities, all others are local.
"""

#  The following code imports packages and sets the ledger to an empty list and provides an
#  equities list.


import datetime
from bs4 import BeautifulSoup
import urllib
import pandas as ps
import numpy as np
equities = ['SNAP', 'AAPL', 'AMZN', 'MSFT', 'INTC']
ledger = []

# The following section defines the main screen
# This part of the code, calls the main functions to Trade, Blotter, P/L and Exit.


def mainscreen():
    print('1. Trade')
    print('2. Show Blotter')
    print('3. Show P/L')
    print('4. Quit')
    print('Please select an option \n')
    selection = int(input('Enter choice: '))
    if selection==1:
        x = trade(ledger)
    elif selection==2:
        show_blotter(ledger)
    elif selection==3:
        show_pl(ledger)
    elif selection==4:
        print('Thanks for using me!\n')
    else:
        print('Invalid choice. Please enter 1-4\n')
        mainscreen()
    ledger.append(x)
    mainscreen()

# The following set of code defines the trading function
def trade(table):
    '''
    This function doesn't take in any variables to start trading.
    Depending on the choice a user makes, it will then call other functions to perform calcs.
    '''
    print('What would you like to do?')
    print('1. Sell')
    print('2. Buy')
    u = table
    option = int(input('Please select: '))
    if option == 1:
        print('Which one do you wish to sell?')
        print('1. SNAP')
        print('2. AAPL')
        print('3. AMZN')
        print('4. MSFT')
        print('5. INTC')
        value = int(input('Please select: '))
        shares = int(input('How many shares? '))
        eq = value-1
        z = stockcashavail(u,value)
        if z[1] > 0:
            entry = sell(value,shares,eq)
        else:
            print('Not enough stock available to sell: ')
            trade(table)
    if option == 2:
        print('Which one do you wish to buy? ')
        print('1. SNAP')
        print('2. AAPL')
        print('3. AMZN')
        print('4. MSFT')
        print('5. INTC')
        value = int(input('Please select? '))
        shares = int(input('How many shares? '))
        eq = value-1
        z = stockcashavail(u,value)
        if z[0] > 0:
            entry = buy(value,shares,eq)
        else:
            print('Not enough money available to buy: ')
            trade(table)
    return entry

# Check to see if we have stock to sell or cash
def stockcashavail(table,eq):
    '''
    This function checks to see if stocks are available to sell or enough cash to buy
    Table comes from ledger and eq is the stock being checked
    
    '''
    cash = 1000000
    
    #import ledger as dataframe and calculate if cash available to buy
    x = ps.DataFrame(table)
    x.columns = ['Side','Ticker','Qty','Price','Date','Cost']
    newcash = cash + sum(x.Cost)
    
    #check to see if stock is available to sell
    l = x[(x.Side == 'sell') & (x.Ticker == equities[eq])]
    stocks = sum(l.Qty)
    
    return newcash, stocks

def sell(value, shares, eq):
    #call link and read page for current price
    '''
    a which is value is used to call the URL from linkcall list
    b which is the number of shares is used in the math
    c which is the ticker is used to record the symbol
    '''
    linkcall = ['https://finance.yahoo.com/quote/SNAP?p=SNAP', 'https://finance.yahoo.com/quote/AAPL?p=AAPL', 
                'https://finance.yahoo.com/quote/AMZN?p=AMZN', 'https://finance.yahoo.com/quote/MSFT?p=MSFT',
                'https://finance.yahoo.com/quote/INTC?p=INTC']
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #this lets me capture the time
    page = urllib.request.urlopen(linkcall[value-1]).read()
    soup=BeautifulSoup(page, "lxml")
    instantprice = float(soup.find('span', {'class' :'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)
    symb = equities[eq]
    
    # do math
    cost = instantprice * shares
    
    newentry = ['sell', symb, shares, instantprice, time, cost] #list to store items related to trade
    return newentry

    
def buy(value, shares, eq):
    #call link and read page for current price
    '''
    a which is value is used to call the URL from linkcall list
    b which is the number of shares is used in the math
    c which is the ticker is used to record the symbol
    '''
    linkcall = ['https://finance.yahoo.com/quote/SNAP?p=SNAP', 'https://finance.yahoo.com/quote/AAPL?p=AAPL', 
                'https://finance.yahoo.com/quote/AMZN?p=AMZN', 'https://finance.yahoo.com/quote/MSFT?p=MSFT',
                'https://finance.yahoo.com/quote/INTC?p=INTC']
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #this lets me capture the time
    page = urllib.request.urlopen(linkcall[value-1]).read()
    soup=BeautifulSoup(page, "lxml")
    instantprice = float(soup.find('span', {'class' :'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)
    symb = equities[eq]
    
    # do math
    cost = instantprice * shares
    
    newentry = ['buy', symb, shares, instantprice, time, cost*-1] #list to store items related to trade
    return newentry


#the following set of code defines the blotter
def show_blotter(table):
    print("this is your current blotter\n")
    if table == []:
        print('No entries yet!\n')
    else:
        x = ps.DataFrame(table)
        x.columns = ['Side','Ticker','Qty','Price','Date','Cost']
        print(ps.DataFrame(x),'\n')
    mainscreen()     
    return None
  
#get prices right now
def pricesnow():
    z = [0,0,0,0,0]
    for i in range(0,5):
        linkcall = ['https://finance.yahoo.com/quote/SNAP?p=SNAP', 'https://finance.yahoo.com/quote/AAPL?p=AAPL', 
                            'https://finance.yahoo.com/quote/AMZN?p=AMZN', 'https://finance.yahoo.com/quote/MSFT?p=MSFT',
                            'https://finance.yahoo.com/quote/INTC?p=INTC']
        page = urllib.request.urlopen(linkcall[i]).read()
        soup=BeautifulSoup(page, "lxml")
        instantprice = float(soup.find('span', {'class' :'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)
        z[i] = instantprice
    return z


#the following set of code shows the P/L
def show_pl(table):
    cash = 1000000
    
    #import ledger as dataframe
    x = ps.DataFrame(table)
    x.columns = ['Side','Ticker','Qty','Price','Date','Cost']
    newcash = cash + sum(x.Cost)
    
    y = ps.DataFrame(ps.np.empty((5,6)), columns = ['Ticker','Position','Market','WAP','UPL','RPL'])
    y.Ticker = equities
    instant = pricesnow()
    y.Market = instant    
    
    # Calculate items for WAP
    l = []
    for i in range(0,5):
        l = x[(x.Side == 'buy') & (x.Ticker == equities[i])]
        if sum(l.Qty) == 0:
            y.WAP[i] = 0
            y.Position[i] = sum(l.Qty)
        else:
            l.Cost = l.Qty * l.Price
            y.WAP[i] = sum(l.Cost)/sum(l.Qty)
            y.Position[i] = sum(l.Qty)
    
    # Calculate items for UPL
    for i in range(0,5):
        if y.UPL[i] > 0:
            y.UPL[i] = (y.Market[i] - y.WAP[i])*y.Position[i]
        else:
            y.UPL[i] = 0
    
    # Display items

    print("this is your current P/L")
    print(y,'\n',newcash)

    
    mainscreen()    
    #do math
    return None


#mainroutine
mainscreen()

'''
done = False
while not done:
    mainscreen()
    option = int(input())
    if option==4:
        done=True
        print('Thank you for trading with us!')
    if option>4:
        print('Incorrect Option, please select from 1 to 4')
    if option==1:
        letstrade = trade()
        done=True
    if option==2:
        show_blotter()
        done=True
    if option==3:
        show_pl()
        done=True
'''