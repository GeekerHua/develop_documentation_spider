# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:15
# @Author  : Hua
# @Site    : 
# @File    : mainSpider.py
# @Software: PyCharm
# from BaseClient import BaseClient
from common.Util import loadInspectorConfig, ReflectTool
from client.SphinxClient import SphinxClient
from client.SiteClient import SiteClient
from client.RdClient import RdClient

if __name__ == '__main__':

    requestsConfig = loadInspectorConfig('config/vender/requests.yaml')
    requestsClicent = ReflectTool.dynamicNewObj(requestsConfig.client, requestsConfig)
    requestsClicent.crawlTheSite()
