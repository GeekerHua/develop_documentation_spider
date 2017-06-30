# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:15
# @Author  : Hua
# @Site    : 
# @File    : mainSpider.py
# @Software: PyCharm

from client.BaseClient import BaseClient
from common.Util import loadInspectorConfig


if __name__ == '__main__':

    for configName in ['config/jinja2.yaml', 'config/requests.yaml']:
        configData = loadInspectorConfig(configName)
        client = BaseClient(configData)
        client.crawlTheSite()


    # requestsConfig = loadInspectorConfig('config/bs4.yaml')
    # requestsClicent = BaseClient(requestsConfig)
    # requestsClicent.crawlTheSite()
