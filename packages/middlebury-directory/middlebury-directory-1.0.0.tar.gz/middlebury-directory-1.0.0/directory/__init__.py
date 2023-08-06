# -*- coding: utf-8 -*-

from directory.search import Search


def search(*args, **kwargs):
    return Search(*args, **kwargs).results()
