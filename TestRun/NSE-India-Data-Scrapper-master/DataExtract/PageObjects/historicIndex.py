'''
Created on 29-Sep-2018

@author: vivkv
'''
from utilities.jsonReader import JSONReader
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class HistoricIndex(object):
    
    def __init__(self, driver):
        self.driver = driver
        self.props = JSONReader("properties/historicIndex.json").getDictionaryFromJson()
        
    def getNiftyData(self,fro,to):
        try:
            fromDate = self.driver.find_element_by_xpath(self.props.get("fromDate"))
            toDate = self.driver.find_element_by_xpath(self.props.get("toDate"))
            fromDate.clear()
            fromDate.send_keys(fro)
            toDate.clear()
            toDate.send_keys(to)
            get = self.driver.find_element_by_xpath(self.props.get("GET"))
            get.click()
            element = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
                        )
            tableValues = self.driver.find_element_by_xpath(self.props.get("tableData"))
            
            return  tableValues
        except Exception as e:
            raise Exception
            
            