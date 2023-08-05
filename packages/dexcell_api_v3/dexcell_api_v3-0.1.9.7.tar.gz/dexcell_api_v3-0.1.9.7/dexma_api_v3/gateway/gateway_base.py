__author__ = 'dcortes'

import abc
from copy import deepcopy

from dexma_drivers.http_management import HttpManagement


""" This is a abstract class, like an interface in java"""
class GatewayBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, endpoint, token, http_management=None):
        self.endpoint = endpoint
        self.headers = {"x-dexcell-token": token}
        self.http_management = http_management if http_management is not None else HttpManagement

    @abc.abstractmethod
    def get(self, id, call):
        return self.http_management.get(self.endpoint, "/{}/{}".format(call, id), headers=self.headers)

    @abc.abstractmethod
    def fetch(self, parameters, call):
        return self.http_management.get(self.endpoint, "/{}".format(call), headers=self.headers, params=parameters)

    @abc.abstractmethod
    def save(self, id, call):
        return self.http_management.post(self.endpoint, "/{}/{}".format(id, call), headers=self.headers)
