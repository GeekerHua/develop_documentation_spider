# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:24
# @Author  : Hua
# @Site    : 
# @File    : sphinxClient.py
# @Software: PyCharm
import os
import shutil
import sqlite3
import re
from bs4 import BeautifulSoup

from BaseClient import BaseClient


class SphinxClient(BaseClient):
    def __init__(self, config):
        """

        :type config: Config
        """
        super(SphinxClient, self).__init__(config)
        # self.resourcesPath = os.path.join(self.outputPath, self.docPath, 'Contents', 'Resources')
        # self.infoPath = os.path.join(self.outputPath, self.docPath, 'Contents', 'Info.plist')
        # self.documentsPath = os.path.join(self.resourcesPath, 'Documents')

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
                        for config in self.config.homePageConfigList:
                            self.writeItemToDB(cur, page, config.regular, config.typeName, fileName)
                    else:
                        for config in self.config.otherPageConfigList:
                            self.writeItemToDB(cur, page, config.regular, config.typeName, fileName)

        db.commit()
        db.close()

    def downloadSite(self):
        super(SphinxClient, self).downloadSite()

        # 下载整站
        os.system('cd output && wget -r -p -np -k %s' % self.url)

        scheme = 'http://'
        self.url.replace('https://', scheme)
        if self.url.startswith(scheme):
            # 移动整站到指定的文件夹
            shutil.move(os.path.join(self.outputPath, self.url.split(scheme)[1]), self.resourcesPath)
            # 删除刚才的下载的临时文件夹
            shutil.rmtree(os.path.join(self.outputPath, '/'.join(self.url.split(scheme)[1].split('/')[0:1])))
        else:
            shutil.move(os.path.join(self.outputPath, self.url), self.resourcesPath)
            shutil.rmtree(os.path.join(self.outputPath, '/'.join(self.url.split('/')[0:1])))

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
