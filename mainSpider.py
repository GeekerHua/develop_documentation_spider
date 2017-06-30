# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:15
# @Author  : Hua
# @Site    : 
# @File    : mainSpider.py
# @Software: PyCharm

from common.Util import loadInspectorConfig
from client.SphinxClient import SphinxClient

if __name__ == '__main__':

    for configName in ['config/vender/jinja2.yaml', 'config/vender/requests.yaml']:
        configData = loadInspectorConfig(configName)
        client = SphinxClient(configData)
        client.crawlTheSite()


    requestsConfig = loadInspectorConfig('config/vender/jinja2.yaml')
    requestsClicent = SphinxClient(requestsConfig)
    requestsClicent.crawlTheSite()
