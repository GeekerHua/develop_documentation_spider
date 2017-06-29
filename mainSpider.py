# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:15
# @Author  : Hua
# @Site    : 
# @File    : mainSpider.py
# @Software: PyCharm

from client.BaseClient import BaseClient
from config.Config import Config
from common.Util import loadInspectorConfig


if __name__ == '__main__':
    jinja2Config = loadInspectorConfig('config/jinja2.yaml')
    jinjia2Clicent = BaseClient(jinja2Config)
    jinjia2Clicent.crawlTheSite()


    # requestsConfig = loadInspectorConfig('config/requests.yaml')
    # requestsClicent = BaseClient(requestsConfig)
    # requestsClicent.crawlTheSite()
