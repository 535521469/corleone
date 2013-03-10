'''
Created on 2013-3-9

@author: Administrator
'''
from DBUtils.PooledDB import PooledDB
import MySQLdb

class MySQLDBHelper(object):
    
    def __init__(self, host, user, passwd, db
                 , port=3306, dsn=None, charset='utf8'):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db
        self._port = port
        self._charset = charset
        self._dsn = dsn
    
    @staticmethod
    def getconnection(host, user, passwd, db
                 , port=3306, dsn=None, charset='utf8'):
        dbhelper = MySQLDBHelper(host, user, passwd
                                 , db, port, dsn, charset)
        dbhelper.connection()
        return dbhelper
    
    def connection(self, creator=MySQLdb, **kws):
        '''
        @param kws: connection pool params 
        use DBUtils ... 
        '''
        
        if hasattr(self, "pool"):
            self.con = self.pool.connection()
            self.cursor = self.con.cursor()
            return self.con
        else:
            self.pool = PooledDB(creator, host=self._host, user=self._user 
                     , passwd=self._passwd, db=self._db
                     , port=self._port, charset=self._charset
#                     , dsn=self._dsn
                     , **kws)
            return self.connection(creator)
        
    def execute(self, operation , parameters=None):
        self.cursor.execute(operation , parameters)
    
    def rollback(self):
        self.con.rollback()
    
    def commit(self):
        self.con.commit()
    
    def close(self):
        self.cursor.close()
        self.con.close()
    
    def callproc(self, procname , parameters):
        return self.cursor.callproc(procname , parameters)
        
    def select(self, operation, parameters=None):
        self.cursor.execute(operation, parameters)
        return self.cursor.fetchall()
    
    def selectcount(self, operation, parameters=None):
        self.cursor.execute(operation, parameters)
        return self.cursor.fetchall()[0][0]
    
    
    
    
