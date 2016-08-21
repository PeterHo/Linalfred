# coding=utf-8

__author__ = 'peter'


class History:
    historyList = []

    @staticmethod
    def add(history):
        History.historyList.append(history)

    @staticmethod
    def clear():
        History.historyList.clear()
