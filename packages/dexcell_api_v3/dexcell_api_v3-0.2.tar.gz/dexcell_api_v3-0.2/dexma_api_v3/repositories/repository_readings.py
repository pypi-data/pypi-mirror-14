__author__ = 'dcortes'

from repository_base import RepositoryBase
from dexma_api_v3.gateway.gateway_readings import GatewayReadings
from dexma_api_v3.factory.readings import Readings


class RepositoryReadings(RepositoryBase):

    def __init__(self, endpoint, token):
        self.gateway = GatewayReadings(endpoint, token)

    def _validate_readings(self, device_dict):
        readings = Readings(device_dict)
        readings.validate()
        return readings

    def get(self, id):
        raise Exception("Method get not allowed by readings, just go for fetch")

    def fetch(self, parameters=None):
        readings = self.gateway.fetch(parameters)
        return self._validate_readings(readings)

    def save(self, device):
        status = self.gateway.save(device)
        return status
