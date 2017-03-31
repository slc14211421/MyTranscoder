#coding=gbk  

import sqlite3
import os,sys,string  
import traceback  
from myTranscoder import settings

class mysqlite:
    def __init__(self):
        self.dbfile = os.path.dirname(os.path.dirname(os.path.abspath(settings.__file__)))+"/db.sqlite3"
        self.cx=sqlite3.Connection(self.dbfile)
    
    def select(self,sqlstr):
        #print self.dbfile
        return self.cx.execute(sqlstr)
    
    def closedb(self):
        self.cx.close()
        


      
class SQLObj(object):  
    def __init__(self, db = 'db.sqlite3'):  
            self.db_name = os.path.dirname(os.path.dirname(os.path.abspath(settings.__file__)))+"/"+db  
            self.connected = 0  
            self.cur  = None 
            self.conn = None 
            self._connect()  
      
    def _connect(self):  
            try:  
             
                self.conn = sqlite3.connect(self.db_name)  
                self.cur = self.conn.cursor()  
                self.connected = 1  
            except:  
                traceback.print_exc()  
                self.connected = 0  
     
    @property  
    def is_connected(self):  
            return self.connected != 0  
      
    def _check_alive(self):  
            if not self.is_connected:  
                self._connect()  
            if not self.is_connected:  
                raise "Can't connect to sqlite3"  
      

    def query(self, sql, warning=1):  
            self._check_alive()  
            try:  
                cur = self.conn.cursor()  
                cur.execute(sql)  
                res = cur.fetchall()  
                cur.close()  
            except:  
                if warning:  
                    traceback.print_exc()  
                return None  
            return res  
      
      

    def dquery(self, sql, warning=1):  
            self._check_alive()  
            try:  
                cur = self.conn.cursor()  
                cur.execute(sql)  
                  
                des = cur.description  
                res = cur.fetchall()   
                ret = []  
                if des:  
                    names = [x[0] for x in des] 
                    for line in res:  
                        ret.append(dict(zip(names, line))) 
                else:  
                    ret = res  
                cur.close()  
            except:  
                if warning:  
                    traceback.print_exc()  
                return None  
            return ret  
      
    def execute(self, sql, warning=1):  
            self._check_alive()  
            try:  
                cur  = self.conn.cursor()  
                rows = cur.execute(sql)  
                self.conn.commit()  
                cur.close()  
                return rows  
            except:  
                if warning:  
                    traceback.print_exc()  
                return -1  
      
    def close(self):  
            if self.connected == 0:  
                return  
            try:  
                self.cur.close()  
                self.conn.close()  
                self.connected = 0  
            except:  
                pass  
      
    def __del__(self):  
            self.close()  
      
def _lbsql_test_sqlite3():  
    db = SQLObj()  
    lists = db.dquery("select * from transcoder_transcodertask where status=2")
    #print lists  
    for l in lists:
        #print l  
        for k, v in l.items():  
            print "%s: %s" %(k, v),  
        print "\n"      
         
      
if __name__ == "__main__":  
        _lbsql_test_sqlite3()              