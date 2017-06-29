# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 16:34
# @Author  : Hua
# @Site    : 
# @File    : Util.py
# @Software: PyCharm
import os
import re

import copy
import yaml
from config.Config import Config

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_TYPE_LIST = [int, unicode, str, bool, tuple, float]

READ_FILE_TYPE = ['r', 'rb', 'r+', 'rb+', 'w+', 'wb+', 'a+', 'ab+']
WRITE_FILE_TYPE = ['r+', 'rb+', 'w', 'wb', 'w+', 'wb+', 'a', 'ab', 'a+', 'ab+']


class Result(object):
    pass



class Sign(object):
    ANNOTATION = '#'
    ENTER = '\n'
    MAC_ENTER = '\r'
    SEP_NEW = '\r\n'
    SEP = '/'
    SPACE = ' '
    NULL = ''
    EQUAL = '='
    IN_LINE = '-'
    DOT = '.'
    COMMA = ','
    UNDERLINE = '_'
    TAB = '\t'
    DOLLAR = '$'
    COLON = ':'
    OR = '|'
    LOGICAL_OR = '||'
    PERCENT = '%'
    PLUS = '+'
    SECTION_BEGIN = '['
    SECTION_END = ']'
    RIGHT_BRACE = '}'
    LEFT_BRACE = '{'
    SEM = ';'
    AT = '@'
    EMPTY_ENV = '${}'
    CHINESE_EQUAL = u'\uff1d'



class JSONParser(object):
    """
    改class用于将dict转object
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
    config = yaml.load(f)
    return JSONParser.getInstance().transform(config, Config())


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
