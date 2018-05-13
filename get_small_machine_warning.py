#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re


class SmallWarning:
    def __init__(self):
        self.session = requests.session()
        self._loginUrl = r"http://www.kadawo.com/fulei/index.php/common/login/company/"
        self._url = r"http://www.kadawo.com/fulei/index.php/common/doLogin/company/"

    def doLogin(self):
        username = 'fulei'
        password = 'bdxl88888*'
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'pgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        cookie = self.getCookie()
        header.setdefault('Cookie', 'PHPSESSID=%s' % cookie)
        response = self.session.get(url=self._loginUrl, headers=header)
        _hash = self.getHash(response.text)

        postData = "userName=" + username + "&password=" + password + "&verify=" + "&__hash__=" + _hash
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Content-Length': '84',
                  'Cache-Control': 'max-age=0',
                  'Origin': 'http://www.kadawo.com',
                  'Upgrade-Insecure-Requests': '1',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/common/login/company/',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        header.setdefault('Cookie', 'PHPSESSID=%s' % cookie)
        result = self.session.post(self._url, data=postData, headers=header)
        print(result.text)

    def getCookie(self):
        r = self.session.get(url="http://www.kadawo.com/",
                             headers={
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                               'Chrome/66.0.3359.117 Safari/537.36'})
        phpsessid = r.cookies['PHPSESSID']
        return phpsessid

    def getHash(self, htm):
        """
        :param: html文本信息
        :return: str字符串
        """
        hash_pattern = re.compile(r'<input type="hidden" name="__hash__" value="(.*?)"')
        _hash = re.findall(hash_pattern, htm)[0]
        return _hash


if __name__ == "__main__":
    small = SmallWarning()
    small.doLogin()
