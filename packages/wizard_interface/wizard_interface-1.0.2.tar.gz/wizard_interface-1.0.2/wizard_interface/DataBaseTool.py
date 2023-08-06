# coding=utf-8
'''
Created on Mar 30, 2016

@author: yangjie
'''
import pymysql

class DataBaseConnector():
    pass


class MYSQLDataBaseConnector():

    def __init__(self, logger, host, user, passwd, port):
        self.logger = logger
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.logger.debug("create MYSQLDataBaseConnector")

    def execute(self, database_name, command):
        self.logger.info("start execute SQL: %s" % command)
        with MYSQLDataBase(self.logger,
                           self.host,
                           self.user,
                           self.passwd,
                           self.port)as (con, cur):
            cur.execute("use %s" % database_name)
            cur.execute(command)
            res = cur.fetchall()
            self.logger.info("execute SQL success")
            return res


class MYSQLDataBase():

    def __init__(self, logger, host, user, passwd, port):
        self.logger = logger
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port

    def connect(self, host, user, passwd, port):
        self.logger.debug("connect to MYSQLDataBase")
        res = pymysql.connect(host=host, user=user, passwd=passwd, port=port)
        return res

    def __enter__(self):
        self.conn = self.connect(self.host, self.user, self.passwd, self.port)
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.logger.debug("disconnect to MYSQLDataBase")
        if exc_type is not None:
            self.logger.error(exc_value)
        self.cur.close()
        self.conn.close()
