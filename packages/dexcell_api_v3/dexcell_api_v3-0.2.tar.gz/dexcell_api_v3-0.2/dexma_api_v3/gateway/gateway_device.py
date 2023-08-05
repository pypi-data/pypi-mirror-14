__author__ = 'dcortes'

from copy import deepcopy

from gateway_base import GatewayBase


class GatewayDevice(GatewayBase):

    def __init__(self, endpoint, token, http_management=None):
        super(GatewayDevice, self).__init__(endpoint, token, http_management=http_management)

    def get(self, id, call="devices"):
        return super(GatewayDevice, self).get(id, call)

    def fetch(self, parameters=None, call="devices"):
        parameters = deepcopy(parameters) if parameters is not None else {}
        parameters["limit"] = 500 if "limit" not in parameters else parameters["limit"]
        parameters["start"] = 0 if "start" not in parameters else parameters["start"]
        data = super(GatewayDevice, self).fetch(parameters, call)
        while len(data) == parameters["limit"]:
            parameters["start"] += 1
            some_devices = super(GatewayDevice, self).fetch(parameters, call)
            data.extend(some_devices)
        return data

    def save(self, device):
        """ #TODO """
        return