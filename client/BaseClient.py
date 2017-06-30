# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:17
# @Author  : Hua
# @Site    : 
# @File    : baseClient.py
# @Software: PyCharm

import shutil
from jinja2 import Environment, PackageLoader
import os, re, sqlite3
from bs4 import BeautifulSoup
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
        self.docName = config.name
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
        infoTxt = template.render({'bundleIdentifier': self.docName, 'homeIndex': self.config.homeIndex})
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

        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if fileName.endswith(".html"):
                    page = open(os.path.join(root, fileName)).read()

                    if fileName == self.config.homeIndex:
                        # Guides
                        guidesPattern = re.compile(
                            r'<a class="reference internal" href="([^#]*?)">{0,1}[^>]*?>(.*?)<[^<]*?<{0,1}/a>')
                        self.writeItemToDB(cur, page, guidesPattern, 'Guides', fileName)

                        # category
                        categoryPattern = re.compile(
                            r'<a class="reference internal" href="(.*?#.*?)">{0,1}[^>]*?>(.*?)<[^<]*?<{0,1}/a>')
                        self.writeItemToDB(cur, page, categoryPattern, 'Category', fileName)

                    classPattern = re.compile(r'class="class">\n.*?id="(.*?)">', re.M)
                    self.writeItemToDB(cur, page, classPattern, 'Class', fileName)

                    methodPattern = re.compile(r'class="method">\n.*?id="(.*?)">', re.M)
                    self.writeItemToDB(cur, page, methodPattern, 'Methods', fileName)

                    attributePattern = re.compile(r'class="attribute">\n.*?id="(.*?)">', re.M)
                    self.writeItemToDB(cur, page, attributePattern, 'Attribute', fileName)

                    functionPattern = re.compile(r'class="function">\n.*?id="(.*?)">', re.M)
                    self.writeItemToDB(cur, page, functionPattern, 'Function', fileName)

        db.commit()
        db.close()

    def writeItemToDB(self, cur, page, pattern, typeName, fileName):
        result = pattern.findall(page)
        for item in result:
            if isinstance(item, tuple):
                if item[1].startswith('Version'):
                    break

                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (item[1].decode('utf-8'), typeName, item[0].decode('utf-8')))
                # print 'type: %s, name: %s, path: %s' % (typeName, item[1], item[0])
            elif isinstance(item, basestring):
                path = '#'.join([fileName, item])
                cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                            (item.decode('utf-8'), typeName, path.decode('utf-8')))
                # print 'type: %s, name: %s, path: %s' % (typeName, item[1], item[0])
        print 'write %d index item type = %s into DB' % (len(result), typeName)

    def downloadSite(self):
        # 创建本地文件夹 docset 的文件夹

        if os.path.exists(self.resourcesPath):
            print '已有这个文件夹name = {name}'.format(name=self.docPath)
        else:
            os.makedirs(self.resourcesPath)
            # 下载整站
            os.system('cd output && wget -r -p -np -k %s' % self.url)

            # 移动整站到指定的文件夹
            if self.url.startswith('http://'):
                scheme = 'http://'
            elif self.url.startswith('https://'):
                scheme = 'https://'
            else:
                scheme = None
            if scheme:
                shutil.move(os.path.join(self.outputPath, self.url.split(scheme)[1]), self.resourcesPath)
                shutil.rmtree(os.path.join(self.outputPath, '/'.join(self.url.split(scheme)[1].split('/')[0:1])))
            else:
                shutil.move(os.path.join(self.outputPath, self.url.split(scheme)), self.resourcesPath)
            # 删除刚才的下载的临时文件夹
                shutil.rmtree(os.path.join(self.outputPath, '/'.join(self.url.split(scheme).split('/')[0:1])))

            os.rename(os.path.join(self.resourcesPath, self.url.split('/')[-1]), self.documentsPath)


    def removeUselessText(self):

        for root, dirs, files in os.walk(self.documentsPath):
            for file in files:
                if file.endswith(".html"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        content = f.read().replace("bodywrapper", "")
                        soup = BeautifulSoup(content)
                        comments = soup.find_all('div', {'class': 'sphinxsidebar'})
                        [comment.extract() for comment in comments]
                    with open(path, "w") as f:
                        result = re.sub(r'^(.*?)<html', '<html', "".join([str(item) for item in soup.contents]))
                        f.write(result)

    def setupIcon(self):
        pass
