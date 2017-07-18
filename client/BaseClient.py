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

    DOWNLOAD_DIR = 'downloads'
    OUTPUT_DIR = 'output'
    def __init__(self, config):
        """

        :type config: Config
        """
        self.config = config
        self.url = config.documentUrl if not config.documentUrl.endswith('/') else config.documentUrl[:-1]
        self.originDir = self.url.split('//')[-1].split('/')[0]  # 获取域名对应的文件夹名
        self.docsetDir = config.name + '.docset'
        self.resourcesPath = os.path.join(self.OUTPUT_DIR, self.docsetDir, 'Contents', 'Resources')
        self.infoPath = os.path.join(self.OUTPUT_DIR, self.docsetDir, 'Contents', 'Info.plist')
        self.documentsPath = os.path.join(self.resourcesPath, 'Documents')

    def crawlTheSite(self):

        nativePath = self.downloadSite()

        self.copySiteToDocsets(nativePath, self.resourcesPath)

        self.changeSomeText()

        self.generateInfoPlist()

        self.generateDB()

        self.setupIcon()

    def generateInfoPlist(self):
        # 根据模板生成 Info.list
        print '4. generate info.plist'
        template = self.ENV.get_template('info.plist')
        infoTxt = template.render({'bundleIdentifier': self.config.name, 'homePage': self.config.homePage or self.config.indexPage})
        with open(self.infoPath, 'w') as f:
            f.write(infoTxt)
            print '4.1. already write info.plist success'

    def generateDB(self):
        dbFilePath = os.path.join(self.resourcesPath, 'docSet.dsidx')
        print '5. generate db path: {path}'.format(path=dbFilePath)

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
            path = self._changeRelativePath(self.documentsPath, fullPath, path)
            cur.execute('REPLACE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (name.decode('utf8'), typeName, path.decode('utf8')))
        if result:
            print 'write %d index item type = %s into DB' % (len(result), typeName)

    def downloadSite(self):
        """
        下载整站
        """
        print '1. start download site from {url} ……'.format(url=self.url)
        newNativePath = os.path.join(self.DOWNLOAD_DIR, self.config.name)  # 本地保存的路径
        if os.path.exists(newNativePath):
            print '1.1. alrady have this path: {path}, skip this step'.format(path=newNativePath)
            return newNativePath

        # 创建downloads文件夹
        if not os.path.exists(self.DOWNLOAD_DIR):
            os.mkdir(self.DOWNLOAD_DIR)

        os.system('cd {download_dir} && wget -r -p -np -q -k {url}'.format(download_dir=self.DOWNLOAD_DIR, url=self.config.documentUrl))
        print '1.1. download: {path} success'.format(path = newNativePath)

        # 重命名
        oldNativePath = os.path.join(self.DOWNLOAD_DIR, self.originDir)

        os.rename(oldNativePath, newNativePath)
        print '1.2. rename folder: {oldName} --> {newName} success'.format(oldName=oldNativePath, newName=newNativePath)
        return newNativePath

    def copySiteToDocsets(self, nativePath, resourcePath):
        """
        将网站内容放到指定docset路径下

        :return:
        """
        print '2. copy site to docsets ……'
        docsetPath = os.path.join(self.OUTPUT_DIR, self.docsetDir)
        if os.path.exists(docsetPath):
            print '2.1. already have this path: {path}, remove this path and then copy it'.format(path=docsetPath)
            shutil.rmtree(docsetPath)

        # 创建本地 docset 的文件夹
        os.makedirs(resourcePath)
        # 判断是否有原始文件夹
        if os.path.exists(resourcePath):
            # 复制整站到指定的文件夹
            shutil.copytree(nativePath, self.documentsPath)
            print '2.2 copy folder: {oldPath} --> {newPath} success'.format(oldPath=nativePath, newPath=self.documentsPath)

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
        print '3. change some text from html'
        pass

    def setupIcon(self):
        print '6. setup icon'
        pass
