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

    def changeSomeText(self):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                fullPath = os.path.join(root, fileName)
                if self.config.homePage and fullPath == os.path.join(self.documentsPath, self.config.homePage):
                    path = os.path.join(root, fileName)
                    with open(path, "r") as f:
                        content = f.read().replace("api#", self.config.homeIndex + "#")
                    with open(path + '.html', "w") as f:
                        f.write(content)
