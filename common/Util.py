# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 16:34
# @Author  : Hua
# @Site    : 
# @File    : Util.py
# @Software: PyCharm
import importlib
import os
import client
import copy

import sys
import yaml

from common.Constants import Sign, BASE_TYPE_LIST, READ_FILE_TYPE
import config.Config


class Result(object):
    pass

class JSONParser(object):
    """
    该class用于将dict转object
    """
    _INSTANCE = None

    def __init__(self):
        self.result = Result()

    def transform(self, jsonData, result):
        if (type(jsonData) == list):
            tmpResult = []
            for item in jsonData:
                if (type(item) in BASE_TYPE_LIST):
                    tmpResult.append(item)
                elif (result and isinstance(result, list)):
                    tmpResult.append(self.transform(item, result[0].__class__()))
                else:
                    tmpResult.append(self.transform(item, Result()))
            return tmpResult
        for key, value in jsonData.items():
            newKey = key.replace(Sign.DOT, Sign.UNDERLINE)
            if (type(value) in BASE_TYPE_LIST or value is None):
                setattr(result, newKey, value)
                continue
            # setattr(result, newKey, Result())
            valueToSet = getattr(result, newKey)
            if (not valueToSet):
                valueToSet = Result()
            response = self.transform(jsonData[key], valueToSet)
            if (type(response) == list):
                setattr(result, newKey, response)
        return result

    @staticmethod
    def objectToDict(obj):
        """
        将对象转换称为dict
        :type obj: object
        :rtype: dict
        """
        if (not isinstance(obj, dict) and not isinstance(obj, list)):
            result = copy.deepcopy(obj.__dict__)
        else:
            result = obj
        if (not isinstance(obj, list)):
            if (isinstance(obj, dict)):
                tmpDict = obj
            else:
                tmpDict = obj.__dict__
            for key, value in tmpDict.items():
                if (not type(value) in BASE_TYPE_LIST and value):
                    result[key] = JSONParser.objectToDict(tmpDict[key])
        return result

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if (cls._INSTANCE):
            result = cls._INSTANCE
        else:
            result = cls(*args, **kwargs)
            cls._INSTANCE = result
        return result


def loadInspectorConfig(inspectorConfigFile):
    """
    获取inspectorConfig
    :type inspectorConfigFile: str
    :rtype: InspectorConfig
    """
    f = readFile(inspectorConfigFile)
    configData = yaml.load(f)
    return JSONParser.getInstance().transform(configData, config.Config.Config())


class ReflectTool(object):
    @staticmethod
    def _getPackageAndClassName(fullName):
        """
        获取module名字和class name
        :type fullName: str
        :rtype: tuple[str,str]
        """
        pos = fullName.rfind(Sign.DOT)
        moduleName = fullName[:pos]
        className = fullName[pos + 1:]
        return moduleName, className

    @staticmethod
    def dynamicNewObj(moduleClassName, *args, **kwargs):
        """
        动态new 对象
        :type moduleClassName: str
        :rtype: object
        """
        moduleName, className = ReflectTool._getPackageAndClassName(moduleClassName)
        if (not sys.modules.has_key(moduleName)):
            targetModule = importlib.import_module(moduleName)
        else:
            targetModule = sys.modules.get(moduleName)
        targetClass = getattr(targetModule, className)
        return targetClass(*args, **kwargs)


def readFile(fileName, mode='r', lines=False):
    """
    :type fileName: str
    :type mode: str
    :type lines: bool
    :rtype str | list[str]
    """
    if mode not in READ_FILE_TYPE:
        pass
        # raise ErrorFileMode('%s file mode error' % fileName)

    try:
        fileHandle = open(fileName, mode)
    except:
        pass
        # raise ErrorFileNotExist('%s not existed' % fileName)
    else:
        if (not lines):
            content = fileHandle.read()
        else:
            content = fileHandle.readlines()
        fileHandle.close()
        return content
