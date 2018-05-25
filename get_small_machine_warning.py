#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import time


class SmallWarning:
    def __init__(self):
        self.session = requests.session()
        self.cookie = self.get_cookie()
        self._loginUrl = r"http://www.kadawo.com/fulei/index.php/common/login/company/"
        self._url = r"http://www.kadawo.com/fulei/index.php/common/doLogin/company/"
        self.search = r"http://www.kadawo.com/fulei/index.php/equipment/shjList"
        self.warning_url = r"http://www.kadawo.com/fulei/index.php/equipment/shjList/goodsStockSort/stock%20asc/dealerId" \
                           r"/485/__hash__/"

    def get_filter_value(self):
        """
        得到过滤后的值,
        过滤规则：
            number小于等于10
        *python循环删除list，必须把它赋新值才能生效
        :return: list
        """
        res = self.get_warning()
        value = res[:]
        for re in res:
            if int(re['number']) > 10:
                value.remove(re)
        return value


    def get_warning_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        tbody = soup.find("tbody")
        rows = tbody.findAll('tr')
        data = []
        for row in rows:
            cols = row.findAll('td')
            if len(cols) > 15:
                da = {}
                da.setdefault("id", cols[2].text.strip())  # id
                da.setdefault("address",
                              cols[3].span.attrs['title'] if not cols[3].span.attrs['title'] == '' else '')  # 设备名称
                da.setdefault("name", self.get_lottery_name(cols[1].text.strip()))  # 当前票种
                da.setdefault("number", cols[11].text.strip())  # 库存
                data.append(da)
        return data

    def get_warning(self):
        # 得到登陆界面的校验值
        username = '' # 用户名
        password = '' # 密码
        header = self.get_login()
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.cookie)
        response = self.session.get(url=self._loginUrl, headers=header)
        dologin_hash = self.get_hash(response.text)

        # 开始登陆
        postData = "userName=" + username + "&password=" + password + "&verify=" + "&__hash__=" + dologin_hash
        dologin_h = self.post_login()
        dologin_h.setdefault('Cookie', 'PHPSESSID=%s' % self.cookie)
        self.session.post(self._url, data=postData, headers=dologin_h)

        # 得到搜索的校验值
        search_h = self.get_search()
        search_h.setdefault('Cookie', 'PHPSESSID=%s' % self.cookie)
        search = self.session.get(url=self.search, headers=search_h)
        search_hash = self.get_hash(search.text)
        search_url = self.warning_url + search_hash
        result = self.session.get(url=search_url, headers=search_h)
        data = self.get_warning_html(result.text)
        return data

    def get_cookie(self):
        r = self.session.get(url="http://www.kadawo.com/",
                             headers={
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                               'Chrome/66.0.3359.117 Safari/537.36'})
        phpsessid = r.cookies['PHPSESSID']
        return phpsessid

    @staticmethod
    def get_hash(htm):
        """
        :param: html文本信息
        :return: str字符串
        """
        hash_pattern = re.compile(r'<input type="hidden" name="__hash__" value="(.*?)"')
        _hash = re.findall(hash_pattern, htm)[0]
        return _hash

    @staticmethod
    def get_login():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'pgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        return header

    @staticmethod
    def get_search():
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'pgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/index/amTable'
                  }
        return header

    @staticmethod
    def post_login():
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
        return header

    # 得到当天0点的时间戳
    @staticmethod
    def getStartTimeOfToday():
        t = time.localtime(time.time())
        return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S')))

    # 得到当天23点59的时间戳
    @staticmethod
    def getEndTimeOfToday():
        t = time.localtime(time.time())
        return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 23:59:59', t), '%Y-%m-%d %H:%M:%S')))

    def get_lottery_name(self, id):
        """
        得到彩票机里存放的彩票种类名
        :return: str字符串
        """
        header = {'Host': 'www.kadawo.com',
                  'Proxy-Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/66.0.3359.117 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'Referer': 'http://www.kadawo.com/fulei/index.php/index/amTable',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9'
                  }
        header.setdefault('Cookie', 'PHPSESSID=%s' % self.cookie)
        url = r"http://www.kadawo.com/fulei/index.php/equipment/eType1/id/"+id+"/"
        htm = self.session.get(url=url, headers=header,
                                allow_redirects=False)

        soup = BeautifulSoup(htm.text, "lxml")
        return soup.tbody.tr.findAll('td')[5].text


if __name__ == "__main__":
    small = SmallWarning()
    print(small.get_warning())
