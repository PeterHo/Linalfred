# coding=utf-8

__author__ = 'peter'


def isNeedLower(keyword):
    if keyword.islower():
        needLower = True
    else:
        needLower = False
    return needLower


def isSmartEqual(text1, text2):
    if isNeedLower(text1):
        text2 = text2.lower()
    if text1 == text2:
        return True
    return False


# 字符串相等或text2以text1开头并且text1的下一个字符是空格
def isSmartStartsWith(text1, text2):
    if isNeedLower(text1):
        text2 = text2.lower()
    if text1 == text2:
        return True
    if text1.startswith(text2) and text1[len(text2)] == ' ':
        return True
    return False
