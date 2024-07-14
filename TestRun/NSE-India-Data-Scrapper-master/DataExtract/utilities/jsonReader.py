'''
Created on 29-Sep-2018

@author: vivkv
'''
import sys
import json

class JSONReader(object):
    
    def __init__(self, filepath):
        try:
            self.f = open(filepath)
            #print "opened file ",filepath
        except Exception as e:
            print "Could not open json file ",filepath, " Exiting..",e
            sys.exit(0)
    
    def getDictionaryFromJson(self):
        try:
            dictionary = json.load(self.f)
            self.f.close()
            return dictionary;
        except Exception as e:
            print "Could not load json file. Exiting..",e
            sys.exit(0)