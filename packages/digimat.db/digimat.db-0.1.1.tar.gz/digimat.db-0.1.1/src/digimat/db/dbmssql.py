# http://pymssql.org/
import pymssql
from warnings import filterwarnings

class DBMSSql(object):
    def __init__(self, host, user, password, db, logger):
        self._host=host
        self._user=user
        self._password=password
        self._db=db
        self._logger=logger
        self._mssql=None

    @property
    def logger(self):
        return self._logger

    @property
    def mssql(self):
        return self._mssql

    # def ignoreWarnings(self):
    #     filterwarnings('ignore', category = MySQLdb.Warning)

    def connect(self):
        if self._mssql is not None:
            return self._mssql
        self.logger.info("mssql(%s):connecting..." % self._host)
        self._mssql=None
        try:
            self._mssql=pymssql.connect(self._host, self._user, self._password, self._db)
            self._mssql.autocommit(False)
        except:
            self.logger.exception("connect error!")

        return self._mssql

    def cursorArray(self):
        try:
            return self.connect().cursor()
        except:
            pass

    def cursor(self):
        return self.cursorArray()

    def cursorDict(self):
        try:
            return self.connect().cursor(as_dict=True)
        except:
            pass

    def commit(self):
        try:
            self._mssql.commit()
            return True
        except:
            self.logger.exception("commit error!")

    def rollback(self):
        try:
            self._mssql.rollback()
            return True
        except:
            self.logger.exception("rollback error!")

    def closeCursor(self, cursor):
        try:
            if cursor:
                cursor.close()
        except:
            pass

    def sqlExecute(self, cursor, sql, args=None):
        if cursor:
            try:
                print "[SQL:%s]" % sql
                cursor.execute(sql, args)
                #print "[SQL-QUERY-ROWCOUNT=%d]" % c.rowcount
                return True
            except:
                self.logger.exception('sqlExecute()')

    def sqlExecuteMany(self, cursor, sql, args=None):
        if cursor:
            try:
                #print "[SQL:%s]" % sql
                cursor.executemany(sql, args)
                #print "[SQL-QUERY-ROWCOUNT=%d]" % c.rowcount
                return True
            except:
                self.logger.exception('sqlExecuteMany()')

    def sqlFetchall(self, cursor, sql, args=None):
        if self.sqlExecute(cursor, sql, args):
            try:
                rows=cursor.fetchall()
            except:
                rows=None
                self.logger.exception('sqlFetchall()')
            return rows

    def disconnect(self):
        try:
            if self._mssql:
                self.logger.info("mssql(%s):disconnect" % self._host)
            self._mssql.close()
        except:
            pass
        self._mssql=None


if __name__ == '__main__':
    pass