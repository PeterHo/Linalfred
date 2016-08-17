# coding=utf-8
import gi

__author__ = 'peter'


class Search:
    def searchApps(self, keyword, allApps):
        apps = []
        for app in allApps:
            if keyword.lower() in app.name.lower():
                apps.append(app)
        print(len(apps))
        return apps
