# coding=utf-8
'''
Created on Mar 31, 2016

@author: yangjie
'''
import http.cookiejar
import json
import logging
import socket
import urllib.request


class HTTPOpener():

    def __init__(self, logger: logging.Logger, enable_cookie: bool=False):
        self.logger = logger
        self.logger.info(
            "create HTTPTool:\n\tenable cookie: %s" % enable_cookie)
        self.opener = self._get_opener(enable_cookie)

    def _get_opener(self, enable_cookie):
        if enable_cookie:
            cookie_jar = http.cookiejar.CookieJar()
            pro = urllib.request.HTTPCookieProcessor(cookie_jar)
            opener = urllib.request.build_opener(pro)
        else:
            opener = urllib.request.build_opener()
        return opener

    def request_url(self, url_str, data_raw=None, encoding="utf-8", method="GET", timeout=5, json_type: bool=False):
        try:
            socket.setdefaulttimeout(timeout)
            if data_raw is None:
                self.logger.info(
                    "start http request:\n\tMethod: %s\n\tEndocing:%s\n\tData: None\n\tTimeout: %d" % (method, encoding, timeout))
                data_send = data_raw
            elif isinstance(data_raw, str):
                self.logger.info(
                    "start http request:\n\tMethod: %s\n\tEndocing:%s\n\tData: String\n\tTimeout: %d" % (method, encoding, timeout))
                data_send = data_raw.encode(encoding)
            elif isinstance(data_raw, dict):
                self.logger.info(
                    "start http request:\n\tMethod: %s\n\tEndocing:%s\n\tData: Dict\n\tUse json:%s \n\tTimeout: %d" % (method, encoding, json_type, timeout))
                if json_type:
                    data_send = json.dumps(data_raw).encode(encoding)
                else:
                    data_send = urllib.parse.urlencode(
                        data_raw).encode(encoding)
            else:
                self.logger.error("http request error: unknown type of data")
                return
            req = urllib.request.Request(
                url_str, data=data_send, method=method)
            print(data_send)
            op = self.opener.open(req, timeout=timeout)
            self.logger.info("http request success: %d" % op.code)
            return op
        except Exception as error:
            self.logger.error(error)
