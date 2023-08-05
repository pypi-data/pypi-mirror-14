__author__ = 'dcortes'

from gateway_base import GatewayBase


class GatewayLocation(GatewayBase):

    def __init__(self, endpoint, token, http_management=None):
        super(GatewayLocation, self).__init__(endpoint, token, http_management=http_management)

    def get(self, id, call="locations"):
        return super(GatewayLocation, self).get(id, call)

    def fetch(self, parameters=None, call="locations"):
        parameters = parameters.deepcopy() if parameters is not None else {}
        parameters["limit"] = 200 if "limit" not in parameters else parameters["limit"]
        parameters["start"] = 0 if "start" not in parameters else parameters["start"]
        data = super(GatewayLocation, self).fetch(parameters, call)
        while len(data) == parameters["limit"]:
            parameters["start"] += 1
            some_locations = super(GatewayLocation, self).fetch(parameters, call)
            data.extend(some_locations)
        return data

    def save(self, location):
        """ #TODO """
        return