# -*- coding: utf-8 -*-
# @Time    : 2017/7/7 16:11
# @Author  : Hua
# @Site    : 
# @File    : pyClient.py
# @Software: PyCharm
import os

from BaseClient import BaseClient


class PyClient(BaseClient):
    def writeDB(self, cur, db):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                indexPath = self.config.indexPage if self.config.indexPage else self.config.homeIndex
                if os.path.join(root, fileName) == os.path.join(self.documentsPath, indexPath):
                    for config in self.config.indexPageConfigList:
                        self.writeItemToDB(cur, root, fileName, config.regular, config.typeName)
                elif fileName.endswith(".html"):
                    if fileName == self.config.homeIndex:
                        for config in self.config.homePageConfigList:
                            if config.regular:
                                self.writeItemToDB(cur, root, fileName, config.regular, config.typeName)
                    else:
                        for config in self.config.otherPageConfigList:
                            if config.regular:
                                self.writeItemToDB(cur, root, fileName, config.regular, config.typeName)
        db.commit()
        db.close()

    def changeSomeText(self):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if '?' in fileName:    # 修改文件名，去掉 ?v=xxxx 的样式
                    newFileName = fileName.split('?')[0]
                    os.rename(os.path.join(root, fileName),os.path.join(root, newFileName))


                    #
                # if fileName == self.config.homeIndex.split('/')[-1]:
                #     path = os.path.join(root, fileName)
                #     with open(path, "r") as f:
                #         content = f.read().replace('../', '/'.join(self.config.homeIndex.split('/')[:-2]))
                #     with open(path, "w") as f:
                #         f.write(content)
