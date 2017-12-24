# -*- coding: utf-8 -*-
"""
Population Growth vs 
Climate Change??

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import statsmodels.api as sm


def main():

    """Read and display csv data from two existing files-population,temprature.""" 
    """https://www.kaggle.com/brajput24/world-population"""
    dfp=pd.read_csv('population.csv')
    displayheader('population.csv')
    dfp.index=dfp['Year']
    dft=pd.read_csv('GlobalLandTemperaturesByCountry.csv')
    displayheader('GlobalLandTemperaturesByCountry.csv')
    
    """ Request user input a country name to investigate""" 
    cn=input("Enter country: ")
    if not cn:
        print("Must provide a country name.")
    cn=cn.title()
    
    """ Use the country user inputed as a filter for both population
        and temperature dataset."""
               
    maskp = dfp['Country'].isin([cn])
    """ Only show Value which is population qty."""
    dfp=dfp[maskp].filter(items=['Value'])
    print(dfp)
    print('\n')
    """Plot the population vs time gragh."""
    plt.figure()
    plt.plot(dfp)
    plt.title('Population vs Time')
    plt.xlabel('Year')
    plt.ylabel('Value')
    """ Display population data info."""
    showp=dfp.describe()
    print(showp)
    print('\n')
    """To examine two factors:p1-quantity increment of population;
        p2-ratio of population to last year's impacts on temperature change."""
    pl=[]
    indarray=[]
    datap1=[]
    datap2=[]
    """Store all the population data of each year in list pl."""
    for index, row in dfp.iterrows():
        pl.append(row['Value'])
    for i in range(51):
        
        p1=pl[i+1]-pl[i]
        p2=pl[i+1]/pl[i]
        datap1.append(p1)
        datap2.append(p2)
        indarray.append(i+1960)
    """create two series based on two factors p1,p2."""            
    s1_p = pd.Series(data=datap1, index=indarray)
    s2_p = pd.Series(data=datap2, index=indarray)
    
    """ Use the country user inputed as a filter for both population
        and temperature dataset."""
    maskt = dft['Country'].isin([cn])
    """Only show Average Temp."""
    dft=dft[maskt].filter(items=['AverageTemperature','dt'])
    
    """group months data into year and take mean of it as inspired by
       wk11 seminar Data Science with Python."""
    times=pd.DatetimeIndex(dft['dt'])
    dft=dft.fillna(method='ffill')
    group=dft.groupby([times.year]).mean()
    dft=group['AverageTemperature']
    dft=dft[dft.index>1959]
    print(dft)
    print('\n')
    """Plot the temperature vs time gragh."""
    plt.figure()
    plt.plot(dft)
    plt.title('AvgTemp vs Time')
    plt.xlabel('Time')
    plt.ylabel('Temp')
    showt=dft.describe()
    print(showt)
    
    tl=[]
    indarray=[]
    datat=[]
    logistic_judge=[]
    """Store all the temperature data of each year in list pl."""
    for index,row in dft.iteritems():
        tl.append(row)
    for i in range(51):
       
        ti=tl[i+1]-tl[i]
        datat.append(ti)
        if ti>0:
            logistic_judge.append(1)
        else:
            logistic_judge.append(0)
    """create index for judge series to use."""
    array=[]
    for i in range(51):
        array.append(i+1960)
    s_lrj=pd.Series(data=logistic_judge,index=array)
    
    """Combine two factors p1 and p2 and judge series into a dataframe lrdf."""
    lrdf={'Population inc':s1_p,'Population ratio':s2_p,'Temp increased':s_lrj}
    lrdf=pd.DataFrame(lrdf)
    print('\n')
    
    '''Logistic regression analysis of dataframe lrdf-
       http://www.powerxing.com/logistic-regression-in-python/'''
    print (lrdf.describe())
    print(pd.crosstab(lrdf['Temp increased'],lrdf['Population inc'],rownames=['Temp increased']))
    
    lrdf.hist()
    plt.show()
   
    lrdf['intercept']=1.0
    train_c=lrdf.columns[:-2]
    logit=sm.Logit(lrdf['Temp increased'],lrdf[train_c])
    result=logit.fit()
    print(result.summary())
  
    
'''create a function for later ease of displaying column headers.'''
def displayheader(filename):
    with open(filename) as f:
        reader=csv.reader(f)
        header=next(reader)
    
        for index,cheader in enumerate(header):
            print(index,cheader)
        print('\n')
     
if __name__=="__main__":
    main()