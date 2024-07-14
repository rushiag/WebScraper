'''
Created on 29-Sep-2018

@author: vivkv
'''
#from Extractor.scrapper import Scrapper
from utilities.jsonReader import JSONReader
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class NSEequities(object):
    
    def __init__(self,driver): 
        self.driver = driver
        self.props = JSONReader("properties/nseEquities.json").getDictionaryFromJson()
    
    def getCompanyData(self,symbol,fro="",to="",selected=False):
        try:
            company = self.driver.find_element_by_xpath(self.props.get("SYMBOL"))
            company.clear()
            company.send_keys(symbol)
            if selected:
                radio = self.driver.find_element_by_xpath(self.props.get("RADIO_BUTTON"))
                radio.click()
                fromDate = self.driver.find_element_by_xpath(self.props.get("FROM_DATE"))
                fromDate.clear()
                fromDate.send_keys(fro)
                toDate = self.driver.find_element_by_xpath(self.props.get("TO_DATE"))
                toDate.clear()
                toDate.send_keys(to)
            else: 
                self.driver.find_element_by_xpath(self.props.get("DROP_DOWN")).click()
                
            self.driver.find_element_by_xpath(self.props.get("GET")).click()
            element = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
                        )
            
            tableValues = self.driver.find_element_by_xpath(self.props.get("TABLE"))
        
            return  tableValues
        except Exception as e:
            raise Exception