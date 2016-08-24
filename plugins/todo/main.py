# coding=utf-8
import os

__author__ = 'peter'


class Main:
    title = 'todo'
    desc = 'Todo List'
    keyword = 'todo'
    iconName = 'todo.jpg'

    @staticmethod
    def getListFileName():
        return os.path.dirname(os.path.abspath(__file__)) + '/list.txt'

    @staticmethod
    def getAllTodoList():
        try:
            with open(Main.getListFileName(), 'r') as f:
                return list(map(lambda x: x.strip(), f.readlines()))
        except IOError:
            return []

    @staticmethod
    def addTodo(text):
        try:
            with open(Main.getListFileName(), 'a') as f:
                f.write(text)
        except IOError:
            pass

    @staticmethod
    def delTodo(text):
        todoList = Main.getAllTodoList()
        try:
            todoList.remove(text)
        except ValueError:
            pass
        try:
            with open(Main.getListFileName(), 'w') as f:
                f.write('\n'.join(todoList) + '\n')
        except IOError:
            pass

    @staticmethod
    def todoListToListList(todoList):
        listList = []
        for todo in todoList:
            listList.append((todo, None, 'todo.jpg', 'todo'))
        return listList

    @staticmethod
    def todoListToDelList(todoList):
        delList = []
        for todo in todoList:
            delList.append((todo, None, 'todo.jpg', 'todo d ' + todo))
        return delList

    @staticmethod
    def run(param):
        if param and len(param) > 1 and param[0] == 'a':
            Main.addTodo(' '.join(param[1:]) + '\n')
            return True
        if param and len(param) > 1 and param[0] == 'd':
            Main.delTodo(' '.join(param[1:]))
            return True
        return False

    @staticmethod
    def list(param):
        if not param or (param[0] != 'a' and param[0] != 'd' and param[0] != 'l'):
            return [
                ('todo a', 'add a todo', 'add.png', 'todo a'),
                ('todo d', 'del a todo', 'del.png', 'todo d'),
                ('todo l', 'list all todos', 'list.png', 'todo l'),
            ]
        if param[0] == 'd':
            return Main.todoListToDelList(Main.getAllTodoList())
        elif param[0] == 'l':
            return Main.todoListToListList(Main.getAllTodoList())
        elif param[0] == 'a':
            return [
                ('Add Todo', 'add a todo', 'add.png', 'todo'),
            ]
        return []
