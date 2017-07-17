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
    # path = 'config/vender/requests.yaml'
    # path = 'config/vender/jinja2.yaml'
    # path = 'config/vender/bs4.yaml'
    # path = 'config/vender/py3.yaml'
    # path = 'config/vender/vue.yaml'
    # path = 'config/vender/django.yaml'
    # path = 'config/vender/tornado.yaml'
    path = 'config/vender/scrapy.yaml'
    requestsConfig = loadInspectorConfig(path)
    requestsClicent = ReflectTool.dynamicNewObj(requestsConfig.client, requestsConfig)
    requestsClicent.crawlTheSite()
