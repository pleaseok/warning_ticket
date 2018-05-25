#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time


class BigWarning:
    def __init__(self):
        self.url = 'http://106.14.133.21:9095/robo/admin/portal/login.jsp'
        self.session = requests.session()

    def get_warning(self):
        """
        :return: [{'id': 'Z1000H4BJ0329', 'address': '长沙一号机', 'ticket': '7', 'ticket_tao': '1排3道', 'number': '0'},]
        """
        j_username = '' # 用户名
        j_password = '' # 密码
        remember = 'on'
        saveflag = '1'

        post_data = "j_username=" + j_username + "&j_password=" + j_password + "&remember" + remember \
                    + "&saveflag=" + saveflag
        headers = self.post_login()
        # headers.setdefault("Cookie", str(self.get_cookie(True)))
        # 登陆
        self.session.post(url=self.url, data=post_data, headers=headers, allow_redirects=False)
        # 保存新的cookies
        r = self.session.get(url='http://106.14.133.21:9095/robo/admin/portal/main.jsp',
                             headers=self.get_login())
        pc_hash = int(round(time.time() * 1000))
        # --------------------------------
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/66.0.3359.139 Safari/537.36',
                  'Referer': 'http://106.14.133.21:9095/robo/admin/machine_status/CurrGoodsWay_List.jsp?'
                             'menuid=6102&stamp=0.7493471796448679&pc_hash=%s' % pc_hash}
        pos_data = {
            'param_sell_machine_id': '',
            'param_shop_id': '',
            'param_shop_name': '',
            'param_goods_name': '',
            'param_row_no': '',
            'param_col_no_merge': '',
            'param_machine_name': '长沙',
            'orderbyitem': '5',
            'orderbytype': '0'
        }
        result = self.session.post(url='http://106.14.133.21:9095/robo/admin/machine_status/CurrGoodsWay_List.jsp',
                                   data=pos_data, headers=header, allow_redirects=False)
        soup = BeautifulSoup(result.text, 'lxml')
        tbody = soup.findAll("tbody")
        rows = tbody[1].findAll("tr")
        data = []
        for row in rows:
            cols = row.findAll("td")
            da = {}
            da.setdefault("id", cols[2].text)
            da.setdefault("address", cols[3].text)
            da.setdefault("ticket", cols[4].text)
            da.setdefault("ticket_tao", cols[5].text)
            da.setdefault("number", cols[6].text)
            data.append(da)
        return data

    def get_filter_value(self):
        """
        得到过滤后的值,
        过滤规则：
            number小于等于20
            address不等于长沙一号机、长沙办公室测试机
        *python循环删除list，必须把它赋新值才能生效
        :return: list
        """
        res = self.get_warning()
        value = res[:]
        for re in res:
            if re['address'] == '长沙一号机' or re['address'] == '长沙办公室测试机':
                value.remove(re)
            elif int(re['number']) > 20:
                value.remove(re)
        return value

    @staticmethod
    def get_login():
        """
        GET http://106.14.133.21:9095/robo/admin/portal/login.jsp HTTP/1.1
        :return: list
        """
        header = {
            'Host': '106.14.133.21:9095',
            'Proxy-Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        return header

    @staticmethod
    def post_login():
        """
        POST http://106.14.133.21:9095/robo/admin/portal/login.jsp HTTP/1.1
        :return:list
        """
        header = {
            'Host': '106.14.133.21:9095',
            'Proxy-Connection': 'keep-alive',
            'Content-Length': '55',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://106.14.133.21:9095',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/66.0.3359.139 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://106.14.133.21:9095/robo/admin/portal/login.jsp',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        return header


# if __name__ == '__main__':
#     login = BigWarning()
#     print(login.get_filter_value())
