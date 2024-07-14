'''

'''

import sys
import stopit
from utilities.jsonReader import JSONReader
from utilities.logger import Log
from Db.dbOperations import DBOp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PageObjects.nseEquities import NSEequities
from PageObjects.historicIndex import HistoricIndex


class Scrapper(object):

    driver = None
    def __init__(self,historic=False):
        
        props = JSONReader("properties/properties.json").getDictionaryFromJson()
       
        try:         
            # creating new instance each time because its a big operation and might get session timeouts if i try to use the same driver
            #driver = webdriver.PhantomJS(executable_path = props.get("phantomJsURL"))
            options = Options()
            options.set_headless(headless=True)
            self.driver = webdriver.Firefox(firefox_options=options)
            self.driver.implicitly_wait(10)
            self.tryCount =0
            self.dbop = DBOp()
            
        except Exception as e:
            print("Could not create a webdriver instance. Exiting..", e)
            self.driver.close()
            sys.exit(0)
        try:
            if not historic:
                self.driver.get(props.get("equityURL"))
            else:
                self.driver.get(props.get("historicURL"))
            
        except Exception as e:
            if not historic:
                print("Could not open the URL - ", props.get("equityURL"))
            else:
                print("Could not open the URL - ", props.get("historicURL"))
            self.driver.close()
    
    
    def numberGenerator(self,value):
        val = value
        if ',' in value:
            val = ''.join(i for i in value if i.isdigit() or i=='.')
        return val
    
    
    def insertScrapedValues(self,symbol,fro,to,stRange,eRange,tableVals):
        inserted = True
        for tr in tableVals.find_elements_by_tag_name('tr'):
            values_temp=[]
            
            for td in tr.find_elements_by_tag_name('td'):
                values_temp.append(td.text)
                if len(values_temp)==eRange:
                    for k in range(stRange,eRange):
                        values_temp[k]=self.numberGenerator(values_temp[k])
                    for i in range(0,eRange):
                        if values_temp[i] == '-':
                            values_temp[i] = None
                    inserted = self.dbop.insertData(symbol,values_temp)
        if not inserted:
            print(symbol, " data for year ", fro, " -- ", to, " already present")
            msg = symbol+" data for year "+fro+" -- "+to+" already present"
            Log(msg)
        else:
            print(symbol, " data for year ", fro, " -- ", to, " has been inserted ")
            msg = symbol+" data for year "+ fro+ " -- "+ to+ " has been inserted "
            Log(msg)
       
    @stopit.threading_timeoutable(default="equity scrapper function is stuck")
    def equityScrapper(self,symbol,fro="",to="",selected=False):
            equityPage = NSEequities(self.driver)
            try:
                tableVals = equityPage.getCompanyData(symbol,fro,to,selected)
                inserted = self.insertScrapedValues(symbol,fro,to,3,15,tableVals)
                self.driver.close()                 # closing this webdriver instance
                
            except Exception as e:
                print("Missing : ", symbol, " No record found for year ", fro, " -- ", to)
                msg = "Missing : "+symbol+" No record found for year "+fro+" -- "+to
                Log(msg)
                self.tryCount += 1
                if self.tryCount<3:
                    print("Trying again..")
                    msg = "Trying again.."
                    Log(msg)
                    result = self.equityScrapper(symbol,fro,to,selected,timeout=100)
                    if result == "equity scrapper function is stuck":
                        self.driver.quit()
                        sc = Scrapper()
                        sc.equityScrapper(symbol,fro,to,selected,timeout=100)
                self.driver.quit()
        
    @stopit.threading_timeoutable(default="historic scrapper function is stuck")    
    def historicScrapper(self,fro,to,symbol="NIFTY 50",timeout=100):
        historicPage = HistoricIndex(self.driver)
        try:
            tableVals = historicPage.getNiftyData(fro,to)
            inserted = self.insertScrapedValues(symbol,fro,to,1,7,tableVals)   
            self.driver.close()
        except Exception as e:
            print("Missing : ", symbol, " No record found for year ", fro, " -- ", to)
            msg = "Missing : "+symbol+" No record found for year "+fro+" -- "+to
            Log(msg)
            self.tryCount += 1
            if self.tryCount<3:
                print("Trying again..")
                msg = "Trying again.."
                Log(msg)
                result = self.equityScrapper(symbol,fro,to,selected,timeout=100)
                if result == "historic scrapper function is stuck":
                    self.driver.quit()
                    sc = Scrapper(historic=True)
                    sc.historicScrapper(fro,to)
            self.driver.quit()