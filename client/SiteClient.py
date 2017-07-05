# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 17:46
# @Author  : Hua
# @Site    : 
# @File    : SiteClient.py
# @Software: PyCharm
import os
import shutil
import sqlite3

from BaseClient import BaseClient


class SiteClient(BaseClient):
    def downloadSite(self):
        if os.path.exists(self.resourcesPath):
            print '已有这个文件夹name = {name}'.format(name=self.docPath)
        else:
            # 创建本地 docset 的文件夹
            os.makedirs(self.resourcesPath)
            # 下载整站
            os.system('cd output && wget -r -p -np -k %s' % self.url)

            # 移动整站到指定的文件夹
            shutil.move(os.path.join(self.outputPath, self.url.split('//')[-1].split('/')[0]), self.resourcesPath)

            os.rename(os.path.join(self.resourcesPath, self.url.split('//')[-1].split('/')[0]), self.documentsPath)

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
                if fileName == self.config.homeIndex.split('/')[-1]:
                    page = open(os.path.join(root, fileName)).read()
                    for config in self.config.homePageConfigList:
                        self.writeItemToDB(cur, page, config.regular, config.typeName, fileName)

        db.commit()
        db.close()

    def changeSomeText(self):

        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if fileName == self.config.homeIndex.split('/')[-1].split('.')[0]:
                    path = os.path.join(root, fileName)
                    with open(path, "r") as f:
                        content = f.read().replace("api#", self.config.homeIndex + "#")
                    with open(path + '.html', "w") as f:
                        f.write(content)
