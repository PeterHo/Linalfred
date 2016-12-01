# coding=utf-8
import os
import apt_pkg

__author__ = 'peter'

apt_pkg.init()
cache = apt_pkg.Cache()

i = 5

for pkg in cache.packages:
    print(pkg.name)
    i -= 1
    if i < 0:
        break
