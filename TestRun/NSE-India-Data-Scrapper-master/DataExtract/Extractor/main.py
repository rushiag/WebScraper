'''
Created on 29-Sep-2018

@author: vivkv

This module is the start of the program,

1. First it loads all the properties from properties.json to form it as a dictionary 
2. It reads the company text file locating it from properties.json file

'''

import sys
import datetime
from utilities.jsonReader import JSONReader
from Db.dbOperations import DBOp
from utilities.dateOps import DateOps
from utilities.logger import Log
from scrapper import Scrapper

# load all the properties from properties.json to form it as a dictionary named props
props = JSONReader("properties/properties.json").getDictionaryFromJson()

# a list variable to store all the company names in program
companies = []

# a list variable to store the company names whose table is created to save time
tableCreationDone = []

# get the current year
currentYear = int(datetime.datetime.now().strftime("%Y"))

# get a handle of db operation
dbop = DBOp()

# get a handle of date operations
dt = DateOps()

# read company text file locating it from properties.json file
def readCompanyFile(): 
    companyFile = props.get("companyTxtFile")
    try:
        comp = open(companyFile)
        for line in comp.readlines():
            companies.append(line.strip())
    except Exception as e:
        print "company txt file could not be opened. exiting..",e
        sys.exit(0)
        
        
def formDateAndCallScrapper(startMonth,endMonth,year,historic=False):
    dates = dt.dateCreator(startMonth,endMonth,year)
    print "start - ",dates[0]," to end - ",dates[1]
    msg = "start - "+dates[0]+" to end - "+dates[1]
    Log(msg)
    if not historic:
        sc = Scrapper()
        return sc.equityScrapper(symbol,dates[0],dates[1],selected=True,timeout=100)
    else:
        sc = Scrapper(historic=True)
        return sc.historicScrapper(dates[0],dates[1])


def getDataFromLastYears(symbol,historic=False):
    
    # get the year from which we have to start scraping.
    year = int(props.get("startYear"))
    
    # check for company's db or create it if not created already.
    isCreated = dbop.createTable(symbol,historic)
        
    # this loop code will form dates and scrape data from the startYear say 2000 till last year's December say 2017.
    while year < currentYear:
        startMonth = 1
        endMonth = startMonth+1
        while endMonth<13:
            if not historic:
                result = formDateAndCallScrapper(startMonth,endMonth,year)
            else:
                result = formDateAndCallScrapper(startMonth,endMonth,year,historic=True)
            startMonth = endMonth+1
            endMonth = startMonth+1
        year += 1
            
    startDay = 1
    startMonth = 1
    endMonth = startMonth+1
    limitMonth = int(datetime.datetime.now().strftime("%m")) # Current month
        
    # now this loop is for the last slot of month/months which couldn't form 2 months pack.
    while endMonth < limitMonth:
        if not historic:
            result = formDateAndCallScrapper(startMonth,endMonth,year)
        else:
            result = formDateAndCallScrapper(startMonth,endMonth,year,historic=True)
        startMonth = endMonth+1
        endMonth = startMonth+1
        
    if limitMonth - startMonth == 0 or limitMonth - startMonth==1:
        startDate = "0"+str(startDay)+"-0"+str(startMonth)+"-"+str(year)
        endDate = str(datetime.datetime.now().strftime("%d-%m-%Y")) 
        print "start - ",startDate," to end - ",endDate
        msg = "start - "+startDate+" to end - "+endDate
        Log(msg)
        if not historic:
            sc = Scrapper()
            result = sc.equityScrapper(symbol,startDate,endDate,selected=True,timeout=100)
        else:
            sc = Scrapper(historic=True)
            result = sc.historicScrapper(startDate,endDate)
 
    

def getDataFromLast7Dayz(symbol):
    isCreated = dbop.createTable(symbol)
    print "getting data from last 7 days for ",symbol
    msg = "getting data from last 7 days for "+symbol
    Log(msg)
    sc = Scrapper()
    result = sc.equityScrapper(symbol,selected=False,timeout=100)
    
    
if __name__ == '__main__':
    
    readCompanyFile()
    
    if bool(props.get("historicMode")):
        print "Historic mode.."
        getDataFromLastYears("NIFTY 50",historic=True)
    else:
        for symbol in companies:
        
            if not  bool(props.get("dailyMode")):
                print "Heavy Data collector mode.."
                getDataFromLastYears(symbol)
            else:
                print "Daily mode.."
                getDataFromLast7Dayz(symbol)    
            print "\n\n"     
        
    print "Data inserted successfully !"
    
    
    #End of program
        
    