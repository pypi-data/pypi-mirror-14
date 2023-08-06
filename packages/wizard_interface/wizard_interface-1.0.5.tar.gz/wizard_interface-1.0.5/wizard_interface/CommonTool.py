# coding=utf-8
'''
Created on Mar 30, 2016

@author: yangjie
'''

import dicttoxml
import gzip
import hashlib
import logging
import xmltodict


class LogTool(logging.Logger):

    def __init__(self, logger_name, logger_level="NOTSET"):
        super(LogTool, self).__init__(logger_name, logger_level)
        self.streamHandler = logging.StreamHandler()
        self.set_logger_formatter()
        self.addHandler(self.streamHandler)

    def set_logger_formatter(self, format_str=None):
        fmt_str = "%(asctime)s [%(filename)s line %(lineno)d]\
[%(name)s %(levelname)s] %(message)s"
        if format_str is None:
            pass
        else:
            fmt_str = format_str
        fmt = logging.Formatter(fmt_str)
        self.streamHandler.setFormatter(fmt)


class MD5Tool():

    def __init__(self, logger: logging.Logger):
        self.logger = logger

        self.logger.debug("create md5 tool")

    def MD5_str(self, src_str: str, encoding="utf-8"):
        try:
            self.logger.debug("md5 str start: %s" % src_str)
            m5 = hashlib.md5()
            m5.update(src_str.encode(encoding))
            res = m5.hexdigest()
            self.logger.debug("md5 str success %s" % res)
            return res
        except Exception as error:
            self.logger.error(error)

    def MD5_dict(self, src_dict: dict, encoding="utf-8", safe_key: str=None):
        try:
            self.logger.debug("md5 dict start: %s" % src_dict)
            sortKey = sorted(src_dict.items(), key=lambda d: d[0])
            resList = []
            for item in sortKey:
                res = "=".join(item)
                resList.append(res)
            resList = "&".join(resList)
            if safe_key is None:
                pass
            else:
                resList += safe_key
            res = self.MD5_str(resList, encoding)
            self.logger.debug("md5 dict success: %s" % res)
            return res
        except Exception as error:
            self.logger.error(error)


class XMLDictTool():

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.debug("create XMLDictTool")

    def dict_to_xml(self, src_dict: dict):
        try:
            self.logger.debug("convert dict to xml start: %s" % src_dict)
            res = dicttoxml.convert_dict(src_dict, None, None, False)
            self.logger.debug(
                "convert dict to xml success: %s" % res)
            return res
        except Exception as error:
            self.logger.error(error)

    def xml_to_dict(self, src_xml: str):
        try:
            self.logger.debug("convert xml to dict start: %s" % src_xml)
            res = xmltodict.parse(src_xml)
            self.logger.debug("convert xml to dict success: %s" % res)
            return res
        except Exception as error:
            self.logger.error(error)


class GzipperTool():

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.debug("create Gzipper")

    def unzip(self, src_data: str):
        try:
            self.logger.debug("unzip start: %s" % src_data)
            res = gzip.decompress(src_data)
            self.logger.debug("unzip success: %s" % res)
            return res
        except Exception as error:
            self.logger.error(error)

    def zip(self, src_data: str, encoding="utf-8", zip_level: int=9):
        try:
            self.logger.debug("zip start: %s" % src_data)
            src = src_data.encode(encoding)
            res = gzip.compress(src, zip_level)
            self.logger.debug("zip success: %s" % res)
            return res
        except Exception as error:
            self.logger.error(error)


class CompareTool():

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.debug("create CompareTool")

    def compare_two_number(self, first_num, second_num):
        res = False
        try:
            self.logger.info("start compare: %s, %s" % (first_num, second_num))
            if first_num == second_num:
                res = True
            else:
                res = False
            self.logger.info("compare success: equal? %s" % res)
        except Exception as error:
            self.logger.error(error)
        finally:
            return res

    def compare_list_number(self, list_num):
        res = True
        try:
            self.logger.info("start compare: %s" % list_num)
            for item in list_num:
                if item == list_num[0]:
                    pass
                else:
                    res = False
                    break
            self.logger.info("compare success: equal? %s" % res)
        except Exception as error:
            self.logger.error(error)
        finally:
            return res
