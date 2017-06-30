# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 14:09
# @Author  : Hua
# @Site    : 
# @File    : Constants.py
# @Software: PyCharm
import os

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_TYPE_LIST = [int, unicode, str, bool, tuple, float]

READ_FILE_TYPE = ['r', 'rb', 'r+', 'rb+', 'w+', 'wb+', 'a+', 'ab+']
WRITE_FILE_TYPE = ['r+', 'rb+', 'w', 'wb', 'w+', 'wb+', 'a', 'ab', 'a+', 'ab+']


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
