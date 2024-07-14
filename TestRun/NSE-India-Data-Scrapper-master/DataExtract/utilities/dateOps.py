'''
Created on 29-Sep-2018

@author: vivkv

This class deals with date related operations while inputting in the start and end date sections.
'''


class DateOps(object):

    def __init__(self,):
        pass
        
    def isLeapYear(self,year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    
    def dateCreator(self,startMonth, endMonth, year):
        startDay = 1                        # month will always have a date 1
        startDate = endDate = ""            # we will have to create based on some logic 
        endDay = 28                         # first February
        if self.isLeapYear(year):           #First check for leap year
            endDay = 29
        if endMonth == 4 or endMonth == 6:  # as only these end months will have 30 days bcoz we are taking 2 months at a time
            endDay = 30
        elif endMonth == 8 or endMonth == 10 or endMonth == 12:     # rest other end months will have 31 days
            endDay = 31
        if startMonth < 10:                 # for putting a zero in moth section while inputting date i.e. 01-04-2018 (in start section)
            startDate = "0" + str(startDay) + "-0" + str(startMonth) + "-" + str(year)
        else:                               # for not putting extra zero in month section i.e. 01-10-2018
            startDate = "0" + str(startDay) + "-" + str(startMonth) + "-" + str(year)
        if endMonth < 10:                   # same for end month
            endDate = str(endDay) + "-0" + str(endMonth) + "-" + str(year)
        else:
            endDate = str(endDay) + "-" + str(endMonth) + "-" + str(year)
        return [startDate, endDate]
