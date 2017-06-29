# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:15
# @Author  : Hua
# @Site    : 
# @File    : mainSpider.py
# @Software: PyCharm

from client.BaseClient import BaseClient

if __name__ == '__main__':
    jinjia2Clicent = BaseClient('jinja2', 'http://docs.jinkan.org/docs/jinja2/')
    jinjia2Clicent.crawlTheSite()
