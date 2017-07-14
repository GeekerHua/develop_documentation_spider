# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 10:24
# @Author  : Hua
# @Site    : 
# @File    : sphinxClient.py
# @Software: PyCharm
import os
import re
from bs4 import BeautifulSoup

from BaseClient import BaseClient


class SphinxClient(BaseClient):

    def changeSomeText(self):
        for root, dirs, files in os.walk(self.documentsPath):
            for fileName in files:
                if fileName.endswith(".html"):
                    path = os.path.join(root, fileName)
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
