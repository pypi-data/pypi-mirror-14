# -*- coding: utf-8 -*-


class Person(object):
    """
    A person in the directory as returned in the search results.

    Every instance of Person has a `webid` attribute, used to uniquely identify
    that person within Middlebury.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '<Person {}>'.format(self.webid)

    def __repr__(self):
        return self.__str__()
