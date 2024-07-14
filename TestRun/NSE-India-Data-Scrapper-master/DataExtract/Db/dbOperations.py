'''
Created on 29-Sep-2018

@author: vivkv

This class deals with DB Insert operations.

'''
import sys
import psycopg2
from psycopg2.extensions import  AsIs
from utilities.logger import Log
from utilities.jsonReader import JSONReader


class DBOp(object):
    
    def __init__(self):
        try:
            
            props = JSONReader("properties/dbProperties.json").getDictionaryFromJson()
            self.USER = props.get("USER")
            self.PASS = props.get("PASSWORD")
        except Exception as e:
            print "Could not read DB properties file. Exiting.."
            sys.exit(0)
    
    def createTable(self,compSymbol,historic=False):
        symbol = ''.join(i for i in compSymbol if  i.isalpha())
        try:  
            con = psycopg2.connect(database='companies', user=self.USER, password=self.PASS)
            cur = con.cursor()
        except Exception as e:
            print "Error connection to DB. Exiting.."
            sys.exit(0)
        try:
            if not historic:
                cur.execute("CREATE TABLE %s(SERIES VARCHAR(5), DATE_ DATE, PREV_CLOSE MONEY, OPEN_PRICE MONEY,\
                HIGH_PRICE MONEY, LOW_PRICE MONEY, LAST_PRICE MONEY, CLOSE_PRICE MONEY,VWAP MONEY,\
                TOTAL_TRAIDED_QUANTITY BIGINT, TURNOVER MONEY, NO_OF_TRADES BIGINT, DELIVERABLE_QUANTITY BIGINT,\
                PERCENTAGE_DLY DOUBLE PRECISION)", (AsIs(symbol),))
            else:
                cur.execute("CREATE TABLE %s(DATE_ DATE, OPEN MONEY, HIGH MONEY,\
                LOW MONEY, CLOSE MONEY, \
                SHARES_TRADED BIGINT, TURNOVER MONEY)", (AsIs(symbol),))
                
            con.commit()
            print "Table created for ",symbol
            msg = "Table created for "+symbol
            Log(msg)        
            return 1
        except psycopg2.DatabaseError, e:
            if "already exists" in str(e):
                return 2
            else:
                print "Error occured while creating Table for ",symbol," Exiting..",e
                con.close()
                sys.exit(0)
        finally:
            con.close()
            
            
    def insertData(self,compSymbol,values):
        symbol = ''.join(i for i in compSymbol if i.isalpha())
        try:
            con = psycopg2.connect(database='companies', user=self.USER, password=self.PASS)
            cur = con.cursor()
        except Exception as e:
            print "Error connection to DB. Exiting.."
            sys.exit(0)
        found = False
        try:
            exists_query = '''
                select exists (
                select 1
                from %s
                where DATE_= %s
            )'''
            if len(values)==7:
                cur.execute(exists_query, (AsIs(symbol),values[0],))
            elif len(values)==15:
                cur.execute(exists_query, (AsIs(symbol),values[2],))
            found = cur.fetchone()[0]

        except psycopg2.DatabaseError, e:
            print 'Error -  %s'%e
            sys.exit(0)

        try:
            if not found and len(values)==15:
                cur.execute("INSERT INTO %s VALUES(%s,to_date(%s,\'DD-Mon-YYYY\'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(AsIs(symbol),values[1],\
                                                                                                                         values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9],\
                                                                                                                         values[10],values[11],values[12],values[13],values[14]))
                
            elif not found and len(values)==7:
                cur.execute("INSERT INTO %s VALUES(to_date(%s,\'DD-Mon-YYYY\'),%s,%s,%s,%s,%s,%s)",(AsIs(symbol),values[0],\
                                                                                                                         values[1],values[2],values[3],values[4],values[5],values[6]))
            else:
                return False
            
            con.commit()
            con.close()
            return True
        except psycopg2.DatabaseError, e:
            print "Could not insert a row to table ",symbol," Exiting.."
            con.close()
            sys.exit(0)
            
            