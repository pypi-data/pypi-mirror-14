# coding=utf-8
'''
Created on Mar 30, 2016

@author: yangjie
'''
from .CommonTool import LogTool, MD5Tool, XMLDictTool, GzipperTool
from .InternetTool import HTTPOpener


class ToolFactory():

    def __init__(self):
        self.default_logger = LogTool("wizard_interface")


class CommonToolFactory(ToolFactory):

    def __init__(self):
        super(CommonToolFactory, self).__init__()
        self.default_logger.info("create CommonToolFactory")

    def get_MD5_tool(self):
        res = MD5Tool(self.default_logger)
        return res

    def get_XMLDict_tool(self):
        res = XMLDictTool(self.default_logger)
        return res

    def get_gzipper_tool(self):
        res = GzipperTool(self.default_logger)
        return res


class InternetToolFactory(ToolFactory):

    def __init__(self):
        super(InternetToolFactory, self).__init__()
        self.default_logger.info("create InternetToolFactory")

    def get_HTTP_opener_tool(self, enable_cookie=False):
        res = HTTPOpener(self.default_logger, enable_cookie)
        return res
