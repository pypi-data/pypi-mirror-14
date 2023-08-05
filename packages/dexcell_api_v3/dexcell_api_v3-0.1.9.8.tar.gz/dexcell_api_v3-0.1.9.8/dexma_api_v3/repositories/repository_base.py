__author__ = 'dcortes'

import abc


""" This is a abstract class, like an interface in java"""
class RepositoryBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, id):
        """Retrieve data from the input source and return an object."""
        return

    @abc.abstractmethod
    def fetch(self):
        """Retrieve data from the input source and return an object."""
        return

    @abc.abstractmethod
    def save(self, data):
        """Save the data object to the output."""
        return

"""
To check his subclasses
for sc in RepositoryBase.__subclasses__():
    print sc.__name__
"""