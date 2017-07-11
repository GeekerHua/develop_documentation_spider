# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:17
# @Author  : Hua
# @Site    : 
# @File    : baseClient.py
# @Software: PyCharm
import shutil

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

        # self.downloadSite()

        self.changeSomeText()

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
        dbFilePath = os.path.join(self.resourcesPath, 'docSet.dsidx')
        db = sqlite3.connect(dbFilePath)
        cur = db.cursor()

        try:
            cur.execute('DROP TABLE searchIndex;')
        except:
            pass

        cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
        cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')
        self.writeDB(cur, db)

    def writeDB(self, cur, db):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if fileName.endswith(".html"):
                    page = open(os.path.join(root, fileName)).read()
                    if fileName == self.config.homeIndex:
                        for config in self.config.homePageConfigList:
                            if config.regular:
                                self.writeItemToDB(cur, page, config.regular, config.typeName, fileName)
                    else:
                        for config in self.config.otherPageConfigList:
                            if config.regular:
                                self.writeItemToDB(cur, page, config.regular, config.typeName, fileName)

        db.commit()
        db.close()

    def writeItemToDB(self, cur, root, fileName, pattern, typeName):
        fullPath = os.path.join(root, fileName)
        page = open(fullPath).read()
        result = pattern.findall(page)
        for item in result:
            if isinstance(item, tuple):
                name = item[1]
                if name.startswith('Version'):
                    break
                path = item[0].decode('utf-8')
            elif isinstance(item, basestring):
                name = item
                path = '#'.join([fullPath[len(self.documentsPath):], item]).decode('utf-8')
            if path.startswith('../'):
                if self.config.indexPage and fullPath == os.path.join(self.documentsPath, self.config.indexPage):
                    tmpPath = self.config.indexPage
                elif self.config.homeIndex and fullPath == os.path.join(self.documentsPath, self.config.homeIndex):
                    tmpPath = self.config.homeIndex
                else:
                    tmpPath = ''
                if len(tmpPath.split('/')) >= 2:
                    path = path.replace('..', '/'.join(tmpPath.split('/')[:-2]))
            cur.execute('REPLACE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (name.decode('utf-8'), typeName, path))
        if result:
            print 'write %d index item type = %s into DB' % (len(result), typeName)

    def downloadSite(self):
        if os.path.exists(self.resourcesPath):
            print '已有这个文件夹name = {name}'.format(name=self.docPath)
        else:
            # 创建本地 docset 的文件夹
            os.makedirs(self.resourcesPath)
            # 下载整站
            os.system('cd output && wget -r -p -np -k %s' % self.url)

            # 移动整站到指定的文件夹
            shutil.move(os.path.join(self.outputPath, self.url.split('//')[-1]), self.resourcesPath)
            # 删除刚才的下载的临时文件夹
            shutil.rmtree(os.path.join(self.outputPath, self.url.split('//')[-1].split('/')[0]))

            os.rename(os.path.join(self.resourcesPath, self.url.split('/')[-1]), self.documentsPath)

    def changeSomeText(self):
        pass

    def setupIcon(self):
        pass
