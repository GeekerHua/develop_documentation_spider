# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 17:46
# @Author  : Hua
# @Site    : 
# @File    : SiteClient.py
# @Software: PyCharm
import os
import shutil

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

    def writeDB(self, cur, db):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if os.path.join(root, fileName) == os.path.join(self.documentsPath, self.config.homeIndex):
                    for config in self.config.homePageConfigList:
                        if config.regular:
                            self.writeItemToDB(cur, root, fileName, config.regular, config.typeName)

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
