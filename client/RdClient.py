# -*- coding: utf-8 -*-
# @Time    : 2017/7/7 16:11
# @Author  : Hua
# @Site    : 
# @File    : pyClient.py
# @Software: PyCharm
import os

from BaseClient import BaseClient


class RdClient(BaseClient):

    def changeSomeText(self):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if '?' in fileName:    # 修改文件名，去掉 ?v=xxxx 的样式
                    newFileName = fileName.split('?')[0]
                    os.rename(os.path.join(root, fileName),os.path.join(root, newFileName))
