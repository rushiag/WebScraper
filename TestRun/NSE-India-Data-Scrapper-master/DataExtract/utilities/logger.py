'''
Created on 29-Sep-2018

@author: vivkv
'''

class Log(object):
    
    def __init__(self, msg):
        with open("log.txt","a") as log_handle:
            log_handle.write(msg+'\n')
    
    