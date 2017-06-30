# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:17
# @Author  : Hua
# @Site    : 
# @File    : baseClient.py
# @Software: PyCharm

from jinja2 import Environment, PackageLoader
import os, sqlite3
from config.Config import Config


class BaseClient(object):
    ENV = Environment(loader=PackageLoader('templates', ''), trim_blocks=True,
                      keep_trailing_newline=True, lstrip_blocks=True)

    def __init__(self, config):
        """

        :type config: Config
        """
        self.config = config
        self.url = config.documentUrl if not config.documentUrl.endswith('/') else config.documentUrl[:-1]
        self.docPath = config.name + '.docset'
        self.outputPath = './output/'
        self.resourcesPath = os.path.join(self.outputPath, self.docPath, 'Contents', 'Resources')
        self.infoPath = os.path.join(self.outputPath, self.docPath, 'Contents', 'Info.plist')
        self.documentsPath = os.path.join(self.resourcesPath, 'Documents')

    def crawlTheSite(self):

        self.downloadSite()

        self.removeUselessText()

        self.generateInfoPlist()

        self.generateDB()

        self.setupIcon()

    def generateInfoPlist(self):

        # 根据模板生成 Info.list
        template = self.ENV.get_template('Sphinx.plist')
        infoTxt = template.render({'bundleIdentifier': self.config.name, 'homeIndex': self.config.homeIndex})
        with open(self.infoPath, 'w') as f:
            f.write(infoTxt)
            print 'already write info.plist'

    def generateDB(self):
        pass

    def writeItemToDB(self, cur, page, pattern, typeName, fileName):
        result = pattern.findall(page)
        for item in result:
            if isinstance(item, tuple):
                if item[1].startswith('Version'):
                    break
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (item[1].decode('utf-8'), typeName, item[0].decode('utf-8')))
            elif isinstance(item, basestring):
                path = '#'.join([fileName, item])
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (item.decode('utf-8'), typeName, path.decode('utf-8')))
        if result:
            print 'write %d index item type = %s into DB' % (len(result), typeName)

    def downloadSite(self):
        if os.path.exists(self.resourcesPath):
            print '已有这个文件夹name = {name}'.format(name=self.docPath)
        else:
            # 创建本地 docset 的文件夹
            os.makedirs(self.resourcesPath)

    def removeUselessText(self):
        pass

    def setupIcon(self):
        pass
