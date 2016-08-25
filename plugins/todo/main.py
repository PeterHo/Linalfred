# coding=utf-8
import os
import traceback

from plugin_common.baseplugin import BasePlugin, RetVal
from plugin_common.baseplugin import Cmd

__author__ = 'peter'


class Main(BasePlugin):
    mainCmd = None
    subCmdList = []

    @staticmethod
    def init():
        Main.mainCmd = Cmd(title='todo', desc='Todo List', icon='todo.jpg', cmd='todo')

        Main.subCmdList = [
            Cmd(title='todo a', desc='add a todo', icon='add.png', cmd='todo a', onRunCmd=Main.onAdd),
            Cmd(title='todo d', desc='del a todo', icon='del.png', cmd='todo d', onRunCmd=Main.onDel),
            Cmd(title='todo l', desc='list all todos', icon='list.png', cmd='todo l'),
            Cmd(title='todo c', desc='clear all todos', icon='del.png', cmd='todo c', onRunCmd=Main.onClear),
        ]

    @staticmethod
    def onList(param):
        if not param:
            return Main.subCmdList
        elif param[0] == 'a':
            return [Main.subCmdList[0]]
        elif param[0] == 'd':
            delList = []
            for todo in Main.getAllTodoList():
                delList.append(
                    Cmd(title=todo, desc=Main.mainCmd.desc, icon=Main.mainCmd.icon, cmd='todo d', param=todo,
                        onRunCmd=Main.onDel))
            return delList
        elif param[0] == 'l':
            listList = []
            for todo in Main.getAllTodoList():
                listList.append(Cmd(title=todo, desc=Main.mainCmd.desc, icon=Main.mainCmd.icon, cmd='todo l'))
            return listList
        elif param[0] == 'c':
            return [Main.subCmdList[3]]

    # add
    @staticmethod
    def onAdd(param):
        if not param:
            return BasePlugin.setShowCmd('todo a')
        try:
            with open(Main.getListFileName(), 'a') as f:
                f.write(param.strip() + "\n")
        except IOError:
            pass
        finally:
            return BasePlugin.setShowCmd('todo l')

    @staticmethod
    def onDel(param):
        if not param:
            return BasePlugin.setShowCmd('todo d')

        todoList = Main.getAllTodoList()
        try:
            todoList.remove(param)
            with open(Main.getListFileName(), 'w') as f:
                f.write('\n'.join(todoList) + '\n')
        except ValueError or IOError:
            traceback.print_exc()
        finally:
            return BasePlugin.setShowCmd('todo l')

    @staticmethod
    def onClear(param):
        os.remove(Main.getListFileName())
        return RetVal.close

    @staticmethod
    def getListFileName():
        return os.path.dirname(os.path.abspath(__file__)) + '/list.txt'

    @staticmethod
    def getAllTodoList():
        try:
            with open(Main.getListFileName(), 'r') as f:
                return list(filter(None, map(lambda x: x.strip(), f.readlines())))
        except IOError:
            return []
