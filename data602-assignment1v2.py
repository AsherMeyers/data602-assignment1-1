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
import os
import socket
import datetime
from bs4 import BeautifulSoup
import urllib
import pandas as ps
import numpy as np
equities = ['SNAP', 'AAPL', 'AMZN', 'MSFT', 'INTC']
ledger = []
from flask import Flask

app = Flask(__name__)

@app.route('/')

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
        if x != None:
            ledger.append(x)
        else:
            print("You couldn't sell")
    elif selection==2:
        show_blotter(ledger)
    elif selection==3:
        show_pl(ledger)
    elif selection==4:
        print('Thanks for using me!\n')
    else:
        print('Invalid choice. Please enter 1-4\n')
        mainscreen()
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
    option = int(input('Please select: '))
    if option == 1:
        print('Which one do you wish to sell?')
        print('1. SNAP')
        print('2. AAPL')
        print('3. AMZN')
        print('4. MSFT')
        print('5. INTC')
        value = int(input('Please select: ')) #this stores the value of the stock ticker
        shares = int(input('How many shares? ')) #this stores the number of stocks
        eq = value-1
        if table == []:
            print('No transactions: \n')
        elif table != [] and stockavail(table,eq)>=shares:
            entry = sell(table, value,shares,eq)
            return entry
        else:
            print('Not enough stocks available to sell: \n')
    elif option == 2:
        print('Which one do you wish to buy? ')
        print('1. SNAP')
        print('2. AAPL')
        print('3. AMZN')
        print('4. MSFT')
        print('5. INTC')
        value = int(input('Please select? '))
        shares = int(input('How many shares? '))
        eq = value-1
        if table == []:
            entry = buy(table, value,shares,eq)
            return entry
        elif table != [] and buy(value,shares,eq)[5]>=cashavail(table):
            entry = buy(table, value,shares,eq)
            return entry
        elif table != [] and cashavail(table)<=0:
            print('Not enough money available to buy: ')
        else:
            print('Not enough money available to buy: ')
    else:
        print('Invalid choice. Please enter 1-2\n')
        mainscreen()
    return
'''
        else:
            z = cashavail(u)
            if z > 0:
                entry = buy(value,shares,eq)
                return entry
            else:
                print('Not enough money available to buy: ')
                mainscreen()
                return None
'''

# Check to see if we have stock to sell or cash
def cashavail(table):
    '''
    This function checks to see if stocks are available to sell or enough cash to buy
    Table comes from ledger and eq is the stock being checked
    
    '''
    cash = 1000000
    
    #import ledger as dataframe and calculate if cash available to buy
    x = ps.DataFrame(table)
    x.columns = ['Side','Ticker','Qty','Price','Date','Cost','tWAP']
    newcash = cash + sum(x.Cost)
    return newcash

def stockavail(table,eq):
    #check to see if stock is available to sell
    x = ps.DataFrame(table)
    x.columns = ['Side','Ticker','Qty','Price','Date','Cost','tWAP']
    
    l = x[(x.Ticker == equities[eq])]
    stocks = sum(l.Qty)
    return stocks


def sell(table, value, shares, eq):
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
    
    if table == []:
        WAP = instantprice
    else:
        y = pl(table)
        WAP = y.WAP[eq]
    
    newentry = ['sell', symb, shares, instantprice, time, cost, WAP] #list to store items related to trade    
    return newentry    

    
def buy(table, value, shares, eq):
    #call link and read page for current price
    '''
    value which is the value is used to call the URL from linkcall list
    shares which is the number of shares is used in the math
    eq which is the ticker is used to record the symbol
    '''
    linkcall = ['https://finance.yahoo.com/quote/SNAP?p=SNAP', 'https://finance.yahoo.com/quote/AAPL?p=AAPL', 
                'https://finance.yahoo.com/quote/AMZN?p=AMZN', 'https://finance.yahoo.com/quote/MSFT?p=MSFT',
                'https://finance.yahoo.com/quote/INTC?p=INTC']
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #this lets me capture the time
    page = urllib.request.urlopen(linkcall[value-1]).read()
    soup=BeautifulSoup(page, "lxml")
    instantprice = float(soup.find('span', {'class' :'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)
    symb = equities[eq]
    
    # Calculate cost of stock purchase
    cost = instantprice * shares
    if table == []:
        WAP = instantprice
    else:
        y = pl(table)
        WAP = y.WAP[eq]

    newentry = ['buy', symb, shares, instantprice, time, cost*-1, WAP] #list to store items related to trade
    return newentry


#the following set of code defines the blotter
def show_blotter(table):
    print("this is your current blotter\n")
    if table == []:
        print('No entries yet!\n')
    else:
        x = ps.DataFrame(table)
        x.columns = ['Side','Ticker','Qty','Price','Date','Cost','WAP']
        x.drop(['WAP'], axis = 1, inplace = True)
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

def pl(table):
    x = ps.DataFrame(table)
    x.columns = ['Side','Ticker','Qty','Price','Date','Cost','tWAP']

    y = ps.DataFrame(ps.np.empty((5,6)), columns = ['Ticker','Position','Market','WAP','UPL','RPL'])
    y.Ticker = equities
    instant = pricesnow()
    y.Market = instant    
    
    # Calculate items for WAP
    l = []
    r = []
    for i in range(0,5):
        l = x[(x.Side == 'buy') & (x.Ticker == equities[i])]
        r = x[(x.Ticker == equities[i])]
        r.loc[r.Side == 'sell', 'Qty'] *= -1
        if sum(l.Qty) == 0:
            y.WAP[i] = 0
            y.Position[i] = sum(r.Qty)
        else:
            l.Cost = l.Qty * l.Price
            y.WAP[i] = sum(l.Cost)/sum(l.Qty)
            y.Position[i] = sum(r.Qty)
    
    # Calculate items for UPL
    for i in range(0,5):
        if y.Position[i] > 0:
            y.UPL[i] = (y.Market[i] - y.WAP[i])*y.Position[i]
        else:
            y.UPL[i] = 0
        
    #calculate RPL
    for i in range(0,5):
        r = x[(x.Side == 'sell') & (x.Ticker == equities[i])]
        r['Profit'] = r.Qty*(r.Price-r.tWAP)
        if sum(l.Qty) == 0:
            y.RPL[i] = 0
        else:
            y.RPL[i] = sum(r.Profit)
    return y

def show_pl(table):
    if table == []:
        print('No P/L until you buy your first stock\n')
        mainscreen()
    else:
        cash = 1000000
        y=pl(table)
        #import ledger as dataframe
        x = ps.DataFrame(table)
        x.columns = ['Side','Ticker','Qty','Price','Date','Cost','WAP']
        newcash = cash + sum(x.Cost)
        
        # Display items
        print('\n')
        print("this is your current P/L")
        print(y,'\n\n','You have this much cash left:',newcash)
    
        
        mainscreen()    
        #do math
        return y


#mainroutine
mainscreen()

if __name__ == "__main__":
    app.run(host='0.0.0.0') #host 0.0.0.0 needed for docker