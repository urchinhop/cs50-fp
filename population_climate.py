# -*- coding: utf-8 -*-
"""
Population vs 
Climate Change

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from sklearn import 

def main():

    """Read and display csv data from two existing files-population,temprature.""" 
    
    dfp=pd.read_csv('population.csv')
    displayheader('population.csv')
    dfp.index=dfp['Year']
    dft=pd.read_csv('GlobalLandTemperaturesByCountry.csv')
    displayheader('GlobalLandTemperaturesByCountry.csv')
    dft.index=dft['dt']
    
    
    cn=input("Enter country: ")
    cn=cn.title()
           
    mask = dfp['Country'].isin([cn])
    dfpp=dfp[mask].filter(items=['Value'])
    print(dfpp)
    print('\n')
    plt.figure()
    plt.plot(dfpp)
    plt.title('Population vs Time')
    plt.xlabel('Year')
    plt.ylabel('Value')
    show=dfpp.filter(items=['Value']).describe()
    print(show)
    print('\n')
    
    mask = dft['Country'].isin([cn])
    times=pd.DatetimeIndex(dft['dt'])
    dft=dft.fillna(method='ffill')
    group=dft.groupby([times.year]).mean()
    dftt=group['AverageTemperature']
    dftt=dftt.loc[dftt.index>1959]
    
    print(dftt)
    print('\n')
    plt.figure()
    plt.plot(dftt)
    plt.title('AvgTemp vs Time')
    plt.xlabel('Time')
    plt.ylabel('Temp')
    show=dftt.describe()
    print(show)
    
  

   

def displayheader(filename):
    with open(filename) as f:
        reader=csv.reader(f)
        header=next(reader)
    
        for index,cheader in enumerate(header):
            print(index,cheader)
        print('\n')
    
        
if __name__=="__main__":
    main()