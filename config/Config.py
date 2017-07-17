# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 16:26
# @Author  : Hua
# @Site    : 
# @File    : Config.py
# @Software: PyCharm
import os
import re
from common.Constants import Sign
# from common.Util import loadInspectorConfig
import common.Util
class Config(object):

    class PageConfig(object):
        def __init__(self):
            self.typeName = None
            self.regex = None
            self.regexPattern = None
            self.keyList = []

        @property
        def regular(self):
            if self.regex:
                return re.compile(self.regex, 0 if self.regexPattern == None else eval(self.regexPattern))
            else:
                return None

    class HomePageConfig(PageConfig):
        pass

    class indexPageConfig(PageConfig):
        pass

    class OtherPageConfig(PageConfig):
        pass

    def __init__(self):
        self._homePage = None
        self._indexPage = None
        self._theme = None
        self.name = None
        self.documentUrl = None
        self.client = 'client.BaseClient'

        self.homePageConfigList = [Config.HomePageConfig()]
        self.indexPageConfigList = [Config.indexPageConfig()]
        self.otherPageConfigList = [Config.OtherPageConfig()]


    @property
    def indexPage(self):
        return os.path.join('/'.join(self.documentUrl.split('//')[1].split('/')[1:]), self._indexPage) if self._indexPage else None

    @indexPage.setter
    def indexPage(self, value):
        self._indexPage = value

    @property
    def homePage(self):
        if self._homePage:
            return self._homePage
        else:
            return os.path.join('/'.join(self.documentUrl.split('//')[1].split('/')[1:]), self._homePage or 'index.html')

    @homePage.setter
    def homePage(self, value):
        self._homePage = value

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        self._theme = value
        if value:
            newValue = value.replace(Sign.DOT, Sign.SEP)
            config = common.Util.loadInspectorConfig(newValue + '.yaml')
            self.homePageConfigList = config.homePageConfigList
            self.otherPageConfigList = config.otherPageConfigList
            self.indexPageConfigList = config.indexPageConfigList

