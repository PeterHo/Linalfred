# coding=utf-8
from PyQt5.QtWidgets import QListWidget

__author__ = 'peter'


class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setMouseTracking(True)

        # def mouseMoveEvent(self, event):
        #     row = self.indexAt(event.pos()).row()
        #     self.setCurrentRow(row)
