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

        self.downloadSite()

        self.changeSomeText()

        self.generateInfoPlist()

        self.generateDB()

        self.setupIcon()

    def generateInfoPlist(self):
        # 根据模板生成 Info.list
        template = self.ENV.get_template('Sphinx.plist')
        infoTxt = template.render({'bundleIdentifier': self.config.name, 'homePage': self.config.homePage or self.config.indexPage})
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
                fullPath = os.path.join(root, fileName)
                if fileName.endswith(".html"):
                    if self.config.indexPage and fullPath == os.path.join(self.documentsPath, self.config.indexPage):
                        configList = self.config.indexPageConfigList
                    elif self.config.homePage and fullPath == os.path.join(self.documentsPath, self.config.homePage):
                        configList = self.config.homePageConfigList
                    else:
                        configList = self.config.otherPageConfigList
                    for config in configList:
                        if config.regular:
                            self.writeItemToDB(cur, fullPath, config.regular, config.typeName)

        db.commit()
        db.close()

    def writeItemToDB(self, cur, fullPath, regex, typeName):
        """
        搜索匹配索引，并写入数据库
        :param cur: 数据库句柄
        :param fullPath: 当前完整的文件路径
        :param regex: 正则对象
        :param typeName: 索引类型
        """
        page = open(fullPath).read()
        result = regex.findall(page)
        for item in result:
            if isinstance(item, tuple):  # 通常是目录
                name = item[1]
                if name.startswith('Version'):
                    break
                path = item[0]
            elif isinstance(item, basestring): # 通常是页内链接
                name = item
                path = '#'.join([fullPath[len(self.documentsPath):], item])
            if not name:
                continue

            # if self.config.indexPage and fullPath == os.path.join(self.documentsPath, self.config.indexPage):
            #     tmpPath = self.config.indexPage
            # elif self.config.homePage and fullPath == os.path.join(self.documentsPath, self.config.homePage):
            #     tmpPath = self.config.homePage
            # else:
            #     tmpPath = ''
            path = self._changeRelativePath(self.documentsPath, fullPath, path)
            # if path.startswith('../'):
            #     if len(tmpPath.split('/')) >= 2:
            #         path = path.replace('..', '/'.join(tmpPath.split('/')[:-2]))
            # elif not path.startswith('doc'):
            #     baseDir = '' #'doc/Django-1.10.5'
            #     # path 需要时从Documents开始的绝对路径，而不能是相对路径
            #     path = os.path.join(baseDir, path)
            cur.execute('REPLACE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (name.decode('utf8'), typeName, path.decode('utf8')))
        if result:
            print 'write %d index item type = %s into DB' % (len(result), typeName)

    def downloadSite(self):
        """
        下载整站
        """
        if os.path.exists(self.resourcesPath):
            # print '已有这个文件夹name = {name}'.format(name=self.docPath)
            shutil.rmtree(self.resourcesPath)

        # 创建本地 docset 的文件夹
        os.makedirs(self.resourcesPath)
        # 下载整站
        os.system('cd output && wget -r -p -np -k %s' % self.url)

        # 复制整站到指定的文件夹
        originDirPath = self.url.split('//')[-1].split('/')[0]
        shutil.move(os.path.join(self.outputPath, originDirPath), self.resourcesPath)

        os.rename(os.path.join(self.resourcesPath, originDirPath), self.documentsPath)

    def _changeRelativePath(self, baseRootPath, basePath, relativePath):
        """
        修改相对路径
        :param baseRootPath: 最终要基于的根路径
        :param basePath: 当前所在的路径
        :param relativePath: 相对于当前路径的目标路径
        :rtype: str
        """
        count = relativePath.count('../')
        tmpPath = '/'.join(basePath.split('/')[:-(count + 1)])
        p = os.path.join(tmpPath, '/'.join(relativePath.split('/')[count:]))
        return p.replace(baseRootPath, '')

    def changeSomeText(self):
        pass

    def setupIcon(self):
        pass
