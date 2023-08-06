# coding=utf-8
'''
Created on Mar 30, 2016

@author: yangjie
'''
from .CommonTool import (LogTool, MD5Tool, XMLDictTool,
                         GzipperTool, CompareTool)
from .InternetTool import HTTPOpener
from .DataBaseTool import MYSQLDataBaseConnector


class ToolFactory():

    def __init__(self, logger=None, logger_level="INFO"):
        if logger is None:
            self.default_logger = LogTool("wizard_interface")
        else:
            self.default_logger = logger
        self.set_logger_level(logger_level)

    def set_logger_level(self, logger_level):
        self.default_logger.setLevel(logger_level)


class LoggerToolFactory(ToolFactory):

    def __init__(self, logger=None, logger_level="INFO"):
        super(LoggerToolFactory, self).__init__(logger, logger_level)
        self.default_logger.debug("create LoggerToolFactory")

    def get_logger(self, logger_name, logger_level="INFO"):
        res = LogTool(logger_name, logger_level)
        return res


class CommonToolFactory(ToolFactory):

    def __init__(self,  logger=None, logger_level="INFO"):
        super(CommonToolFactory, self).__init__(logger, logger_level)
        self.default_logger.debug("create CommonToolFactory")

    def get_MD5_tool(self):
        res = MD5Tool(self.default_logger)
        return res

    def get_XMLDict_tool(self):
        res = XMLDictTool(self.default_logger)
        return res

    def get_gzipper_tool(self):
        res = GzipperTool(self.default_logger)
        return res

    def get_compare_tool(self):
        res = CompareTool(self.default_logger)
        return res


class InternetToolFactory(ToolFactory):

    def __init__(self,  logger=None, logger_level="INFO"):
        super(InternetToolFactory, self).__init__(logger, logger_level)
        self.default_logger.debug("create InternetToolFactory")

    def get_HTTP_opener_tool(self, enable_cookie=False):
        res = HTTPOpener(self.default_logger, enable_cookie)
        return res


class DataBaseToolFactory(ToolFactory):

    def __init__(self,  logger=None, logger_level="INFO"):
        super(DataBaseToolFactory, self).__init__(logger, logger_level)
        self.default_logger.debug("create DataBaseToolFactory")

    def get_MYSQL_Connector(self, host, user, passwd, port, charset="utf-8"):
        res = MYSQLDataBaseConnector(
            self.default_logger, host, user, passwd, port, charset)
        return res
