#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 12:15:59 2021

@author: jamesdebeer
"""

#%%

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import requests #API


#%%

#Price API
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()


#%%

BTC_price = data["bpi"]["USD"]["rate"].replace(",", "")


innitial_investment = 0.2 #BTC
entry_price_BTC = 46500
leverage = 20

def pnl(entry_price_BTC, current_price_BTC, innitial_investment , leverage):
    contract_price = 100
    
    ballance_USD = innitial_investment*entry_price_BTC
    no_contracts = ballance_USD*leverage/contract_price 
    contract_buy_value = contract_price*no_contracts
    buy_value_BTC = contract_buy_value/entry_price_BTC
    sell_value_BTC = contract_buy_value/current_price_BTC
    pnl = buy_value_BTC - sell_value_BTC
    
    return pnl


x = range(entry_price_BTC ,200000,1000)
y = []

for i in x:
    y = pd.to_numeric(pnl(entry_price_BTC , pd.to_numeric(x), innitial_investment, leverage))


#%%

# Let's define our sample data:
    
def elbox_idx (x,y):
    
    #Elbow of Curve
    from kneebow.rotor import Rotor #curve elbow
    
    x = np.array(x)
    x = x[::-1]

    data = np.array([x,y])
    data = data.transpose()
    
    rotor = Rotor()
    rotor.fit_rotate(data)
    
    elbow_idx = rotor.get_elbow_index()
    print(elbow_idx)
    return elbow_idx

elbow_index = elbox_idx(x,y)

data = np.array([x,y]).transpose()
elbow_price = data[elbow_index]


#%%

#Plot profit Curve

plt.plot(x, y, color='r', lw=0.7)

plt.axvline(x=elbow_price[0] ,  color='k', lw = 0.5,  ls="--", label= "Exit Price {}")
plt.axhline(y = pd.to_numeric(pnl(entry_price_BTC ,elbow_price[0] ,innitial_investment , leverage)), color='k', ls="--", lw = 0.3, label="PNL(BTC)" )
plt.legend(bbox_to_anchor=(1,0.6))

# Adding Title
plt.title("Perpetual Futures BTC Coin-Margin Profit Curve")
  
# Labeling the axes
plt.xlabel("BTC Price (USD)")
plt.ylabel("PNL (Profit & Loss) (BTC)")
  
# function to show the plot 
plt.show()



#%%


PNL  =  pd.to_numeric(pnl(entry_price_BTC ,elbow_price[0] ,innitial_investment , leverage))

ROE = (PNL/ (PNL+innitial_investment))*100 # %
ROE_dollar = innitial_investment*pd.to_numeric((BTC_price))


PNL2 = pd.to_numeric(pnl(elbow_price[0], 164000, innitial_investment, leverage))
ROE2 = (PNL2/ (PNL2+innitial_investment))*100 # %

PNL_total = PNL + PNL2

PNL3 = pd.to_numeric(pnl(entry_price_BTC ,164000,innitial_investment , leverage))

print("\n If you sell at " + str(elbow_price[0]) + " , and enter a new contract at that price with the  same specs \n and sell at "  + str(elbow_price[0]) + " , your profit is: " + 
      str(round(PNL_total,3)) + 
      " BTC, \n but if you held the trade from entry to exit price 2 your profit is: " 
      + str(round(PNL3, 3)) + " BTC")
 
 
 
 