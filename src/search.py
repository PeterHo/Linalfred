# coding=utf-8
import re

import gi

__author__ = 'peter'


class Search:
    def getRegex(self, keyword):
        pattern = '.*?'.join(keyword)
        return re.compile(pattern)

    def searchApps(self, keyword, allApps):
        if keyword.islower():
            needLower = True
        else:
            needLower = False
        apps = []
        regex = self.getRegex(keyword)
        for app in allApps:
            match = regex.search(app.name.lower() if needLower else app.name)
            if match:
                apps.append((len(match.group()), match.start(), app))
        return [x for _, _, x in sorted(apps, key=lambda x: (x[0], x[1], x[2].name.lower()))]
